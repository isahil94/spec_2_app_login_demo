# Developer Guide

Document Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved

## 1. Purpose
This guide is the official onboarding and extension reference for contributors working on the Agentic SDLC platform.

Its goals are:

1. Help new contributors become productive quickly.
2. Explain the platform mental model and subsystem responsibilities.
3. Provide clear extension paths for agents, prompts, skills, workflows, and tools.
4. Standardize contribution quality, testing, and governance expectations.
5. Enable platform evolution without changing the orchestration engine.

This guide is architecture and contribution focused, not implementation focused.

## 2. Getting Started

### 2.1 Repository overview
The repository is organized around four areas:

1. Platform intelligence in ai for agents, prompts, skills, contracts, and governance.
2. Runtime services in orchestration for execution and subsystem coordination.
3. Outputs in artifacts and apps for generated deliverables and runnable applications.
4. Operational support in configs, scripts, tests, docs, and observability assets.

### 2.2 Prerequisites
Before contributing, ensure you have:

1. Local development capability for the project runtime stack.
2. Access to project dependencies listed in project setup and requirements files.
3. Familiarity with Markdown-first agent definitions and contract-driven design.
4. Familiarity with local-first execution constraints and Supervisor-mediated approvals.

### 2.3 Development environment
Recommended environment setup flow:

1. Review platform architecture and execution references first.
2. Use setup scripts and local configuration to initialize dependencies.
3. Verify baseline tests and run scripts execute successfully.
4. Confirm artifact and observability output paths are available for diagnostics.

### 2.4 Project layout
Start by reading these documents in order:

1. [docs/architecture.md](docs/architecture.md)
2. [docs/execution-flow.md](docs/execution-flow.md)
3. [docs/project-structure.md](docs/project-structure.md)

Then read subsystem references under orchestration and contract references under ai/contracts.

## 3. Platform Concepts
The platform is contract-first and subsystem-driven. Contributors should understand these core concepts and interactions.

1. Agents
Role-specialized autonomous contributors that consume and produce contract-governed artifacts.

2. Workflows
Ordered execution plans that govern stage progression, dependencies, and completion criteria.

3. Artifacts
Versioned, owner-scoped deliverables that serve as the source of truth for stage outputs.

4. Events
Coordination signals used for lifecycle updates, state transitions, and cross-service communication.

5. Memory
Context layer storing references, history, and execution continuity information.

6. Validation
Mandatory correctness gate before stage progression and publication.

7. Approvals
Human-in-the-loop control points mediated only by Supervisor through Approval Service.

8. Supervisor
Central orchestration authority that decides progression, pause and resume behavior, retries, and terminal states.

9. Runtime
Single local runtime where all subsystem services coordinate workflow execution.

Interaction model summary:

1. Workflows drive stage order.
2. Agents produce artifacts and events.
3. Validation gates progression.
4. Memory preserves context.
5. Approvals resolve blocked decisions.
6. Supervisor remains final control authority.

## 4. Creating a New Agent
A new agent is added as a contract-conformant role extension, not as an orchestration engine modification.

### 4.1 Location
Store agent definitions under ai/agents.

### 4.2 Required metadata
Agent definition must include at minimum:

1. Agent identity and version.
2. Role and mission.
3. Supported workflow stages.
4. Inputs and outputs.
5. Required skills and tools.
6. Events produced and consumed.
7. Retry, timeout, and approval behavior.

### 4.3 Responsibilities
Define explicit bounded responsibilities. Avoid overlap with existing agent ownership unless intentionally refactoring ownership boundaries.

### 4.4 Inputs and outputs
Declare:

1. Artifact types consumed.
2. Artifact types produced.
3. Required memory scopes.
4. Required event dependencies.

### 4.5 Skills
Declare reusable skills rather than embedding large, role-specific procedural logic.

### 4.6 Expected artifacts
Ensure each produced artifact has one owner and aligns with artifact contract envelope and lifecycle rules.

### 4.7 Validation requirements
Document required validation categories and thresholds for the agent outputs.

### 4.8 Approval behavior
Define when the agent must emit blocked or approval-related events and what supporting artifacts must be published.

### 4.9 Testing considerations
Add or update tests that validate:

1. Metadata correctness.
2. Input and output contract conformance.
3. Validation and blocked-path behavior.
4. Event emission expectations.

### 4.10 Documentation requirements
Update architecture and workflow documentation where agent stage impact exists.

