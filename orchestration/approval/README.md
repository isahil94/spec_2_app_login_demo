# Approval Service Architecture

Document Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved

## 1. Purpose
The Approval Service exists to provide a controlled, auditable, and deterministic human-in-the-loop decision mechanism for an otherwise autonomous SDLC platform.

Approvals are distinct from workflow execution:

1. Workflow execution progresses stages, dependencies, and runtime transitions.
2. Approval handling captures and resolves decision points that require explicit human authorization.
3. The Approval Service governs decision lifecycle, while Supervisor governs workflow control.

Approvals are distinct from validation:

1. Validation determines conformance to contracts, policy rules, and structural correctness.
2. Approval determines whether to proceed when policy requires human judgment, exception handling, or risk acceptance.
3. Validation outputs may trigger approval requests, but validation and approval remain separate control domains.

The Approval Service does not execute agents or workflows. It manages approval state, routing, decisions, and traceability.

## 2. Responsibilities
The Approval Service is responsible for:

1. Approval creation from Supervisor-approved request intents.
2. Approval routing to designated approvers based on policy and role mapping.
3. Approval tracking across full lifecycle states.
4. Approval expiration handling for due-date and timeout conditions.
5. Workflow pausing coordination through Supervisor integration.
6. Workflow resuming coordination after approved decisions.
7. Decision recording with rationale and condition capture.
8. Audit logging of all request, assignment, decision, and escalation actions.
9. Notification dispatch for pending actions, reminders, and outcomes.
10. Escalation handling for overdue, missing-approver, or high-risk approvals.

## 3. Design Principles
Approval Service architecture follows these principles:

1. Human-in-the-loop: Human decisions are explicit control points for risk and exception handling.
2. Supervisor controlled: Supervisor is the only authority that initiates and applies approval outcomes to workflow execution.
3. Configuration-driven: Approval rules, routing, priority, and timeout behavior are policy-configured.
4. Auditable: Every action is attributable, timestamped, and historically inspectable.
5. Observable: Pending load, decision latency, escalation rate, and workflow impact are measurable.
6. Deterministic: Equivalent requests and policy context produce predictable approval outcomes.
7. Secure: Authorization, integrity, traceability, and least-privilege controls are enforced.
8. Local-first: Decision lifecycle control remains in local runtime governance boundaries.
9. Extensible: New approval types, policies, and channels can be added without redesigning core service behavior.

## 4. Approval Types
The Approval Service supports multiple approval types for governance coverage.

1. Workflow Approval
Used to authorize continuation, rerouting, retry exception, or terminal workflow decisions.

2. Artifact Approval
Used to authorize publication or downstream consumption of policy-sensitive artifacts.

3. Architecture Approval
Used to authorize architecture decisions with significant system impact or tradeoff risk.

4. Code Review Approval
Used to authorize implementation readiness based on review findings and policy gates.

5. Deployment Approval
Used to authorize deployment progression, release gates, and rollback-risk acceptance.

6. Requirement Clarification
Used when ambiguous requirements require human clarification before progression.

7. Risk Acceptance
Used to formally accept identified risks with explicit rationale and conditions.

8. Manual Decision
Used for policy-defined discretionary decisions not covered by predefined approval templates.

9. Emergency Approval
Used for urgent exception scenarios requiring accelerated decision flow with enhanced audit requirements.

Each approval type defines required context, approver policy, expiration behavior, and escalation path.

## 5. Internal Components
The Approval Service consists of the following logical components.

### 5.1 Approval Manager
Coordinates approval lifecycle operations, state transitions, and policy application.

### 5.2 Approval Queue
Maintains pending approvals awaiting assignment or decision, ordered by priority and due constraints.

### 5.3 Request Registry
Stores canonical request records, metadata, context references, and status lineage.

### 5.4 Decision Recorder
Captures approvals, rejections, rationale, conditions, and decision provenance.

### 5.5 Notification Manager
Issues request notifications, reminders, expiration warnings, and decision outcomes.

### 5.6 Timeout Manager
Tracks due dates and timeout windows, applying expiration and escalation rules.

### 5.7 Escalation Manager
Routes unresolved or high-risk approvals to designated escalation paths.

### 5.8 Workflow Coordinator
Coordinates state effects with Supervisor for pause, resume, retry, cancel, or fail actions.

