# Agent Reference Inventory

Document Version: 1.0.0
Effective Date: 2026-07-06
Status: Approved
Authority: Platform AI Governance Council

## Purpose

This document lists the guardrails, governance files, skills, and hooks that are actually referenced by the current agent definitions.

## Key

- Guardrails = behavioral constraints and scope boundaries
- Governance = policy files that define universal execution rules
- Skills = reusable capability definitions used by an agent
- Hooks = integration points or automation hooks referenced by the workflow

---

## Business Analyst Agent

### Key Name
- `business-analyst`

### Guardrails
- Scope boundary: business requirements only; no implementation, architecture, API, database, or design-token output
- Do not add or remove BA artifacts from the fixed output list
- Do not fetch, parse, or reconstruct Figma or make exports
- Keep guidance concise and lightweight
- Record unresolved gaps in openlog.md

### Governance References
- `ai/governance/core-behavior.md`
- `ai/governance/artifact-and-openlog-standard.md`

### Skills Used
- `ai/skills/business-analyst.md`

### Hooks Used
- None explicitly referenced in the agent definition

---

## Solution Architect Agent

### Key Name
- `solution-architect`

### Guardrails
- Work only from approved upstream artifacts and required contracts
- Do not invent implementation details beyond the approved scope
- Keep governance artifacts compact and schema-compliant
- Do not load unrelated workspace files

### Governance References
- `ai/governance/core-behavior.md`
- `ai/governance/artifact-and-openlog-standard.md`
- `ai/governance/role-specific/architecture-and-coding.md`

### Skills Used
- Translate business requirements into architecture and interface decisions
- Produce implementation-ready architecture and design artifacts
- Preserve traceability from requirements through technical design

### Hooks Used
- None explicitly referenced in the agent definition

---

## UI/UX Developer Agent

### Key Name
- `ui-ux-developer`

### Guardrails
- Design-file intake and presentation-layer implementation only
- Do not mix implementation code with governance markdown
- Validate API/data assumptions against approved contracts
- Keep governance output compact and template-based

### Governance References
- `ai/governance/core-behavior.md`
- `ai/governance/artifact-and-openlog-standard.md`
- `ai/governance/role-specific/architecture-and-coding.md`

### Skills Used
- Build responsive pages, layouts, and reusable components
- Implement navigation flow, routing, forms, and state scaffolding
- Implement accessibility, design tokens/styles, and API service placeholders
- Ensure WCAG 2.1 AA compliance

### Hooks Used
- None explicitly referenced in the agent definition

---

## Backend Developer Agent

### Key Name
- `backend-developer`

### Guardrails
- Implement approved contracts and architecture exactly
- Do not invent or alter endpoints, schemas, or auth requirements
- Keep governance markdown compact and schema-compliant
- Do not overwrite published artifacts

### Governance References
- `ai/governance/core-behavior.md`
- `ai/governance/artifact-and-openlog-standard.md`

### Skills Used
- Implement APIs from `api-specifications.md` as the authoritative contract
- Implement business/domain services and DTOs
- Implement authn/authz, validation, and exception handling
- Implement logging, configuration, and unit-test scaffolding

### Hooks Used
- Logging and audit hooks are referenced as implementation concerns, but no specific hook file is declared

---

## Database Developer Agent

### Key Name
- `database-developer`

### Guardrails
- Implement approved architecture exactly
- Do not redesign the data model or redefine business rules
- Reference upstream artifacts instead of copying architecture content verbatim
- Do not overwrite published artifacts

### Governance References
- `ai/governance/core-behavior.md`
- `ai/governance/artifact-and-openlog-standard.md`

### Skills Used
- Design Schema
- Create Migrations
- Optimize Performance
- Implement approved database schema in SQL, including constraints and indexes
- Generate ORM mappings and database README

### Hooks Used
- None explicitly referenced in the agent definition

---

## QA Engineer Agent

### Key Name
- `qa-engineer`

### Guardrails
- Validate against requirements, architecture, and implementation outputs
- Preserve evidence and traceability in reports
- Do not invent missing requirements or weaken standards
- Keep reports concise and evidence-based

### Governance References
- `ai/governance/core-behavior.md`
- `ai/governance/artifact-and-openlog-standard.md`
- `ai/governance/role-specific/testing-philosophy.md`

### Skills Used
- Review implementation against requirements and architecture
- Verify traceability and evidence quality
- Execute validation and regression checks
- Report blockers, risks, and readiness clearly

### Hooks Used
- None explicitly referenced in the agent definition

---

## Presentation Summary: Key Guardrails and Governance

### Business Analyst
- Key guardrails: stay in business scope, do not invent implementation, preserve traceability, and keep outputs artifact-driven.
- Key governance: follow core agent behavior and artifact/openlog standards; produce governed business artifacts and log unresolved gaps.

### Solution Architect
- Key guardrails: work from approved upstream artifacts, avoid invented design details, and keep outputs contract-aligned.
- Key governance: follow core behavior, artifact/openlog standards, and architecture/coding governance.

### UI/UX Developer
- Key guardrails: stay in presentation-layer scope, validate assumptions against approved contracts, and avoid mixing code with governance content.
- Key governance: follow core behavior, artifact/openlog standards, and architecture/coding governance.

### Backend Developer
- Key guardrails: implement only approved contracts, preserve security and validation boundaries, and do not overwrite published artifacts.
- Key governance: follow core behavior and artifact/openlog standards while producing backend implementation artifacts.

### Database Developer
- Key guardrails: implement approved data design only, preserve integrity and performance, and do not redefine business rules.
- Key governance: follow core behavior and artifact/openlog standards while generating schema, migrations, and database artifacts.

### QA Engineer
- Key guardrails: validate evidence, preserve traceability, and report blockers clearly without inventing missing requirements.
- Key governance: follow core behavior, artifact/openlog standards, and testing philosophy.

---

## Notes

- The current repository uses governance and skills as the main reusable reference layer.
- Hooks are not yet explicitly enumerated per agent in the current agent definition files.
- If you want, this inventory can be expanded into a more machine-readable format such as YAML or JSON later.
