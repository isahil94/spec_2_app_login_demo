# Agentic SDLC Platform Architecture

Document Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved

## 1. Executive Summary
This document defines the target architecture for a local-first, enterprise-grade Agentic SDLC platform that transforms a software specification and optional Figma input into a running application through an autonomous, contract-governed workflow.

The platform is designed as a single runtime system with configuration-driven behavior, markdown-defined agents, artifact-driven handoffs, and event-driven orchestration. Human involvement is strictly mediated through Supervisor-controlled approvals. The architecture prioritizes deterministic execution, traceability, governance, and operational simplicity by intentionally excluding distributed control planes and orchestration complexity.

This document is the definitive architecture reference for runtime behavior, subsystem boundaries, contract alignment, lifecycle flow, and extension strategy.

## 2. Goals
The platform goals are:

1. Execute end-to-end SDLC autonomously from specification intake to local build and run.
2. Enforce contract-first interoperability across agents, orchestration, memory, validation, approval, and quality gates.
3. Preserve deterministic and reproducible execution under equivalent inputs and configuration.
4. Keep runtime local-first and single-process oriented for control, portability, and reduced operational overhead.
5. Ensure complete auditability through artifacts, structured events, memory references, and quality reporting.
6. Support safe human decision points only through Supervisor-managed approval flow.
7. Enable role specialization through markdown-defined agent definitions and reusable skills.
8. Provide enterprise governance through validation, policy guardrails, and observability.

## 3. Non Goals
The platform explicitly excludes:

1. Distributed multi-runtime orchestration across nodes or regions.
2. Container-orchestrated deployment models such as Docker and Kubernetes.
3. Agent-to-agent direct coordination protocols outside Supervisor-governed orchestration.
4. Free-form conversational coordination as a control mechanism.
5. Hidden or implicit state transitions not represented through contracts, memory, and events.
6. Non-deterministic workflow mutation outside versioned configuration and governed approvals.
7. Runtime assumptions tied to a specific cloud provider.

## 4. Design Principles
The architecture follows these governing principles:

1. Local-first: Runtime control, policy enforcement, artifacts, and execution state are managed locally.
2. Single runtime: One orchestration runtime governs workflow state, agent execution, memory updates, and event publication.
3. Configuration-driven: Workflow behavior, policies, and agent capabilities are declared through configuration and contracts.
4. Contract-first: Subsystem interactions are governed by explicit contracts before implementation choices.
5. Autonomous execution: Agents complete lifecycle responsibilities without direct human interaction.
6. Supervisor-mediated human control: Human decisions enter the system only through approval contracts managed by Supervisor.
7. Artifact-driven communication: Durable artifacts and references are the primary medium of cross-agent collaboration.
8. Event-driven lifecycle: State changes and significant actions are represented as typed events.
9. Deterministic governance: Validation, quality, and transition rules are applied consistently across runs.
10. Extensible by composition: New roles and capabilities are added through metadata, skills, and contracts without redesigning core orchestration.

## 5. High Level Architecture
The platform is organized into tightly scoped subsystems with explicit responsibilities.

### 5.1 Supervisor Subsystem
Supervisor is the authoritative control layer. It initializes workflows, enforces transition legality, coordinates stage progression, routes blocked conditions into approval flow, and closes workflows in terminal states. Supervisor never delegates governance decisions to downstream agents.

### 5.2 Orchestration Subsystem
The orchestration subsystem executes workflow plans, schedules agent stages according to pipeline order, applies retry and timeout policy, and persists transition context. It binds runtime execution to contract constraints and guarantees lifecycle integrity.

### 5.3 Agent Execution Subsystem
This subsystem runs specialized SDLC agents as contract-conformant workers. Every agent executes a standardized lifecycle, consumes governed inputs, produces owner-scoped artifacts, validates outputs, emits events, and updates memory references.

### 5.4 Artifact Subsystem
The artifact subsystem provides durable, versioned outputs and strict ownership enforcement. Artifacts are immutable after publication and serve as the canonical communication channel across pipeline stages.

### 5.5 Event Bus Subsystem
The event subsystem publishes lifecycle, success, blocked, failure, retry, approval, and memory events. It provides ordered workflow context, enables observability, and supports deterministic replay and audit trails.

### 5.6 Memory Subsystem
The memory subsystem maintains workflow, execution, and agent-scoped references. It stores only references and metadata, never full artifacts. It supports recovery, retries, approvals, and historical traceability.

