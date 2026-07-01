# Workflow Correlation and Traceability Instructions

**Version:** 1.0.0  
**Status:** Shared Platform Capability  
**Last Updated:** 2026-07-01

This document provides unified workflow correlation and traceability guidance for all agents in the Agentic SDLC platform.

**Purpose:** Enable deterministic tracing, auditing, debugging, reporting, and observability across the entire SDLC pipeline.

---

## Overview

Every project execution generates three tiers of correlation IDs:

1. **Workflow ID** — Unique identifier for entire project execution (created once, propagated unchanged)
2. **Correlation ID** — Groups related operations across agent boundaries
3. **Activity ID** — Traces individual significant actions within an agent

These identifiers must flow through all artifacts, logs, audits, and metrics to enable complete end-to-end traceability.

---

## Workflow ID

### What Is It?

A unique identifier for a complete project execution from Business Analysis through production deployment.

### Format

```
WF-YYYYMMDD-NNNN
```

- **WF** = Workflow prefix (constant)
- **YYYYMMDD** = Date (ISO 8601 date only)
- **NNNN** = Sequential counter for that day (0001, 0002, etc.)

### Examples

```
WF-20260701-0001  (First workflow on July 1, 2026)
WF-20260701-0002  (Second workflow on July 1, 2026)
WF-20260702-0001  (First workflow on July 2, 2026)
WF-20261231-9999  (9999th workflow on Dec 31, 2026)
```

### Lifecycle

```
Supervisor starts workflow execution
  ↓
Supervisor generates Workflow ID (e.g., WF-20260701-0001)
  ↓
Supervisor passes to Business Analyst
  ↓
Business Analyst preserves Workflow ID (no changes)
  ↓
Business Analyst passes to Solution Architect
  ↓
Solution Architect preserves Workflow ID (no changes)
  ↓
... [all agents preserve unchanged] ...
  ↓
Documentation Agent finishes
  ↓
Supervisor archives with Workflow ID as key
```

### Responsibility

**Supervisor ONLY:**
- Creates initial Workflow ID once per workflow
- Passes Workflow ID to first agent (Business Analyst)
- Retrieves Workflow ID from each agent's handoff

**All Agents:**
- Receive Workflow ID from Supervisor
- Preserve Workflow ID unchanged
- Include Workflow ID in all artifacts
- Include Workflow ID in all logs
- Include Workflow ID in all audit records
- Include Workflow ID in all metrics
- Pass same Workflow ID to next agent

---

## Correlation ID

### What Is It?

A unique identifier that groups a set of related operations that logically belong together, even if they span multiple agents or time periods.

### Format

```
CORR-XXXXXXXX
```

- **CORR** = Correlation prefix (constant)
- **XXXXXXXX** = Random 8-character hex or alphanumeric string

### Examples

```
CORR-8A7F2D  (Analyze requirements phase)
CORR-C3E9K7  (Architecture design phase)
CORR-F2M4X1  (Approval workflow)
CORR-Q9N6P8  (Database migration)
```

### Lifecycle

```
Agent starts significant operation (e.g., "Analyze all requirements")
  ↓
Agent generates Correlation ID (e.g., CORR-8A7F2D)
  ↓
Agent includes Correlation ID in first log entry
  ↓
Related log entries reuse same Correlation ID
  ↓
Related audit records reuse same Correlation ID
  ↓
Subtasks within operation use same Correlation ID
  ↓
Operation completes
  ↓
Next phase generates NEW Correlation ID
```

### Usage Patterns

