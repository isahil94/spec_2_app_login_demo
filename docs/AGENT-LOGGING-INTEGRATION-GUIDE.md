# Agent Integration Guide: Logging, Audit & Observability

**Version:** 1.0.0  
**Status:** Implementation Guide  
**Last Updated:** 2026-07-01

## Quick Start for Agents

This guide shows how agents integrate logging, audit, and observability into their execution.

---

## Step 1: Agent Startup

When your agent starts execution:

```
1. Record start timestamp (ISO 8601)
2. Emit startup log entry (status: started)
3. Load input artifacts
4. Begin work
```

### Example: Business Analyst Startup

```yaml
# Log Entry - Agent Startup
timestamp: 2026-07-01T14:20:05.000Z
agent: business_analyst
action: agent_startup
status: started
artifact: n/a
duration: 0
message: "Business Analyst starting execution"
```

---

## Step 2: Log Actions During Execution

For every significant action, emit a log entry:

```
1. Record start timestamp
2. Emit log entry with status: started
3. Perform work
4. Record end timestamp
5. Emit log entry with status: completed (or failed)
6. Include measured duration
```

### Pattern: Action Execution with Logging

```
START = 2026-07-01T14:22:30.000Z
EMIT LOG: action=analyze_requirements, status=started

[... work happens ...]

END = 2026-07-01T14:22:33.125Z
DURATION = (END - START) = 3125ms
EMIT LOG: action=analyze_requirements, status=completed, duration=3125ms
```

### Example: Business Analyst Action Logging

```yaml
# Log Entry 1 - Action Start
timestamp: 2026-07-01T14:22:30.000Z
agent: business_analyst
action: analyze_requirements
status: started
artifact: specification.md
duration: 0
message: "Starting requirements analysis"

# ... 3+ seconds of work happens ...

# Log Entry 2 - Action Complete
timestamp: 2026-07-01T14:22:33.125Z
agent: business_analyst
action: analyze_requirements
status: completed
artifact: requirements-spec.md
duration: 3125
message: "Completed requirements analysis. Generated 42 requirements."
metadata:
  requirement_count: 42
  validation_score: 0.94
```

---

## Step 3: Create Audit Records for Decisions

When you make a significant decision, create an audit record:

### Decision Points

Create audit records for:
- ✅ Generating a new artifact
- ✅ Accepting/rejecting a requirement
- ✅ Choosing between options
- ✅ Passing/failing a validation gate
- ✅ Requesting human approval
- ✅ Escalating a blocker

### Pattern: Audit Record Creation

```
1. Identify the decision made
2. Identify input artifacts consumed
3. Identify output artifacts created
4. Assess confidence in decision
5. Write justification
6. Create audit record using template
```

### Example: Artifact Generation Audit

```yaml
# Audit Record - Artifact Generated
audit_id: audit-20260701-001
timestamp: 2026-07-01T14:22:45.300Z
agent: business_analyst
action: artifact_generated
reason: "Requirements analysis complete and validated successfully."
input_artifacts:
  - name: specification.md
    version: v1.0.0
    source_agent: user
output_artifacts:
  - name: requirements-spec.md
    version: v1.0.0
    status: generated
  - name: user-stories.md
    version: v1.0.0
    status: generated
decision: APPROVED_FOR_HANDOFF
confidence: 0.95
justification: "42 requirements extracted and validated. All acceptance criteria defined."
```

---

## Step 4: Collect Metrics at Completion

When your agent completes execution, collect metrics:

### Metrics to Collect

```
1. Total execution time (measured in milliseconds)
2. Artifacts produced (count)
3. Validation score (0.0-1.0, based on validation rules)
4. Warning count (actual count)
5. Error count (actual count)
6. Open question count (questions requiring clarification)
7. Confidence score (0.0-1.0, your confidence in outputs)
8. Completion percentage (0.0-1.0, % of planned work done)
```

### Pattern: Metrics Collection

