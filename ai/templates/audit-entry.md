# Audit Entry Template

**Template Version:** 1.0.0  
**Status:** Standard Template  
**Last Updated:** 2026-07-01

Use this template for every audit record. Audit records capture decisions with complete traceability.

---

## Audit Record

### Required Fields

**Audit ID**
```
audit-20260701-001
```
Unique identifier. Format: `audit-YYYYMMDD-###` or UUID.

**Timestamp**
```
2026-07-01T14:22:33.125Z
```
ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sssZ). Use creation time.

**Agent**
```
business_analyst
```
Agent name making the decision.

**Action**
```
artifact_generated
```
Type of decision. Examples:
- artifact_generated
- artifact_updated
- requirement_rejected
- requirement_accepted
- approval_requested
- approval_decision
- quality_gate_passed
- quality_gate_failed
- escalation_issued
- traceability_mapped

**Reason**
```
Requirements analysis complete and validated. All acceptance criteria defined.
```
Brief explanation (1-2 sentences) of why this decision was made.

**Input Artifacts**
```yaml
- name: specification.md
  version: v1.0.0
  source_agent: user

- name: figma_url.txt
  version: v1.0.0
  source_agent: user
```
List of artifacts consumed to make this decision. Include version.

**Output Artifacts**
```yaml
- name: requirements-spec.md
  version: v1.0.0
  status: generated

- name: user-stories.md
  version: v1.0.0
  status: generated

- name: acceptance-criteria.md
  version: v1.0.0
  status: generated
```
List of artifacts produced by this decision. Include status: generated | updated | not-applicable.

**Decision**
```
APPROVED_FOR_HANDOFF
```
The actual decision made. Examples:
- APPROVED
- REJECTED
- APPROVED_WITH_CHANGES
- APPROVED_WITH_CAVEATS
- AWAITING_APPROVAL
- APPROVED_FOR_HANDOFF
- READY_FOR_RELEASE
- REQUIRES_REVISION

**Confidence**
```
0.95
```
Confidence in this decision. Range: 0.0 to 1.0.
- 0.9-1.0: High confidence
- 0.7-0.89: Confident, minor concerns
- 0.5-0.69: Moderate confidence
- 0.0-0.49: Low confidence

---

### Optional Fields

**Justification**
```
All requirements extracted from specification and validated against acceptance criteria template.
42 requirements identified, 18 user stories created, validation score 0.94.
No critical gaps identified. Ready for architecture phase.
```
Extended explanation of reasoning. Use Markdown. Can be multiple paragraphs.

**Approval Information**
```yaml
approval_request_id: apr-20260701-001
status: pending
required_reviewers:
  - solution-architect-lead
  - backend-tech-lead
approval_timestamp: 2026-07-01T16:30:00.000Z
approved_by:
  - reviewer1
  - reviewer2
decision_notes: "Architecture is scalable and aligns with requirements."
approval_deadline: 2026-07-02T00:00:00.000Z
```
For approval-related decisions. Include request ID, status, reviewer info.

**Version**
```
requirements-spec.md:v1.0.0
```
Version identifier for traceability. Format: artifact-name:vX.Y.Z or commit-hash.

**Alternative Options**
```yaml
- option: "Implement WebSocket for real-time sync"
  pros: "True real-time updates"
  cons: "6 weeks additional work, infrastructure cost"
  decision: "Rejected - exceeds MVP timeline"

- option: "Use polling with 5-second intervals"
  pros: "Shorter implementation, lower cost"
  cons: "Slight delay in updates"
  decision: "Accepted - compromise solution"
```
Other options considered and why they were rejected. Optional but recommended for complex decisions.

**Risk Assessment**
```
High complexity architecture may require additional documentation.
Database scaling approach may need validation under load.
Microservices communication overhead needs performance testing.
```
Any risks identified with this decision.

**Metadata**
```yaml
requirement_count: 42
story_count: 18
validation_rules_checked: 23
validation_rules_passed: 22
warnings: 2
completion_percentage: 1.0
```
Additional contextual key-value pairs.

**Previous Decision**
```
audit-20260628-015
```
Reference to prior audit record if this decision reverses or updates it.

---

## Complete Example

```
---
audit_id: audit-20260701-001
timestamp: 2026-07-01T14:22:33.125Z
agent: business_analyst
action: artifact_generated
reason: "Requirements analysis complete and validated. All acceptance criteria defined."
input_artifacts:
  - name: specification.md
    version: v1.0.0
    source_agent: user
  - name: figma_url.txt
    version: v1.0.0
    source_agent: user
output_artifacts:
  - name: requirements-spec.md
    version: v1.0.0
    status: generated
  - name: user-stories.md
    version: v1.0.0
    status: generated
  - name: acceptance-criteria.md
    version: v1.0.0
    status: generated
decision: APPROVED_FOR_HANDOFF
confidence: 0.95
justification: |
  All requirements extracted from specification and validated.
  42 requirements identified, 18 user stories created.
  Validation score: 0.94. No critical gaps. Ready for architecture phase.
metadata:
  requirement_count: 42
  story_count: 18
  validation_score: 0.94
  completion_percentage: 1.0
---
```

## Usage Notes

1. **One record per decision**, not per step
2. **Always version artifacts** for reproducibility
3. **Cite reasons** sufficient for external review
4. **Use consistent decision keywords** across agents
5. **Link to approval requests** when applicable
6. **Timestamps are immutable** - never adjust retroactively
7. **Include alternatives** for complex decisions
8. **Conservative confidence** - be honest about uncertainty

## Audit Record Lifecycle

```
Agent makes decision
↓
Create audit record with all required fields
↓
Include clear justification
↓
Link input/output artifacts
↓
Publish to Supervisor
↓
Supervisor retains indefinitely
↓
Audit record available for review/forensics
```

## Decision Mapping

Map decisions to audit actions:

| Decision Type | Action | Example |
|---------------|--------|---------|
| Creating artifact | artifact_generated | Requirements document created |
| Updating artifact | artifact_updated | Architecture document revised |
| Accepting requirement | requirement_accepted | User story approved |
| Rejecting requirement | requirement_rejected | Feature deemed unfeasible |
| Requesting review | approval_requested | Design sent for approval |
| Completing review | approval_decision | Design approved by lead |
| Passing QA | quality_gate_passed | Tests passed, ready to release |
| Failing QA | quality_gate_failed | Tests failed, requires fixes |
| Escalating issue | escalation_issued | Blocker escalated to lead |
| Mapping traceability | traceability_mapped | Requirement linked to design |

## Supervisor Aggregation

The Supervisor collects all audit records into `audit-trail.md` with structure:

```markdown
# Audit Trail

**Workflow:** [workflow-id]  
**Start Time:** [ISO 8601]  
**End Time:** [ISO 8601]  

## Audit Records (Chronological)

[all audit records sorted by timestamp]

## Summary

- Total Decisions: [count]
- By Agent: [breakdown]
- By Action: [breakdown]
- Approval Gates Passed: [count]
- Approval Gates Failed: [count]
- Escalations: [count]
```
