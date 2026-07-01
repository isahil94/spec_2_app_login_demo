# Workflow Correlation Integration Guide for Agents

**Version:** 1.0.0  
**Status:** Implementation Guide  
**Last Updated:** 2026-07-01

This guide shows how each agent should implement workflow correlation to ensure complete end-to-end traceability.

---

## Step-by-Step Integration

### Step 1: Receive IDs from Supervisor

**When:** Agent startup  
**From:** Supervisor handoff  
**What you receive:**

```
Workflow ID: WF-20260701-0001
Prior Correlation IDs: [CORR-8A7F2D]
Activity ID Counter Start: 6
```

**What you must do:**
```python
workflow_id = "WF-20260701-0001"  # PRESERVE unchanged
correlation_id = None  # Will generate new one
activity_id_counter = 6  # Start from received value
```

---

### Step 2: Generate IDs for Your Phase

**Correlation ID:**
```python
import uuid
# Generate NEW correlation ID for your phase
correlation_id = "CORR-" + uuid.uuid4().hex[:6].upper()
# Example: CORR-C3E9K7
```

**Activity IDs:**
```python
activity_id_counter = 6  # Received from prior agent
activity_id = activity_id_counter  # ACT-000006

# Each new action increments
activity_id_counter += 1  # Next action: ACT-000007
```

---

### Step 3: Log Agent Startup

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-C3E9K7
activity_id: ACT-000006
timestamp: 2026-07-01T10:20:00Z
agent: solution_architect
action: agent_startup
status: started
artifact: n/a
duration: 0
message: "Solution Architect starting execution"
---
```

---

### Step 4: Log Each Major Action

```
ACTION 1: Load Input Artifacts
  └─ Increment Activity ID: 6 → 7

activity_id = 7

LOG ENTRY (start):
  workflow_id: WF-20260701-0001
  correlation_id: CORR-C3E9K7
  activity_id: ACT-000007
  status: started

[Work happens for 2.4 seconds]

LOG ENTRY (completion):
  workflow_id: WF-20260701-0001
  correlation_id: CORR-C3E9K7
  activity_id: ACT-000007
  status: completed
  duration: 2400
  message: "Loaded all input artifacts (5 files)"

ACTION 2: Design Architecture
  └─ Increment Activity ID: 7 → 8

[Repeat pattern for each action]
```

---

### Step 5: Generate Artifacts with IDs in Metadata

**Every artifact must include:**

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-C3E9K7
artifact_version: v1.0.0
generated_by: solution_architect
activity_id: ACT-000008
timestamp: 2026-07-01T10:22:15Z
---

# Architecture Design

[Content here]
```

**Files generated in Phase 2 (Architecture):**
- architecture-design.md (workflow_id: WF-20260701-0001, correlation_id: CORR-C3E9K7)
- api-contracts.md (workflow_id: WF-20260701-0001, correlation_id: CORR-C3E9K7)
- technology-stack.md (workflow_id: WF-20260701-0001, correlation_id: CORR-C3E9K7)
- security-architecture.md (workflow_id: WF-20260701-0001, correlation_id: CORR-C3E9K7)

---

### Step 6: Create Audit Records with IDs

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-C3E9K7
activity_id: ACT-000009
audit_id: audit-ACT-000009-001
timestamp: 2026-07-01T10:22:20Z
agent: solution_architect
action: artifact_generated
reason: "Generated architecture-design.md with all components specified"
output_artifacts:
  - name: architecture-design.md
    version: v1.0.0
    status: generated
decision: APPROVED_FOR_HANDOFF
confidence: 0.95
---
```

---

### Step 7: Collect Metrics with IDs

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-C3E9K7
activity_id: ACT-000012
timestamp: 2026-07-01T10:25:30.450Z
agent: solution_architect
execution_time: 330000
artifact_count: {generated: 4, updated: 0}
validation_score: 0.88
confidence_score: 0.92
completion_percentage: 1.0
---
```

---

### Step 8: Include IDs in Handoff Contract

```yaml
---
workflow_id: WF-20260701-0001
correlation_ids_used: [CORR-C3E9K7]
activity_id_last: ACT-000012
---

## Current Stage

- Workflow: WF-20260701-0001 [UNCHANGED]
- Agent: Solution Architect
- Stage: Architecture Design Complete
- Outcome: completed

## Inputs Consumed
- requirements-spec.md (v1.0.0) [from business_analyst]
- user-stories.md (v1.0.0) [from business_analyst]

## Artifacts Produced
- architecture-design.md (v1.0.0)
- api-contracts.md (v1.0.0)
- technology-stack.md (v1.0.0)
- security-architecture.md (v1.0.0)

## Next Agent(s)
- Primary: Backend Developer, UI/UX Developer, Database Developer (Parallel)
- Workflow ID (preserved): WF-20260701-0001
- Next Correlation ID (for parallel agents):
  - Backend: CORR-F1X9K2
  - Database: CORR-P7R2N4

## Workflow Status
- Status: READY
- Next Activity ID Counter: 13
```