**Pattern 1: Single-Agent Operation**
```
Analyze Requirements
  ├─ CORR-8A7F2D: Parse specification
  ├─ CORR-8A7F2D: Extract requirements
  ├─ CORR-8A7F2D: Create user stories
  ├─ CORR-8A7F2D: Validate completeness
  └─ CORR-8A7F2D: Generate requirement artifacts

Pattern 2: Multi-Agent Workflow**
Architecture Design
  ├─ Agent: Solution Architect
  │  ├─ CORR-C3E9K7: Design layers
  │  ├─ CORR-C3E9K7: Specify components
  │  └─ CORR-C3E9K7: Define APIs
  │
  └─ Agent: Backend Developer (receives CORR-C3E9K7 from handoff)
     ├─ CORR-C3E9K7: Implement API endpoints
     ├─ CORR-C3E9K7: Add middleware
     └─ CORR-C3E9K7: Create service layer

Pattern 3: Approval Workflow**
Approval Gate
  ├─ CORR-F2M4X1: Backend Developer requests approval
  ├─ CORR-F2M4X1: Reviewer receives request
  ├─ CORR-F2M4X1: Reviewer reviews code
  ├─ CORR-F2M4X1: Reviewer approves
  └─ CORR-F2M4X1: Backend Developer notified of approval

Pattern 4: Phase Transition**
Phase 1: Business Analysis
  └─ CORR-8A7F2D: All requirements work

Phase 2: Architecture
  └─ CORR-C3E9K7: All architecture work (NEW Correlation ID)

Phase 3: Development
  ├─ CORR-F1X9K2: All frontend work (NEW Correlation ID)
  ├─ CORR-Q8M3L6: All backend work (NEW Correlation ID)
  └─ CORR-P7R2N4: All database work (NEW Correlation ID)
```

### Responsibility

**All Agents:**
- Generate new Correlation ID for each logical operation
- Reuse Correlation ID for related sub-operations
- Include Correlation ID in logs, audits, and metrics
- Pass Correlation ID to related operations
- Document which Correlation IDs were used in handoff contract

**Supervisor:**
- Receives Correlation IDs from each agent
- Groups logs/audits/metrics by Correlation ID
- Reconstructs logical workflows from Correlation IDs

---

## Activity ID

### What Is It?

A unique identifier for a single, discrete action or significant event within an agent's execution.

### Format

```
ACT-NNNNNN
```

- **ACT** = Activity prefix (constant)
- **NNNNNN** = Sequential number (000001, 000002, etc.)

### Examples

```
ACT-000001  (Generate requirements-spec.md)
ACT-000002  (Generate user-stories.md)
ACT-000003  (Validate requirements)
ACT-000004  (Create acceptance-criteria.md)
ACT-000005  (Agent completion)
```

### Lifecycle

```
Activity starts (e.g., "Generate artifact")
  ↓
Activity generates Activity ID (e.g., ACT-000001)
  ↓
Activity emits log entry with Activity ID
  ↓
Activity creates audit record with Activity ID
  ↓
Activity records metrics with Activity ID
  ↓
Activity completes
  ↓
Next activity generates NEW Activity ID (ACT-000002)
```

### Usage Patterns

**Pattern 1: Single Log Entry per Activity**
```
LOG: timestamp=14:22:30, activity_id=ACT-000001, action=analyze_requirements, status=started
LOG: timestamp=14:22:35, activity_id=ACT-000001, action=analyze_requirements, status=completed, duration=5000ms
```

**Pattern 2: Multi-Step Activity**
```
LOG: timestamp=14:22:30, activity_id=ACT-000001, action=generate_artifact, status=started
LOG: timestamp=14:22:31, activity_id=ACT-000001, action=generate_artifact, status=in_progress, message="Writing 127 lines"
LOG: timestamp=14:22:33, activity_id=ACT-000001, action=generate_artifact, status=completed, duration=3000ms, artifact=requirements-spec.md
```

**Pattern 3: Activity with Audit Trail**
```
LOG: activity_id=ACT-000001, action=validate_artifact, status=completed
AUDIT: activity_id=ACT-000001, action=quality_gate_passed, artifact=requirements-spec.md
```

**Pattern 4: Activity Sequence**
```
Phase: Business Analysis

ACT-000001: Analyze Requirements
├─ LOG: Started
├─ AUDIT: Artifact generated
└─ LOG: Completed

ACT-000002: Create User Stories
├─ LOG: Started
├─ AUDIT: Artifact generated
└─ LOG: Completed

ACT-000003: Validate Output
├─ LOG: Started
├─ AUDIT: Quality gate passed
└─ LOG: Completed
```

