# Agent Contract

Contract Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved

## 0. Mandatory Execution Governance (Shared, All Agents)

This section is mandatory for all agents and overrides any weaker retry, timeout, or model-selection guidance.

### 0.1 Retry Policy (Mandatory)

- Max Retries: 1
- Retry Strategy: retry only for transient/runtime errors.
- Do not retry validation failures.
- Do not retry business-rule failures.
- Do not retry approval-related failures.
- On second failure:
	- mark execution status as FAILED
	- append failure record to openlog.md
	- record failure in handoff_contract.md
	- record failure in quality_report.md
	- return control to Supervisor immediately

### 0.2 Execution Budgets (Mandatory)

| Agent | Context Budget | Max Duration |
|---|---|---|
| Supervisor | Small | 30 sec |
| Business Analyst | Medium | 3 min |
| Solution Architect | Large | 5 min |
| UI/UX Developer | Medium | 3 min |
| Backend Developer | Large | 5 min |
| Database Developer | Medium | 3 min |
| QA Engineer | Medium | 3 min |
| Reviewer | Large | 4 min |
| Documentation | Small | 2 min |
| DevOps | Medium | 3 min |

If a budget is exceeded:

- mark execution status as TIMEOUT
- record timeout in AI Usage
- append timeout in openlog.md
- record timeout in handoff_contract.md
- record timeout in quality_report.md
- return control to Supervisor immediately

### 0.3 Model Profile Policy (Mandatory)

Provider-agnostic model profiles are required. Vendor-specific model names must not be hardcoded.

| Agent | Required Profile |
|---|---|
| Supervisor | FAST |
| Business Analyst | BALANCED |
| Solution Architect | HIGH_REASONING |
| UI/UX Developer | BALANCED |
| Backend Developer | HIGH_REASONING |
| Database Developer | BALANCED |
| QA Engineer | BALANCED |
| Reviewer | HIGH_REASONING |
| Documentation | FAST |
| DevOps | BALANCED |

### 0.4 Inheritance and Non-Duplication Rule

- All agents inherit this policy from shared configuration.
- Agent-specific files must not redefine these retry, budget, or model-profile rules.
- Conflicts must be resolved in favor of this shared section.

## 1. Purpose
This contract defines the common runtime and governance obligations that every autonomous agent must satisfy in the Agentic SDLC platform. A unified contract is required to guarantee that independently specialized agents behave consistently under orchestration, exchange artifacts and events safely, and produce traceable outcomes that can be validated, audited, and resumed deterministically.

Without a shared contract, agent outputs become non-interoperable, event semantics drift, and workflow control becomes fragile. This document establishes a stable, implementation-independent foundation so all current and future agents can execute autonomously while remaining compliant with platform controls.

## 2. Scope
This contract governs agent behavior, interfaces, lifecycle, metadata, validation, memory interaction, event obligations, security expectations, and compliance requirements.

It applies to every platform agent regardless of responsibility, including Supervisor, Business Analyst, Solution Architect, UI/UX Developer, Backend Developer, Database Developer, QA Engineer, Reviewer, DevOps & Release, and Documentation.

This contract is normative for both current and future agents introduced into the platform.

## 3. Design Principles
All agents must conform to the following principles:

- Configuration-driven: Agent behavior is governed by declarative configuration and contracts, not hidden runtime conventions.
- Deterministic behavior: Given equivalent inputs, policy, and contract versions, agents produce reproducible decisions and outputs.
- Autonomous execution: Agents perform planning, execution, validation, and publication without direct human conversation.
- Contract-first: Artifact, event, state, memory, approval, validation, and quality contracts are binding interfaces.
- Observable: Every meaningful step emits telemetry and events that support diagnostics and governance.
- Auditable: Decisions, transitions, and outputs are attributable, versioned, and retained per policy.
- Reusable: Agent capabilities are composed from reusable skills and shared contracts.
- Extensible: New capabilities and agents can be introduced through metadata and configuration, not orchestration rewrites.
- Local-first: Execution is designed for local control of runtime, data, and policy.
- Human-in-the-loop through Supervisor only: Human approval is mediated exclusively by Supervisor and Approval Service.

## 4. Agent Lifecycle
Every agent must execute the same standard lifecycle:

Initialize -> Read Inputs -> Load Memory -> Plan -> Reason -> Execute Skills -> Generate Artifacts -> Validate -> Self Review -> Publish Artifacts -> Emit Events -> Update Memory -> Complete

Stage definitions:

