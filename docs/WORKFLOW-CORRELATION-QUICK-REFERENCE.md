# Workflow Correlation and Traceability - Quick Reference

**Implementation Date:** 2026-07-01  
**Status:** ✅ COMPLETE  

---

## Three-Tier ID System

| ID Type | Format | Created By | Scope | Example |
|---------|--------|-----------|-------|---------|
| **Workflow ID** | WF-YYYYMMDD-NNNN | Supervisor (once) | Entire project execution | WF-20260701-0001 |
| **Correlation ID** | CORR-XXXXXXXX | Agent (per phase) | Logical phase/operation | CORR-8A7F2D |
| **Activity ID** | ACT-NNNNNN | Agent (per action) | Single action | ACT-000001 |

---

## Quick Rules

### Workflow ID
✅ Created once by Supervisor at startup  
✅ NEVER modified by any agent  
✅ MUST appear in all artifacts, logs, audits, metrics  
✅ Used to reconstruct complete execution  

### Correlation ID
✅ Generated per logical phase  
✅ Groups all related operations  
✅ New ID on phase transition  
✅ Included in logs, audits, metrics  

### Activity ID
✅ Sequential within workflow (ACT-000001, ACT-000002, etc.)  
✅ One per significant action  
✅ Never reused  
✅ Included in logs, audits, metrics  

---

## Example Workflow

```
Workflow ID: WF-20260701-0001 [CREATED ONCE, PRESERVED UNCHANGED]

├─ Phase 1: Business Analysis
│  ├─ Correlation ID: CORR-8A7F2D
│  ├─ Activity IDs: ACT-000001 to ACT-000005
│  └─ All records include: WF-20260701-0001, CORR-8A7F2D
│
├─ Phase 2: Architecture
│  ├─ Correlation ID: CORR-C3E9K7 [NEW]
│  ├─ Activity IDs: ACT-000006 to ACT-000012
│  └─ All records include: WF-20260701-0001 [SAME], CORR-C3E9K7 [NEW]
│
├─ Phase 3a: Backend (Parallel)
│  ├─ Correlation ID: CORR-F1X9K2 [NEW]
│  ├─ Activity IDs: ACT-000013 to ACT-000020
│  └─ All records include: WF-20260701-0001 [SAME], CORR-F1X9K2 [NEW]
│
├─ Phase 3b: Database (Parallel)
│  ├─ Correlation ID: CORR-P7R2N4 [NEW]
│  ├─ Activity IDs: ACT-000021 to ACT-000028
│  └─ All records include: WF-20260701-0001 [SAME], CORR-P7R2N4 [NEW]
│
└─ ... [remaining phases] ...

KEY: WF-20260701-0001 never changes throughout entire workflow
```

---

## ID Usage Location

### In Artifacts (Metadata Header)

```yaml
---
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
activity_id: ACT-000001
timestamp: 2026-07-01T10:15:21Z
generated_by: business_analyst
---
```

### In Log Entries

```yaml
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
activity_id: ACT-000001
timestamp: 2026-07-01T10:15:03.125Z
agent: business_analyst
action: analyze_requirements
status: completed
```

### In Audit Records

```yaml
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
activity_id: ACT-000001
audit_id: audit-ACT-000001-001
timestamp: 2026-07-01T10:15:05.200Z
agent: business_analyst
action: artifact_generated
decision: APPROVED_FOR_HANDOFF
```

### In Metrics Records

```yaml
workflow_id: WF-20260701-0001
correlation_id: CORR-8A7F2D
activity_id: ACT-000005
timestamp: 2026-07-01T10:15:45.300Z
agent: business_analyst
execution_time: 45000
validation_score: 0.94
```

### In Handoff Contracts

```yaml
---
workflow_id: WF-20260701-0001
correlation_ids_used: [CORR-8A7F2D]
activity_id_last: ACT-000005
---
```

---

## Queries by ID Type

### Query by Workflow ID

```sql
SELECT * FROM logs WHERE workflow_id = 'WF-20260701-0001'
```
Returns: Complete execution timeline (all 50+ actions)

### Query by Correlation ID

