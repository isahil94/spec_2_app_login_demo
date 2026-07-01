# Log Entry Template

**Template Version:** 1.0.0  
**Status:** Standard Template  
**Last Updated:** 2026-07-01

Use this template for every log entry. Include all required fields. Optional fields can be omitted if not applicable.

---

## Log Entry

### Required Fields

**Timestamp**
```
2026-07-01T14:22:33.125Z
```
Format: ISO 8601 (YYYY-MM-DDTHH:MM:SS.sssZ)

**Agent**
```
business_analyst
```
Agent name in snake_case.

**Action**
```
analyze_requirements
```
Specific action performed (snake_case). Examples:
- analyze_requirements
- generate_artifact
- validate_artifact
- update_artifact
- request_approval
- process_approval
- execute_skill
- load_memory
- publish_artifact

**Status**
```
completed
```
One of: `started` | `in_progress` | `completed` | `failed` | `skipped`

**Artifact**
```
requirements-spec.md
```
Name of artifact being processed. Use "n/a" if not applicable.

**Duration**
```
2500
```
Milliseconds elapsed for this action. Use 0 for instantaneous actions.

**Message**
```
Completed requirements analysis. Generated 42 requirements with 18 user stories.
```
Human-readable description of what happened. Be specific and concise.

---

### Optional Fields

**Error** (if Status = failed)
```
Validation failed: Missing acceptance criteria for 3 requirements.
Schema validation error at line 42: Invalid field 'priority' value 'urgent'.
```
Error message or exception. Include relevant details for debugging.

**Warning** (if applicable)
```
Incomplete pricing requirements. Scalability metrics missing.
```
Warning message for validation warnings or quality concerns.

**Metadata**
```yaml
requirement_count: 42
user_story_count: 18
quality_score: 0.94
validation_score: 0.94
lines_generated: 287
size_kb: 12.5
```
Key-value pairs for contextual information. Use YAML format.

**Retry**
```
1
```
Current retry attempt number. Only include if retrying.

**Version**
```
requirements-spec.md:v1.0.0
```
Version of artifact being processed. Format: artifact-name:vX.Y.Z

---

## Complete Example

```
---
timestamp: 2026-07-01T14:22:33.125Z
agent: business_analyst
action: analyze_requirements
status: completed
artifact: requirements-spec.md
duration: 2500
message: "Completed requirements analysis. Generated 42 requirements with 18 user stories."
metadata:
  requirement_count: 42
  user_story_count: 18
  quality_score: 0.94
  validation_score: 0.94
  lines_generated: 287
  size_kb: 12.5
---
```

## Usage Notes

1. Create one log entry per discrete action
2. Always include timestamp with millisecond precision
3. Use consistent action names across executions
4. Keep Message field concise (one sentence)
5. Use YAML or JSON for metadata
6. Include Duration even if 0
7. Reference artifact name, not full path
8. Use actual measurements, never estimates

## Log Entry Lifecycle

```
Agent executes action
↓
Create log entry with 'started' status
↓
Action executes...
↓
Log entry updated with 'completed'/'failed' status and duration
↓
Log entry published to Supervisor
↓
Supervisor aggregates into execution-log.md
```

## Collection Pattern for Agents

Every agent should emit logs following this pattern:

```
1. Log agent startup (started, action=agent_startup)
2. Log each major phase (started, in_progress, completed)
3. Log artifact generation (completed, action=generate_artifact)
4. Log validation results (completed/failed, action=validate_artifact)
5. Log errors immediately (failed, action=..., error message)
6. Log agent completion (completed, action=agent_completion)
```

## Supervisor Aggregation

The Supervisor collects all logs into `execution-log.md` with structure:

```markdown
# Execution Log

**Workflow:** [workflow-id]  
**Start Time:** [ISO 8601]  
**End Time:** [ISO 8601]  
**Duration:** [total milliseconds]  
**Status:** COMPLETED | FAILED | BLOCKED

## Log Entries (Chronological)

[all log entries sorted by timestamp]

## Summary Statistics

- Total Entries: [count]
- Errors: [count]
- Warnings: [count]
- Average Duration per Entry: [ms]
- Longest Operation: [action, duration]
```
