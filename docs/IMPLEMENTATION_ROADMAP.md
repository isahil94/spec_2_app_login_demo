# Specs → Running App: Implementation Roadmap (Updated)

**Challenge:** Spec file + Chat command → Autonomous App Generation (locally executable + passing tests)  
**User Flow:** 
```
1. Create spec.md (you write requirements)
2. Run: python main.py --spec=spec.md
3. Chat: "Start building app"
4. System: Automatically orchestrates 10 agents (you only approve at gates)
5. Result: Running app + tests + docs
```

**Timeline:** 30-45 minutes per spec (you: ~5 minutes effort)

---

## ARCHITECTURE: NO Custom AI Runtime

**Key Decision:** Use GitHub Copilot Chat + API directly. Build ONLY orchestration layer.

### What We're NOT Building
- ❌ Custom LLM abstraction
- ❌ Prompt execution engine
- ❌ Model management
- ❌ Token counting/management

### What We ARE Building
- ✅ **Supervisor** - Orchestrates agent sequence
- ✅ **Memory Service** - Persists workflow state
- ✅ **Event Bus** - Coordinates agent handoffs
- ✅ **Artifact Manager** - Saves outputs to `artifacts/`
- ✅ **Validation Engine** - Enforces contracts
- ✅ **Approval Service** - Gates at key points
- ✅ **Agent Scripts** - Call Copilot via subprocess/API

---

## PHASE 1: ORCHESTRATION KERNEL (Days 1-3)

### 1.1 Main Entry Point
**File:** `main.py`

```python
# Structure:
def main():
    # Parse CLI args: --spec=file.md
    # Load specification
    # Initialize: Supervisor, Memory, EventBus
    # Start event loop listening for Copilot Chat commands
    # Command "Start building app" → trigger Supervisor.execute_pipeline()
    
if __name__ == '__main__':
    main()
```

**Deliverable:** 
- Accepts `--spec=spec.md` 
- Waits for chat command "Start building app"
- Launches pipeline automatically

### 1.2 Supervisor Orchestrator
**File:** `orchestration/supervisor/supervisor.py`

**Responsibilities:**
- Load 10-agent workflow DAG
- Activate agents in sequence (or parallel where applicable)
- Coordinate artifact handoff between agents
- Manage approval gates (block workflow, wait for approval)
- Handle errors and retry
- Report progress

**Core Flow:**
```python
execute_pipeline():
  1. Load workflow DAG (agent sequence)
  2. For each agent in sequence:
     - Check dependencies met
     - Activate agent (call subprocess)
     - Wait for agent to complete
     - Validate outputs against contract
     - Emit event to chat: "Agent X completed"
  3. At approval gates:
     - Emit: "Approval needed: review artifacts, say 'approve' to continue"
     - Wait for chat command "approve" or "reject"
  4. After all agents complete:
     - Emit: "Build complete! App running at http://localhost:5000"
```

### 1.3 Memory Service (State Persistence)
**File:** `memory/memory_store.py`

**Responsibilities:**
- Store workflow execution state
- Enable resumable workflows (if interrupted, resume from last checkpoint)
- Pass data from one agent to next
- Track which agents have completed

**Storage:** JSON files in `memory/` directory
```
memory/
├── workflow_state.json (current stage, completed agents)
├── agent_outputs.json (each agent's outputs)
└── execution_log.jsonl (complete audit trail)
```

### 1.4 Event Bus (Agent Coordination)
**File:** `events/event_bus.py`

**Responsibilities:**
- Publish events when agents complete
- Emit progress updates to Copilot Chat
- Handle approval decisions
- Track workflow state transitions

**Events:**
```
AgentStarted(agent_name, timestamp)
AgentCompleted(agent_name, artifacts_produced)
AgentFailed(agent_name, error_message)
ApprovalRequested(description, blocking=True)
ApprovalApproved()
ApprovalRejected()
WorkflowCompleted()
```

---

## PHASE 2: COORDINATION INFRASTRUCTURE (Weeks 2-3)

### 2.1 Event Bus
**File:** `events/event_bus.py`