```sql
SELECT * FROM logs 
WHERE workflow_id = 'WF-20260701-0001' 
AND correlation_id = 'CORR-8A7F2D'
```
Returns: Business Analysis phase only

### Query by Activity ID

```sql
SELECT * FROM logs 
WHERE workflow_id = 'WF-20260701-0001' 
AND activity_id = 'ACT-000001'
```
Returns: Specific action ("analyze_requirements")

---

## Validation Checklist

- [ ] Workflow ID created once by Supervisor
- [ ] Workflow ID preserved unchanged through all agents
- [ ] All artifacts have Workflow ID in metadata header
- [ ] All log entries have Workflow ID
- [ ] All audit records have Workflow ID
- [ ] All metrics records have Workflow ID
- [ ] Correlation IDs generated per phase
- [ ] Activity IDs sequential and unique
- [ ] Handoff contracts include Workflow ID (unchanged)
- [ ] OpenLog includes Workflow ID
- [ ] Quality reports include Workflow ID
- [ ] Supervisor can reconstruct by Workflow ID

---

## Implementation Files

| File | Purpose |
|------|---------|
| `ai/instructions/workflow-correlation.md` | Complete guidance |
| `ai/templates/workflow-correlation.md` | Reference example |
| Agent files (all 10) | Updated to reference instructions |

---

## ID Lifecycle

```
Supervisor Startup
  ├─ Generate Workflow ID: WF-20260701-0001
  └─ Pass to Business Analyst
      ├─ Preserve Workflow ID
      ├─ Generate Correlation ID: CORR-8A7F2D
      ├─ Generate Activity IDs: ACT-000001 to ACT-000005
      ├─ Include all IDs in logs, audits, metrics
      └─ Pass to Solution Architect
          ├─ Preserve Workflow ID: WF-20260701-0001 [SAME]
          ├─ Generate NEW Correlation ID: CORR-C3E9K7
          ├─ Generate Activity IDs: ACT-000006 to ACT-000012
          ├─ Include all IDs in logs, audits, metrics
          └─ Pass to Next Agents...
              └─ Repeat pattern for all agents
```

---

## Supervisor Responsibilities

The Supervisor must:

✅ Create initial Workflow ID  
✅ Pass Workflow ID to first agent  
✅ Retrieve Workflow ID from each handoff contract  
✅ Verify Workflow ID is unchanged  
✅ Collect all logs with Workflow ID  
✅ Collect all audits with Workflow ID  
✅ Collect all metrics with Workflow ID  
✅ Index records by Workflow ID  
✅ Enable queries by Workflow ID, Correlation ID, Activity ID  
✅ Reconstruct complete execution history  

---

## Agent Responsibilities

All agents must:

✅ Receive Workflow ID from Supervisor  
✅ Preserve Workflow ID unchanged  
✅ Include Workflow ID in all artifacts (metadata header)  
✅ Include Workflow ID in all logs  
✅ Include Workflow ID in all audits  
✅ Include Workflow ID in all metrics  
✅ Generate unique Activity IDs  
✅ Generate new Correlation ID per phase  
✅ Include all IDs in handoff contract  
✅ Pass Workflow ID to next agent  

---

## Benefits

| Benefit | Enabled By |
|---------|-----------|
| Find any action | Activity ID |
| Reconstruct phase | Correlation ID |
| Replay entire workflow | Workflow ID |
| Search all decisions | Workflow ID in audits |
| Debug root causes | Workflow ID + Activity ID |
| Analyze performance | Workflow ID + Correlation ID |
| Compliance reporting | Workflow ID + audit trail |
| End-to-end observability | Workflow ID in all records |

---

## References

**Detailed Guidance:**
- [ai/instructions/workflow-correlation.md](ai/instructions/workflow-correlation.md)

**Complete Example:**
- [ai/templates/workflow-correlation.md](ai/templates/workflow-correlation.md)

**Full Implementation:**
- [WORKFLOW-CORRELATION-IMPLEMENTATION.md](WORKFLOW-CORRELATION-IMPLEMENTATION.md)

---

**Status:** ✅ Ready for Implementation  
**Date:** 2026-07-01  
**Version:** 1.0.0
