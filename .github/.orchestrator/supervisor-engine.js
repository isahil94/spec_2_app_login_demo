const fs = require('fs');
const path = require('path');
const { parseOpenlog, countArtifacts } = require('./parser');

const ROOT = path.resolve(__dirname, '..');
const WORKFLOW = JSON.parse(fs.readFileSync(path.join(__dirname, 'workflow.json'), 'utf8'));
const STATE_PATH = path.join(__dirname, 'state.json');
const NEXT_ACTION_PATH = path.join(__dirname, 'next-action.md');
const QUEUE_PATH = path.join(ROOT, 'artifacts/supervisor/approval-queue.md');
const LOG_PATH = path.join(ROOT, 'artifacts/supervisor/execution-log.md');

function loadState() {
  if (!fs.existsSync(STATE_PATH)) {
    return { currentStage: WORKFLOW.stages[0].id, retries: {}, history: [] };
  }
  return JSON.parse(fs.readFileSync(STATE_PATH, 'utf8'));
}
function saveState(s) {
  fs.writeFileSync(STATE_PATH, JSON.stringify(s, null, 2));
}
function appendLog(line) {
  fs.mkdirSync(path.dirname(LOG_PATH), { recursive: true });
  fs.appendFileSync(LOG_PATH, `- ${new Date().toISOString()} — ${line}\n`);
}
function writeNextAction(md) {
  fs.writeFileSync(NEXT_ACTION_PATH, md);
}
function writeApprovalQueue(entries) {
  fs.mkdirSync(path.dirname(QUEUE_PATH), { recursive: true });
  const body = entries.map(e =>
    `## ${e.stage} — ${e.question}\n- Severity: ${e.severity || 'critical'}\n- Raised: ${new Date().toISOString()}\n`
  ).join('\n');
  fs.writeFileSync(QUEUE_PATH, `# Approval Queue\n\n${body || '_No pending items._\n'}`);
}
function findStage(id) {
  return WORKFLOW.stages.find(s => s.id === id) ||
    WORKFLOW.stages.flatMap(s => s.branches || []).find(b => b.id === id);
}

// Evaluate a single (non-parallel, non-gate) stage: artifact completeness + openlog blockers.
function evaluateWorkerStage(stage) {
  const artifactCheck = countArtifacts(stage.artifact_dir, stage.required_artifacts, ROOT);
  const openlogPath = path.join(ROOT, stage.artifact_dir, 'openlog.md');
  const openlog = parseOpenlog(openlogPath, WORKFLOW.openlog_fields);
  return { stage, artifactCheck, openlog };
}