---

### Step 9: Include IDs in OpenLog

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-C3E9K7
---

## Workflow Status

- Workflow ID: WF-20260701-0001 [Preserved from Business Analyst]
- Correlation ID: CORR-C3E9K7 [Generated for Architecture phase]
- Status: READY
- Activities Completed: ACT-000006 to ACT-000012
- Artifacts Generated: 4
- Validation Score: 0.88
- Approval Status: AWAITING_APPROVAL

## Open Questions

- Should architecture support multi-tenancy? [Needs clarification]
```

---

### Step 10: Include IDs in Quality Report

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-C3E9K7
activity_id: ACT-000011
timestamp: 2026-07-01T10:25:15Z
---

## Quality Assessment

- Workflow: WF-20260701-0001
- Phase: Architecture Design (CORR-C3E9K7)
- Validation Score: 0.88
- Quality Score: 0.90
- Completeness: 100%
- Approval Status: APPROVED
```

---

## Complete Execution Flow Example

### Business Analyst (Phase 1)

```
Receive from Supervisor:
  workflow_id: WF-20260701-0001
  activity_id_counter_start: 1

Generate:
  correlation_id: CORR-8A7F2D (NEW)
  activity_ids: ACT-000001 to ACT-000005

Emit:
  LOG: agent_startup (WF-20260701-0001, CORR-8A7F2D, ACT-000001)
  LOG: analyze_requirements (WF-20260701-0001, CORR-8A7F2D, ACT-000002)
  LOG: generate_artifact (WF-20260701-0001, CORR-8A7F2D, ACT-000003)
  AUDIT: artifact_generated (WF-20260701-0001, CORR-8A7F2D, ACT-000003)
  METRICS: completion (WF-20260701-0001, CORR-8A7F2D, ACT-000005)

Artifacts:
  requirements-spec.md (WF-20260701-0001, CORR-8A7F2D, ACT-000003)
  user-stories.md (WF-20260701-0001, CORR-8A7F2D, ACT-000003)

Handoff:
  workflow_id: WF-20260701-0001 [UNCHANGED]
  correlation_ids_used: [CORR-8A7F2D]
  activity_id_last: ACT-000005
  next_agent: Solution Architect
```

### Solution Architect (Phase 2)

```
Receive from Supervisor:
  workflow_id: WF-20260701-0001 [SAME]
  activity_id_counter_start: 6

Generate:
  correlation_id: CORR-C3E9K7 (NEW - different phase)
  activity_ids: ACT-000006 to ACT-000012

Emit:
  LOG: agent_startup (WF-20260701-0001, CORR-C3E9K7, ACT-000006)
  LOG: design_architecture (WF-20260701-0001, CORR-C3E9K7, ACT-000007)
  LOG: specify_api_contracts (WF-20260701-0001, CORR-C3E9K7, ACT-000008)
  AUDIT: artifact_generated (WF-20260701-0001, CORR-C3E9K7, ACT-000009)
  METRICS: completion (WF-20260701-0001, CORR-C3E9K7, ACT-000012)

Artifacts:
  architecture-design.md (WF-20260701-0001, CORR-C3E9K7, ACT-000009)
  api-contracts.md (WF-20260701-0001, CORR-C3E9K7, ACT-000009)

Handoff:
  workflow_id: WF-20260701-0001 [UNCHANGED]
  correlation_ids_used: [CORR-C3E9K7]
  activity_id_last: ACT-000012
  next_agents: Backend Developer, Database Developer (parallel)
```

### Backend Developer (Phase 3a - Parallel)

```
Receive from Supervisor:
  workflow_id: WF-20260701-0001 [SAME]
  activity_id_counter_start: 13

Generate:
  correlation_id: CORR-F1X9K2 (NEW - parallel phase)
  activity_ids: ACT-000013 to ACT-000020

Emit:
  LOG: agent_startup (WF-20260701-0001, CORR-F1X9K2, ACT-000013)
  LOG: implement_api (WF-20260701-0001, CORR-F1X9K2, ACT-000014)
  [... continue with correlation_id = CORR-F1X9K2 ...]
  METRICS: completion (WF-20260701-0001, CORR-F1X9K2, ACT-000020)

Artifacts:
  api-spec.md (WF-20260701-0001, CORR-F1X9K2, ACT-000014)
  backend-design.md (WF-20260701-0001, CORR-F1X9K2, ACT-000015)

Handoff:
  workflow_id: WF-20260701-0001 [UNCHANGED]
  correlation_ids_used: [CORR-F1X9K2]
  activity_id_last: ACT-000020
  next_agent: QA Engineer
```

