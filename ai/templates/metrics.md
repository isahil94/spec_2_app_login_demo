# Metrics Template

**Template Version:** 1.0.0  
**Status:** Standard Template  
**Last Updated:** 2026-07-01

Use this template for agent metrics. Metrics summarize execution quality and performance.

---

## Metrics Record

### Required Fields

**Timestamp**
```
2026-07-01T14:22:45.300Z
```
ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sssZ). Time when metrics are finalized.

**Agent**
```
business_analyst
```
Agent name that produced these metrics.

**Execution Time**
```
2500
```
Total milliseconds elapsed for this agent's execution. Measured, not estimated.

**Artifact Count**
```
generated: 5
updated: 0
```
Number of artifacts produced and updated.

**Validation Score**
```
0.94
```
Overall validation pass rate. Range: 0.0 to 1.0.
- 0.90-1.0: All rules passed
- 0.70-0.89: Minor issues
- 0.50-0.69: Significant issues
- 0.00-0.49: Critical issues

**Warning Count**
```
2
```
Total warnings generated during execution.

**Error Count**
```
0
```
Total errors encountered during execution.

**Open Question Count**
```
0
```
Total blocking or clarification questions requiring response.

**Confidence Score**
```
0.95
```
Overall confidence in outputs. Range: 0.0 to 1.0.
- 0.90-1.0: High confidence
- 0.70-0.89: Confident, minor concerns
- 0.50-0.69: Moderate confidence
- 0.00-0.49: Low confidence

**Completion Percentage**
```
1.0
```
Percentage of planned work completed. Range: 0.0 to 1.0.
- 1.0: All planned work complete
- 0.8-0.99: Most work complete
- 0.5-0.79: Significant portion complete
- 0.0-0.49: Early stage

---

### Optional Fields

**Memory Usage**
```
128.5
```
Peak memory consumed in MB. Only if measurable.

**Token Usage**
```
14200
```
LLM tokens consumed. Only for LLM-based operations.

**Retry Count**
```
1
```
Number of retries needed. Only if retries occurred.

**Cache Hit Rate**
```
0.65
```
Percentage of operations using cached results. Range: 0.0 to 1.0.

**Performance Trend**
```
Faster than previous run by 15%
```
Comparison to previous execution. Examples:
- Faster than previous run by 15%
- Slower than previous run by 8%
- Baseline (first execution)
- Comparable to previous run

**Quality Trend**
```
Improved validation score by 0.03
```
Comparison to previous quality metrics. Examples:
- Improved validation score by 0.03
- Degraded validation score by 0.08
- Warnings increased from 2 to 7
- Error count reduced from 5 to 2

**Bottleneck**
```
API endpoint design review (1200ms)
```
Most time-consuming or problematic step. Format: "step-name (duration-ms)".

**Metadata**
```yaml
artifacts_generated:
  - requirements-spec.md
  - user-stories.md
  - acceptance-criteria.md
  - non-functional-requirements.md
  - traceability.md
validation_rules_checked: 23
validation_rules_passed: 22
warnings:
  - Incomplete pricing requirements
  - Missing scalability metrics
```
Additional key-value context. Use YAML or JSON.

---

## Complete Example

```
---
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
    - Incomplete pricing requirements
    - Missing scalability metrics
---
```

## Scoring Guidelines

### Validation Score

How many validation rules passed:

```
Validation Rules Checked: 23
Validation Rules Passed: 22
Validation Score = 22 / 23 = 0.956 ≈ 0.94 (rounded down)
```

Scoring:
- **0.95-1.0**: All or nearly all rules passed (excellent)
- **0.80-0.94**: Most rules passed (good)
- **0.60-0.79**: Significant portion passed (acceptable, needs attention)
- **0.40-0.59**: Only half passed (poor, rework needed)
- **0.00-0.39**: Very few passed (critical issues)

### Confidence Score

How confident are you in the work produced:

```
Factors:
- Validation Score: 0.94
- Completeness: 100%
- Known Issues: 2 warnings
- Uncertainties: 0 open questions
- Test Coverage: 94%

Overall Confidence = 0.95
(High validation score, complete work, low uncertainties)
```

Scoring:
- **0.90-1.0**: High confidence, production ready
- **0.75-0.89**: Confident, minor concerns or review recommended
- **0.60-0.74**: Moderate confidence, significant review needed
- **0.45-0.59**: Low confidence, substantial rework likely
- **0.00-0.44**: Very low confidence, fundamentally uncertain

### Quality Score (if used separately)

Overall quality of work:

```
Factors:
- Completeness: 100%
- Accuracy: 95%
- Documentation: Good
- Best practices: Followed
- Known issues: 2 warnings

Overall Quality = 0.88
(Good quality, minor documentation gaps)
```

### Completion Percentage

Percentage of planned work that was actually completed:

```
Planned Work Steps: 5
  1. Analyze requirements ✓
  2. Create user stories ✓
  3. Define acceptance criteria ✓
  4. Identify non-functional requirements ✓
  5. Create traceability matrix ✓

Completion = 5/5 = 1.0 (100%)
```

---

## Metric Examples by Scenario

### Scenario 1: Successful Execution

```yaml
execution_time: 2500
artifact_count: {generated: 5, updated: 0}
validation_score: 0.94
warning_count: 2
error_count: 0
open_question_count: 0
confidence_score: 0.95
completion_percentage: 1.0
bottleneck: null
approval_status: approved
```

### Scenario 2: Execution with Warnings

```yaml
execution_time: 4200
artifact_count: {generated: 4, updated: 1}
validation_score: 0.78
warning_count: 7
error_count: 1
open_question_count: 2
confidence_score: 0.72
completion_percentage: 0.95
bottleneck: "Database schema design review (1800ms)"
approval_status: pending
```

### Scenario 3: Blocked Execution

```yaml
execution_time: 1200
artifact_count: {generated: 0, updated: 0}
validation_score: 0.0
warning_count: 0
error_count: 3
open_question_count: 5
confidence_score: 0.0
completion_percentage: 0.0
bottleneck: "Blocked on missing requirements"
approval_status: blocked
```

---

## Collection Pattern for Agents

Agents should collect metrics at these points:

```
Agent Start
  ├─ Record start timestamp
  ├─ Note planned steps
  └─ Note expected artifact count

During Execution
  ├─ Track action timings
  ├─ Count warnings/errors
  ├─ Count open questions
  └─ Monitor memory/tokens

Agent Completion
  ├─ Calculate total execution time
  ├─ Count artifacts produced
  ├─ Run validation → score
  ├─ Assess confidence
  ├─ Calculate completion %
  ├─ Identify bottleneck
  └─ Finalize metrics
```

## Supervisor Aggregation

The Supervisor collects all metrics into `metrics-summary.md`:

```markdown
# Execution Metrics

**Workflow:** [workflow-id]  
**Start Time:** [ISO 8601]  
**End Time:** [ISO 8601]  

## Agent Performance

| Agent | Time (ms) | Artifacts | Validation | Errors | Confidence | Status |
|-------|-----------|-----------|-----------|--------|-----------|--------|
| business_analyst | 2500 | 5 | 0.94 | 0 | 0.95 | ✓ |
| solution_architect | 3200 | 4 | 0.88 | 0 | 0.92 | ✓ |
| backend_developer | 5200 | 3 | 0.76 | 2 | 0.68 | ⚠ |

## Workflow Summary

- Total Execution Time: [sum]
- Total Artifacts: [count]
- Average Validation: [mean]
- Total Errors: [count]
- Total Warnings: [count]
- Workflow Status: [status]

## Performance Trends

[comparison to baseline or previous runs]
```
