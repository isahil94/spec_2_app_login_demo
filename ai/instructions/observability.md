# Observability Instructions

**Version:** 1.0.0  
**Status:** Shared Platform Capability  
**Last Updated:** 2026-07-01

This document provides unified observability guidance for all agents in the Agentic SDLC platform.

**Purpose:** Enable Supervisor to understand workflow health, agent performance, and execution quality without requiring custom metrics implementations in every agent.

## Overview

Observability captures **metrics** and **health signals** for the entire workflow. These are aggregate measurements that summarize execution quality, progress, and performance.

- **Logs** = timeline of actions
- **Audit records** = decisions and changes
- **Metrics** = aggregate performance and quality measurements

The Supervisor aggregates all metrics to provide unified workflow observability dashboard.

## Metrics Structure

Use the template `ai/templates/metrics.md` for all metrics.

Every metrics record **must** contain:

### Required Fields
- **Timestamp**: ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sssZ)
- **Agent**: Name of the executing agent
- **Execution Time**: Total milliseconds elapsed for this agent's execution
- **Artifact Count**: Number of artifacts produced/updated
- **Validation Score**: Overall validation pass rate (0.0 to 1.0)
- **Warning Count**: Total warnings generated
- **Error Count**: Total errors encountered
- **Open Question Count**: Total blocking or clarification questions
- **Confidence Score**: Overall confidence in outputs (0.0 to 1.0)
- **Completion Percentage**: Percentage of planned work completed (0.0 to 1.0)

### Optional Fields
- **Memory Usage**: Peak memory consumed (in MB)
- **Token Usage**: LLM tokens consumed (for AI operations)
- **Retry Count**: Total retries needed
- **Cache Hit Rate**: Percentage of operations using cached results
- **Performance Trend**: Change vs. previous execution (faster/slower)
- **Quality Trend**: Change vs. previous execution (improved/degraded)
- **Bottleneck**: Identified performance bottleneck (if any)
- **Metadata**: Key-value pairs for contextual information

## Metric Categories

### 1. Execution Performance Metrics

Track **how fast** work was completed:

```
- Execution Time: [milliseconds]
- Steps Completed: [count]
- Average Time per Step: [milliseconds]
- Slowest Step: [step name, milliseconds]
- Memory Peak: [MB]
- Token Usage: [count, for LLM operations]
```

### 2. Output Quality Metrics

Track **quality of artifacts produced**:

```
- Artifacts Generated: [count]
- Artifacts Updated: [count]
- Validation Score: [0.0-1.0]
- Quality Score: [0.0-1.0]
- Completeness: [0.0-1.0]
- Confidence Score: [0.0-1.0]
```

### 3. Issue Metrics

Track **problems encountered**:

```
- Error Count: [count]
- Warning Count: [count]
- Open Question Count: [count]
- Blocker Count: [count]
- Resolution Rate: [0.0-1.0, % of issues resolved]
```

### 4. Progress Metrics

Track **workflow advancement**:

```
- Completion Percentage: [0.0-1.0]
- Planned Work: [count]
- Work Completed: [count]
- Approval Status: pending | approved | rejected | escalated
```

## Metric Examples

### Example 1: Successful Agent Execution

```
Metrics Record:
- Timestamp: 2026-07-01T14:22:45.300Z
- Agent: business_analyst
- Execution Time: 2500
- Artifact Count: 5
  - Generated: 5
  - Updated: 0
- Validation Score: 0.94
- Warning Count: 2
- Error Count: 0
- Open Question Count: 0
- Confidence Score: 0.95
- Completion Percentage: 1.0
- Memory Usage: 128.5
- Token Usage: 14200
- Performance Trend: "Faster than previous run by 15%"
- Quality Trend: "Improved validation score by 0.03"
- Metadata:
  - artifacts_generated: ["requirements_spec.md", "user_stories.md", "acceptance_criteria.md", "non_functional_requirements.md", "traceability.md"]
  - validation_rules_checked: 23
  - validation_rules_passed: 22
  - warnings: ["Incomplete pricing requirements", "Missing scalability metrics"]
```

### Example 2: Agent with Issues

```
Metrics Record:
- Timestamp: 2026-07-01T15:50:12.800Z
- Agent: backend_developer
- Execution Time: 5200
- Artifact Count: 3
  - Generated: 3
  - Updated: 0
- Validation Score: 0.76
- Warning Count: 7
- Error Count: 2
- Open Question Count: 3
- Confidence Score: 0.68
- Completion Percentage: 0.85
- Memory Usage: 256.0
- Token Usage: 32450
- Retry Count: 2
- Performance Trend: "Slower than previous run by 22%"
- Quality Trend: "Degraded validation score by 0.12"
- Bottleneck: "API endpoint design review (1200ms)"
- Metadata:
  - artifacts_generated: ["api-spec.md", "database-integration.md", "error-handling.md"]
  - errors: ["Missing authentication handler", "Incomplete error responses"]
  - warnings: [
      "Missing rate-limiting documentation",
      "Deprecated library dependency",
      "Async operation lacks timeout",
      "Missing input sanitization",
      "Database query not indexed",
      "Cache strategy undefined",
      "Missing API versioning plan"
    ]
  - open_questions: [
      "Should API use OAuth2 or API keys?",
      "Cache timeout settings?",
      "Maximum request payload size?"
    ]
  - requires_approval: true
  - approval_blocker: "Error count exceeds quality gate (2 > 0)"
```

