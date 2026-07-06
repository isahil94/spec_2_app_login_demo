# Handoff Contract

## Workflow Context
- Workflow ID: WF-1783344648928
- Correlation ID: WF-1783344648928
- Agent: qa-engineer
- Stage: QA
- Figma Reference (if present): Not applicable
- Design Intake Artifact: Not applicable

## Artifacts Produced
| Artifact | Status |
|---|---|
| coverage-matrix.md | Updated |
| gap-analysis.md | Updated |
| qa-blockers.md | Updated |
| test-execution-log.md | Updated |
| quality-report.md | Updated |
| handoff-contract.md | Updated |
| ui-live-test-report.md | Created |

## Artifact Status
- Created: ui-live-test-report.md
- Updated: coverage-matrix.md, gap-analysis.md, qa-blockers.md, test-execution-log.md, quality-report.md, handoff-contract.md
- Skipped: None
- Artifact Versions: v1.1

## OpenLog Summary
- Open Items: 2
- Blocking Items: 2
- Approval Required: Yes

## AI Usage Summary
| Field | Value |
|---|---|
| Workflow ID | WF-1783344648928 |
| Correlation ID | WF-1783344648928 |
| Agent Name | qa-engineer |
| Stage Name | QA |
| Model Name | MAI-Code-1-Flash |
| Model Provider | copilot |
| Session ID | N/A |
| Start Time | 2026-07-06 |
| End Time | 2026-07-06 |
| Duration | Short |
| Input Tokens | N/A |
| Output Tokens | N/A |
| Total Tokens | N/A |
| Estimated Cost | N/A |
| Retry Count | 0 |
| Status | Completed with blockers |
| Blocking Reason | Two live UI scenarios failed during end-to-end verification |

## Workflow Status
- Status: BLOCKED
- Reason: Two end-to-end UI scenarios failed during live verification, so the release confidence is reduced.
- Ready for Next Stage: No

## Next Agents
- Primary: frontend
- Sequential order: frontend → backend
