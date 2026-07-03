# Validation Contract

Contract Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved

## 1. Purpose and Scope
This document defines mandatory validation performed by every agent before publishing artifacts, emitting completion events, or requesting release progression.

Related contracts:
- artifact-contracts.md
- workflow-state.md
- quality-report-contract.md
- approval-contract.md

## 2. Validation Categories

### 2.1 Input Validation
Checks:
- Required input artifact references exist and are readable.
- Input artifact versions are supported.
- Input checksums match metadata.
- Input status is Published or explicitly permitted Draft by policy.

Failure behavior:
- Emit Blocked or Failure event.
- Transition to Blocked if missing prerequisites are recoverable.
- Hard-stop execution immediately when any required input artifact is missing.
- Do not generate functional artifacts under missing-input conditions.

### 2.2 Output Validation
Checks:
- Output artifact conforms to artifact type contract.
- Required fields are present and non-empty.
- Artifact envelope metadata is complete.

Failure behavior:
- Reject publication.
- Enter Retrying if auto-correction policy permits.

### 2.3 Artifact Validation
Checks:
- Artifact ownership is correct and exclusive.
- Version increment follows semantic versioning rules.
- Traceability references are valid.

Failure behavior:
- Reject artifact.
- Emit Failure event if ownership violation occurs.

### 2.4 Business Validation
Checks:
- Business rules are satisfied.
- Acceptance criteria alignment is preserved.
- Domain constraints are not violated.
- Open questions use the mandatory structured schema with no empty required fields.
- Workflow Status is computed from structured open-question metadata.

Business Analyst boundary checks (when agentId = business_analyst):
- No API endpoints or HTTP method definitions.
- No request/response payloads, DTOs, or schema definitions.
- No authentication implementation details.
- No framework, technology, architecture, deployment, or infrastructure decisions.
- No physical database design details (tables, columns, SQL, indexes, migrations).
- Business capability requirements are present instead of API Notes style content.
- Business data model remains conceptual only.
- Exactly this BA artifact package is produced:
  - requirements_spec.md
  - user_stories.md
  - acceptance_criteria.md
  - non_functional_requirements.md
  - ui_observations.md
  - figma_design_intake.md
  - screen_elements.md
  - personas.md
  - business_process_flows.md
  - business_rules.md
  - data_requirements.md
  - glossary.md
  - openlog.md
  - traceability.md
  - quality_report.md
  - handoff_contract.md
- No additional BA artifacts are produced outside the package.
- No duplicate information is spread across BA artifacts.
- If a Figma URL exists in `specification.md`, it is consumed automatically and preserved unchanged in BA outputs.
- If no Figma URL is present or inaccessible, check `examples/task-management/` for reference screenshots (SS) and use those as the visual reference source instead.
- If a Figma URL exists in `specification.md`, `figma_design_intake.md` must also be generated with the URL, covered screens, and frontend-relevant visual notes.
- If no Figma URL exists but screenshots are available from `examples/task-management/`, `figma_design_intake.md` must reference those screenshots instead.
- If neither Figma nor screenshots are available, the frontend stage must continue without blocking and may proceed using the other approved requirement artifacts.
- Acceptance criteria are centralized in `acceptance_criteria.md` and are not duplicated in `user_stories.md`.

Solution Architect boundary checks (when agentId = solution_architect):
- All Business Analyst artifacts are consumed as read-only inputs before architecture publication.
- Architecture preserves BA requirements intent without redefining business requirements.
- Every epic, feature, and user story is represented in architecture decomposition and contracts.
- Module decomposition is complete with clear responsibilities and inter-module dependencies.
- Layer interactions are explicit across presentation, business, and data layers.
- API contracts, data contracts, and integration contracts are complete and traceable.
- Security, validation, authorization, and error-handling are defined as architecture constraints.
- Navigation, workflows, and state transitions are defined where applicable.
- Component, service, repository, and database responsibilities are explicit where applicable.
- Cross-cutting concerns include logging, configuration, observability, auditing, and performance.
- No implementation code is included.
- No implementation-critical architectural information is missing.

Failure behavior:
- Block execution and generate open questions when ambiguity exists.
- Fail execution for explicit rule conflicts.
- Fail execution if Business Analyst boundary checks are violated.
- Fail execution if Solution Architect boundary checks are violated.

