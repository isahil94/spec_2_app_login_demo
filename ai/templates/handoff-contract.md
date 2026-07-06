# Handoff Contract

## Workflow Context
- Workflow ID:
- Correlation ID:
- Agent:
- Stage:
- Figma Reference (if present):
- Design Intake Artifact: [figma_design_intake.md | Not provided]

<!-- MANDATORY_COMMAND: On completion, implement the UI using the tech stack specified in upstream artifacts; generate a runnable frontend under `apps/frontend/`, run it locally, and open it in the default browser. This directive must be followed and must not be duplicated in this file. -->

## Artifacts Produced
| Artifact | Status |
|---|---|
| [artifact-name.md] | Created | Updated | Skipped |

## Artifact Status
- Created:
- Updated:
- Skipped:
- Artifact Versions:

## OpenLog Summary
- Open Items:
- Blocking Items:
- Approval Required: Yes | No

## AI Usage Summary
| Field | Value |
|---|---|
| Workflow ID | |
| Correlation ID | |
| Agent Name | |
| Stage Name | |
| Model Name | |
| Model Provider | |
| Session ID | |
| Start Time | |
| End Time | |
| Duration | |
| Input Tokens | |
| Output Tokens | |
| Total Tokens | |
| Estimated Cost | |
| Retry Count | |
| Status | |
| Blocking Reason | |

## Execution Automation Summary

## Initialization Summary

## Execution Steps (Mandatory)
- Validation Run (no-persist): Performed | Not Performed
- Initialization Run: Performed | Not Performed
- Start/Verification Run: Performed | Not Performed

## Constraints & Guardrails Checks
- Constraints Validation: Performed | Not Performed
- Constraints Results: (summary of enforced/ missing constraints)
- Guardrails Validation: Performed | Not Performed
- Guardrails Results: (summary of guardrail check outcomes)

## Initialization Summary
- Initializer Script Created: Yes | No
- Sample Migration Added: Yes | No
- Persistent DB Initialized: Yes | No

## Workflow Status
- Status: READY | BLOCKED | WAITING_FOR_APPROVAL | FAILED
- Reason:
- Ready for Next Stage: Yes | No | Conditional

## Next Agents
- Primary:
- Sequential order: frontend → backend → database (if applicable):

## Rules
- Compact the content, never compact the schema.
- Keep field values concise (1-3 lines where appropriate).
- AI Usage is metadata-only; do not add narrative explanations.
- In backend stage, FULL_AUTO is mandatory unless workflow status is BLOCKED/FAILED.
