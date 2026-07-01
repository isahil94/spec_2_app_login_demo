# Workflow Correlation Template

**Template Version:** 1.0.0  
**Status:** Standard Template  
**Last Updated:** 2026-07-01

Use this template to understand how Workflow ID, Correlation ID, and Activity ID flow through the platform.

---

## Workflow ID Format

```
WF-YYYYMMDD-NNNN
```

Example:
```
WF-20260701-0001
WF-20260701-0002
WF-20260702-0001
```

---

## Correlation ID Format

```
CORR-XXXXXXXX
```

Example:
```
CORR-8A7F2D
CORR-C3E9K7
CORR-F1X9K2
```

---

## Activity ID Format

```
ACT-NNNNNN
```

Example:
```
ACT-000001
ACT-000002
ACT-000003
```

---

## Complete Workflow Example

### Project: Task Management System

**Workflow Started:** 2026-07-01 10:15 AM  
**Workflow ID:** WF-20260701-0001

---

### Phase 1: Business Analysis

**Agent:** Business Analyst  
**Correlation ID:** CORR-8A7F2D  
**Activity IDs:** ACT-000001 to ACT-000005

#### Activity Sequence

```
ACT-000001: Agent Startup
  ├─ LOG: agent_startup, workflow_id=WF-20260701-0001, correlation_id=CORR-8A7F2D, activity_id=ACT-000001
  └─ Timestamp: 2026-07-01T10:15:00Z

ACT-000002: Analyze Requirements
  ├─ LOG: analyze_requirements, status=started, workflow_id=WF-20260701-0001, correlation_id=CORR-8A7F2D, activity_id=ACT-000002
  ├─ [work for 3.1 seconds]
  ├─ LOG: analyze_requirements, status=completed, duration=3100ms
  └─ Timestamp: 2026-07-01T10:15:03.125Z

ACT-000003: Generate Artifacts
  ├─ LOG: generate_artifact, status=started, artifact=requirements-spec.md, activity_id=ACT-000003
  ├─ ARTIFACT: requirements-spec.md generated with:
  │  └─ HEADER: workflow_id=WF-20260701-0001, correlation_id=CORR-8A7F2D, activity_id=ACT-000003
  ├─ LOG: generate_artifact, status=completed
  └─ AUDIT: artifact_generated, workflow_id=WF-20260701-0001, activity_id=ACT-000003

ACT-000004: Validate Output
  ├─ LOG: validate_output, status=started, activity_id=ACT-000004
  ├─ LOG: validate_output, status=completed, validation_score=0.94
  └─ AUDIT: quality_gate_passed, workflow_id=WF-20260701-0001, activity_id=ACT-000004

ACT-000005: Agent Completion
  ├─ HANDOFF CONTRACT: (preservation of IDs)
  │  ├─ workflow_id: WF-20260701-0001 [UNCHANGED]
  │  ├─ correlation_ids_used: [CORR-8A7F2D]
  │  ├─ activity_id_last: ACT-000005
  │  └─ Next Stage: Solution Architect
  ├─ METRICS: workflow_id=WF-20260701-0001, correlation_id=CORR-8A7F2D, activity_id=ACT-000005
  └─ Timestamp: 2026-07-01T10:15:45Z
```

---

### Phase 2: Solution Architecture

**Agent:** Solution Architect  
**Correlation ID:** CORR-C3E9K7 (NEW)  
**Activity IDs:** ACT-000006 to ACT-000012

#### Activity Sequence