### 5.7 Validation and Quality Subsystem
This subsystem enforces contract, schema, business, traceability, and guardrail checks. It is responsible for accepting or rejecting outputs, producing validation summaries, and creating quality reports for stage readiness decisions.

### 5.8 Approval Subsystem
The approval subsystem handles all human-in-the-loop decisions through Supervisor-mediated requests and responses. It ensures blocked or policy-sensitive scenarios are resolved without violating autonomous agent boundaries.

### 5.9 Observability and Audit Subsystem
This subsystem captures structured logs, metrics, traces, event streams, and decision records. It enables operational diagnostics, governance reporting, and compliance verification.

### 5.10 Tools and Skills Subsystem
Skills provide reusable capability units and tools provide controlled execution interfaces. Together they standardize how agents perform work while preserving traceability and policy enforcement.

### 5.11 Configuration Subsystem
Configuration defines model selection, workflow sequencing, policy thresholds, and runtime behavior. It separates control intent from execution logic and allows predictable platform tuning.

## 6. Directory Structure
The repository structure maps directly to architectural responsibilities.

1. [ai/agents](ai/agents): Markdown agent definitions for role mission, scope, responsibilities, and lifecycle constraints.
2. [ai/contracts](ai/contracts): Platform contracts for agent, artifact, event, workflow state, memory, approval, validation, and quality behaviors.
3. [ai/governance](ai/governance): Governance policies, approval boundaries, and role access constraints.
4. [ai/guardrails](ai/guardrails): Input, output, and security guardrail definitions used by validation gates.
5. [ai/hooks](ai/hooks): Lifecycle hook specifications for build, test, commit, and deploy control points.
6. [ai/instructions](ai/instructions): Domain instructions for architecture, coding, testing, review, and documentation behavior.
7. [ai/prompts](ai/prompts): Shared and role-specific prompt assets and standards.
8. [ai/skills](ai/skills): Reusable skill definitions invoked by agents for bounded operations.
9. [orchestration](orchestration): Workflow engine, supervisor logic, agent runner, and state manager components.
10. [events](events): Event types, bus integration, and subscriber coordination.
11. [memory](memory): Workflow, shared, and artifact memory management logic.
12. [observability](observability): Logging, metrics, and tracing utilities.
13. [tools](tools): Controlled tool interfaces for filesystem, browser, terminal, database, git, figma, and model interaction.
14. [artifacts](artifacts): Persisted stage outputs grouped by architecture, backend, database, frontend, documentation, tests, and related domains.
15. [configs](configs): Configuration files controlling agents, models, workflow, and global settings.
16. [docs](docs): Authoritative documentation including this architecture reference.
17. [templates](templates): Specification templates for blank and task management bootstrap scenarios.
18. [scripts](scripts): Local setup, build, run, and test automation scripts.
19. [tests](tests): Testing guidance and validation assets for platform verification.
20. [apps](apps): Generated or target application outputs managed by the pipeline.
21. [audit](audit): Audit-related documentation and retained governance records.

## 7. Runtime Architecture
Runtime execution is centered around a single orchestration process that coordinates all subsystems.

Runtime flow:

1. Supervisor initializes workflow context from specification input and optional Figma reference.
2. Workflow engine creates execution plan according to configured pipeline and contract constraints.
3. Agent runner executes each stage with lifecycle compliance and state checks.
4. Validation and quality gates evaluate outputs before publication.
5. Events are emitted at lifecycle boundaries and persisted for traceability.
6. Memory references are updated for continuity, retries, and recovery.
7. Approval flow is triggered only by Supervisor when required.
8. Workflow terminates in Completed, Failed, or Cancelled with full audit context.

Runtime characteristics:

1. Deterministic transition control by state contract.
2. At-least-once event publication with idempotent consumption.
3. Immutable artifact publication with semantic versioning.
4. Recovery through retry and resume from persisted state and memory references.

## 8. Agent Architecture
Agents are role-specialized autonomous workers that inherit the common agent contract.

Agent model:

1. Identity: Each agent has stable metadata, capabilities, required tools, and approved input and output types.
2. Lifecycle: Every stage follows initialize, plan, execute, validate, self-review, publish, emit, and complete responsibilities.
3. Isolation: Agents operate within declared scope and least-privilege access boundaries.
4. Ownership: Each artifact type has exactly one owner agent.
5. Governance: Agents cannot bypass validation, quality, or approval policy gates.

Role-specific specialization:

