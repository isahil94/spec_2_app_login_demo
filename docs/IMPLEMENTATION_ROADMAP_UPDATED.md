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
- Report progress to Copilot Chat

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

## PHASE 2: AGENT INTEGRATION (Days 3-5)

### 2.1 Refactor Agent Scripts
**Files:** `scripts/business_analyst.py`, `scripts/solution_architect.py`, etc.

**Current (Placeholder):**
```python
# Just logs what would happen
logger.info("Business Analyst would execute here")
```

**New (Copilot Integration):**
```python
def execute(spec_file, output_dir):
    # 1. Load input artifact (spec.md)
    spec = load_artifact(spec_file)
    
    # 2. Invoke Copilot Chat
    #    Option A: Subprocess call to copilot CLI
    #    Option B: Use Copilot API
    #    Option C: Use VSCode extension API
    copilot_prompt = read_file('ai/prompts/business-analyst/v1.0.md')
    
    result = copilot_chat(
        prompt=copilot_prompt,
        input=spec,
        model='gpt-4',  # Or your Copilot model
        skills=['Analyze Requirements', 'Create User Stories', ...]
    )
    
    # 3. Parse output (should be structured: requirements, user_stories, etc.)
    requirements = parse_output(result, template='requirements.md')
    
    # 4. Write to artifacts/
    write_artifact('requirements-spec.md', requirements.spec)
    write_artifact('user-stories.md', requirements.stories)
    write_artifact('business-rules.md', requirements.rules)
    
    # 5. Emit completion event
    emit_event(AgentCompleted('business_analyst'))
    
    return artifacts_produced
```

**Do this for all 10 agents:**
- business_analyst.py
- solution_architect.py
- uiux_developer.py
- backend_developer.py
- database_developer.py
- qa_engineer.py
- reviewer.py
- documentation.py
- devops_release.py

### 2.2 Artifact Manager
**File:** `orchestration/artifact/artifact_manager.py`

**Responsibilities:**
- Write agent outputs to `artifacts/`
- Create timestamped versions (v1, v2, etc.)
- Validate artifact structure against contract
- Track artifact dependencies

**Usage:**
```python
manager = ArtifactManager('artifacts/')

# Agent writes output
manager.write_artifact(
    name='requirements-spec.md',
    content=spec_content,
    agent='business_analyst',
    contract='requirements-contract.md'
)

# Next agent reads input
requirements = manager.read_artifact('requirements-spec.md')
```

### 2.3 Validation Engine
**File:** `orchestration/validation/validator.py`

**Responsibilities:**
- Check artifact against contract schema
- Enforce quality gates (e.g., test coverage > 80%)
- Block invalid transitions
- Provide detailed validation errors

**Validation Points:**
```python
# Before agent activation
validator.validate_dependencies_met(agent_id)

# After agent completion
validator.validate_artifact(
    artifact_name='requirements-spec.md',
    contract='requirements-contract.md',
    quality_thresholds={'completeness': 0.9}
)

# Before approval gate
validator.validate_readiness_for_deployment()
```

---

## PHASE 3: APPROVAL GATES & COMPLETION (Days 5-6)

### 3.1 Approval Service
**File:** `orchestration/approval/approval_service.py`

**Approval Points in Pipeline:**
```
1. After Solution Architect
   Message to Chat: "Architecture designed. Review artifacts/architecture-design.md"
   Wait for: "approve" → continue, "reject" → retry, "modify" → escalate

2. After Reviewer Agent
   Message to Chat: "Final review complete. All quality gates passed."
   Wait for: "approve" → deploy, "reject" → send back to developers

3. Optional: Before deployment
   Message to Chat: "Ready to build Docker image and deploy?"
   Wait for: "deploy" → proceed, "cancel" → stop
```

