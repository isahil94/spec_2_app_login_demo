# Lifecycle Hook Catalog

Document Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved and Mandatory  
Authority: Runtime Governance Council  
Scope: All runtime-managed workflows, agents, artifacts, memory, events, validation, approvals, and observability paths

## 1. Purpose
Hooks are reusable runtime execution points that inject standard behavior at defined lifecycle moments.

Why hooks exist:
- Enforce consistency across workflows and agents
- Centralize cross-cutting behavior
- Reduce duplicated lifecycle logic
- Improve traceability, reliability, and governance

Term boundaries:
- Agent: role-scoped autonomous actor
- Prompt: instruction text shaping behavior
- Skill: reusable capability definition
- Hook: runtime-triggered lifecycle execution point
- Tool: concrete mechanism used during execution

Hooks promote consistency and automation by standardizing when governance actions occur and what outcomes must be produced.

## 2. Hook Lifecycle
- Registration: Hook is declared and bound to a lifecycle trigger.
- Trigger: Runtime detects trigger condition and schedules hook.
- Execution: Hook runs within runtime policy and scope boundaries.
- Validation: Hook output and side effects are checked.
- Completion: Hook marks success and emits required records.
- Failure Handling: Hook reports failure, impact, and recovery path.
- Recovery: Runtime retries, remediates, or escalates per policy.

## 3. Workflow Hooks
### Before Workflow
- Purpose: Prepare workflow context and governance checks.
- Trigger: Immediately before workflow starts.
- Required Inputs: Workflow definition, dependencies, policy context.
- Expected Outputs: Readiness status, preflight findings.
- Validation Rules: Required dependencies and policy checks must pass.
- Success Criteria: Workflow is safe and ready to start.
- Failure Handling: Block start and emit workflow-prestart failure signal.

### After Workflow
- Purpose: Finalize records and post-execution summaries.
- Trigger: Immediately after workflow terminal state.
- Required Inputs: Final workflow state, artifacts, events.
- Expected Outputs: Completion summary, audit references.
- Validation Rules: Terminal state and evidence must be coherent.
- Success Criteria: Workflow closure is complete and traceable.
- Failure Handling: Emit closure failure and request remediation.

### Workflow Started
- Purpose: Record official workflow start.
- Trigger: Transition to running state.
- Required Inputs: Workflow id, execution id, start metadata.
- Expected Outputs: Start record and observability signal.
- Validation Rules: Identifiers and state transition must be valid.
- Success Criteria: Start event is uniquely and correctly recorded.
- Failure Handling: Retry emission, then escalate runtime issue.

### Workflow Completed
- Purpose: Record successful workflow completion.
- Trigger: Transition to completed state.
- Required Inputs: Final outputs, validation status, completion metadata.
- Expected Outputs: Completion record and quality summary link.
- Validation Rules: All required gates must be satisfied.
- Success Criteria: Completion is governance-valid and auditable.
- Failure Handling: Prevent final closure and raise compliance incident.

### Workflow Failed
- Purpose: Record workflow failure and failure context.
- Trigger: Transition to failed state.
- Required Inputs: Failure reason, impact scope, recovery context.
- Expected Outputs: Failure record and remediation recommendation.
- Validation Rules: Failure classification must be present.
- Success Criteria: Failure is explicit, traceable, and actionable.
- Failure Handling: Trigger recovery or escalation policy.

### Workflow Cancelled
- Purpose: Record controlled cancellation.
- Trigger: Transition to cancelled state.
- Required Inputs: Cancellation reason, initiator, affected scope.
- Expected Outputs: Cancellation record and cleanup requirements.
- Validation Rules: Cancellation must be authorized and traceable.
- Success Criteria: Cancellation is safely finalized.
- Failure Handling: Escalate unauthorized or inconsistent cancellation.