## 5. Creating a New Prompt
Prompts are reusable platform assets and must be structured for consistency and maintainability.

### 5.1 Prompt organization
Use existing prompt domains under ai/prompts, including shared, standards, system, and templates.

### 5.2 Naming conventions
Use clear domain and intent-oriented names that indicate owner role and purpose.

### 5.3 Variable usage
Use explicit variables and deterministic placeholders for context injection. Avoid ambiguous dynamic references.

### 5.4 Reuse
Favor shared prompt fragments where common constraints or formatting rules already exist.

### 5.5 Prompt validation
Validate prompt structure against expected context dependencies and contract language.

### 5.6 Versioning
Prompt changes should be tracked with change rationale and impact notes, especially when affecting output structure.

## 6. Creating a New Skill
Skills are reusable capability units shared across agents.

### 6.1 Purpose
Define one clear purpose per skill and avoid blending unrelated concerns.

### 6.2 Reuse
Design skill inputs and outputs so multiple agents can consume them without role-specific coupling.

### 6.3 Composition
Build skills to compose with other skills through clear boundaries and deterministic outputs.

### 6.4 Dependencies
Document required dependencies, constraints, and compatible runtime contexts.

### 6.5 Testing
Validate skill correctness under nominal, edge, and failure conditions.

### 6.6 Documentation
Document capability, inputs, outputs, assumptions, and known limitations.

## 7. Creating a New Workflow
Workflows define stage execution plans and governance boundaries.

### 7.1 Workflow definition
Add new workflow definitions in configuration and document purpose, scope, and expected outputs.

### 7.2 Stages
Define stage order and ownership with explicit role mapping.

### 7.3 Dependencies
Declare hard and soft dependencies across stages and artifacts.

### 7.4 Parallel execution
Allow parallel stages only when dependencies and ownership constraints are safe.

### 7.5 Approvals
Define approval points for high-risk, policy-sensitive, or ambiguous transitions.

### 7.6 Validation
Map validation gates to stage entry and exit criteria.

### 7.7 Completion criteria
Define clear terminal completion criteria for artifacts, quality, approvals, and run readiness.

## 8. Creating a New Tool
Tools are platform interfaces used by agents and runtime services.

### 8.1 Purpose
Define the operational need and scope boundaries of the new tool.

### 8.2 Registration
Register tools through approved runtime and configuration pathways.

### 8.3 Inputs and outputs
Define strict input and output expectations with validation and traceability considerations.

### 8.4 Error handling
Classify errors into recoverable and non-recoverable outcomes and define retry guidance.

### 8.5 Security
Apply least privilege and explicit authorization boundaries.

### 8.6 Logging
Emit structured operational logs for usage, failures, and decision context.

### 8.7 Testing
Add tests for compatibility, safety boundaries, and workflow impact.

## 9. Configuration
Configuration is the primary control surface for platform behavior.

### 9.1 Platform configuration
Use global settings for default policies and system-wide controls.

### 9.2 Workflow configuration
Define stage order, dependency logic, retry policies, and completion criteria.

### 9.3 Agent configuration
Control agent enablement, role mappings, and capability constraints.

### 9.4 Runtime configuration
Define runtime-level controls for scheduling, service behavior, and operational thresholds.

### 9.5 Environment configuration
Manage environment-specific values without hardcoding them into core logic.

### 9.6 Best practices

1. Keep configuration explicit and documented.
2. Version and review configuration changes.
3. Validate configuration before execution.
4. Avoid hidden defaults for critical behavior.

## 10. Testing
Testing is required for all extension work.

1. Unit testing
Validate isolated logic and deterministic outcomes.

2. Integration testing
Validate subsystem interactions and data flow boundaries.

3. Workflow testing
Validate stage progression, dependencies, and completion behavior.

4. Agent testing
Validate role-specific contract conformance and outputs.

5. End-to-end testing
Validate full workflow behavior from input to final outputs.

6. Regression testing
Protect previously validated behavior from unintended breakage.

## 11. Debugging
Use observability and subsystem evidence to diagnose issues.

1. Logs
Inspect execution, agent, service, and error logs.

2. Metrics
Inspect pass rates, latencies, queue depth, and failure rates.

3. Tracing
Follow correlated execution paths across services and events.

4. Workflow inspection
Inspect stage states, transitions, blocked points, and retries.