```
METRICS_START = agent_startup
METRICS_END = agent_completion
EXECUTION_TIME = (METRICS_END - METRICS_START)

VALIDATION_SCORE = (rules_passed / rules_checked)
CONFIDENCE_SCORE = (assessment_of_confidence)
COMPLETION = (planned_work_completed / total_planned_work)

EMIT METRICS with all collected values
```

### Example: Agent Completion Metrics

```yaml
# Metrics Record - Agent Completion
timestamp: 2026-07-01T14:22:45.300Z
agent: business_analyst
execution_time: 2500
artifact_count:
  generated: 5
  updated: 0
validation_score: 0.94
warning_count: 2
error_count: 0
open_question_count: 0
confidence_score: 0.95
completion_percentage: 1.0
memory_usage: 128.5
token_usage: 14200
performance_trend: "Faster than previous run by 15%"
quality_trend: "Improved validation score by 0.03"
metadata:
  artifacts_generated:
    - requirements-spec.md
    - user-stories.md
    - acceptance-criteria.md
    - non-functional-requirements.md
    - traceability.md
  validation_rules_checked: 23
  validation_rules_passed: 22
  warnings:
    - "Incomplete pricing requirements"
    - "Missing scalability metrics"
```

---

## Step 5: Handle Errors and Failures

When an error occurs:

```
1. Log the error immediately (status: failed)
2. Include error message and context
3. Create audit record for the failed decision (optional)
4. Collect partial metrics
5. Emit metrics for failed execution
6. STOP execution or continue based on recovery logic
```

### Example: Error Handling with Logging

```yaml
# Log Entry - Error Occurred
timestamp: 2026-07-01T14:25:10.450Z
agent: backend_developer
action: validate_api_spec
status: failed
artifact: api-spec.md
duration: 1200
message: "API validation failed: 3 errors, 2 warnings"
error: "Missing authentication handler in 5 endpoints"
metadata:
  error_count: 3
  warning_count: 2
  affected_endpoints: 5
  retry_attempt: 1

# Audit Record - Validation Failed (if decision-level)
audit_id: audit-20260701-005
timestamp: 2026-07-01T14:25:10.450Z
agent: backend_developer
action: quality_gate_failed
reason: "API validation failed. Missing required security handlers."
decision: FAILED
confidence: 0.0
error: "3 critical validation errors"
approval_blocker: true
```

---

## Step 6: Agent Completion

When your agent finishes (success or failure):

```
1. Emit final log entry (status: completed or failed)
2. Collect final metrics
3. Emit metrics record
4. Publish handoff contract
5. Signal completion to Supervisor
```

### Example: Agent Completion

```yaml
# Log Entry - Agent Completion
timestamp: 2026-07-01T14:22:50.000Z
agent: business_analyst
action: agent_completion
status: completed
artifact: n/a
duration: 45000
message: "Business Analyst execution complete. 5 artifacts generated."
metadata:
  total_artifacts: 5
  validation_score: 0.94
  errors: 0
  warnings: 2

# Metrics Record - Final
timestamp: 2026-07-01T14:22:50.000Z
agent: business_analyst
execution_time: 45000
artifact_count: {generated: 5, updated: 0}
validation_score: 0.94
warning_count: 2
error_count: 0
open_question_count: 0
confidence_score: 0.95
completion_percentage: 1.0
```

---

## Implementation Checklist

### For Every Agent

- [ ] Read `ai/instructions/logging.md`
- [ ] Read `ai/instructions/audit.md`
- [ ] Read `ai/instructions/observability.md`
- [ ] Review `ai/templates/log-entry.md`
- [ ] Review `ai/templates/audit-entry.md`
- [ ] Review `ai/templates/metrics.md`
- [ ] Emit log entry on agent startup
- [ ] Emit log entries for major actions
- [ ] Create audit records for decisions
- [ ] Collect metrics during execution
- [ ] Emit metrics record on completion
- [ ] Include all required fields in records
- [ ] Use consistent action names (snake_case)
- [ ] Use accurate timestamps (ISO 8601)
- [ ] Use measured durations (not estimates)
- [ ] Do NOT create custom logging logic

