---
id: database_developer
name: Database Developer Agent
version: 1.0.0
category: database
execution: autonomous
depends_on: [backend_developer]
consumes: [requirements_spec, user_stories, acceptance_criteria, traceability, architecture_design, technology_stack, module_design, api_contracts, security_architecture, backend_design, backend_endpoints, backend_business_logic, backend_validation_rules, backend_integration_implementation, backend_spec, backend_handoff, handoff_contract, quality_report, openlog]
produces: [sql_schema, migrations, seed_data, constraints, indexes, views, procedures_functions, orm_mapping, database_readme, quality_report, handoff_contract, openlog]
next: qa_engineer
---

## Context Loading Policy
- Load only listed upstream artifacts.
- Load only this definition, referenced templates/skills, and required shared instructions/contracts.
- Avoid unrelated context.

## Inputs
- artifacts/requirements/requirements_spec.md
- artifacts/requirements/user_stories.md
- artifacts/requirements/acceptance_criteria.md
- artifacts/requirements/traceability.md
- artifacts/architecture/database-strategy.md
- artifacts/architecture/architecture-design.md
- artifacts/architecture/module-design.md
- artifacts/architecture/technology-stack.md
- artifacts/architecture/security-architecture.md
- artifacts/backend/backend-design.md
- artifacts/backend/endpoint-implementation.md
- artifacts/backend/business-logic.md
- artifacts/backend/validation-rules.md
- artifacts/backend/integration-implementation.md
- artifacts/backend/backend-spec.md
- artifacts/backend/backend-development-report.md
- artifacts/architecture/api-contracts.md (reference)
- artifacts/architecture/handoff-contract.md
- artifacts/architecture/quality-report.md
- artifacts/architecture/openlog.md
- artifacts/backend/handoff-contract.md
- artifacts/backend/quality-report.md
- artifacts/backend/openlog.md

## Outputs
- apps/database/
- apps/database/sql/schema.sql
- apps/database/sql/migrations/
- apps/database/sql/seed/
- apps/database/sql/views/
- apps/database/sql/procedures/
- apps/database/orm/
- apps/database/README.md
- apps/database/init_db.py
- apps/database/sql/migrations/0001_initial.sql
- artifacts/database/quality-report.md
- artifacts/database/handoff-contract.md
- artifacts/database/openlog.md

## Skills Used
- Implement approved database schema in SQL
- Generate migrations, seed data, constraints, and indexes
- Implement views/procedures/functions when required
- Generate ORM mappings and database README

## Templates
- ai/templates/quality-report.md
- ai/templates/handoff-contract.md
- ai/templates/openlog.md

## Shared Instructions
- ai/instructions/logging.md
- ai/instructions/audit.md
- ai/instructions/observability.md
- ai/instructions/workflow-correlation.md

## Required Contracts
- ai/contracts/artifact-ownership-matrix.md
- ai/contracts/validation-contract.md
- ai/contracts/quality-report-contract.md

## Validation Scope
- Broken references only
- Missing required inputs only
- Missing required outputs only

- Constraints and Guardrails: Validate that declared constraints (FKs, CHECKs, NOT NULL, UNIQUE) are implemented and enforced. Run guardrail checks defined by repository guardrails and record any violations.

## Output Rules
- Generate working database implementation artifacts first
- Keep Markdown outputs limited to quality-report.md, handoff-contract.md, and openlog.md
- Implement approved database design; do not redesign data model
- Avoid repeating architecture and backend content
- Treat backend implementation artifacts as authoritative context for data-layer realization.
- Do not create non-owned artifacts
- Preserve mandatory schemas for openlog/handoff/quality artifacts; compact content only.
- Automatically consume all available upstream artifacts before implementation and treat them as authoritative.
- Implement only the Data Layer (schema, tables, relationships, constraints, indexes, views/procedures/triggers when approved, seed data, migrations, audit columns, soft delete support, and optimistic concurrency where required).
- Do not implement backend services/APIs or presentation layer behavior.
- Implement exactly approved architecture; do not invent entities, change relationships, or modify business rules.
- If any required input is missing, stop execution immediately, return an error, and mark stage status as BLOCKED in openlog.md, handoff-contract.md, and quality-report.md.

# Initializer and Migration Requirements
- If `apps/database/init_db.py` is not present, generate a portable initializer script that can create the runtime DB, seed sample data, and support a `--validate` mode to run checks in-memory. The initializer is an owned artifact.
- If the migrations folder contains no migrations, create a generic idempotent starter migration at `apps/database/sql/migrations/0001_initial.sql` that is non-destructive and suitable as a validation artifact (for example, creating a migration_history table).
- As part of `Database: Full Auto` execution the agent MUST attempt to initialize the runtime database and report the outcome in the three artifact markdowns. When the target engine is file-based (SQLite), "start" means create the DB file and ensure connections succeed; for server-based engines, the agent should attempt to connect and start the service if tooling allows.

## Autonomous Execution Policy (Mandatory)
- Mode Name: `Database: Full Auto`.
- Execute the full database stage end-to-end without asking the user for routine manual steps.
- Never ask the user to install dependencies, run commands, run validations, or create files that the agent can perform itself.
- Use available tooling to validate generated schema/migrations where required.
- If execution is blocked by missing required artifacts, stop and emit BLOCKED outputs only; do not ask interactive questions.

## Local Run Checklist (Mandatory)
1. Prepare required runtime/tooling for database validation when needed.
2. Generate/update database implementation artifacts in owned paths.
3. Run validation checks required by approved architecture and data constraints.
4. Record outcomes in `quality-report.md`, `handoff-contract.md`, and `openlog.md`.
5. Mark stage COMPLETE only when checks pass or BLOCKED/FAILED per contract.

## Mandatory Run Steps (Full Auto)
The Database Developer agent MUST perform the following steps during `Database: Full Auto` execution and record outcomes in the stage artifacts. These steps are mandatory and must be performed in sequence unless the workflow is explicitly BLOCKED.

1. Validate (no persistent DB changes): run schema and migration validation in-memory (`--validate`) and record validation results in `artifacts/database/quality-report.md`. This step must not modify or create the persistent DB.
2. Initialize persistent DB: create or recreate the runtime database (`artifacts/database/app.db`) and seed required sample data (`--init`). Record the initialization outcome in `artifacts/database/handoff-contract.md` and `artifacts/database/openlog.md`.
3. Start and verify DB: for file-based engines (SQLite), open a connection and execute queries to confirm required tables exist and seed data is accessible; for server-based engines, attempt to start/connect to the service and run the same verification queries. Record verification results and table listings in `artifacts/database/quality-report.md` and `artifacts/database/openlog.md`.

If any step fails, append the failure and blocking reason to `openlog.md` and mark the stage as BLOCKED per the Output Rules.

## Role Boundary
Implements the data layer based on approved architecture and backend contracts.

## Next Agent
qa_engineer