### Workflow Paused
- Purpose: Record pause and preserve execution continuity.
- Trigger: Transition to paused state.
- Required Inputs: Pause reason, current checkpoints.
- Expected Outputs: Pause record and resume prerequisites.
- Validation Rules: Checkpoint integrity must be preserved.
- Success Criteria: Workflow can safely resume later.
- Failure Handling: Initiate recovery state reconciliation.

### Workflow Resumed
- Purpose: Record restart from paused state.
- Trigger: Transition from paused to running.
- Required Inputs: Resume authorization, checkpoint references.
- Expected Outputs: Resume record and resumed-state confirmation.
- Validation Rules: Resume prerequisites must be satisfied.
- Success Criteria: Execution continues from valid state.
- Failure Handling: Revert to pause and escalate resolution request.

## 4. Agent Hooks
### Before Agent
- Purpose: Pre-agent readiness and scope checks.
- Trigger: Before agent invocation.
- Required Inputs: Agent role, stage context, dependencies.
- Expected Outputs: Agent-start readiness status.
- Validation Rules: Role scope and dependencies must be valid.
- Success Criteria: Agent invocation is safe and authorized.
- Failure Handling: Skip invocation and emit blocked status.

### After Agent
- Purpose: Consolidate agent outputs and status.
- Trigger: After agent invocation ends.
- Required Inputs: Agent result, produced artifacts, validation status.
- Expected Outputs: Agent completion summary and trace links.
- Validation Rules: Output and status must align.
- Success Criteria: Agent closeout is complete and consistent.
- Failure Handling: Emit post-agent reconciliation task.

### Agent Started
- Purpose: Record agent execution start.
- Trigger: Agent state enters running.
- Required Inputs: Agent id, execution context.
- Expected Outputs: Start signal and observability correlation.
- Validation Rules: Agent identity and state transition valid.
- Success Criteria: Start is uniquely recorded.
- Failure Handling: Retry publish, then log runtime anomaly.

### Agent Completed
- Purpose: Record successful agent completion.
- Trigger: Agent terminal success.
- Required Inputs: Output summary, quality status.
- Expected Outputs: Completion signal and handoff links.
- Validation Rules: Completion criteria must be met.
- Success Criteria: Agent success is auditable.
- Failure Handling: Downgrade to failed and trigger remediation.

### Agent Failed
- Purpose: Record failed agent execution.
- Trigger: Agent terminal failure.
- Required Inputs: Error details, impacted outputs.
- Expected Outputs: Failure signal and retry recommendation.
- Validation Rules: Failure must include cause and scope.
- Success Criteria: Failure is diagnosable.
- Failure Handling: Invoke retry or escalation flow.

### Agent Blocked
- Purpose: Record unresolved blocker state.
- Trigger: Agent cannot proceed under policy.
- Required Inputs: Blocker reason, open questions, dependency impact.
- Expected Outputs: Blocked signal and approval prerequisites.
- Validation Rules: Blocked reason must be explicit.
- Success Criteria: Blocked path is decision-ready.
- Failure Handling: Force Supervisor escalation.

### Agent Retried
- Purpose: Record controlled retry attempt.
- Trigger: Retry policy initiates new attempt.
- Required Inputs: Previous failure context, retry count.
- Expected Outputs: Retry signal and updated attempt metadata.
- Validation Rules: Retry policy limits must be respected.
- Success Criteria: Retry is policy-compliant.
- Failure Handling: Halt retries and escalate after limit.

### Agent Skipped
- Purpose: Record intentional skip with justification.
- Trigger: Stage policy or conditions skip agent.
- Required Inputs: Skip rationale, impact assessment.
- Expected Outputs: Skip signal and downstream implications.
- Validation Rules: Skip must be policy-authorized.
- Success Criteria: Skip is explicit and non-ambiguous.
- Failure Handling: Reopen decision for Supervisor review.

## 5. Validation Hooks
### Before Validation
- Purpose: Prepare validation scope and criteria.
- Trigger: Before validation execution.
- Required Inputs: Target outputs, validation policy.
- Expected Outputs: Validation plan context.
- Validation Rules: Criteria completeness required.
- Success Criteria: Validation can run deterministically.
- Failure Handling: Block validation and report missing criteria.