**Implementation:**
```python
approval_service = ApprovalService()

# Block workflow until approval
approval_service.request_approval(
    gate_name='architecture_review',
    message='Architecture designed. Review and approve to continue.',
    blocking=True
)

# Wait for approval in chat
if approval_service.wait_for_approval('architecture_review', timeout=3600):
    supervisor.continue_workflow()
else:
    supervisor.handle_rejection()
```

### 3.2 Chat Integration
**File:** `main.py` (chat listener)

**Listen for Chat Commands:**
```
"Start building app" 
  → supervisor.execute_pipeline()

"approve" (at approval gate)
  → approval_service.approve()

"reject" (at approval gate)  
  → approval_service.reject()

"show progress"
  → display_workflow_progress()

"show artifacts"
  → display_artifact_list()
```

---

## PHASE 4: END-TO-END EXECUTION (Day 7)

### 4.1 Complete Flow

**Input:** `spec.md` describing a Task Manager

```
You create: spec.md
├─ Features: Create, Read, Update, Delete tasks
├─ Tech: React frontend, Node.js API, PostgreSQL
└─ Requirements: Responsive, accessible, tested

You run: python main.py --spec=spec.md

You say in Chat: "Start building app"

[Supervisor Orchestrates]:
  
  [BA] Analyzing spec... ✓
    → requirements-spec.md
    → user-stories.md
    → acceptance-criteria.md
    Chat: "Requirements complete. 12 user stories identified."
  
  [SA] Designing architecture... ✓
    → architecture-design.md
    → api-contracts.md
    → folder-structure.md
    Chat: "Architecture designed. Review?"
    [APPROVAL GATE] Waiting for approval...
    
  You: "approve"
    [GATE] ✓ Approved
  
  [Parallel - 10 min]:
    [UI/UX] Generating React components...
      → react_components/
      → pages/
      Chat: "Frontend complete. 15 components."
    
    [Backend] Generating Node.js API...
      → controllers/
      → services/
      → middleware/
      Chat: "Backend complete. 12 endpoints."
    
    [Database] Designing schema...
      → schema.sql
      → migrations/
      Chat: "Database designed. 8 tables."
  
  [QA] Generating & running tests... ✓
    → unit_tests/
    → integration_tests/
    Chat: "Tests running..."
    Chat: "✅ All tests passing! Coverage: 82%"
  
  [Reviewer] Final review... ✓
    → review_report.md
    Chat: "Code quality: A, Architecture: A, Security: A"
    Chat: "Ready for deployment?"
    [APPROVAL GATE] Waiting for approval...
    
  You: "approve"
    [GATE] ✓ Approved
  
  [DevOps] Building & packaging... ✓
    → Dockerfile
    → docker_image.tar
    → .env.example
    Chat: "Docker image built: specs-to-app:latest"
  
  [Documentation] Generating docs... ✓
    → README.md
    → API_DOCUMENTATION.md
    → DEVELOPER_GUIDE.md
    Chat: "Documentation complete."
  
  [Supervisor] Workflow complete! ✓
    Chat: "🎉 App ready! Run: docker run -p 5000:5000 specs-to-app:latest"

You run: docker run -p 5000:5000 specs-to-app:latest

Result:
  ✅ App running at http://localhost:5000
  ✅ Tests: 82% coverage, all passing
  ✅ Documentation: complete
  ✅ Your effort: ~5 minutes (two "approve" commands)
  ✅ Time: 30-45 minutes total
```

---

## IMPLEMENTATION SEQUENCE (SIMPLIFIED)

### Days 1-2: Orchestration Core
- [ ] **main.py** - CLI + chat integration
- [ ] **Supervisor** - Agent orchestration
- [ ] **Memory** - State persistence
- [ ] **Event Bus** - Progress updates

### Days 3-4: Agent Integration  
- [ ] Refactor **business_analyst.py** → call Copilot
- [ ] Refactor **solution_architect.py** → call Copilot
- [ ] Refactor **backend_developer.py** → call Copilot
- [ ] Refactor **database_developer.py** → call Copilot
- [ ] Refactor remaining agents