### 2.5 Schema Validation
Checks:
- Structural schema compliance for metadata and content blocks.
- Enumerations and field types match contract.
- Compact-content policy is applied without removing required sections/fields.
- `openlog.md` includes all mandatory fields per entry.
- `handoff_contract.md` includes mandatory sections: Workflow Context, Artifacts Produced, Artifact Status, OpenLog Summary, AI Usage Summary, Workflow Status, Next Agent.
- `quality_report.md` includes mandatory sections: Validation Summary, Coverage Summary, OpenLog Summary, AI Usage Summary, Confidence Score, Readiness, Blocking Issues.
- AI Usage sections contain metadata fields only (no narrative explanations).

Failure behavior:
- Reject output.
- Retry only for deterministic fixable errors.

### 2.6 Traceability Validation
Checks:
- Output links to source requirements and preceding artifacts.
- No orphan deliverables without trace references.

Failure behavior:
- Reject publication.
- Mark quality status as NeedsApproval or Blocked.

### 2.7 Quality Validation
Checks:
- Quality report is generated.
- Confidence score is computed.
- Risk and recommendation fields are complete.

Failure behavior:
- Do not emit Success completion event.
- Request approval if thresholds are below release policy limits.

### 2.8 Guardrails Validation
Checks:
- Security policies
- Input and output safety policies
- Governance and compliance policies

Failure behavior:
- Immediate block for guardrail-critical violations.
- Supervisor approval required for policy exceptions.

## 3. Validation Pipeline
```text
Read Inputs
-> Input Validation
-> Execute Agent Work
-> Output Validation
-> Artifact Validation
-> Business Validation
-> Schema Validation
-> Traceability Validation
-> Quality Validation
-> Guardrails Validation
-> Publish Artifact
-> Emit Success Event
```

## 4. Validation Result Contract
Required fields:
- validationId
- workflowId
- executionId
- agentId
- artifactRefs
- validationTimestamp
- checksPerformed
- checkResults
- overallResult: Pass | Warning | Fail
- confidenceScore: 0-100

Optional fields:
- warnings
- errors
- recommendation
- approvalRequired

Example structure:
```yaml
validationResult:
  validationId: val-qa-0142
  workflowId: wf-2026-06-30-001
  executionId: exec-0142
  agentId: qa-engineer
  overallResult: Warning
  confidenceScore: 84
  checksPerformed: [input, output, schema, traceability, quality]
  checkResults:
    schema: Pass
    traceability: Warning
  approvalRequired: false
```

## 5. Validation Failure Behavior
1. Fail-fast for security and ownership violations.
2. Fail-fast for missing required input artifacts.
3. Do not retry validation, business-rule, or approval-related failures.
4. Retry is permitted only for transient/runtime failures and only within retry limits.
5. Block and request approval when policy exceptions are needed.
6. Persist validation summary and emit corresponding event.

## 6. Retry Behavior
- Retry is allowed only when:
  - error category is transient/runtime retryable
  - retry count < 1
  - no guardrail-critical violation
- Retry is not allowed for validation failures.
- Retry is not allowed for business-rule failures.
- Retry is not allowed for approval-related failures.
- Retry metadata must be recorded in memory.
- Second failure transitions to Failed.
- On second failure, the agent must update openlog.md, handoff_contract.md, and quality_report.md, then return control to Supervisor.

## 6.1 Timeout Behavior
- If execution exceeds the stage budget, status must transition to TIMEOUT.
- TIMEOUT must be recorded in AI Usage, openlog.md, handoff_contract.md, and quality_report.md.
- After TIMEOUT recording, control must return to Supervisor.

## 7. Blocking Conditions
Automatic Blocked state when any occurs:
- Missing required input artifacts.
- Unresolved open questions affecting correctness.
- Policy conflict requiring human decision.
- Non-retryable external dependency unavailability within timeout window.

Structured open-question gate:
- If any open question has Blocking = Yes, Workflow Status must be REQUIRES HUMAN APPROVAL.
- If all open questions have Blocking = No, Workflow Status must be READY.
- Supervisor continuation decisions must use only Blocking, Approval Required, and Workflow Status fields.

## 8. Confidence Thresholds
- 90-100: Ready
- 80-89: Minor Review
- 60-79: Needs Approval
- below 60: Blocked

Thresholds must align with quality-report-contract.md.

## 9. Supervisor Governance
Supervisor must:
- enforce validation completion before accepting success events
- prevent state transition to Completed if mandatory validations are missing
- route Needs Approval and Blocked outcomes to approval flow when required