### After Validation
- Purpose: Consolidate validation outcomes.
- Trigger: After validation ends.
- Required Inputs: Validation results, evidence links.
- Expected Outputs: Final validation summary.
- Validation Rules: Result-to-evidence mapping required.
- Success Criteria: Decision is auditable.
- Failure Handling: Mark unresolved and trigger review.

### Validation Passed
- Purpose: Record pass decision.
- Trigger: Validation pass outcome.
- Required Inputs: Passed checks and evidence.
- Expected Outputs: Pass signal.
- Validation Rules: No critical unresolved findings.
- Success Criteria: Output may progress.
- Failure Handling: Reclassify if contradictory evidence appears.

### Validation Failed
- Purpose: Record fail decision.
- Trigger: Validation fail outcome.
- Required Inputs: Failure findings and severity.
- Expected Outputs: Fail signal and remediation path.
- Validation Rules: Failure details must be complete.
- Success Criteria: Remediation is actionable.
- Failure Handling: Block progression and escalate if critical.

## 6. Artifact Hooks
### Before Artifact Creation
- Purpose: Ensure creation prerequisites are met.
- Trigger: Before artifact generation.
- Required Inputs: Artifact type, owner, source context.
- Expected Outputs: Creation readiness status.
- Validation Rules: Ownership and type validity required.
- Success Criteria: Safe artifact creation start.
- Failure Handling: Block creation and report missing prerequisites.

### After Artifact Creation
- Purpose: Record created artifact state.
- Trigger: Immediately after creation.
- Required Inputs: Artifact metadata and content references.
- Expected Outputs: Creation record.
- Validation Rules: Metadata completeness required.
- Success Criteria: Artifact is traceable and valid.
- Failure Handling: Mark artifact invalid and request fix.

### Before Artifact Publish
- Purpose: Verify publish eligibility.
- Trigger: Before publish action.
- Required Inputs: Artifact version, validation status.
- Expected Outputs: Publish authorization status.
- Validation Rules: Validation and compliance must pass.
- Success Criteria: Publish is governance-approved.
- Failure Handling: Reject publish and keep draft state.

### After Artifact Publish
- Purpose: Confirm publication and lineage.
- Trigger: After publish success.
- Required Inputs: Published artifact id/version.
- Expected Outputs: Publish record and downstream notification.
- Validation Rules: Version and lineage must be valid.
- Success Criteria: Published artifact is immutable and discoverable.
- Failure Handling: Emit post-publish integrity alert.

### Artifact Version Created
- Purpose: Record new version lineage.
- Trigger: New artifact version generated.
- Required Inputs: Previous and new version references.
- Expected Outputs: Version lineage record.
- Validation Rules: Version increment must be valid.
- Success Criteria: History is preserved without overwrite.
- Failure Handling: Reject invalid version transition.

### Artifact Archived
- Purpose: Record archival action.
- Trigger: Artifact enters archive state.
- Required Inputs: Archive reason, retention policy reference.
- Expected Outputs: Archival record.
- Validation Rules: Archival authorization required.
- Success Criteria: Artifact is archived with retrieval trace.
- Failure Handling: Revert archive state and escalate policy breach.

## 7. Approval Hooks
### Approval Requested
- Purpose: Record approval request initiation.
- Trigger: Agent/workflow enters approval-needed state.
- Required Inputs: Decision package, risk and impact context.
- Expected Outputs: Approval request record.
- Validation Rules: Request completeness required.
- Success Criteria: Request is decision-ready.
- Failure Handling: Block progression and require package completion.

### Approval Granted
- Purpose: Record approved decision.
- Trigger: Approval authority grants request.
- Required Inputs: Approval decision and conditions.
- Expected Outputs: Grant record and resume prerequisites.
- Validation Rules: Conditions must be explicit.
- Success Criteria: Execution can resume safely.
- Failure Handling: Hold resume until conditions are satisfiable.

