# Project Structure Reference

Document Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved

## 1. Purpose
This document explains how the repository is organized into well-defined modules so architects and developers can quickly understand ownership boundaries, execution flow, and extension points.

A modular structure is essential for this platform because:

1. Autonomous SDLC execution spans many concerns, including orchestration, contracts, artifacts, memory, validation, and approvals.
2. Subsystems must evolve independently without creating cross-cutting coupling.
3. New agents, workflows, and services must be added predictably using stable directory conventions.
4. Onboarding requires a clear mental model from architecture through runtime execution.

## 2. Repository Overview
The repository is organized around AI definitions, orchestration services, runtime outputs, and operational support assets.

Complete directory tree, major folders and key files:

```text
Specs_to_APP/
  .github/
  ai/
    agents/
    contracts/
    governance/
    guardrails/
    hooks/
    instructions/
    prompts/
      shared/
      standards/
      system/
      templates/
    skills/
  apps/
  artifacts/
    architecture/
    backend/
    database/
    design/
    documentation/
    frontend/
    planning/
    requirements/
    tests/
  audit/
  configs/
    agents.yaml
    models.yaml
    settings.yaml
    workflow.yaml
  docs/
    api.md
    architecture.md
    execution-flow.md
    project-structure.md
    setup.md
  events/
  memory/
  observability/
  orchestration/
    approval/
    artifact/
    event-bus/
    memory/
    observability/
    supervisor/
    validation/
    workflow/
    agent_runner.py
    planner_executor.py
    supervisor.py
    task_manager.py
    workflow_engine.py
    workflow_state.py
  scripts/
    build.ps1
    run.ps1
    setup.ps1
    test.ps1
  templates/
    blank/
    task-management/
  tests/
    README.md
  tools/
  .env.example
  .gitignore
  README.md
  main.py
  pyproject.toml
  requirements.txt
```

Notes on requested logical folders:

1. contracts directory: implemented in this repository as ai/contracts.
2. logs directory: treated as runtime-generated operational output and can be introduced as logs when persistent local log storage is enabled.

## 3. AI Directory
The ai directory contains model-facing platform intelligence and agent definitions.

1. ai/agents
Defines role-specific agent behavior in Markdown, including mission, responsibilities, and lifecycle expectations.

2. ai/prompts
Holds reusable prompt assets used across system, standards, and templates.

3. ai/skills
Defines reusable capability modules that agents invoke to perform bounded tasks.

4. ai/instructions
Holds domain and execution instructions that standardize architecture, coding, testing, and review behavior.

5. ai/hooks
Defines lifecycle hook behavior around build, test, commit, and deploy checkpoints.

6. ai/prompts/templates
Template prompt structures for planning and domain output generation.

7. ai/prompts/shared
Shared prompt fragments and constraints used across multiple agents and workflows.

Additional supporting AI folders:

1. ai/contracts for platform contract specifications.
2. ai/governance for policy and approval governance controls.
3. ai/guardrails for validation and safety boundary definitions.

## 4. Orchestration Directory
The orchestration directory contains runtime control services and execution coordinators.

1. orchestration/supervisor
Central orchestration authority for workflow decisions, approval mediation, and terminal state control.

2. orchestration/workflow
Workflow Engine architecture and execution coordination logic for stage sequencing, dependencies, and transitions.

3. orchestration/runtime
Runtime subsystem documentation and orchestration runtime concerns.

4. orchestration/memory
Memory Service architecture for context storage, retrieval, history, and recovery support.

5. orchestration/artifact
Artifact Manager architecture for artifact lifecycle, versioning, publishing, and discovery.

6. orchestration/validation
Validation Engine architecture for contract and policy conformance gates.

7. orchestration/approval
Approval Service architecture for Supervisor-mediated human decision lifecycle.

8. orchestration/observability
Observability subsystem architecture for metrics, logs, traces, dashboards, and reports.

9. orchestration/event-bus
Event Bus architecture for publish-subscribe routing, delivery, replay, and dead-letter handling.

Supporting orchestration files:

1. orchestration/workflow_engine.py and orchestration/workflow_state.py for workflow runtime state concerns.
2. orchestration/supervisor.py and orchestration/task_manager.py for orchestration entry coordination.
3. orchestration/agent_runner.py and orchestration/planner_executor.py for execution dispatch pathways.

## 5. Contracts Directory
Contracts define stable interfaces and governance rules across all runtime services and agents.

Current physical location:

1. ai/contracts

Contract purposes:

1. agent-contract.md
Defines mandatory lifecycle, metadata, responsibilities, and compliance for all agents.

2. artifact-contracts.md
Defines artifact ownership, schema envelope, lifecycle, and version rules.

3. event-contracts.md
Defines event categories, payload requirements, and lifecycle semantics.

4. workflow-state.md
Defines valid workflow states, transitions, and recovery behavior.

5. memory-contract.md
Defines memory scopes, persistence, retention, and concurrency rules.

6. approval-contract.md
Defines approval lifecycle, request and response behavior, escalation, and audit requirements.

7. validation-contract.md
Defines mandatory validation categories and failure handling behavior.

8. quality-report-contract.md
Defines quality reporting structure, thresholds, and readiness interpretation.

## 6. Configuration Directory
The configs directory holds declarative runtime control surfaces.

1. Workflow configuration
configs/workflow.yaml controls stage order, dependency behavior, and execution progression policy.