**Event Types:**
```
- AgentStarted(agent_id, timestamp)
- AgentCompleted(agent_id, outputs, timestamp)
- AgentBlocked(agent_id, reason)
- AgentFailed(agent_id, error)
- ApprovalRequested(agent_id, artifacts)
- ApprovalApproved(agent_id)
- ApprovalRejected(agent_id)
- WorkflowCompleted(artifacts)
```

### 2.2 Artifact Manager
**File:** `orchestration/artifact/artifact_manager.py`

**Responsibilities:**
- Write agent outputs to versioned storage
- Validate artifact ownership
- Track artifact dependencies
- Enforce write-once semantics

**Artifact Structure:**
```
artifacts/
├── requirements/
│   ├── user-stories.md (v1)
│   ├── acceptance-criteria.md (v1)
│   └── business-rules.md (v1)
├── architecture/
│   ├── design.md (v1)
│   └── api-contracts.md (v1)
├── frontend/
│   ├── components/
│   └── pages/
├── backend/
│   ├── controllers/
│   └── services/
├── database/
│   └── schema.sql (v1)
├── tests/
│   ├── unit/
│   └── integration/
└── docs/
    ├── README.md
    └── API.md
```

### 2.3 Validation Engine
**File:** `orchestration/validation/validator.py`

**Validation Gates:**
```
Before → Agent Activation:
✓ Input artifacts valid
✓ Dependencies satisfied
✓ Config constraints met

After → Agent Completion:
✓ Output artifacts match contract
✓ Quality gates passed
✓ No blocked conditions
```

### 2.4 Approval Service
**File:** `orchestration/approval/approval_service.py`

**Approval Points:**
- After Solution Architect (architecture review)
- After Reviewer (final quality gate)
- Before DevOps (production deployment)

---

## PHASE 3: AGENT ACTIVATION (Weeks 3-4)

### 3.1 Supervisor → Agent Integration

Current agent scripts are **placeholders**. Activate them:

**File:** `scripts/business_analyst.py` (refactor)

```python
def execute(input_spec, output_dir):
    # Today: Placeholder logging
    # Tomorrow: Invoke GitHub Copilot Agent
    
    # Step 1: Load input artifact
    spec = read_artifact(input_spec)
    
    # Step 2: Invoke Copilot with Business Analyst prompt
    requirements = copilot_agent.execute(
        prompt='ai/prompts/business-analyst/v1.0.md',
        input=spec,
        skills=['Analyze Requirements', 'Create User Stories', ...]
    )
    
    # Step 3: Write output artifacts
    write_artifact('requirements-spec.md', requirements)
    write_artifact('user-stories.md', stories)
    
    # Step 4: Emit completion event
    event_bus.publish(AgentCompleted(agent_id='business_analyst'))
```

**Repeat for all 9 agents:**
- `solution_architect.py` → invokes Copilot Agent
- `uiux_developer.py` → invokes Copilot Agent
- `backend_developer.py` → invokes Copilot Agent
- `database_developer.py` → invokes Copilot Agent
- `qa_engineer.py` → invokes Copilot Agent
- `reviewer.py` → invokes Copilot Agent
- `devops_release.py` → invokes Copilot Agent
- `documentation.py` → invokes Copilot Agent

### 3.2 Copilot Integration Points

**Expected Copilot Agent Inputs:**
- Agent prompt version (from `ai/prompts/`)
- Input artifacts (requirements, architecture, etc.)
- Relevant skills to use (from `ai/skills/`)
- Validation contracts (from `ai/contracts/`)

**Expected Outputs:**
- Generated artifacts (code, docs, tests, etc.)
- Quality report
- Blockers or open questions

---

## PHASE 4: END-TO-END WORKFLOW (Week 4)

### 4.1 Full Pipeline Execution