### Approval Rejected
- Purpose: Record rejection and required changes.
- Trigger: Approval authority rejects request.
- Required Inputs: Rejection rationale.
- Expected Outputs: Rejection record and remediation directive.
- Validation Rules: Rejection context must be actionable.
- Success Criteria: Clear next step exists.
- Failure Handling: Route back to analysis/remediation path.

### Approval Timed Out
- Purpose: Record decision timeout.
- Trigger: Approval SLA expires.
- Required Inputs: Request id, timeout metadata.
- Expected Outputs: Timeout record and escalation action.
- Validation Rules: Timeout policy thresholds must apply.
- Success Criteria: Timeout is escalated consistently.
- Failure Handling: Notify Supervisor and pause workflow.

### Workflow Resumed
- Purpose: Confirm resumption after approval path.
- Trigger: Resume authorized post-approval.
- Required Inputs: Approved conditions, checkpoint context.
- Expected Outputs: Resume confirmation.
- Validation Rules: Conditions must be validated before run.
- Success Criteria: Execution resumes from valid checkpoint.
- Failure Handling: Re-pause and emit resume failure signal.

## 10. Error Hooks
### Execution Error
- Purpose: Handle execution-time task failures.
- Trigger: Runtime execution step error.
- Required Inputs: Error details, context scope.
- Expected Outputs: Error incident and remediation path.
- Validation Rules: Error must be classified.
- Success Criteria: Recovery action is clear.
- Failure Handling: Retry or escalate based on policy.

### Validation Error
- Purpose: Handle validation subsystem errors.
- Trigger: Validation processing error.
- Required Inputs: Validator context and error details.
- Expected Outputs: Validation error incident.
- Validation Rules: Distinguish system error from validation fail.
- Success Criteria: Correct follow-up path chosen.
- Failure Handling: Re-run validation or escalate runtime issue.

### Runtime Error
- Purpose: Handle runtime infrastructure failures.
- Trigger: Runtime component failure.
- Required Inputs: Runtime component id, error metadata.
- Expected Outputs: Runtime incident record.
- Validation Rules: Impact scope and severity required.
- Success Criteria: Containment and recovery initiated.
- Failure Handling: Escalate to Supervisor and recovery hooks.

### Unexpected Exception
- Purpose: Catch unclassified exceptions safely.
- Trigger: Unhandled exception boundary.
- Required Inputs: Exception details and stack context.
- Expected Outputs: Exception incident record.
- Validation Rules: Must preserve forensic evidence.
- Success Criteria: No silent failure.
- Failure Handling: Enter safe recovery mode.

### Recovery Started
- Purpose: Record start of recovery process.
- Trigger: Recovery policy initiated.
- Required Inputs: Incident reference and recovery plan.
- Expected Outputs: Recovery-start signal.
- Validation Rules: Recovery authority and scope required.
- Success Criteria: Recovery begins under governance.
- Failure Handling: Escalate blocked recovery.

### Recovery Completed
- Purpose: Record recovery completion.
- Trigger: Recovery process finishes.
- Required Inputs: Recovery outcomes and validation results.
- Expected Outputs: Recovery completion record.
- Validation Rules: Post-recovery checks must pass.
- Success Criteria: System is stable and traceable.
- Failure Handling: Re-enter incident workflow.

## 11. Observability Hooks
### Logging
- Purpose: Ensure structured lifecycle logging.
- Trigger: At defined lifecycle boundaries.
- Required Inputs: Context metadata, status, severity.
- Expected Outputs: Structured log records.
- Validation Rules: Required fields must be present.
- Success Criteria: Logs support diagnosis and audit.
- Failure Handling: Emit observability degradation warning.

### Metrics
- Purpose: Capture quantitative runtime signals.
- Trigger: At key state transitions and outcomes.
- Required Inputs: Metric identity, values, dimensions.
- Expected Outputs: Metric records.
- Validation Rules: Metric schema consistency required.
- Success Criteria: Metrics are reliable and comparable.
- Failure Handling: Flag metric pipeline issue.