2. LLM configuration
configs/models.yaml controls model selection and model-specific runtime settings.

3. Platform configuration
configs/settings.yaml controls platform-wide behavior and defaults.

4. Environment configuration
Environment-specific values are represented through environment files and runtime environment variables.

5. Agent configuration
configs/agents.yaml maps agent registry behavior, role settings, and activation controls.

## 7. Artifacts Directory
The artifacts directory stores generated workflow deliverables and execution outputs.

1. Generated artifacts
Organized by domain folders such as requirements, architecture, frontend, backend, database, documentation, and tests.

2. Versioning
Artifact lineage is managed through metadata and version references, not by ad hoc file replacement.

3. Reports
Quality, validation, QA, review, and release-related outputs are stored as traceable artifacts.

4. Execution outputs
Intermediate and final workflow outputs are retained for downstream stages and auditability.

## 8. Applications Directory
The apps directory is the target location for generated runnable applications.

1. Generated applications
Each completed workflow can publish a runnable application package into this area.

2. Templates
Application generation often starts from templates defined under templates and becomes concrete output under apps.

3. Demo applications
Reference or demonstration outputs can be stored for validation, showcase, and regression checks.

4. Task Management System
The default platform demo scenario maps naturally to generated output under apps.

## 9. Documentation Directory
The docs directory contains architecture and operational knowledge for engineers.

1. Architecture documentation
docs/architecture.md defines the platform-wide architectural model.

2. Execution Flow
docs/execution-flow.md explains end-to-end workflow execution behavior.

3. Developer Guide
docs/setup.md and related documents guide local setup and operation.

4. Technology Decisions
Architecture and subsystem documentation capture key decisions and constraints.

5. Subsystem documentation
Subsystem-specific READMEs under orchestration folders are companion references for service-level architecture.

## 10. Tests Directory
The tests directory holds validation assets for platform reliability.

1. Unit tests
Component-level correctness tests for isolated logic.

2. Integration tests
Cross-service interaction tests for orchestration, events, memory, and artifact flows.

3. Workflow tests
End-to-end workflow execution validations against expected stage behavior.

4. Agent tests
Role-specific behavior and contract-conformance checks.

5. Regression tests
Stability tests that protect previously validated execution behavior from regressions.

## 11. Scripts Directory
The scripts directory provides operational entry points for local lifecycle tasks.

1. Bootstrap
Initial environment setup and baseline preparation workflows.

2. Setup
Repeatable local setup scripts for dependencies and runtime readiness.

3. Utilities
Reusable helper scripts for build, run, test, and maintenance automation.

4. Maintenance
Operational scripts for routine repository and environment upkeep.

Current script set includes setup, build, run, and test entry points.

## 12. Logs Directory
A logs directory is a standard operational extension point for persistent local telemetry.

Expected log classes:

1. Execution logs
2. Workflow logs
3. Audit logs
4. Performance logs

Current repository note:

1. Persistent logs folder is not currently materialized at top level.
2. Logging is supported by observability and can be routed to a dedicated logs directory by runtime configuration.

## 13. Design Principles
This structure supports enterprise growth through explicit modular boundaries.

1. Scalability
Subsystem separation allows individual services to grow in capability without destabilizing the full platform.

2. Maintainability
Contracts, configurations, and subsystem docs reduce implicit coupling and maintenance ambiguity.

3. Modularity
AI definitions, orchestration services, and operational assets are organized by responsibility.

4. Extensibility
New agents, workflows, tools, and integrations can be added via dedicated modules and contracts.

5. Traceability
Artifacts, events, memory, and approvals remain navigable through consistent directory conventions.

## 14. Example Repository Walkthrough
A recommended onboarding walkthrough for new developers:

1. Start at README.md
Understand platform purpose, default workflow, and local execution model.

2. Read docs/architecture.md
Build the high-level architecture mental model and subsystem boundaries.

3. Read docs/execution-flow.md
Understand end-to-end runtime behavior from SRS intake to local run completion.

4. Explore ai/contracts
Understand cross-cutting runtime contracts that govern all services and agents.

5. Explore orchestration subsystem folders
Read each subsystem README to understand Supervisor, workflow, event bus, memory, artifact, validation, approval, and observability responsibilities.

6. Explore ai/agents and ai/skills
Understand agent specialization and reusable capability composition.

7. Inspect configs
Understand how behavior is configured rather than hardcoded.

8. Inspect artifacts and apps
Understand where workflow outputs and generated applications appear.

9. Run scripts
Use setup, test, build, and run scripts for lifecycle execution.

10. Review tests and observability outputs
Validate expected behavior and inspect runtime evidence.

## 15. Future Repository Evolution
The repository is designed to evolve without disruptive restructuring.

1. Additional agents
Add new role definitions under ai/agents and corresponding skills under ai/skills.

2. Additional workflows
Add workflow definitions and configuration entries without changing core module boundaries.

3. Additional tools
Add new integrations under tools while preserving orchestration and contract interfaces.

4. Additional services
Add new orchestration subsystem folders with dedicated architecture documentation.

5. Additional contract families
Expand ai/contracts with versioned contracts for new capability domains.

6. Logging and operational expansion
Materialize a top-level logs directory and related retention policies when persistent local telemetry storage requirements increase.

This evolutionary model preserves existing architecture while enabling controlled enterprise growth.
