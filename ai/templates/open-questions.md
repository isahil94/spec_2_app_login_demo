# Open Questions

## Purpose
Track unresolved decisions using a deterministic schema that supports Supervisor-only orchestration and HITL approval routing.

## Metadata
- Version: [Version]
- Author: [Author]
- Date: [Date]
- Workflow ID: [Workflow ID]
- Artifact ID: [Artifact ID]
- Owner Agent: [Agent Name]

## Structured Questions

### OQ-001

Category:
Business | Functional | UX | Security | Performance | Compliance | Data | Integration | Architecture | Testing | Documentation | Deployment

Question:
[Describe the unresolved question]

Reason:
[Why this question is raised]

Impact:
High | Medium | Low

Default Assumption:
[Assumption used to continue work, or None]

Blocking:
Yes | No

Approval Required:
Yes | No

Target Stage:
Business Analysis | Solution Architecture | UI/UX | Backend | Database | QA | Documentation | DevOps

Confidence:
[0-100%]

Owner:
[Name of the agent generating the question]

Related Requirement(s):
[Requirement IDs or None]

Potential Risk:
[Risk if the assumption is incorrect]

## Open Question Summary
- Total Questions: [Number]
- Blocking Questions: [Number]
- Approval Requests Required: [Number]
- Workflow Status: [REQUIRES HUMAN APPROVAL | READY]
- Next Agent: [Agent Name | Approval Path]

## Rules
1. No required field may be empty.
2. If no reasonable assumption exists, set Default Assumption: None.
3. If work cannot safely continue, set Blocking: Yes and Approval Required: Yes.
4. Otherwise set Blocking: No and Approval Required: No.
5. Compute Workflow Status from structured metadata only:
	- If any question has Blocking: Yes -> REQUIRES HUMAN APPROVAL
	- Else -> READY