```
Input: specification.md
  ↓
[Supervisor] Initialize workflow
  ↓
[Business Analyst Agent] → outputs: requirements-spec.md, user-stories.md
  ↓ (Copilot invoked with BA prompt + requirements skills)
  ↓
[Solution Architect Agent] → outputs: architecture-design.md, api-contracts.md
  ↓ (Copilot invoked with SA prompt + architecture skills)
  ↓ (APPROVAL GATE)
  ↓
[UI/UX Developer] | [Backend Developer] | [Database Developer] (PARALLEL)
  ↓
[QA Engineer] → outputs: unit_tests/, integration_tests/
  ↓
[Reviewer Agent] → APPROVE or BLOCK
  ↓ (APPROVAL GATE)
  ↓
[DevOps Agent] → outputs: docker_image, ci_cd_config
  ↓
[Documentation Agent] → outputs: README.md, API_DOC.md
  ↓
Output: Running Application (docker run)
         + Passing Tests
         + Complete Documentation
```

### 4.2 Success Criteria (TRACKA)

✅ **App Running Locally**
```bash
docker run -p 5000:5000 specs-to-app:latest
# App responds to requests
```

✅ **Test Suite Passing**
```bash
pytest tests/ --cov=
# All tests pass, coverage > 80%
```

✅ **Full Documentation**
- README.md (setup instructions)
- API_DOCUMENTATION.md (endpoints)
- DEVELOPER_GUIDE.md (code structure)

---

## PHASE 5: VALIDATION & QUALITY (Week 5)

### 5.1 Quality Gates

**After each agent:**
- Output artifacts match contract schema
- No validation errors
- Quality score meets threshold

**Before deployment:**
- All tests passing
- Code review approved
- No security issues

### 5.2 Self-Check Loop (Agent Loop)

```
Agent Action:
  1. Generate artifact
  2. Run validation
  3. If invalid → regenerate
  4. If valid → emit completion
  
Supervisor Check:
  1. Verify all dependencies met
  2. Validate quality gates
  3. If blocked → request approval
  4. If approved → activate next agent
```

---

## IMPLEMENTATION SEQUENCE

### Week 1
- [ ] **main.py** - CLI entry point
- [ ] **Supervisor** - Orchestration core
- [ ] **Memory Service** - State persistence
- [ ] **Event Bus** - Async coordination

### Week 2
- [ ] **Artifact Manager** - Output storage
- [ ] **Validation Engine** - Contract checking
- [ ] **Approval Service** - Human gates

### Week 3
- [ ] Refactor **business_analyst.py** → Copilot integration
- [ ] Refactor **solution_architect.py** → Copilot integration
- [ ] Refactor **backend_developer.py** → Copilot integration

### Week 4
- [ ] Refactor remaining agents
- [ ] End-to-end workflow testing
- [ ] Integration testing

### Week 5
- [ ] Performance optimization
- [ ] Error handling & recovery
- [ ] Production readiness

---

## CODE STRUCTURE AFTER IMPLEMENTATION

```
Specs_to_APP/
├── main.py ✨ NEW
├── orchestration/
│   ├── supervisor/
│   │   ├── supervisor.py ✨ NEW
│   │   ├── workflow_coordinator.py ✨ NEW
│   │   └── approval_mediator.py ✨ NEW
│   ├── workflow/
│   │   ├── workflow_engine.py ✨ NEW
│   │   └── dependency_resolver.py ✨ NEW
│   ├── artifact/
│   │   ├── artifact_manager.py ✨ NEW
│   │   └── storage.py ✨ NEW
│   ├── validation/
│   │   ├── validator.py ✨ NEW
│   │   └── contract_checker.py ✨ NEW
│   └── approval/
│       └── approval_service.py ✨ NEW
├── memory/
│   ├── memory_store.py ✨ NEW
│   └── persistence.py ✨ NEW
├── events/
│   ├── event_bus.py ✨ NEW
│   └── events.py ✨ NEW
├── scripts/
│   ├── business_analyst.py 🔄 REFACTOR
│   ├── solution_architect.py 🔄 REFACTOR
│   ├── backend_developer.py 🔄 REFACTOR
│   ├── database_developer.py 🔄 REFACTOR
│   ├── qa_engineer.py 🔄 REFACTOR
│   ├── uiux_developer.py 🔄 REFACTOR
│   ├── reviewer.py 🔄 REFACTOR
│   ├── documentation.py 🔄 REFACTOR
│   └── devops_release.py 🔄 REFACTOR
├── ai/
│   ├── agents/ ✅ COMPLETE
│   ├── prompts/ ✅ COMPLETE
│   ├── skills/ ✅ COMPLETE
│   ├── contracts/ ✅ COMPLETE
│   └── templates/ ✅ COMPLETE
├── artifacts/ (OUTPUT DIRECTORY)
├── configs/ ✨ NEW (add YAML files)
└── docs/ ✅ COMPLETE
```