5. Memory inspection
Inspect workflow memory, shared context, and execution history.

6. Artifact inspection
Inspect ownership, version lineage, dependencies, and publication status.

7. Validation reports
Inspect validation failures, severities, and remediation recommendations.

## 12. Best Practices
Contributors should follow these platform practices.

1. Modularity
Keep responsibilities bounded by subsystem and role.

2. Reusability
Prefer shared prompts, skills, and patterns before introducing duplicates.

3. Consistency
Use contract terminology and established naming conventions.

4. Naming
Use clear, role-specific names for agents, artifacts, events, and workflow stages.

5. Documentation
Document every new capability, behavior change, and extension point.

6. Versioning
Apply semantic versioning expectations to contracts, artifacts, and major behavior changes.

7. Performance
Avoid changes that increase runtime cost without measurable benefit.

8. Security
Treat authorization, integrity, and auditability as mandatory requirements.

## 13. Common Mistakes
Common design and contribution mistakes to avoid:

1. Adding direct agent-to-human interaction paths.
2. Bypassing Supervisor for approval-required decisions.
3. Publishing artifacts without validation evidence.
4. Reusing artifact types without clear ownership rules.
5. Introducing workflow changes without updating dependencies and completion criteria.
6. Embedding configuration as hardcoded behavior.
7. Ignoring observability updates when adding new runtime paths.
8. Adding new features without contract or documentation updates.

## 14. Contribution Guidelines
All contributions must meet project standards before merge.

1. Coding standards
Follow repository conventions and keep changes scoped and reviewable.

2. Documentation standards
Update architecture, subsystem, and guide documentation when behavior or responsibilities change.

3. Review process
All contributions require peer review focused on contracts, governance, and operational impact.

4. Testing requirements
Required tests must pass, and new behavior must include adequate coverage.

5. Pull request expectations
Each pull request should include:

1. Clear scope and motivation.
2. Impacted subsystems and contracts.
3. Testing evidence.
4. Documentation updates.
5. Rollback or mitigation considerations when relevant.

## 15. Example Extension
This section walks through adding a new Security Review Agent.

### 15.1 Define role and scope
Create a new agent definition under ai/agents for Security Review Agent with a clear mission: evaluate security posture and policy compliance before release progression.

### 15.2 Declare metadata and contract alignment
Define required metadata, supported stage, consumed artifacts, produced artifacts, events, validation expectations, and approval behavior consistent with the agent contract.

### 15.3 Define inputs and outputs
Inputs might include architecture artifacts, backend outputs, database schema, QA outputs, and review artifacts. Outputs should include security review report artifacts and risk recommendations.

### 15.4 Add or reuse skills
Map existing review and validation skills where possible. Add new security-specific skills only when no reusable equivalent exists.

### 15.5 Update workflow configuration
Insert Security Review stage into workflow configuration at the intended governance point, typically before final release readiness.

### 15.6 Update dependencies and validation gates
Add explicit dependencies so the stage unlocks only when required technical and quality artifacts are published. Add security validation gates and severity policy mapping.

### 15.7 Define event behavior
Ensure the agent emits lifecycle, validation, blocked, and completion events with proper correlation.

### 15.8 Define approval behavior
If high-risk findings require human acceptance, configure blocked and approval request behavior through Supervisor-mediated flow.

### 15.9 Add tests
Add unit, integration, and workflow tests verifying:

1. Stage insertion behavior.
2. Dependency enforcement.
3. Artifact outputs.
4. Validation outcomes.
5. Approval-trigger behavior.

### 15.10 Update documentation
Update relevant architecture and execution docs to include the new stage, artifacts, and governance impact.

### 15.11 Validate end-to-end behavior
Run full workflow test to verify the Security Review Agent integrates without changing orchestration engine code paths.

## 16. Future Extensions
The platform supports controlled extension without core orchestration rewrites.

1. Plugin architecture
Introduce plugin-style capabilities for tools, skills, and validation rule packs.

2. Custom workflows
Add domain-specific stage sequences using configuration and contracts.

3. Additional agent types
Add specialized agents for compliance, security, performance, or domain intelligence.

4. New LLM providers
Extend model provider support through configuration and model abstraction boundaries.

5. Community contributions
Enable external contributors through clear contracts, templates, testing guidance, and review standards.

Extension growth should always preserve local-first execution, single-runtime governance, contract-first interoperability, and Supervisor-controlled decision boundaries.
