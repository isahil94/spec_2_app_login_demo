// Usage: node .orchestrator/watcher.js
// Watches artifacts/** for changes. Debounces bursts of writes (an agent
// writing 8 files in a row shouldn't trigger 8 evaluations), then runs
// the supervisor engine once things go quiet.

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const WATCH_DIR = path.join(ROOT, 'artifacts');
const DEBOUNCE_MS = 4000;

let timer = null;

function trigger(filename) {
  console.log(`[watcher] change detected: ${filename}`);
  if (timer) clearTimeout(timer);
  timer = setTimeout(() => {
    console.log('[watcher] quiet period elapsed, running supervisor engine...');
    try {
      const out = execSync('node .orchestrator/supervisor-engine.js', { cwd: ROOT }).toString();
      console.log(out);
      console.log('[watcher] see .orchestrator/next-action.md for what to do next');
    } catch (e) {
      console.error('[watcher] engine error:', e.message);
    }
  }, DEBOUNCE_MS);
}

fs.mkdirSync(WATCH_DIR, { recursive: true });
console.log(`[watcher] watching ${WATCH_DIR} for agent output...`);
fs.watch(WATCH_DIR, { recursive: true }, (event, filename) => {
  if (!filename) return;
  if (filename.endsWith('openlog.md') || filename.endsWith('handoff_contract.md') || filename.includes('qa-report')) {
    trigger(filename);
  }
});