```
ACT-000006: Load Input Artifacts
  ├─ LOG: load_artifacts, workflow_id=WF-20260701-0001, correlation_id=CORR-C3E9K7, activity_id=ACT-000006
  │  (Note: workflow_id is PRESERVED from Business Analyst)
  └─ Timestamp: 2026-07-01T10:20:00Z

ACT-000007: Design Architecture
  ├─ LOG: design_architecture, status=started, activity_id=ACT-000007
  ├─ [work for 3.2 seconds]
  └─ LOG: design_architecture, status=completed, duration=3200ms

ACT-000008: Specify API Contracts
  ├─ LOG: specify_api_contracts, status=started, activity_id=ACT-000008
  └─ LOG: specify_api_contracts, status=completed

ACT-000009: Generate Architecture Artifacts
  ├─ ARTIFACT: architecture-design.md with:
  │  └─ HEADER: workflow_id=WF-20260701-0001, correlation_id=CORR-C3E9K7, activity_id=ACT-000009
  ├─ ARTIFACT: api-contracts.md with:
  │  └─ HEADER: workflow_id=WF-20260701-0001, correlation_id=CORR-C3E9K7, activity_id=ACT-000009
  └─ AUDIT: artifact_generated, workflow_id=WF-20260701-0001, correlation_id=CORR-C3E9K7, activity_id=ACT-000009

ACT-000010: Request Approval
  ├─ LOG: request_approval, workflow_id=WF-20260701-0001, activity_id=ACT-000010
  ├─ AUDIT: approval_requested, workflow_id=WF-20260701-0001, correlation_id=CORR-C3E9K7, activity_id=ACT-000010
  ├─ Approval Request ID: apr-WF-20260701-0001-ACT-000010
  └─ Status: AWAITING_APPROVAL

ACT-000011: Receive Approval Decision
  ├─ LOG: approval_decision_received, decision=APPROVED, activity_id=ACT-000011
  └─ AUDIT: approval_decision, workflow_id=WF-20260701-0001, correlation_id=CORR-C3E9K7, activity_id=ACT-000011

ACT-000012: Agent Completion
  ├─ HANDOFF CONTRACT:
  │  ├─ workflow_id: WF-20260701-0001 [PRESERVED]
  │  ├─ correlation_ids_used: [CORR-C3E9K7]
  │  ├─ activity_id_last: ACT-000012
  │  └─ Next Stage: Parallel Development (Backend, Frontend, Database)
  └─ Timestamp: 2026-07-01T10:25:30Z
```

---

### Phase 3a: Backend Development (Parallel)

**Agent:** Backend Developer  
**Correlation ID:** CORR-F1X9K2 (NEW, different from Frontend)  
**Activity IDs:** ACT-000013 to ACT-000020

#### Activity Sequence (Simplified)

```
ACT-000013-ACT-000020: Backend Development
  ├─ All logs include: workflow_id=WF-20260701-0001 [PRESERVED]
  ├─ All logs include: correlation_id=CORR-F1X9K2 [NEW for Backend]
  ├─ ARTIFACTS: api-spec.md, backend-design.md, etc.
  │  └─ Each with header: workflow_id=WF-20260701-0001, correlation_id=CORR-F1X9K2
  └─ HANDOFF: workflow_id preserved
```

---

### Phase 3b: Database Development (Parallel)

**Agent:** Database Developer  
**Correlation ID:** CORR-P7R2N4 (NEW, different from Backend)  
**Activity IDs:** ACT-000021 to ACT-000028

#### Activity Sequence (Simplified)

```
ACT-000021-ACT-000028: Database Development
  ├─ All logs include: workflow_id=WF-20260701-0001 [PRESERVED]
  ├─ All logs include: correlation_id=CORR-P7R2N4 [NEW for Database]
  ├─ ARTIFACTS: database-schema.md, migrations.md, etc.
  │  └─ Each with header: workflow_id=WF-20260701-0001, correlation_id=CORR-P7R2N4
  └─ HANDOFF: workflow_id preserved
```

---

### Phase 4: QA Testing

**Agent:** QA Engineer  
**Correlation ID:** CORR-Q8M3L6 (NEW)  
**Activity IDs:** ACT-000029 to ACT-000035

#### Activity Sequence (Simplified)

```
ACT-000029-ACT-000035: QA Testing
  ├─ All logs include: workflow_id=WF-20260701-0001 [PRESERVED]
  ├─ All logs include: correlation_id=CORR-Q8M3L6 [NEW for QA]
  ├─ ARTIFACTS: test-report.md, test-results.md
  │  └─ Each with header: workflow_id=WF-20260701-0001, correlation_id=CORR-Q8M3L6
  └─ HANDOFF: workflow_id preserved
```

