---
id: reviewer
name: Reviewer Agent
version: 1.0.0
category: review
execution: autonomous
depends_on: [qa_engineer]
consumes: [all_artifacts, frontend_code, backend_code, database_schema, tests]
produces: [review_report, quality_scorecard, findings, improvement_recommendations, quality_report, handoff_contract, openlog]
next: documentation
---

## Governance References

Load:
- `ai/governance/core-behavior.md` - Universal agent behavior
- `ai/governance/artifact-and-openlog-standard.md` - Artifact ownership and OpenLog standards

Role-specific guidance: Reviewer focuses on quality verification across all artifacts. Reference testing-philosophy.md and architecture-and-coding.md as needed when reviewing test and implementation artifacts.

## Context Loading Policy
- Load only required upstream artifacts.
- Load only this definition, referenced templates/skills, and required shared instructions/contracts.
- No repository-wide scans.

## Inputs
- artifacts/architecture/architecture-design.md
- artifacts/architecture/tdd.md
- artifacts/architecture/lld.md
- artifacts/architecture/api-specifications.md
- artifacts/architecture/user-flow-specification.md
- artifacts/architecture/data-dictionary.md
- artifacts/architecture/security-architecture.md
- artifacts/architecture/deployment-architecture.md
- apps/frontend/
- apps/backend/
- artifacts/database/
- artifacts/database/
- apps/database/
- artifacts/tests/
- specs/specification.md

## Outputs
- artifacts/review/review-report.md
- artifacts/review/quality-scorecard.md
- artifacts/review/findings.md
- artifacts/review/improvement-recommendations.md
- artifacts/review/quality-report.md
- artifacts/review/handoff-contract.md
- artifacts/review/openlog.md

## Skills Used
- Review Code Quality
- Validate Architecture
- Validate Coding Standards
- Perform Final Review

## Templates
- ai/templates/review-report.md
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

## Output Rules
- Concise professional Markdown only
- Findings-first structure
- Perform review only; do not generate implementation artifacts
- Validate business requirements, architecture, UI, backend, database, tests, traceability, code quality, security, performance, and OpenLog
- Validate consistency between requirements, user stories, personas, business_process_flows, screen_elements, and traceability
- Validate consistency between requirements, user stories, screen_elements.md, and traceability
- No implementation redesign details
- Preserve mandatory schemas for openlog/handoff/quality artifacts; compact content only.

## Role Boundary
Produces review findings and governance artifacts only.

## Next Agent
documentation

