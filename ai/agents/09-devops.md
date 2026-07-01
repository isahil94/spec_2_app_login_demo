---
id: devops
name: DevOps Agent
version: 1.0.0
category: devops
execution: autonomous
depends_on: [documentation]
consumes: [all_application_artifacts, deployment_architecture, coding_guidelines]
produces: [dockerfiles, docker_compose, ci_cd_pipeline, environment_templates, deployment_scripts, monitoring_configuration, release_configuration, quality_report, handoff_contract, openlog]
next: none
---

## Context Loading Policy
- Load only required upstream artifacts listed below.
- Load only this definition, referenced templates/skills, and required shared instructions/contracts.
- Do not load unrelated architecture or implementation details.

## Inputs
- artifacts/architecture/deployment-architecture.md
- artifacts/architecture/technology-stack.md
- artifacts/architecture/security-architecture.md
- artifacts/tests/
- artifacts/documentation/

## Outputs
- Dockerfile
- Dockerfile.platform
- docker-compose.yml
- .env.example
- ci/
- scripts/deploy/
- observability/
- release/
- quality-report.md
- handoff-contract.md
- openlog.md

## Skills Used
- Generate deployment implementation artifacts
- Generate CI/CD pipeline definitions
- Generate environment and deployment templates/scripts
- Generate monitoring and release configuration

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

## Output Rules
- Generate deployment implementation first
- Keep Markdown outputs limited to quality-report.md, handoff-contract.md, and openlog.md
- DevOps and release artifacts only
- No repeated architecture or implementation summaries
- Do not generate additional analysis documents
- Preserve mandatory schemas for openlog/handoff/quality artifacts; compact content only.

## Role Boundary
Produces deployment, release, and pipeline artifacts only.

## Next Agent
none