### Database Developer (Phase 3b - Parallel)

```
Receive from Supervisor:
  workflow_id: WF-20260701-0001 [SAME]
  activity_id_counter_start: 21

Generate:
  correlation_id: CORR-P7R2N4 (NEW - different parallel phase)
  activity_ids: ACT-000021 to ACT-000028

Emit:
  LOG: agent_startup (WF-20260701-0001, CORR-P7R2N4, ACT-000021)
  LOG: design_schema (WF-20260701-0001, CORR-P7R2N4, ACT-000022)
  [... continue with correlation_id = CORR-P7R2N4 ...]
  METRICS: completion (WF-20260701-0001, CORR-P7R2N4, ACT-000028)

Artifacts:
  database-schema.md (WF-20260701-0001, CORR-P7R2N4, ACT-000022)
  migrations.md (WF-20260701-0001, CORR-P7R2N4, ACT-000023)

Handoff:
  workflow_id: WF-20260701-0001 [UNCHANGED]
  correlation_ids_used: [CORR-P7R2N4]
  activity_id_last: ACT-000028
  next_agent: QA Engineer
```

---

## Key Principles

### 1. Preserve Workflow ID

```python
# ✅ DO
workflow_id_in = "WF-20260701-0001"
workflow_id_out = workflow_id_in  # SAME

# ❌ DON'T
workflow_id_out = "WF-20260701-0001-MODIFIED"  # Never change
```

### 2. Generate New Correlation ID per Phase

```python
# ✅ DO
if new_phase:
    correlation_id = generate_correlation_id()  # CORR-C3E9K7

# ❌ DON'T
correlation_id = prior_correlation_id  # Don't reuse from prior agent
```

### 3. Increment Activity IDs

```python
# ✅ DO
activity_id_counter = 6  # Received from prior agent
activity_id = activity_id_counter  # ACT-000006
activity_id_counter += 1  # Next: ACT-000007

# ❌ DON'T
activity_id = "ACT-000001"  # Don't reset counter
activity_id = uuid.uuid4()  # Don't use random IDs
```

### 4. Include All IDs in All Records

```python
# ✅ DO
log_entry = {
    "workflow_id": "WF-20260701-0001",
    "correlation_id": "CORR-C3E9K7",
    "activity_id": "ACT-000008",
    "timestamp": "2026-07-01T10:22:15Z",
    "agent": "solution_architect",
    "action": "specify_api_contracts",
    ...
}

# ❌ DON'T
log_entry = {
    "agent": "solution_architect",
    "action": "specify_api_contracts",
    # Missing: workflow_id, correlation_id, activity_id
    ...
}
```

---

## Validation Checklist for Each Agent

- [ ] Workflow ID received from Supervisor/prior agent
- [ ] Workflow ID preserved unchanged
- [ ] New Correlation ID generated for this phase
- [ ] Activity ID counter received from prior agent
- [ ] Activity IDs incremented sequentially (not reset)
- [ ] All logs include: workflow_id, correlation_id, activity_id
- [ ] All audit records include: workflow_id, correlation_id, activity_id
- [ ] All metrics include: workflow_id, correlation_id, activity_id
- [ ] All artifacts have metadata header with all IDs
- [ ] Handoff contract includes workflow_id (unchanged)
- [ ] Handoff contract includes correlation_ids_used
- [ ] Handoff contract includes activity_id_last
- [ ] OpenLog includes workflow_id in metadata
- [ ] Quality report includes workflow_id in metadata
- [ ] No orphaned records (missing workflow_id)

---

## Supervisor Verification

After each handoff, Supervisor must:

```python
# 1. Verify Workflow ID unchanged
assert handoff["workflow_id"] == prior_workflow_id

# 2. Verify Correlation IDs
assert len(handoff["correlation_ids_used"]) > 0

# 3. Verify Activity ID continuity
next_activity_id = handoff["activity_id_last"] + 1
for log in next_agent_logs:
    if log["activity_id"].startswith("ACT-"):
        assert int(log["activity_id"][4:]) >= next_activity_id

# 4. Verify all records have workflow_id
for record in all_records:
    assert record["workflow_id"] == workflow_id
```

---

**Status:** ✅ Ready for Implementation  
**Last Updated:** 2026-07-01  
**Version:** 1.0.0