---

## Common Patterns

### Pattern 1: Successful Artifact Generation

```
1. Log: action_start (status: started)
2. [work]
3. Log: artifact_generated (status: completed, artifact name)
4. Audit: artifact_generated (decision, confidence, justification)
5. Continue to next action
```

### Pattern 2: Validation Gate

```
1. Log: validation_start (status: started)
2. [run validation]
3. Log: validation_result (status: completed)
4. IF validation_passed:
     Audit: quality_gate_passed
     Continue
5. ELSE:
     Audit: quality_gate_failed
     Log: error details
     Signal blocker to Supervisor
```

### Pattern 3: Approval Required

```
1. Audit: approval_requested (decision: AWAITING_APPROVAL)
2. Emit approval request to Supervisor
3. Wait for approval decision from Supervisor
4. Audit: approval_decision (decision: APPROVED or REJECTED)
5. If approved: continue
6. If rejected: signal blocker, halt execution
```

---

## Record Field Reference

### Log Entry Fields

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| timestamp | ✓ | ISO 8601 | 2026-07-01T14:22:33.125Z |
| agent | ✓ | snake_case | business_analyst |
| action | ✓ | snake_case | analyze_requirements |
| status | ✓ | started/in_progress/completed/failed/skipped | completed |
| artifact | ✓ | filename or n/a | requirements-spec.md |
| duration | ✓ | milliseconds | 2500 |
| message | ✓ | string, <100 chars | Completed analysis |
| error | optional | string | Validation failed |
| metadata | optional | YAML/JSON | {key: value} |
| version | optional | v1.0.0 | requirements-spec.md:v1.0.0 |

### Audit Record Fields

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| audit_id | ✓ | audit-YYYYMMDD-### | audit-20260701-001 |
| timestamp | ✓ | ISO 8601 | 2026-07-01T14:22:33.125Z |
| agent | ✓ | snake_case | business_analyst |
| action | ✓ | snake_case | artifact_generated |
| reason | ✓ | string, <200 chars | Requirements complete |
| input_artifacts | ✓ | array with name/version | [...] |
| output_artifacts | ✓ | array with name/version | [...] |
| decision | ✓ | APPROVED/REJECTED/AWAITING_APPROVAL | APPROVED |
| confidence | ✓ | 0.0-1.0 | 0.95 |
| justification | optional | Markdown | [...] |
| metadata | optional | YAML/JSON | {key: value} |

### Metrics Fields

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| timestamp | ✓ | ISO 8601 | 2026-07-01T14:22:45.300Z |
| agent | ✓ | snake_case | business_analyst |
| execution_time | ✓ | milliseconds | 2500 |
| artifact_count | ✓ | {generated, updated} | {generated: 5, updated: 0} |
| validation_score | ✓ | 0.0-1.0 | 0.94 |
| warning_count | ✓ | number | 2 |
| error_count | ✓ | number | 0 |
| open_question_count | ✓ | number | 0 |
| confidence_score | ✓ | 0.0-1.0 | 0.95 |
| completion_percentage | ✓ | 0.0-1.0 | 1.0 |
| memory_usage | optional | MB | 128.5 |
| token_usage | optional | count | 14200 |
| bottleneck | optional | string | API design (1200ms) |
| metadata | optional | YAML/JSON | {...} |

---

## Anti-Patterns: DO NOT

❌ **Do NOT:**
- Embed logging code in prompts
- Create separate log files per action
- Use non-standard timestamp formats
- Hardcode duration values
- Create duplicate log entries
- Use inconsistent action names
- Include PII in logs
- Create custom log storage
- Skip metrics collection
- Estimate rather than measure
- Create logs for every line of code
- Mix log levels inconsistently

✅ **DO:**
- Follow instruction templates
- Use consistent action naming
- Measure actual durations
- Include all required fields
- Reference artifacts by name
- Use structured format (YAML/JSON)
- Clean up temporary data before completion
- Delegate log aggregation to Supervisor