1. Business Analyst defines requirements and acceptance structures.
2. Solution Architect defines architecture and interface contracts.
3. UI and backend and database agents create role-owned technical specifications.
4. QA and Reviewer enforce quality and policy confidence.
5. Documentation and DevOps and Release finalize operational readiness and local execution outcome.

## 9. Workflow Architecture
The default workflow pipeline is sequential and deterministic:

1. Specification and optional Figma input
2. Supervisor
3. Business Analyst
4. Solution Architect
5. UI and UX Developer
6. Backend Developer
7. Database Developer
8. QA Engineer
9. Reviewer
10. Documentation
11. DevOps and Release
12. Local Build and Run

Workflow control model:

1. State transitions are governed by workflow-state contract rules.
2. Stage entry requires required inputs and prior completion criteria.
3. Retry and timeout policy applies per stage.
4. Blocked states are resolved through Supervisor and approval flow.
5. Completion requires validated artifacts, quality status, and event confirmation.

## 10. Event Architecture
Events provide runtime coordination, visibility, and auditability.

Event categories:

1. Lifecycle events for state changes and stage boundaries.
2. Success events for completed stage outcomes.
3. Blocked events for unresolved dependencies or policy constraints.
4. Failure events for terminal or non-recoverable errors.
5. Retry events for controlled re-execution attempts.
6. Approval events for request, decision, timeout, escalation, and resume.
7. Memory events for significant memory updates and maintenance actions.

Event requirements:

1. Required identifiers include workflow and execution and emitting agent context.
2. Status, duration, confidence, warnings, and errors are standardized fields.
3. Events reference artifacts and memory entries rather than embedding content.
4. Consumers apply idempotency and ordering rules by workflow and execution keys.

## 11. Artifact Architecture
Artifacts are the canonical cross-stage communication unit.

Artifact model:

1. Single owner per artifact type.
2. Immutable after publication.
3. Semantic versioning for controlled evolution.
4. Required metadata envelope for traceability and integrity.
5. Input references linking outputs to upstream dependencies.

Artifact lifecycle:

1. Draft
2. Validated
3. Published
4. Deprecated when superseded
5. Archived by policy

Artifact governance:

1. Non-owner mutation is prohibited.
2. Ownership and schema violations are high-severity failures.
3. Quality and validation references are required for publication readiness.

## 12. Memory Architecture
Memory supports continuity without duplicating artifact content.

Memory domains:

1. Workflow memory for state pointers, indexes, approvals, and event references.
2. Execution memory for attempt-scoped context, retries, and timeout metadata.
3. Agent memory for stage-scoped inputs, outputs, and validation references.

Memory constraints:

1. Reference-only storage, no embedded artifacts.
2. Append-oriented, versioned mutation model for auditability.
3. Concurrency control for state-critical keys.
4. Retention and cleanup rules aligned to governance and audit policy.

## 13. Validation Architecture
Validation is a mandatory gate before publication and stage completion.

Validation layers:

1. Input validation
2. Output validation
3. Artifact validation
4. Business validation
5. Schema validation
6. Traceability validation
7. Quality validation
8. Guardrail validation

Validation outcomes:

1. Pass allows progression.
2. Warning allows conditional progression by policy.
3. Fail triggers retry, block, or fail transition depending on severity and recoverability.

Supervisor enforces that no stage reports completion without required validation outcomes.

## 14. Approval Architecture
Approval architecture enforces controlled human intervention.

Approval flow:

1. Agent encounters blocking or policy-sensitive condition.
2. Agent emits blocked event and structured open-question context.
3. Supervisor creates approval request.
4. Approval service routes decision task to dashboard or CLI.
5. Human decision is recorded with rationale and conditions.
6. Supervisor applies decision and resumes, fails, or escalates workflow.

Approval guarantees:

1. No direct agent-to-human interaction.
2. Full auditability of request, decision, conditions, and resulting transitions.
3. Timeout and escalation paths for unresolved approvals.

## 15. Observability
Observability provides runtime transparency and governance confidence.

Core telemetry dimensions:

1. Execution time by workflow, stage, and agent.
2. Retry counts and retry outcomes.
3. Failure rates and failure categories.
4. Validation scores and gate outcomes.
5. Artifact production volume and version churn.
6. Event emission and processing health.
7. Memory usage and mutation frequency.

Operational outcomes:

1. Faster root-cause analysis.
2. Trend-based quality and policy monitoring.
3. Compliance evidence generation from structured runtime records.

## 16. Error Handling
Error handling is policy-driven and contract-aware.