### Responsibility

**All Agents:**
- Generate unique Activity ID for each significant action
- Include Activity ID in every log entry for that action
- Include Activity ID in audit records
- Include Activity ID in metrics for that activity
- Never reuse Activity ID within same workflow

**Log Aggregation:**
- Supervisor groups logs by Activity ID
- Can reconstruct sequence of all activities using Activity IDs

---

## Including IDs in Artifacts

### 1. Handoff Contract

```markdown
---
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
activity_id: ACT-000005
stage: Business Analysis
agent: Business Analyst
timestamp: 2026-07-01T10:31:21Z
---

## Current Stage

- Workflow: WF-20260701-0001
- Agent: Business Analyst
- Stage: Business Analysis Phase Complete
- Outcome: completed
```

### 2. OpenLog

```markdown
---
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
---

## Workflow Status

- Workflow ID: WF-20260701-0001
- Correlation ID: CORR-8A7F2D
- Status: READY
```

### 3. Quality Report

```markdown
---
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
activity_id: ACT-000003
timestamp: 2026-07-01T10:31:15Z
---

## Quality Assessment

- Workflow ID: WF-20260701-0001
- Validation Score: 0.94
```

### 4. All Core Artifacts

Every generated artifact (requirements-spec.md, architecture-design.md, etc.) must include:

```markdown
---
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
artifact_version: v1.0.0
generated_by: business_analyst
activity_id: ACT-000001
timestamp: 2026-07-01T10:31:21Z
---

# Artifact Content
```

### 5. Log Entries

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
activity_id: ACT-000001
timestamp: 2026-07-01T14:22:33.125Z
agent: business_analyst
action: analyze_requirements
status: completed
duration: 2500
message: "Completed requirements analysis"
---
```

### 6. Audit Records

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
activity_id: ACT-000001
audit_id: audit-20260701-001
timestamp: 2026-07-01T14:22:33.125Z
agent: business_analyst
action: artifact_generated
decision: APPROVED_FOR_HANDOFF
---
```

### 7. Metrics Records

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
activity_id: ACT-000001
timestamp: 2026-07-01T14:22:45.300Z
agent: business_analyst
execution_time: 2500
validation_score: 0.94
---
```

---

## Workflow Reconstruction

The Supervisor can reconstruct the complete execution history using only the Workflow ID:

```
QUERY: Retrieve all records for Workflow ID = WF-20260701-0001

RESULTS:
├─ All log entries with workflow_id = WF-20260701-0001
│  ├─ Business Analyst logs (CORR-8A7F2D, ACT-000001...ACT-000005)
│  ├─ Solution Architect logs (CORR-C3E9K7, ACT-000006...ACT-000012)
│  ├─ Backend Developer logs (CORR-F1X9K2, ACT-000013...ACT-000020)
│  ├─ Database Developer logs (CORR-P7R2N4, ACT-000021...ACT-000028)
│  ├─ QA Engineer logs (CORR-Q8M3L6, ACT-000029...ACT-000035)
│  ├─ Reviewer logs (CORR-R9N2K4, ACT-000036...ACT-000040)
│  └─ DevOps logs (CORR-D4X7L1, ACT-000041...ACT-000045)
│
├─ All audit records with workflow_id = WF-20260701-0001
│  ├─ 7 artifact_generated records (one per phase)
│  ├─ 3 approval_requested records
│  ├─ 3 approval_decision records (2 approved, 1 pending)
│  └─ 2 quality_gate_passed records
│
├─ All metrics with workflow_id = WF-20260701-0001
│  ├─ Business Analyst metrics (execution_time: 2500ms, validation: 0.94)
│  ├─ Solution Architect metrics (execution_time: 3200ms, validation: 0.88)
│  ├─ Backend Developer metrics (execution_time: 5200ms, validation: 0.76)
│  └─ ... [complete timeline]
│
└─ Handoff contracts (each preserves WF-20260701-0001)
   ├─ business_analyst_handoff.md
   ├─ solution_architect_handoff.md
   ├─ backend_developer_handoff.md
   └─ ... [all agents]