### 5.9 Metrics Collector
Captures queue, latency, decision, escalation, and workflow impact metrics.

### 5.10 Audit Logger
Persists immutable audit records for all approval lifecycle actions.

## 6. Approval Lifecycle
Approvals progress through defined lifecycle states.

1. Request Created
Supervisor submits approval request intent with required metadata and context references.

2. Registered
Approval record is validated and registered in request registry.

3. Queued
Approval enters active queue awaiting assignment and decision processing.

4. Assigned
Approver identity is resolved and assignment context is recorded.

5. Waiting
Approval is pending approver decision within defined due window.

6. Approved
Approver accepts request and may include conditions and rationale.

7. Rejected
Approver denies request with mandatory rejection rationale.

8. Expired
Approval exceeds due window without decision and is marked expired.

9. Cancelled
Approval is cancelled by policy, Supervisor action, or superseded context.

10. Completed
Lifecycle closes after decision propagation, workflow coordination, and audit finalization.

Lifecycle transitions are deterministic, evented, and auditable.

## 7. Approval Requests
Approval requests must include complete metadata and context.

Required request metadata:

1. Workflow ID
Identifies workflow scope impacted by the decision.

2. Approval ID
Uniquely identifies approval record and lifecycle lineage.

3. Requesting Agent
Identifies originating agent whose execution context triggered the request.

4. Reason
Summarizes why approval is required and what risk or ambiguity exists.

5. Required Decision
Defines explicit decision needed, such as approve, reject, or approve with conditions.

6. Context
Provides structured context references needed for informed decision-making.

7. Artifacts
Lists related artifact references and versions relevant to decision scope.

8. Priority
Defines urgency and queue ordering class.

9. Due Date
Defines expiration boundary and timeout behavior.

10. Approver
Defines designated approver identity or policy-resolved approver role.

Requests missing mandatory metadata are invalid and must be rejected prior to queueing.

## 8. Workflow Integration
Approval outcomes directly influence workflow progression through Supervisor control.

Workflow integration behaviors:

1. Pause workflow
When approval is required, Supervisor transitions workflow to waiting-for-approval state.

2. Resume workflow
Approved decisions trigger Supervisor-mediated resume transitions.

3. Reject workflow
Rejected decisions may terminate stage progression or workflow branch according to policy.

4. Retry workflow
Approval outcomes may authorize controlled retry paths for previously blocked stages.

5. Cancel workflow
Approval cancellation may trigger workflow cancellation when policy requires hard stop.

6. Escalation
Unresolved or expired approvals trigger escalation pathways and governance decisions.

The Approval Service informs workflow behavior; Supervisor applies workflow transitions.

## 9. Supervisor Integration
Supervisor is the exclusive orchestration authority for approval initiation and workflow impact.

Integration model:

1. Supervisor creates approval requests from blocked events, open questions, or policy-defined decision points.
2. Approval Service validates and tracks request lifecycle and decision outcomes.
3. Decisions are returned to Supervisor with rationale, conditions, and status.
4. Supervisor resumes, retries, blocks, fails, or cancels workflow based on decision and policy.

This integration preserves the platform rule that agents never communicate directly with humans.

## 10. Agent Interaction
Agents interact with approval flow indirectly through governed artifacts and events.

Agent interaction model:

1. Agent detects need for clarification, approval, or risk decision.
2. Agent enters blocked execution state and emits blocked or approval-requested events.
3. Agent publishes open question and approval request artifacts with required context references.
4. Supervisor creates approval request through Approval Service.
5. After decision, Supervisor updates workflow state and agent continuation eligibility.

Agents never submit decisions directly to approvers and never bypass Supervisor mediation.

## 11. Event Integration
Approval lifecycle is communicated through event-driven contracts.

Core events include:

1. ApprovalRequested
2. ApprovalApproved
3. ApprovalRejected
4. ApprovalExpired
5. WorkflowPaused
6. WorkflowResumed
7. WorkflowCancelled

Event integration behaviors:

1. Approval events update workflow context, memory references, and operational dashboards.
2. Event Bus transports lifecycle changes to Supervisor, Workflow Engine, and observability subsystems.
3. Event ordering and correlation preserve decision traceability.

## 12. Artifact Integration
Approval Service manages and references multiple artifact classes.

Artifact integration includes:

