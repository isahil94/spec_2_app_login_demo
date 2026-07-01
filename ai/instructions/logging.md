# Logging Instructions

**Version:** 1.0.0  
**Status:** Shared Platform Capability  
**Last Updated:** 2026-07-01

This document provides unified logging guidance for all agents in the Agentic SDLC platform.

**Purpose:** Ensure consistent, structured logging across all agents without duplicating logic in every agent.

## Overview

Logging captures real-time events and actions during agent execution. Every log entry represents a discrete, timestamped action that contributes to workflow observability and debugging.

The Supervisor aggregates all log entries to provide unified workflow visibility.

## Log Entry Structure

Use the template `ai/templates/log-entry.md` for all logging.

Every log entry **must** contain:

### Required Fields
- **Timestamp**: ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sssZ)
- **Agent**: Name of the executing agent (e.g., "business_analyst", "backend_developer")
- **Action**: Type of action performed (e.g., "analyze_requirements", "generate_artifact", "validate_output")
- **Status**: One of: `started`, `in_progress`, `completed`, `failed`, `skipped`
- **Artifact**: Name of artifact being processed (if applicable)
- **Duration**: Milliseconds elapsed for this action
- **Message**: Human-readable description of what happened

### Optional Fields
- **Error**: Error message or stack trace (if status = failed)
- **Warning**: Warning message (if validation warning occurred)
- **Metadata**: Key-value pairs for contextual information
- **Retry**: Current retry attempt number (if applicable)
- **Version**: Version of artifact being processed

## Log Levels

Every log entry specifies **Status** which categorizes the log level:

| Status | Usage | Example |
|--------|-------|---------|
| `started` | Action beginning | "Started analyzing requirements" |
| `in_progress` | Action ongoing (optional) | "Processing user stories (50% complete)" |
| `completed` | Action succeeded | "Generated acceptance criteria: 24 items" |
| `failed` | Action failed | "Validation failed: 3 required fields missing" |
| `skipped` | Action skipped due to conditions | "Skipped UI observations (no Figma URL)" |

## When to Log

Every agent **must** log:

1. **Lifecycle events**: started, completed, failed
2. **Artifact generation**: Each artifact created
3. **Artifact updates**: Each artifact modified
4. **Validation events**: Validation pass/fail
5. **Quality metrics**: Quality scores, warning counts
6. **Approval events**: Approval requested, decision made
7. **Errors**: Any error or exception
8. **Skipped steps**: Conditional steps that were skipped

## Logging Patterns

### Pattern 1: Action Lifecycle

```
Log Entry:
- Timestamp: [ISO 8601]
- Agent: business_analyst
- Action: analyze_requirements
- Status: started
- Artifact: n/a
- Duration: 0
- Message: "Beginning requirements analysis"

[... work happens ...]

Log Entry:
- Timestamp: [ISO 8601]
- Agent: business_analyst
- Action: analyze_requirements
- Status: completed
- Artifact: requirements_spec.md
- Duration: 2500
- Message: "Completed requirements analysis in 2.5 seconds"
```

### Pattern 2: Artifact Generation

```
Log Entry:
- Timestamp: [ISO 8601]
- Agent: solution_architect
- Action: generate_artifact
- Status: completed
- Artifact: architecture-design.md
- Duration: 3200
- Message: "Generated architecture design (8.5 KB, 127 lines)"
- Metadata:
  - lines: 127
  - size_kb: 8.5
  - quality_score: 0.92
```

### Pattern 3: Validation Event

```
Log Entry:
- Timestamp: [ISO 8601]
- Agent: backend_developer
- Action: validate_artifact
- Status: completed
- Artifact: api-spec.md
- Duration: 850
- Message: "Validation passed: API spec conforms to contract"
- Metadata:
  - endpoints_count: 24
  - validation_score: 0.98
  - warnings_count: 2
  - warning_list: ["Endpoint lacking deprecation notice", "Missing rate-limit documentation"]
```

### Pattern 4: Error Handling

```
Log Entry:
- Timestamp: [ISO 8601]
- Agent: database_developer
- Action: validate_schema
- Status: failed
- Artifact: database-schema.md
- Duration: 1200
- Message: "Schema validation failed: 3 errors, 2 warnings"
- Error: "Missing foreign key constraint on projects.owner_id"
- Metadata:
  - error_count: 3
  - warning_count: 2
  - retry_attempt: 1
```

## Log Aggregation by Supervisor

The Supervisor collects all log entries into a unified `execution-log.md` that includes:

- Complete timeline of all agent actions
- Filtered by severity/status
- Sortable by agent, artifact, action
- Provides insight into execution flow, performance, and issues

## Implementation Rules

1. **Immutable**: Log entries are append-only. Never modify or delete prior entries.
2. **Timestamp accuracy**: Use system clock with millisecond precision.
3. **No PII**: Do not log sensitive information (API keys, passwords, user data).
4. **Structured format**: Always use the template structure. Do not embed logs in prose.
5. **Consistent naming**: Use consistent action names across runs (use snake_case).
6. **Timing accuracy**: Always measure and report duration in milliseconds.
7. **Batch logging**: Create one log entry per discrete action, not per line of work.

## Logging Anti-Patterns

❌ **Do NOT:**
- Log verbose debug information inside prompts
- Create logs for trivial operations (reading a config file)
- Include unstructured prose in the Message field
- Log sensitive data
- Create duplicate entries for the same action
- Use inconsistent status values (e.g., "success" vs "completed")

## Reference Template

Use `ai/templates/log-entry.md` for the complete template structure.

## Supervisor Responsibilities

The Supervisor:
- Collects logs from all agents in execution order
- Creates unified `execution-log.md` with timeline
- Calculates aggregate metrics (total duration, error count, etc.)
- Flags performance anomalies
- Retains logs for audit trail

**Agents do not need to implement custom log collection or aggregation.**