---

## EXPECTED EXECUTION FLOW (Example)

**Input:** `spec.md` describing a Task Management System

```
$ python main.py --spec=spec.md --output=artifacts/

[Supervisor] Loading workflow specification...
[Supervisor] Initializing memory service...
[Supervisor] Starting event bus...

[Business Analyst Agent] Starting...
  → Reading: spec.md
  → Invoking: GitHub Copilot Agent
  → Prompt: ai/prompts/business-analyst/v1.0.md
  → Skills: [Analyze Requirements, Create User Stories, Define Acceptance Criteria]
  → Writing: requirements-spec.md
  → Writing: user-stories.md
  → Event: AgentCompleted('business_analyst')

[Solution Architect Agent] Starting...
  → Reading: requirements-spec.md, user-stories.md
  → Invoking: GitHub Copilot Agent
  → Prompt: ai/prompts/solution-architect/v1.0.md
  → Writing: architecture-design.md, api-contracts.md
  → Event: ApprovalRequested('solution_architect')

[Supervisor] Waiting for architecture approval...
→ User reviews artifacts/architecture-design.md in VS Code
→ User approves in Copilot Chat: "Approve architecture"
→ Event: ApprovalApproved('solution_architect')

[UI/UX Developer Agent] Starting (parallel)...
[Backend Developer Agent] Starting (parallel)...
[Database Developer Agent] Starting (parallel)...

... (all agents execute in sequence/parallel) ...

[QA Engineer Agent] All tests passing ✓
[Reviewer Agent] All reviews approved ✓
[DevOps Agent] Docker image built ✓
[Documentation Agent] Docs generated ✓

[Supervisor] Workflow complete!

Output:
  ✅ artifacts/README.md
  ✅ artifacts/docker_image.tar
  ✅ app/frontend/ (React)
  ✅ app/backend/ (API)
  ✅ app/database/ (Schema)
  ✅ tests/ (Unit + Integration)
  ✅ docs/ (Complete)

$ docker run -p 5000:5000 specs-to-app:latest
# App running at http://localhost:5000
```

---

## DELIVERABLE CHECKLIST (TRACKA)

✅ **Spec → Running App**

- [ ] Specification file as input
- [ ] Zero human coding required (Copilot does all generation)
- [ ] App running locally (`docker run`)
- [ ] Test suite passing (`pytest`)
- [ ] Complete documentation
- [ ] Human approval gates before key transitions
- [ ] Self-checking loops (validation, quality gates)
- [ ] Full audit trail (who approved what, when)

---

## SUCCESS METRICS

| Metric | Target |
|--------|--------|
| Spec → App time | < 30 minutes |
| Test coverage | > 80% |
| Code quality | SonarQube B+ or higher |
| Documentation completeness | 100% |
| Human approval gates | 3 mandatory checkpoints |
| Error recovery | Automatic retry on transient failures |
| Audit trail | Complete end-to-end logging |

---

## NEXT STEPS

### Immediate (This week)
1. **Create main.py** - Platform entry point
2. **Implement Supervisor** - Orchestration core
3. **Implement Memory Service** - State persistence

### Short-term (Next 2 weeks)
4. **Build Workflow Engine** - Execution core
5. **Build Event Bus** - Agent coordination
6. **Build Artifact Manager** - Output persistence

### Medium-term (Weeks 3-4)
7. **Refactor agent scripts** - Copilot integration
8. **Build validation layer** - Contract enforcement
9. **Build approval flow** - Human gates

### Test & Polish (Week 5)
10. **End-to-end testing**
11. **Performance tuning**
12. **Documentation & demo**

Would you like me to start implementing Phase 1 starting with main.py and the Supervisor?