---

## Supervisor Collection Process

### What the Supervisor Does

The Supervisor automatically:

1. **Collects** all log entries from agents
2. **Collects** all audit records from agents
3. **Collects** all metrics from agents
4. **Aggregates** into unified files:
   - `execution-log.md` — All logs chronologically
   - `audit-trail.md` — All decisions with traceability
   - `metrics-summary.md` — Performance and quality dashboard
5. **Provides** workflow visibility without custom agent logic

### Agents Do NOT Need To:

- ❌ Implement custom log collection
- ❌ Implement custom audit storage
- ❌ Calculate aggregate metrics
- ❌ Create custom aggregation logic
- ❌ Manage log files or databases
- ❌ Implement performance dashboards

---

## Testing Your Implementation

### Verify Log Entries

```
Checklist:
- [ ] Timestamp is ISO 8601 format
- [ ] Agent name matches your agent_id
- [ ] Action is snake_case
- [ ] Status is one of: started/in_progress/completed/failed/skipped
- [ ] Duration is in milliseconds
- [ ] Artifact name matches actual file or is n/a
- [ ] Message is under 100 characters
- [ ] No PII in any field
- [ ] Metadata is valid YAML/JSON
```

### Verify Audit Records

```
Checklist:
- [ ] Audit ID is unique
- [ ] Timestamp is ISO 8601 format
- [ ] Agent matches your agent_id
- [ ] Action is documented in instruction
- [ ] Reason explains the decision
- [ ] Input artifacts have versions
- [ ] Output artifacts have versions
- [ ] Decision is standard keyword
- [ ] Confidence is between 0.0 and 1.0
- [ ] Justification explains reasoning
```

### Verify Metrics

```
Checklist:
- [ ] Execution time is measured (not estimated)
- [ ] Artifact counts are actual
- [ ] Validation score is calculated
- [ ] Confidence score is realistic
- [ ] Completion percentage is accurate
- [ ] Warning/error counts are actual
- [ ] All required fields present
- [ ] Metadata is valid YAML/JSON
- [ ] No duplicate metrics records
```

---

## Example: Complete Agent Execution Flow

### Business Analyst Full Execution

```
┌─ STARTUP ────────────────────────────────────
│ LOG: agent_startup, status=started
│ TIMESTAMP: 2026-07-01T14:20:05.000Z
│
├─ PHASE 1: ANALYZE REQUIREMENTS ──────────────
│ LOG: analyze_requirements, status=started
│ [work for 3.1 seconds]
│ LOG: analyze_requirements, status=completed, duration=3100ms
│ AUDIT: artifact_generated (requirements-spec.md)
│
├─ PHASE 2: CREATE USER STORIES ───────────────
│ LOG: create_stories, status=started
│ [work for 2.8 seconds]
│ LOG: create_stories, status=completed, duration=2800ms
│ AUDIT: artifact_generated (user-stories.md)
│
├─ PHASE 3: DEFINE ACCEPTANCE CRITERIA ────────
│ LOG: define_criteria, status=started
│ [work for 2.4 seconds]
│ LOG: define_criteria, status=completed, duration=2400ms
│ AUDIT: artifact_generated (acceptance-criteria.md)
│
├─ PHASE 4: VALIDATE OUTPUT ───────────────────
│ LOG: validate_output, status=started
│ [validation takes 1.2 seconds]
│ LOG: validate_output, status=completed, duration=1200ms
│ AUDIT: quality_gate_passed
│
├─ COMPLETION ──────────────────────────────────
│ LOG: agent_completion, status=completed, duration=45000ms
│ METRICS: execution_time=45000, validation_score=0.94, confidence=0.95
│ HANDOFF: Ready for Solution Architect
│
└─ SUPERVISOR AGGREGATES ───────────────────────
  ├─ execution-log.md (includes all logs)
  ├─ audit-trail.md (includes all audits)
  └─ metrics-summary.md (includes all metrics)
```

---

**Document Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Status:** Ready for Agent Implementation