- Initialize: Agent identity, contract version, configuration, and execution context are resolved and validated before any work starts.
- Read Inputs: Required artifacts, workflow state, events, and approval outcomes are retrieved as references and checked for availability.
- Load Memory: Agent loads workflow, execution, and agent-scoped memory references needed for context continuity.
- Plan: Agent determines stage-conformant objectives, dependencies, and execution order based on inputs and contracts.
- Reason: Agent evaluates constraints, policies, risks, and trade-offs to choose the most compliant path.
- Execute Skills: Agent invokes reusable skills to perform bounded tasks while respecting tool and policy constraints.
- Generate Artifacts: Agent produces owner-scoped artifacts with required metadata and traceability.
- Validate: Agent executes mandatory validation pipeline on inputs, outputs, artifacts, contracts, and quality.
- Self Review: Agent performs internal quality and standards review before publication.
- Publish Artifacts: Agent publishes immutable, versioned artifacts that passed validation gates.
- Emit Events: Agent emits lifecycle, quality, and outcome events for orchestration and observability.
- Update Memory: Agent writes reference-only memory updates for continuity, retries, and auditability.
- Complete: Agent finalizes stage status as Completed, Blocked, Failed, or equivalent contract-valid outcome.

Lifecycle stages are mandatory and cannot be bypassed by implementation shortcuts.

## 5. Mandatory Agent Metadata
Every agent definition must include the following required metadata fields:

- Agent ID: Globally unique identifier used in events, memory, and audit trails.
- Agent Name: Human-readable role name.
- Version: Semantic version of the agent definition contract binding.
- Description: Concise mission and operating boundaries.
- Owner: Organizational or governance owner accountable for the agent definition.
- Supported Workflow Stages: Explicit list of workflow stages the agent may execute.
- Capabilities: Declared functional capabilities provided by the agent.
- Required Skills: Skills that must be available for compliant execution.
- Required Tools: Tools the agent is authorized and expected to invoke.
- Input Artifact Types: Artifact types the agent may consume.
- Output Artifact Types: Artifact types the agent owns and may publish.
- Events Produced: Event types and categories the agent is expected to emit.
- Events Consumed: Event types used as triggers, dependencies, or context.
- Retry Policy: Retry eligibility, limits, and backoff strategy declaration.
- Timeout: Execution timeout limits and timeout handling policy.
- Approval Requirements: Conditions requiring Supervisor-mediated approval.

Metadata must be explicit, complete, and versioned. Missing metadata invalidates the agent definition.

## 6. Inputs
Allowed input categories are:

- Artifacts: Versioned artifact references from upstream agents.
- Workflow State: Current workflow and execution states from orchestration.
- Memory: Workflow, execution, and agent memory references.
- Configuration: Contract versions, stage policies, runtime constraints, and role configuration.
- Events: Relevant consumed events for orchestration context and dependencies.
- Approval Responses: Supervisor-mediated approval outcomes, including conditions.
- Environment Context: Local runtime context and allowed environment metadata.

Input rules:

- Inputs must be validated for existence, version compatibility, integrity, and access rights.
- Inputs are consumed as references and metadata where required by contracts.
- Unsupported input versions must be rejected with contract-compliant failure handling.

## 7. Outputs
Agents may produce only contract-governed outputs:

- Artifacts: Owner-scoped, immutable, versioned deliverables.
- Events: Lifecycle and outcome events aligned with event naming and payload contracts.
- Logs: Structured execution logs supporting traceability and diagnostics.
- Quality Reports: Mandatory quality report for material outputs.
- Validation Reports: Validation outcomes and gate decisions.
- Audit Records: Attributable records of decisions and transitions.
- Memory Updates: Reference-only updates for workflow continuity.

Output rules:

- Outputs must be complete, validated, and attributable to the producing agent.
- Outputs that fail validation must not be published as successful stage results.

## 8. Responsibilities
Every agent is responsible for the following obligations during execution:

- Planning: Create stage-appropriate objective and dependency plan.
- Reasoning: Apply constraints, policies, and contract rules to decisions.
- Execution: Perform role-specific work through declared skills and tools.
- Validation: Enforce mandatory validation gates before publication.
- Publishing: Publish only compliant, versioned artifacts owned by the agent.
- Event Emission: Emit required events for lifecycle and status transitions.
- Memory Updates: Persist reference-only context updates.
- Error Handling: Classify errors correctly and apply retry, block, or fail policies.

Responsibility delegation does not remove accountability from the agent owner.

## 9. Skills
Agents must execute reusable skills rather than embedding all logic within monolithic agent definitions. Skills provide composable behavior units that improve consistency, testability, and extensibility.