### Example 3: Blocked Execution

```
Metrics Record:
- Timestamp: 2026-07-01T16:10:33.450Z
- Agent: solution_architect
- Execution Time: 1800
- Artifact Count: 1
  - Generated: 1
  - Updated: 0
- Validation Score: 0.0
- Warning Count: 0
- Error Count: 3
- Open Question Count: 5
- Confidence Score: 0.0
- Completion Percentage: 0.0
- Memory Usage: 64.2
- Token Usage: 8100
- Retry Count: 0
- Bottleneck: "Blocked on missing requirements"
- Metadata:
  - status: "BLOCKED"
  - blocker_reason: "Cannot proceed without requirements from Business Analyst"
  - required_inputs_missing: ["requirements_spec.md", "acceptance_criteria.md"]
  - open_questions: [
      "Should architecture support multi-tenancy?",
      "Real-time or eventual consistency?",
      "On-premise or cloud-only?",
      "Maximum concurrent users?",
      "API versioning strategy?"
    ]
  - approval_request: "apr-20260701-001"
  - approval_status: "pending"
```

## How Agents Produce Metrics

### At Agent Startup

1. Record start timestamp
2. Plan work steps
3. Note expected artifact count

### During Execution

1. Track actions and their timings
2. Count warnings and errors as they occur
3. Track open questions
4. Update token usage if using LLM

### At Agent Completion

1. Calculate total execution time
2. Count artifacts actually produced/updated
3. Run validation and record score
4. Assess confidence in work
5. Calculate completion percentage
6. Identify bottlenecks
7. Record final metrics

## Scoring Guidelines

### Validation Score
- **0.90-1.0**: All validation rules passed
- **0.70-0.89**: Minor issues, acceptable with warnings
- **0.50-0.69**: Significant issues, requires attention
- **0.00-0.49**: Critical issues, blocked

### Quality Score
- **0.90-1.0**: Production ready
- **0.70-0.89**: Good quality, ready with review
- **0.50-0.69**: Acceptable, needs improvement
- **0.00-0.49**: Poor quality, rework needed

### Confidence Score
- **0.90-1.0**: High confidence in outputs
- **0.70-0.89**: Confident, minor concerns
- **0.50-0.69**: Moderate confidence, uncertainty exists
- **0.00-0.49**: Low confidence, work requires review

### Completion Percentage
- **1.0**: All planned work completed
- **0.8-0.99**: Most work complete, minor gaps
- **0.5-0.79**: Significant portion complete
- **0.00-0.49**: Early stage, significant work remaining

## Implementation Rules

1. **Accurate timing**: Measure wall-clock time, not estimated time.
2. **Real counts**: Count actual warnings/errors, not potential ones.
3. **Conservative scoring**: Use lower confidence scores when uncertain.
4. **Trend analysis**: Compare to previous execution if data available.
5. **Identify bottlenecks**: Note what took most time or caused issues.
6. **No fabrication**: Never invent metrics. Use actual measurements.

## Metrics Anti-Patterns

❌ **Do NOT:**
- Estimate metrics instead of measuring
- Include non-numeric data in numeric fields
- Use inconsistent naming for same metrics
- Create metrics for every debug step
- Fabricate confidence scores
- Report metrics before execution completes
- Create metrics for failures without context

## Reference Template

Use `ai/templates/metrics.md` for the complete template structure.

## Supervisor Responsibilities

The Supervisor:
- Collects metrics from all agents
- Creates unified metrics dashboard showing:
  - Timeline of execution
  - Performance trends
  - Quality trends
  - Bottleneck analysis
  - Error/warning summary
  - Approval gate status
- Calculates aggregate workflow metrics
- Alerts on anomalies or degradation
- Provides metrics for performance tuning

**Agents do not need to implement custom metrics collection or analysis.**

## Workflow Observability

Combined metrics, logs, and audit records provide complete workflow visibility:

```
Timeline View:
- [14:22] Business Analyst: 2.5s, 5 artifacts, 0.94 validation, 0 errors
- [15:50] Solution Architect: 3.2s, 4 artifacts, 0.88 validation, 0 errors
- [16:15] UI/UX Developer: 2.8s, 6 artifacts, 0.91 validation, 1 warning
- [16:40] Backend Developer: 5.2s, 3 artifacts, 0.76 validation, 2 errors [BLOCKED]
- [approval pending]

Dashboard:
- Total Execution Time: 14.7s
- Total Artifacts: 18
- Average Validation: 0.87
- Total Errors: 2
- Total Warnings: 8
- Workflow Status: BLOCKED on Backend Developer approval gate
```