### Tracing
- Purpose: Preserve end-to-end execution correlation.
- Trigger: Workflow/agent execution lifecycle.
- Required Inputs: Trace and span context.
- Expected Outputs: Trace records.
- Validation Rules: Correlation ids must remain intact.
- Success Criteria: Full path reconstruction is possible.
- Failure Handling: Emit trace integrity alert.

### Audit Recording
- Purpose: Preserve compliance evidence.
- Trigger: Governance-relevant lifecycle events.
- Required Inputs: Decisions, outcomes, references.
- Expected Outputs: Audit entries.
- Validation Rules: Audit records must be immutable and complete.
- Success Criteria: Independent audit can reconstruct events.
- Failure Handling: Trigger audit-gap incident.

### Performance Measurement
- Purpose: Capture runtime performance indicators.
- Trigger: Execution checkpoints.
- Required Inputs: Timing and resource usage data.
- Expected Outputs: Performance records and trend links.
- Validation Rules: Measurement context must be comparable.
- Success Criteria: Performance drift is detectable.
- Failure Handling: Emit measurement integrity warning.

### Health Monitoring
- Purpose: Track service and lifecycle health.
- Trigger: Periodic checks and lifecycle boundaries.
- Required Inputs: Health probes and component status.
- Expected Outputs: Health status records.
- Validation Rules: Health criteria must be explicit.
- Success Criteria: Degradation is detected early.
- Failure Handling: Escalate unhealthy state immediately.

## 12. Hook Ordering
- Execution order: System-level hooks run before domain hooks, then post-action hooks finalize.
- Dependencies: Hooks requiring outputs from others run strictly after providers.
- Nested hooks: Child hooks inherit parent correlation context and cannot break parent guarantees.
- Priority: Critical safety and governance hooks execute before optimization hooks.
- Conflict resolution: Precedence order is Guardrails, Contracts, Workflow Policy, Hook Priority, Local Preferences.

## 13. Hook Composition
Hooks compose as layered runtime behavior.

Composition examples:
- Workflow start chain: Before Workflow -> Workflow Started -> Logging and Metrics and Tracing
- Agent completion chain: Before Agent -> Agent Started -> After Agent -> Agent Completed -> After Validation
- Publish chain: Before Artifact Publish -> Before Event Publish -> After Event Publish -> After Artifact Publish -> Audit Recording
- Approval recovery chain: Approval Requested -> Approval Granted -> Workflow Resumed -> Recovery Completed
- Failure chain: Execution Error -> Recovery Started -> Validation Failed or Recovery Completed -> Create escalation signal

Composition rule: A composed chain is valid only when each hook’s prerequisites and validation rules are satisfied.

## 14. Hook Safety Rules
- Hooks must not modify agent responsibilities.
- Hooks must be deterministic under equivalent context.
- Hooks must be idempotent where repeat invocation is possible.
- Hooks must preserve execution history and lineage.
- Hooks must never bypass validation gates.
- Hooks must never bypass approval pathways.
- Hooks must never suppress failures or blocker signals.

## 15. Hook Failure Strategy
- Retry policy: Use bounded retries for transient failures only.
- Recovery: Execute controlled recovery hooks with traceable context.
- Rollback considerations: Rollback only where safe and state-consistent.
- Escalation: Escalate unresolved or critical failures immediately.
- Supervisor notification: Notify Supervisor for blocked, repeated, or high-severity hook failures.

Failure strategy outcome: Preserve safety, integrity, and auditability before restoring throughput.

## 16. Future Hooks
Future hooks can be added safely by:
- Introducing new triggers without changing existing trigger semantics
- Preserving backward compatibility of current hook contracts
- Defining clear precedence and dependency behavior
- Requiring validation rules and success criteria for each new hook
- Applying governance review before activation

Stability rule: New hooks may extend lifecycle behavior but must not invalidate existing workflow guarantees.

This document is the authoritative lifecycle hook catalog for the platform.