1. Approval Request artifacts capturing request intent, context, and required decision.
2. Decision artifacts capturing decision outcomes, rationale, and conditions.
3. Review artifacts referenced as supporting evidence for decisions.
4. Approval history records preserving lifecycle transitions and trace links.
5. Versioning of approval artifacts when request context or decision context evolves.
6. Traceability links connecting approvals to workflow states, events, artifacts, and quality outcomes.

Artifact integration is contract-governed and immutable after publication where policy requires.

## 13. Security
Approval decisions are high-governance actions and require strong controls.

Security controls:

1. Authorization ensures only permitted roles can create, view, decide, or escalate approvals.
2. Authentication considerations ensure decision actors are verifiable and attributable.
3. Integrity controls protect request and decision records from unauthorized modification.
4. Audit logging records all lifecycle actions, including assignments, reminders, decisions, and overrides.
5. Decision traceability ensures every decision is linked to actor, context, time, and rationale.
6. Least privilege limits access to only the minimum approval scopes required by role.

Security violations are escalated and may force approval invalidation or workflow blocking.

## 14. Observability
Approval Service observability provides governance and operational insight.

Observable dimensions:

1. Pending approvals by type, priority, age, and workflow.
2. Approval time metrics including queue wait and decision latency.
3. Decision metrics including approved, rejected, expired, and cancelled counts.
4. Workflow impact metrics such as paused duration and resume lead time.
5. Escalation metrics including frequency, causes, and resolution outcomes.
6. Reports for SLA performance, decision quality, and policy compliance trends.

Observability enables proactive queue management and governance assurance.

## 15. Failure Handling
Approval failures are handled through deterministic policy paths.

Failure scenarios and handling:

1. Timeouts
Timeout Manager marks expired approvals and triggers escalation or terminal workflow handling.

2. Missing approver
Routing failure triggers fallback role resolution or escalation path activation.

3. Rejected approvals
Supervisor applies rejection policy, such as block, fail, or reroute workflow execution.

4. Expired approvals
Expired approvals trigger policy-defined retry request, escalation, or workflow cancellation.

5. Recovery
Service restoration replays pending state and preserves decision lineage from registry and audit logs.

6. Escalation
High-risk unresolved approvals are escalated to designated governance authorities.

Failure handling remains auditable and contract-compliant.

## 16. Performance
Approval Service performance focuses on timely decision handling without sacrificing governance controls.

Performance considerations:

1. Approval queue efficiency through priority-aware ordering and aging controls.
2. Notification efficiency through targeted delivery and reminder throttling policies.
3. Workflow resume latency minimization after decision finalization.
4. Scalability considerations for growing approval volumes within single-runtime local-first constraints.

Performance optimization must preserve determinism, security, and traceability.

## 17. Example Approval Flow
This example describes an Architecture Approval end-to-end flow.

1. Solution Architect requests approval
Solution Architect identifies architecture decision requiring human authorization, emits blocked and approval-requested events, and publishes approval request artifact references.

2. Workflow pauses
Supervisor receives blocked context and transitions workflow to waiting-for-approval state.

3. Supervisor creates approval
Supervisor submits structured approval request to Approval Service with reason, context, artifacts, priority, due date, and approver mapping.

4. Approval is routed and tracked
Approval Service registers request, assigns approver, sends notification, and tracks waiting status.

5. User approves
Approver records approved decision with rationale and optional conditions. Decision Recorder stores immutable decision record.

6. Workflow resumes
Approval Service emits approval-approved event and returns outcome to Supervisor. Supervisor applies decision conditions and transitions workflow to resumed and running states.

7. Continuation and closure
Workflow Engine continues execution from checkpoint, and Approval Service marks approval lifecycle completed with full audit trace.

Every interaction is logged, evented, and traceable across workflow, artifact, and approval records.

## 18. Future Enhancements
Potential future enhancements include:

1. Multiple approvers for quorum-based or staged approval strategies.
2. Approval policies with richer dynamic routing, conditional logic, and SLA classes.
3. Role-based approvals with fine-grained entitlement and delegation controls.
4. Digital signatures for stronger non-repudiation and governance assurance.
5. External approval system integration for enterprise governance interoperability.
6. Mobile approvals for faster decision latency in high-priority workflows.

Future enhancements must preserve Supervisor control, contract compliance, deterministic behavior, and local-first governance boundaries.