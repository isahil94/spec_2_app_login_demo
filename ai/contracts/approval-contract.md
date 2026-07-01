# Approval Contract

Contract Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved

## 1. Purpose and Scope
This document defines the human approval contract for blocked or exception workflows. Agents never communicate directly with humans.

Related contracts:
- workflow-state.md
- event-contracts.md
- memory-contract.md
- validation-contract.md

## 2. Approval Flow
```text
Agent
  -> Block
  -> Supervisor
  -> Approval Service
  -> Dashboard / CLI
  -> Human Decision
  -> Supervisor Resume
```

Rules:
1. Only Supervisor may create approval requests.
2. Approval Service is the only interface to human decision channels.
3. Agents receive approval outcome through Supervisor events and memory updates only.

## 3. Approval Request Contract
Required fields:
- approvalId
- workflowId
- executionId
- requestedByAgentId
- requestedBySupervisorId
- requestedAt
- requestType: BlockerResolution | ExceptionOverride | RiskAcceptance | ScopeChange
- priority: Low | Medium | High | Critical
- reasonCode
- reasonSummary
- impactAssessment
- options[]
- defaultRecommendation
- decisionDeadline
- relatedArtifactRefs
- relatedEventIds

Optional fields:
- escalationPolicyRef
- supportingEvidenceRefs
- knownRisks

Example structure:
```yaml
approvalRequest:
  approvalId: apr-00291
  workflowId: wf-2026-06-30-001
  executionId: exec-0142
  requestedByAgentId: backend-developer
  requestedBySupervisorId: supervisor
  requestType: ExceptionOverride
  priority: High
  reasonCode: DEPENDENCY_POLICY_CONFLICT
  reasonSummary: "External service policy mismatch"
  impactAssessment: "Backend completion blocked"
  options:
    - optionId: OPT-1
      label: "Approve temporary compatibility mode"
    - optionId: OPT-2
      label: "Reject and fail workflow"
  defaultRecommendation: OPT-1
  decisionDeadline: 2026-06-30T14:00:00Z
  relatedArtifactRefs:
    - art-backend-spec-0011@1.1.0
```

## 4. Approval Response Contract
Required fields:
- approvalId
- workflowId
- executionId
- decision: Approved | Rejected | Timeout | Escalated
- decisionBy
- decisionAt
- selectedOptionId
- rationale
- conditions
- expiresAt

Optional fields:
- followUpActions
- reviewAfter

Example structure:
```yaml
approvalResponse:
  approvalId: apr-00291
  workflowId: wf-2026-06-30-001
  executionId: exec-0142
  decision: Approved
  decisionBy: human-approver-07
  decisionAt: 2026-06-30T13:10:10Z
  selectedOptionId: OPT-1
  rationale: "Temporary compatibility mode accepted with monitoring"
  conditions:
    - "Enable elevated logging"
    - "Review within 7 days"
```

## 5. Timeout Behavior
- If decisionDeadline passes with no decision:
  1. Approval Service sets decision to Timeout.
  2. Emit Approval timeout event.
  3. Supervisor applies policy:
     - Move to Failed, or
     - Escalate for higher-level decision.

## 6. Reject Behavior
When decision is Rejected:
1. Supervisor updates workflow to Failed or Blocked per policy.
2. Rejection rationale is persisted in Approval Metadata.
3. Failure event is emitted with reason and affected artifacts.

## 7. Resume Behavior
When decision is Approved:
1. Supervisor validates decision conditions.
2. Supervisor transitions state:
   - WaitingForApproval -> Resumed -> Running.
3. Supervisor emits Approval.Resumed and Lifecycle transition events.
4. Execution continues from last safe checkpoint.

## 8. Escalation Contract
Escalation triggers:
- Critical priority requests not decided before warning threshold.
- Timeout on mandatory approvals.
- Policy-defined high-risk rejections.

Escalation required fields:
- escalationId
- approvalId
- escalatedAt
- escalationLevel
- escalationReason
- escalatedTo

## 9. Audit Requirements
Every approval operation must be auditable with:
- who initiated request
- what was requested
- when requested
- who decided
- decision and rationale
- conditions and expiry
- resulting workflow transition

Audit records are immutable and retained per memory-contract.md.

## 10. Notification Contract
Approval Service must generate notifications for:
- Request created
- Reminder before deadline
- Decision recorded
- Timeout
- Escalation

Notification payload required fields:
- notificationId
- approvalId
- workflowId
- eventType
- recipients
- createdAt
- deliveryStatus

## 11. Security and Access Control
- Decision rights are role-based and policy-driven.
- Unauthorized decision attempts are rejected and audited.
- Approval request content must exclude secrets and sensitive credentials.