RECONSTRUCTION:
- Complete execution timeline (sorted by timestamp)
- All decisions made (audit trail)
- Performance metrics (quality trends)
- Error/warning history
- Approval gate history
- Phase transitions
- Total execution time
```

---

## ID Propagation Rules

### Supervisor → Agent

```
Supervisor generates Workflow ID: WF-20260701-0001
Supervisor → Business Analyst:
  ├─ workflow_id: WF-20260701-0001
  ├─ sequence_number: 1
  └─ Request: Execute Business Analysis

Business Analyst executes and generates Correlation ID: CORR-8A7F2D
Business Analyst generates Activity IDs: ACT-000001...ACT-000005

Business Analyst → Supervisor (in handoff):
  ├─ workflow_id: WF-20260701-0001 [UNCHANGED]
  ├─ correlation_ids_used: [CORR-8A7F2D]
  ├─ activity_id_last: ACT-000005
  └─ Result: READY for Solution Architect
```

### Agent → Next Agent

```
Supervisor → Solution Architect:
  ├─ workflow_id: WF-20260701-0001 [FROM Business Analyst]
  ├─ sequence_number: 2
  ├─ prior_correlation_ids: [CORR-8A7F2D]
  ├─ activity_id_counter_start: 6
  └─ Request: Execute Architecture Design

Solution Architect executes and generates Correlation ID: CORR-C3E9K7
Solution Architect generates Activity IDs: ACT-000006...ACT-000012

Solution Architect → Supervisor (in handoff):
  ├─ workflow_id: WF-20260701-0001 [UNCHANGED]
  ├─ correlation_ids_used: [CORR-C3E9K7]
  ├─ activity_id_last: ACT-000012
  └─ Result: READY for Parallel Developers
```

---

## Implementation Rules

1. **Never regenerate Workflow ID**: Once created, it must be identical throughout entire pipeline
2. **Activity IDs are sequential**: Within an agent, ACT-000001, ACT-000002, etc.
3. **Correlation IDs group operations**: New Correlation ID per logical phase
4. **All records reference IDs**: Logs, audits, metrics, artifacts all include IDs
5. **Preserve in handoff**: Every handoff contract includes workflow_id unchanged
6. **Supervisor aggregates by ID**: All records keyed by Workflow ID for reconstruction

---

## Traceability Anti-Patterns

❌ **Do NOT:**
- Modify Workflow ID at any point
- Reuse Activity ID within same agent
- Create Activity ID without logging
- Omit IDs from artifacts
- Use non-standard ID formats
- Lose track of correlation boundaries
- Forget to include IDs in handoff contracts

✅ **DO:**
- Preserve Workflow ID unchanged
- Generate unique Activity IDs sequentially
- Create new Correlation ID per logical phase
- Include IDs in all records
- Use standard ID formats
- Pass IDs to next agent
- Document ID usage in handoff

---

## Reference Templates

Use the following templates:

- `ai/templates/workflow-correlation.md` — Complete ID usage template
- `ai/templates/handoff-contract.md` — Update to include IDs in header
- `ai/templates/openlog.md` — Update to include IDs in metadata
- `ai/templates/quality-report.md` — Update to include IDs in metadata

---

## Supervisor Responsibilities

The Supervisor:
- Creates initial Workflow ID on startup
- Passes Workflow ID to each agent
- Verifies Workflow ID preservation in each handoff
- Collects all logs, audits, metrics with Workflow ID
- Indexes records by Workflow ID for retrieval
- Reconstructs complete execution history using Workflow ID
- Detects missing or orphaned records (not in Workflow ID)
- Provides tracing/debugging tools based on IDs

**Agents do not need to implement custom traceability logic. Use shared instructions and templates only.**