---

### Phase 5: Review

**Agent:** Reviewer  
**Correlation ID:** CORR-R9N2K4 (NEW)  
**Activity IDs:** ACT-000036 to ACT-000040

#### Activity Sequence (Simplified)

```
ACT-000036-ACT-000040: Review
  ├─ All logs include: workflow_id=WF-20260701-0001 [PRESERVED]
  ├─ All logs include: correlation_id=CORR-R9N2K4 [NEW for Review]
  ├─ ARTIFACTS: review-report.md, findings.md
  │  └─ Each with header: workflow_id=WF-20260701-0001, correlation_id=CORR-R9N2K4
  └─ HANDOFF: workflow_id preserved
```

---

### Phase 6: DevOps & Release

**Agent:** DevOps & Release  
**Correlation ID:** CORR-D4X7L1 (NEW)  
**Activity IDs:** ACT-000041 to ACT-000045

#### Activity Sequence (Simplified)

```
ACT-000041-ACT-000045: Deployment
  ├─ All logs include: workflow_id=WF-20260701-0001 [PRESERVED]
  ├─ All logs include: correlation_id=CORR-D4X7L1 [NEW for DevOps]
  ├─ ARTIFACTS: deployment-plan.md, release-notes.md
  │  └─ Each with header: workflow_id=WF-20260701-0001, correlation_id=CORR-D4X7L1
  └─ HANDOFF: workflow_id preserved
```

---

### Phase 7: Documentation

**Agent:** Documentation  
**Correlation ID:** CORR-E2K5J8 (NEW)  
**Activity IDs:** ACT-000046 to ACT-000050

#### Activity Sequence (Simplified)

```
ACT-000046-ACT-000050: Documentation
  ├─ All logs include: workflow_id=WF-20260701-0001 [PRESERVED]
  ├─ All logs include: correlation_id=CORR-E2K5J8 [NEW for Documentation]
  ├─ ARTIFACTS: user-guide.md, developer-guide.md, api-documentation.md
  │  └─ Each with header: workflow_id=WF-20260701-0001, correlation_id=CORR-E2K5J8
  └─ HANDOFF: workflow_id preserved
```

---

## Supervisor Reconstruction Example

**Query:** "Show me complete execution history for WF-20260701-0001"

**Result:**

```
Workflow ID: WF-20260701-0001
Start Time: 2026-07-01T10:15:00Z
End Time: 2026-07-01T11:45:30Z
Total Duration: 1h 30m 30s
Status: COMPLETED

PHASE BREAKDOWN:

├─ Business Analysis (10:15-10:15:45)
│  ├─ Correlation: CORR-8A7F2D
│  ├─ Activities: ACT-000001 to ACT-000005
│  ├─ Artifacts: 5 generated
│  ├─ Validation: 0.94
│  └─ Status: READY
│
├─ Architecture (10:20-10:25:30)
│  ├─ Correlation: CORR-C3E9K7
│  ├─ Activities: ACT-000006 to ACT-000012
│  ├─ Artifacts: 4 generated
│  ├─ Validation: 0.88
│  ├─ Approval: APPROVED
│  └─ Status: READY
│
├─ Backend Development (10:30-11:00) [Parallel]
│  ├─ Correlation: CORR-F1X9K2
│  ├─ Activities: ACT-000013 to ACT-000020
│  ├─ Artifacts: 3 generated
│  ├─ Validation: 0.76
│  └─ Status: READY
│
├─ Database Development (10:30-11:05) [Parallel]
│  ├─ Correlation: CORR-P7R2N4
│  ├─ Activities: ACT-000021 to ACT-000028
│  ├─ Artifacts: 2 generated
│  ├─ Validation: 0.92
│  └─ Status: READY
│
├─ QA Testing (11:10-11:25)
│  ├─ Correlation: CORR-Q8M3L6
│  ├─ Activities: ACT-000029 to ACT-000035
│  ├─ Artifacts: 2 generated
│  ├─ Validation: 0.98
│  └─ Status: READY
│
├─ Review (11:30-11:38)
│  ├─ Correlation: CORR-R9N2K4
│  ├─ Activities: ACT-000036 to ACT-000040
│  ├─ Artifacts: 2 generated
│  ├─ Validation: 0.95
│  ├─ Approval: APPROVED
│  └─ Status: READY
│
└─ Deployment (11:40-11:45:30)
   ├─ Correlation: CORR-D4X7L1
   ├─ Activities: ACT-000041 to ACT-000050
   ├─ Artifacts: 2 generated
   ├─ Validation: 0.97
   └─ Status: COMPLETED

AGGREGATE METRICS:
- Total Activities: 50
- Total Artifacts: 20
- Average Validation: 0.91
- Total Approvals: 2 (both approved)
- Errors: 0
- Warnings: 3
- Final Status: READY FOR PRODUCTION

TRACEABILITY:
- Used by: Query "SELECT * WHERE workflow_id = 'WF-20260701-0001'"
- Can retrieve: All logs, audits, metrics, artifacts
- Can debug: Any activity using Activity ID
- Can group: Operations using Correlation ID
- Can timeline: Complete execution path
```