Typical skill classes include:

- Read File
- Write File
- Generate Code
- Review
- Validate
- Summarize
- Refactor
- Analyze
- Search

Skill usage rules:

- Skills must be explicitly declared in agent metadata.
- Skill execution must produce traceable outcomes.
- Skill outputs are subject to the same validation and audit controls as agent outputs.

## 10. Tools
Agents invoke tools as governed operational interfaces.

Tool governance requirements:

- Tool Inputs: Inputs must be explicit, validated, and bounded to minimum required scope.
- Tool Outputs: Outputs must be interpreted deterministically and captured in logs/events when relevant.
- Timeouts: Each tool invocation must respect declared timeout policy.
- Errors: Tool errors must be normalized to recoverable or non-recoverable classes.
- Audit Logging: Tool invocations must be logged with who, what, when, why, and result.

Tool invocation must never bypass contract validation, security policy, or ownership rules.

## 11. Memory Usage
Agents use memory to preserve execution continuity and orchestration integrity.

Required memory behaviors:

- Read Memory: Agents must read relevant workflow, execution, and agent memory before planning.
- Write Memory: Agents must write only reference-based updates needed for continuity, retries, and audit.
- Shared Memory: Shared memory is used for cross-agent references and workflow coordination.
- Workflow Memory: Stores workflow-level state pointers, indexes, and approval context.
- Long-term Memory: Stores retained historical references and summaries per retention policy.
- Memory Constraints: Artifacts are never stored directly in memory; memory stores references only.

Memory operations must follow concurrency, retention, cleanup, and versioning rules from memory contract.

## 12. Validation Rules
Every agent must validate:

- Inputs
- Outputs
- Artifacts
- Events
- Contracts
- Quality

Validation obligations:

- Validation occurs before publication and completion events.
- Validation failures trigger retry, block, or fail behavior according to policy.
- Critical guardrail or ownership violations require immediate stop and escalation.
- Validation outcomes must be persisted and linked to quality reporting.

## 13. Self Review
Before publishing outputs, every agent must perform mandatory self-review.

Self-review minimum checks:

- Completeness: Required sections and fields are present.
- Consistency: Internal and cross-artifact consistency is maintained.
- Standards Compliance: Content conforms to platform standards and contracts.
- Missing Sections: Any omissions are identified and resolved.
- Open Questions: Ambiguities and unresolved dependencies are captured explicitly.

Open question structure requirement:

- Open questions must use the platform structured schema with mandatory non-empty fields.
- Required control fields include Blocking, Approval Required, and Workflow Status.
- Workflow Status rule: any Blocking = Yes means REQUIRES HUMAN APPROVAL, else READY.
- Unstructured bullet-only open-question lists are non-compliant.

Self-review is a release gate. Publication without self-review is non-compliant.

## 14. Failure Handling
Agents must classify and handle failures using contract-governed paths:

- Recoverable Errors: Temporary or fixable issues eligible for retry.
- Non-Recoverable Errors: Contract, policy, or integrity violations requiring fail or escalation.
- Retries: Executed only within retry policy limits and eligibility constraints.
- Blocked State: Used when progress is impossible without external resolution.
- Escalation: Routed to Supervisor with blocker reason, impact, and required action.
- Approval Waiting: Entered only through Supervisor-mediated approval flow.

Failure handling must preserve auditability and state transition legality.

## 15. Event Responsibilities
Agents must emit required events for observability and orchestration.

Typical event actions include:

- AgentStarted
- ArtifactCreated
- ValidationPassed
- ValidationFailed
- Blocked
- Completed
- Failed

Event obligations:

- Event names and payloads must conform to event contract.
- Events must include required identifiers, status, timing, confidence, warnings, and errors.
- Events must be emitted at the correct lifecycle boundaries.

## 16. Artifact Responsibilities
Agents must produce versioned artifacts under strict ownership controls.

Artifact obligations:

- Versioning: Semantic versioning must be applied to all artifact updates.
- Ownership: Each artifact type has exactly one owner agent.
- Immutability: Published artifacts are immutable; corrections require a new version.
- Traceability: Outputs must reference source artifacts, requirements, and decisions where applicable.

Artifact-first response requirement:

- Agents must write required stage outputs to owned artifact files before final response completion.
- Agents must not provide full inline deliverables as a substitute for artifact persistence.
- Final response content must be a concise artifact update summary and handoff metadata.
- If persistence fails, agents must report failure and mark execution as not-ready.

Agents must never overwrite artifacts owned by another agent.

