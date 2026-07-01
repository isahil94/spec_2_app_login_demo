# Open Log

Template Version: 4.0.0
Owner Agent: [Agent Name]
Workflow ID: [Workflow ID]
Correlation ID: [Correlation ID]
Generated: [ISO-8601]
Last Updated: [ISO-8601]

## Workflow Status
| Field | Value |
|---|---|
| Workflow ID | [WF-YYYYMMDD-NNNN] |
| Current Stage | [agent_stage] |
| Current State | READY | BLOCKED | WAITING_FOR_APPROVAL | FAILED |
| Execution Mode | FULL_AUTO |
| Open Items | [count] |
| Blocking Items | [count] |
| Pending HITL | [count] |
| Next Agent | [agent_id or none] |
| Supervisor Action | Continue | Pause | Request Approval | Escalate |

## Initialization Summary
| Field | Value |
|---|---|
| Initializer Script Present | Yes | No |
| Sample Migration Present | Yes | No |
| Persistent DB Initialized | Yes | No |

## Execution Steps
| Step | Performed | Result |
|---|---:|---|
| Validation Run (no-persist) | Yes | Pass | Fail |
| Initialization Run | Yes | Success | Fail |
| Start/Verification Run | Yes | Success | Fail |

## Constraints & Guardrails
- Constraints Validation: Performed | Not Performed
- Constraints Details: (list of enforced constraints / missing constraints)
- Guardrails Validation: Performed | Not Performed
- Guardrails Details: (list of guardrail checks and outcomes)

## Open Question Lifecycle
NEW -> UNDER_REVIEW -> WAITING_FOR_APPROVAL -> APPROVED/REJECTED -> RESOLVED -> CLOSED

## Open Items

### OQ-001
| Field | Value |
|---|---|
| Entry ID | OQ-001 |
| Workflow ID | [WF-YYYYMMDD-NNNN] |
| Correlation ID | [CORR-XXXXXXXX] |
| Date | [ISO-8601] |
| Category | Open Question | Assumption | Risk | Decision | Escalation | Governance Violation |
| Title | [1 line] |
| Question | [1-3 lines] |
| Reason | [1-3 lines] |
| Priority | Critical | High | Medium | Low |
| Impact | High | Medium | Low |
| Blocking | Yes | No |
| Approval Required | Yes | No |
| Default Assumption | [1 line] |
| Owner Agent | [agent_id] |
| Target Stage | [target stage] |
| Related Artifact(s) | [artifact refs or N/A] |
| Related Requirement(s) | [FR refs or N/A] |
| Related User Story(ies) | [US refs or N/A] |
| Potential Risk | [1-3 lines] |
| Status | NEW | UNDER_REVIEW | WAITING_FOR_APPROVAL | APPROVED | REJECTED | RESOLVED | CLOSED |
| Resolution | [1-3 lines or Pending] |
| Decision | [1-3 lines or Pending] |
| Decision By | [owner or Pending] |
| Decision Date | [ISO-8601 or Pending] |

#### History
- [ISO-8601] Created. Status: NEW.

## Append Rules
- Compact the content, never compact the schema.
- Keep field values concise (1-3 lines where appropriate).
- Append-only: never delete existing entries.
- Record every status transition in History.
- Use this as the only governance open-items artifact.
- For backend stage, any required manual user step must be logged as a Governance Violation entry.