---

## Implementation in Log Entries

### Business Analyst Log Entry

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
activity_id: ACT-000002
timestamp: 2026-07-01T10:15:03.125Z
agent: business_analyst
action: analyze_requirements
status: completed
artifact: requirements-spec.md
duration: 3100
message: "Analyzed requirements and generated requirements-spec.md"
---
```

### Solution Architect Log Entry

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-C3E9K7
activity_id: ACT-000008
timestamp: 2026-07-01T10:23:15.450Z
agent: solution_architect
action: specify_api_contracts
status: completed
artifact: api-contracts.md
duration: 2400
message: "Specified all API contracts with 24 endpoints"
---
```

### Backend Developer Log Entry

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-F1X9K2
activity_id: ACT-000018
timestamp: 2026-07-01T10:45:22.800Z
agent: backend_developer
action: validate_api
status: completed
artifact: api-spec.md
duration: 1500
message: "API validation passed: 24 endpoints, 0 errors"
---
```

---

## Implementation in Audit Records

### Artifact Generation Audit

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
activity_id: ACT-000003
audit_id: audit-ACT-000003-001
timestamp: 2026-07-01T10:15:05.200Z
agent: business_analyst
action: artifact_generated
reason: "Generated requirements-spec.md with 42 requirements"
output_artifacts:
  - name: requirements-spec.md
    version: v1.0.0
    status: generated
decision: APPROVED_FOR_HANDOFF
confidence: 0.95
---
```

### Approval Decision Audit

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-C3E9K7
activity_id: ACT-000011
audit_id: audit-ACT-000011-001
timestamp: 2026-07-01T10:25:20.100Z
agent: supervisor
action: approval_decision
reason: "Architecture approved by lead architect"
decision: APPROVED
approval_request_id: apr-WF-20260701-0001-ACT-000010
confidence: 1.0
---
```

---

## Implementation in Metrics

### Business Analyst Metrics

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
activity_id: ACT-000005
timestamp: 2026-07-01T10:15:45.300Z
agent: business_analyst
execution_time: 45000
artifact_count: {generated: 5, updated: 0}
validation_score: 0.94
confidence_score: 0.95
completion_percentage: 1.0
---
```

### Solution Architect Metrics

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

## Anti-Patterns

❌ **Do NOT:**
- Change Workflow ID at any point
- Reuse Activity ID in same agent
- Create logs without IDs
- Omit IDs from artifacts
- Use different ID formats
- Lose Correlation ID between related operations
- Create Activity ID without corresponding log

✅ **DO:**
- Preserve Workflow ID unchanged
- Generate unique Activity IDs sequentially
- Include IDs in all records
- Document ID usage in handoff
- Use standard ID formats
- Pass IDs to related operations
- Reference IDs in logs and audits

---

**Template Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Status:** Reference Implementation
