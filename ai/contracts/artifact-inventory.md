# Artifact Inventory

Document Version: 1.0.0
Effective Date: 2026-07-06
Status: Approved
Authority: Platform AI Governance Council

## Purpose

This document provides a compact inventory of the platform's major artifacts, their primary use, and the agent that owns them.

## How to Use This Inventory

- Use this document as a quick lookup for artifact purpose and ownership.
- Treat the artifact ownership matrix as the authoritative enforcement contract.
- Each artifact listed below has one owning agent and one primary purpose.

---

## Business Analyst Artifacts

| Artifact | Primary Use | Owner |
|---|---|---|
| requirements_spec.md | Consolidated business requirements, scope, goals, and functional coverage. | Business Analyst |
| user_stories.md | User-centric stories decomposed from business requirements. | Business Analyst |
| acceptance_criteria.md | Testable completion conditions for each story. | Business Analyst |
| non_functional_requirements.md | Business-facing quality expectations such as performance, security, and reliability. | Business Analyst |
| ui_observations.md | Business-oriented observations from design references for downstream UI work. | Business Analyst |
| screen_elements.md | Inventory of business-relevant screen elements and behaviors. | Business Analyst |
| business_rules.md | Business rules, validation rules, and policy constraints. | Business Analyst |
| data_requirements.md | Conceptual data needs, entities, relationships, and constraints. | Business Analyst |
| glossary.md | Canonical business terminology and definitions. | Business Analyst |
| traceability.md | Cross-linking between requirements, stories, rules, and downstream artifacts. | Business Analyst |
| personas.md | Stakeholder and user personas with goals and pain points. | Business Analyst |
| business_process_flows.md | End-to-end business workflows and state transitions. | Business Analyst |
| figma_design_intake.md | Structured intake of design references for downstream UI handoff. | Business Analyst |

---

## Solution Architect Artifacts

| Artifact | Primary Use | Owner |
|---|---|---|
| architecture-design.md | High-level system architecture and component structure. | Solution Architect |
| module-design.md | Detailed decomposition of modules and responsibilities. | Solution Architect |
| tdd.md | Test-driven development guidance aligned to architecture. | Solution Architect |
| lld.md | Low-level design for components and interactions. | Solution Architect |
| api-specifications.md | API contracts and interface definitions. | Solution Architect |
| user-flow-specification.md | End-to-end user flows for the proposed solution. | Solution Architect |
| data-dictionary.md | Shared data definitions and semantic meaning. | Solution Architect |
| security-architecture.md | Security model, access boundaries, and controls. | Solution Architect |
| deployment-architecture.md | Deployment topology and runtime structure. | Solution Architect |
| architecture-decision-records.md | Architectural decisions and rationale. | Solution Architect |
| database-strategy.md | Database approach and storage strategy. | Solution Architect |
| technology-stack.md | Selected technologies and platform choices. | Solution Architect |

---

## UI/UX Developer Artifacts

| Artifact | Primary Use | Owner |
|---|---|---|
| ui-specification.md | UI structure, layouts, and experience direction. | UI/UX Developer |
| design-system.md | Reusable visual and interaction design guidance. | UI/UX Developer |
| component-specification.md | Component-level behavior and composition. | UI/UX Developer |
| interaction-flow.md | Interaction paths and navigation behavior. | UI/UX Developer |
| accessibility-report.md | Accessibility review and remediation notes. | UI/UX Developer |
| frontend-handoff.md | Frontend implementation handoff package. | UI/UX Developer |

---

## Backend Developer Artifacts

| Artifact | Primary Use | Owner |
|---|---|---|
| backend-design.md | Backend component structure and responsibilities. | Backend Developer |
| endpoint-implementation.md | Implementation details for exposed endpoints. | Backend Developer |
| business-logic.md | Core business logic and service behavior. | Backend Developer |
| validation-rules.md | Server-side validation rules and enforcement logic. | Backend Developer |
| integration-implementation.md | Integration implementation and external dependency handling. | Backend Developer |
| backend-spec.md | Backend implementation specification and contract. | Backend Developer |
| backend-development-report.md | Backend implementation status and evidence. | Backend Developer |

---

## Database Developer Artifacts

| Artifact | Primary Use | Owner |
|---|---|---|
| database-schema.md | Physical schema definition. | Database Developer |
| er-diagram.md | Entity relationship model. | Database Developer |
| migration-plan.md | Database migration and rollout plan. | Database Developer |
| indexing-strategy.md | Index design and performance strategy. | Database Developer |
| seed-data-plan.md | Seed and initial data strategy. | Database Developer |
| database-report.md | Database implementation status and notes. | Database Developer |

---

## QA Engineer Artifacts

| Artifact | Primary Use | Owner |
|---|---|---|
| test-plan.md | Overall test strategy and scope. | QA Engineer |
| unit-test-cases.md | Unit-level test coverage and expected results. | QA Engineer |
| integration-test-cases.md | Cross-component integration coverage. | QA Engineer |
| system-test-cases.md | End-to-end system testing scenarios. | QA Engineer |
| regression-test-plan.md | Regression coverage plan. | QA Engineer |
| test-execution-report.md | Evidence of executed test runs and outcomes. | QA Engineer |

---

## Documentation Artifacts

| Artifact | Primary Use | Owner |
|---|---|---|
| user-guide.md | End-user operating guidance. | Documentation |
| developer-guide.md | Developer-facing implementation guidance. | Documentation |
| api-documentation.md | API reference and usage documentation. | Documentation |
| deployment-guide.md | Environment deployment documentation. | Documentation |
| release-notes.md | Release summary and change summary. | Documentation |

---

## Per-Agent Governance Artifacts

These artifacts are owned by the agent that produces them for a given execution, with scoped per-run instances.

| Artifact | Primary Use | Owner |
|---|---|---|
| quality_report.md | Validation evidence, completeness checks, and stage readiness summary. | Owning agent for the current stage |
| handoff-contract.md | Handoff summary, produced artifacts, and next-agent contract. | Owning agent for the current stage |
| openlog.md | Append-only log of open questions, assumptions, risks, decisions, and blockers. | Owning agent for the current stage |