Error classes:

1. Recoverable errors, including transient dependencies and deterministic correction opportunities.
2. Non-recoverable errors, including ownership violations, contract incompatibility, and critical guardrail failures.

Handling strategy:

1. Normalize error category and severity.
2. Persist error context with references.
3. Emit corresponding failure, blocked, or retry event.
4. Apply retry policy where eligible.
5. Escalate to approval path when decision authority is required.
6. Transition to failed terminal state on retry exhaustion or hard-fail conditions.

## 17. Security
Security controls are integrated into runtime governance.

Security requirements:

1. Least privilege access for tools, artifacts, and memory scopes.
2. Input and output validation before any publish or state progression.
3. Deterministic execution with no hidden state dependencies.
4. Structured audit logs for all security-relevant actions.
5. Integrity checks for artifact and reference consistency.
6. Policy-based rejection of unauthorized operations.

Security posture focuses on preventing unauthorized mutation, preserving traceability, and enforcing governance boundaries.

## 18. Extensibility
The architecture supports growth without destabilizing orchestration.

Extension mechanisms:

1. Add new agents through markdown definitions that inherit the agent contract.
2. Add new skills as reusable capability units.
3. Extend contract-compatible artifact types and event actions through versioned evolution.
4. Introduce new policy controls through configuration and validation rules.

Extensibility boundaries:

1. Core workflow state and approval governance remains Supervisor-controlled.
2. Contract-breaking changes require major version increments and explicit compatibility planning.

## 19. Technology Stack
This architecture is intentionally implementation-independent while constraining runtime style.

Stack characteristics:

1. Local runtime execution environment.
2. Markdown-defined agent and contract assets.
3. Configuration files for models, workflow, and settings.
4. Structured event, memory, and artifact persistence within local platform boundaries.
5. Scripted local build, run, and test operations.

Excluded stack elements:

1. Docker.
2. Kubernetes.
3. Distributed agent mesh.
4. Externalized multi-runtime control planes.

## 20. Example Execution
This section describes one complete autonomous SDLC run from specification intake to local build and run.

1. Intake
Supervisor receives specification and optional Figma URL, validates baseline inputs, creates workflow and execution context, and emits workflow creation lifecycle event.

2. Requirements Phase
Business Analyst consumes specification artifacts and produces requirements, business rules, epics, features, user stories, acceptance criteria, and gherkin outputs. Validation and quality reports are generated. Success events are emitted.

3. Architecture Phase
Solution Architect consumes requirements outputs and produces architecture and interface contract artifacts. Validation gates confirm schema, traceability, and business alignment. Publication triggers architecture completion events.

4. Design and Implementation Specification Phase
UI and UX Developer, Backend Developer, and Database Developer each produce owner-scoped specifications aligned to architecture and requirements contracts. Each stage publishes artifacts, validation outcomes, and quality reports, with events and memory references updated.

5. Quality Assurance Phase
QA Engineer consumes upstream artifacts, produces qa report outputs, and emits quality gate decisions. Failures or ambiguities produce blocked or failure events according to policy.

6. Review Phase
Reviewer performs governance and quality assessment, produces review report artifact, and issues readiness decision context.

7. Documentation Phase
Documentation agent generates final readme and operational documentation outputs with traceability to prior artifacts and decisions.

8. Release Preparation Phase
DevOps and Release produces release notes, deployment and rollback context, and local execution readiness guidance.

9. Approval and Exceptions
If any stage is blocked or requires policy exception, Supervisor creates approval request. Human decision through dashboard or CLI is recorded, then Supervisor resumes, fails, or escalates.

10. Local Build and Run
Workflow reaches release-ready state, local build and run sequence executes, and final completion event and audit records are published.

11. Closure
Supervisor transitions workflow to terminal state, archives references per retention policy, and finalizes execution summary.

## 21. Future Enhancements
Planned architectural enhancement directions include:

1. Contract compatibility matrix and automated compatibility validation across versions.
2. Richer policy packs for domain-specific compliance profiles.
3. Expanded observability dashboards for stage-level and contract-level health trends.
4. Advanced recovery strategies with policy-governed partial rerun scopes.
5. Enhanced template catalog for broader application archetypes beyond default task management.
6. Stronger automated traceability analysis linking requirements to final deliverables.
7. Optional parallelization of eligible stages under explicit contract and dependency controls.

These enhancements preserve the existing architectural core: local-first operation, single runtime governance, contract-first interoperability, and Supervisor-mediated human oversight.