### Days 5-6: Validation & Approval
- [ ] **Validation Engine** - Contract checking
- [ ] **Approval Service** - Gate at key points
- [ ] **Artifact Manager** - Output storage

### Day 7: End-to-End Testing
- [ ] Full pipeline test with simple spec
- [ ] Validate app runs locally
- [ ] Validate tests pass
- [ ] Validate documentation generated

### Day 8: Polish
- [ ] Error handling & retry
- [ ] Resume capability
- [ ] Performance optimization
- [ ] Logging & observability

---

## CODE STRUCTURE (After Implementation)

```
Specs_to_APP/
├── main.py ✨ NEW (entry point + chat listener)
├── orchestration/
│   ├── supervisor/
│   │   └── supervisor.py ✨ NEW (orchestrator)
│   ├── artifact/
│   │   └── artifact_manager.py ✨ NEW
│   ├── validation/
│   │   └── validator.py ✨ NEW
│   └── approval/
│       └── approval_service.py ✨ NEW
├── memory/
│   └── memory_store.py ✨ NEW
├── events/
│   └── event_bus.py ✨ NEW
├── scripts/
│   ├── business_analyst.py 🔄 (add Copilot call)
│   ├── solution_architect.py 🔄 (add Copilot call)
│   ├── backend_developer.py 🔄 (add Copilot call)
│   ├── database_developer.py 🔄 (add Copilot call)
│   ├── qa_engineer.py 🔄 (add Copilot call)
│   ├── uiux_developer.py 🔄 (add Copilot call)
│   ├── reviewer.py 🔄 (add Copilot call)
│   ├── documentation.py 🔄 (add Copilot call)
│   └── devops_release.py 🔄 (add Copilot call)
├── ai/
│   ├── agents/ ✅ COMPLETE
│   ├── prompts/ ✅ COMPLETE
│   ├── skills/ ✅ COMPLETE
│   ├── contracts/ ✅ COMPLETE
│   └── templates/ ✅ COMPLETE
├── artifacts/ (generated outputs)
└── memory/ (workflow state)
```

---

## EXPECTED OUTPUT

**Command:**
```bash
python main.py --spec=spec.md
# Then in chat: "Start building app"
```

**Result after ~35 minutes:**
```
artifacts/
├── requirements/
│   ├── requirements-spec.md
│   ├── user-stories.md
│   └── acceptance-criteria.md
├── architecture/
│   ├── architecture-design.md
│   ├── api-contracts.md
│   └── deployment-architecture.md
├── app/
│   ├── frontend/  (React components)
│   ├── backend/   (Node.js API)
│   ├── database/  (PostgreSQL schema)
│   └── tests/     (Unit + Integration tests)
├── docker_image.tar
├── README.md
├── API_DOCUMENTATION.md
├── DEVELOPER_GUIDE.md
└── DEPLOYMENT_GUIDE.md

Docker container running:
$ docker run -p 5000:5000 specs-to-app:latest
# ✅ App responding at http://localhost:5000

Tests passing:
$ pytest tests/
# ✅ 145 tests passed, 82% coverage
```

---

## SUCCESS METRICS

| Metric | Target | Status |
|--------|--------|--------|
| Spec → App time | < 45 min | ⏳ To test |
| Human effort | < 5 min | ⏳ To test |
| Test coverage | > 80% | ⏳ To test |
| Approval gates | 2-3 checkpoints | ✓ Designed |
| Autonomous execution | 95%+ | ✓ Designed |
| TRACKA challenge pass | YES | ⏳ To test |

---

## NEXT STEP: BUILD PHASE 1

Ready to start?

I'll create:
1. **main.py** - Entry point
2. **supervisor.py** - Orchestrator
3. **memory_store.py** - State persistence
4. **event_bus.py** - Progress updates

This gives you a working orchestration kernel by end of today. ✨

**Shall I start building now?**
