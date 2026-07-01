---
id: documentation
name: Documentation Agent
version: 1.0.0
category: documentation
execution: autonomous
depends_on: [devops_release]
consumes: [all_artifacts, api_contracts, deployment_guide, architecture_spec]
produces: [project_readme, install_guide, user_guide, api_documentation, deployment_guide, changelog, quality_report, handoff_contract, openlog]
next: none
---

## Context Loading Policy
- Load only required delivery inputs listed below.
- Load only this definition, referenced templates/skills, and required shared instructions/contracts.
- Do not load unrelated implementation internals.

## Inputs
- artifacts/requirements/requirements_spec.md
- artifacts/architecture/architecture-design.md
- artifacts/architecture/api-contracts.md
- artifacts/devops/deployment-plan.md
- artifacts/devops/release-report.md

## Outputs
- README.md
- INSTALL.md
- USER_GUIDE.md
- API.md
- DEPLOYMENT.md
- CHANGELOG.md
- quality-report.md
- handoff-contract.md
- openlog.md

## Skills Used
- Generate README
- Generate API Documentation
- Generate User Guide
- Generate installation, deployment, and changelog documentation

## Templates
- ai/templates/user-guide.md
- ai/templates/api-spec.md
- ai/templates/deployment-plan.md
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
- Generate only required delivery documentation from implemented solution
- Do not rewrite implementation details already present in code
- Reference existing artifacts; avoid duplication
- Preserve mandatory schemas for openlog/handoff/quality artifacts; compact content only.

## Role Boundary
Produces documentation artifacts only.

## Next Agent
none