function decide() {
  const state = loadState();
  const stage = findStage(state.currentStage);

  if (!stage) { appendLog(`ERROR: unknown stage ${state.currentStage}`); return; }

  if (stage.type === 'terminal') {
    writeNextAction(`# Pipeline complete\nAll stages finished. See artifacts/supervisor/workflow-status.md`);
    appendLog('Pipeline COMPLETE');
    return;
  }

  if (stage.type === 'approval_gate') {
    writeNextAction(
`# ACTION REQUIRED — Human approval gate: ${stage.id}
Review the artifacts produced so far, then resolve this gate.

To approve: edit .orchestrator/state.json is NOT needed — just run:
  node .orchestrator/supervisor-engine.js approve ${stage.id}

To reject / send back:
  node .orchestrator/supervisor-engine.js reject ${stage.id} "<reason>"`);
    appendLog(`WAITING_FOR_APPROVAL at gate ${stage.id}`);
    writeApprovalQueue([{ stage: stage.id, question: 'Human review required before proceeding', severity: 'gate' }]);
    return;
  }

  if (stage.type === 'parallel') {
    const results = stage.branches.map(evaluateWorkerStage);
    const anyMissing = results.filter(r => r.artifactCheck.missing.length > 0);
    const anyBlocking = results.filter(r => r.openlog.criticalBlocking.length > 0);

    if (anyMissing.length) {
      for (const r of anyMissing) retryMissing(r.stage, r.artifactCheck.missing, state);
      saveState(state);
      return;
    }
    if (anyBlocking.length) {
      escalateBlocking(anyBlocking.map(r => ({ stage: r.stage.id, items: r.openlog.criticalBlocking })));
      return;
    }
    // both branches clean -> advance
    appendLog(`Parallel stage ${stage.id} complete (${stage.branches.map(b=>b.id).join(', ')})`);
    state.currentStage = stage.next;
    saveState(state);
    writeNextAction(`# Ready\nParallel branches complete. Advancing to: ${stage.next}\nRun this orchestrator again after invoking that stage's agent, or it will be auto-suggested below.`);
    suggestInvoke(findStage(stage.next));
    return;
  }

  // normal worker stage
  const { artifactCheck, openlog } = evaluateWorkerStage(stage);

  if (artifactCheck.missing.length > 0) {
    retryMissing(stage, artifactCheck.missing, state);
    saveState(state);
    return;
  }

  if (openlog.criticalBlocking.length > 0) {
    escalateBlocking([{ stage: stage.id, items: openlog.criticalBlocking }]);
    return;
  }

  // QA special case: route defects back to owning stage
  if (stage.id === 'qa') {
    const defects = (openlog.items || []).filter(r =>
      (r['Status'] || '').toUpperCase() === 'FAILED' || (r['Defect'] || '').toLowerCase() === 'yes'
    );
    if (defects.length) {
      const owner = defects[0]['Owner'] || defects[0]['Component'] || 'unknown';
      const ownerStage = stage.owner_map_for_defects[owner.toLowerCase()] || null;
      if (ownerStage) {
        const attemptKey = `qa_fix_${ownerStage}`;
        state.retries[attemptKey] = (state.retries[attemptKey] || 0) + 1;
        if (state.retries[attemptKey] > 1) {
          escalateBlocking([{ stage: 'qa', items: defects }]);
          return;
        }
        appendLog(`QA found defect owned by ${ownerStage}. Routing fix request.`);
        writeNextAction(
`# ACTION — Send fix request to ${ownerStage}
QA reported a defect owned by ${ownerStage}.

Run the ${findStage(ownerStage).agent} agent with this prompt:
---
Fix the following defect reported by QA:
${defects.map(d => `- ${JSON.stringify(d)}`).join('\n')}
After fixing, update your handoff_contract.md and re-run.
---
Then re-run: node .orchestrator/supervisor-engine.js`);
        state.currentStage = ownerStage; // loop back
        saveState(state);
        return;
      }
    }
  }

  // clean -> advance
  appendLog(`Stage ${stage.id} complete. Advancing to ${stage.next}`);
  state.currentStage = stage.next;
  saveState(state);
  suggestInvoke(findStage(state.currentStage));
}

function retryMissing(stage, missing, state) {
  const key = `missing_${stage.id}`;
  state.retries[key] = (state.retries[key] || 0) + 1;
  if (state.retries[key] > 1) {
    escalateBlocking([{ stage: stage.id, items: [{ reason: `Artifacts still missing after retry: ${missing.join(', ')}` }] }]);
    return;
  }
  appendLog(`Stage ${stage.id} missing artifacts: ${missing.join(', ')}. Requesting regeneration.`);
  writeNextAction(
`# ACTION — Regenerate missing artifacts for ${stage.id}
Missing: ${missing.join(', ')}

Run the ${stage.agent} agent with this one-line prompt:
---
Regenerate only these missing output files, do not redo completed work: ${missing.join(', ')}
---
Then re-run: node .orchestrator/supervisor-engine.js`);
}

function escalateBlocking(list) {
  appendLog(`BLOCKED — human input needed: ${JSON.stringify(list)}`);
  writeApprovalQueue(list.flatMap(l => l.items.map(item => ({
    stage: l.stage,
    question: item['Open Question'] || item['Description'] || item.reason || JSON.stringify(item),
    severity: 'critical'
  }))));
  writeNextAction(
`# ACTION REQUIRED — Blocking question(s)
${list.map(l => `## Stage: ${l.stage}\n` + l.items.map(i => `- ${JSON.stringify(i)}`).join('\n')).join('\n\n')}

Answer these, update the relevant openlog.md with the resolution (Status -> APPROVED/REJECTED),
then re-run: node .orchestrator/supervisor-engine.js`);
}

function suggestInvoke(stage) {
  if (!stage || stage.type) return; // gates/terminal handled elsewhere
  writeNextAction(
`# Ready — run next agent
Run: ${stage.agent}
One-line prompt: "Proceed with ${stage.id} using inputs from previous stage handoff_contract.md"

After it finishes, this watcher will detect the new files and re-run automatically.`);
}

// CLI entry points for approve/reject
const [,, cmd, arg1, arg2] = process.argv;
if (cmd === 'approve') {
  const state = loadState();
  const stage = findStage(arg1);
  state.currentStage = stage.next;
  saveState(state);
  appendLog(`Gate ${arg1} APPROVED by human`);
  decide();
} else if (cmd === 'reject') {
  appendLog(`Gate ${arg1} REJECTED: ${arg2}`);
  writeNextAction(`# Gate rejected\nReason: ${arg2}\nFix the flagged stage and re-run.`);
} else {
  decide();
}

module.exports = { decide };