## 17. Human Interaction Policy
Human interaction is strictly controlled:

- Agents never interact directly with humans.
- Only Supervisor creates and manages approval requests.
- Agents emit Blocked events when human decision is required.
- Agents create open-question outputs or references to capture unresolved ambiguity.
- Supervisor resumes execution after approved decision and policy checks.

Supervisor continuation compatibility requirement:

- Supervisor must determine continuation using only structured fields: Blocking, Approval Required, and Workflow Status.
- Supervisor and agents must not infer criticality from free-form open-question prose.

Any direct human-agent interaction path is non-compliant.

## 18. Security Requirements
Every agent must satisfy baseline security requirements:

- Least privilege: Access only required artifacts, tools, and memory scopes.
- No hidden state: Decisions must not depend on untracked or opaque state.
- Audit logging: Security-relevant actions are fully logged and attributable.
- Deterministic execution: Security controls must not rely on undefined behavior.
- Input validation: All consumed data is validated before use.
- Output validation: All produced outputs are validated before publication.

Security violations are handled as high-severity failures.

## 19. Observability
Agents must emit observability signals sufficient for governance and operations.

Minimum observable dimensions:

- Metrics
- Execution Time
- Retries
- Failures
- Validation Score
- Artifact Count
- Events
- Memory Usage

Observability data must support root-cause analysis, trend tracking, and compliance reporting.

## 20. Compliance Rules
Every agent must comply with the following platform contracts:

- Artifact Contract
- Event Contract
- Workflow State Contract
- Memory Contract
- Approval Contract
- Validation Contract
- Quality Report Contract

Compliance is mandatory for execution eligibility. Non-compliant agents must not be scheduled for production workflows.

## 21. Example Agent Definition
This section provides a complete contract-conformant example for Backend Developer Agent.

Backend Developer Agent definition:

- Agent ID: backend-developer
- Agent Name: Backend Developer
- Version: 1.0.0
- Description: Produces backend service specifications and implementation-facing backend artifacts aligned with architecture, API contracts, database schema, and business rules.
- Owner: Platform Engineering
- Supported Workflow Stages: Backend Development
- Capabilities: Domain service design, integration flow definition, backend behavior specification, error strategy definition, observability requirement definition.
- Required Skills: Analyze, Read File, Write File, Generate Code, Validate, Summarize, Review, Refactor, Search.
- Required Tools: Filesystem access, contract lookup, validation tooling, event emission interface, memory update interface.
- Input Artifact Types: requirements.md, business-rules.md, features.md, user-stories.md, acceptance-criteria.md, gherkin.md, architecture.md, api-contracts.md, database-schema.md, frontend-spec.md.
- Output Artifact Types: backend-spec.md, quality-report.md for backend stage outputs, validation report reference.
- Events Produced: AgentStarted, ArtifactCreated, ValidationPassed, ValidationFailed, Blocked, Completed, Failed, Retry events when applicable.
- Events Consumed: ArchitectureCompleted, DatabaseCompleted where applicable, approval decision events, relevant lifecycle events.
- Retry Policy: Retry recoverable validation and transient dependency failures up to configured limit; stop on guardrail-critical and ownership violations.
- Timeout: Must complete stage operations within configured execution timeout; timeout triggers retry or block based on policy.
- Approval Requirements: Requires Supervisor-mediated approval for policy exceptions, unresolved high-impact open questions, and low-confidence outcomes.

Behavioral obligations of Backend Developer Agent:

- Reads upstream artifacts and validates compatibility and traceability.
- Produces backend-spec.md as owner-scoped immutable artifact with semantic versioning.
- Generates mandatory quality and validation outcomes before publication.
- Emits lifecycle and status events at required checkpoints.
- Updates memory with reference-only records, including artifact references and retry metadata.
- Enters Blocked state and escalates to Supervisor for unresolved policy conflicts.

This example is normative in structure and illustrative in stage specialization.

## 22. Future Extensions
The contract is designed to allow new agents to be added without changing orchestration logic.

Extension model:

- New agents inherit this contract and declare role-specific metadata, inputs, outputs, skills, tools, and events.
- Orchestration behavior remains stable because execution semantics are contract-driven.
- New capabilities are introduced through configuration and skill composition, not hardcoded workflow branching.
- Backward compatibility is preserved by semantic versioning and explicit contract compatibility rules.

As the platform evolves, additional agent types can be integrated by conforming to this contract and existing cross-contract interfaces, preserving deterministic execution, governance, and interoperability across the full agent ecosystem.
