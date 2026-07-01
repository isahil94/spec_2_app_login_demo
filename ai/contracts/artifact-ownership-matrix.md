# Artifact Ownership Matrix

Contract Version: 1.0.0
Effective Date: 2026-07-01
Status: Approved
Authority: Platform AI Governance Council

---

## 1. Purpose

This document is the single authoritative source of truth for artifact ownership across all SDLC agents.

Every agent **must** consult this matrix before generating any artifact to verify:

1. The artifact is within my ownership scope.
2. I am not regenerating an artifact owned by a downstream or upstream agent.
3. I am consuming upstream artifacts instead of recreating them.
4. I am only extending artifacts explicitly marked as extendable.

Violation of artifact ownership is a **critical guardrail failure**. The offending agent must stop, reference the owning agent, and record the dependency in its Handoff Contract.

---

## 2. Ownership Status Definitions

Every cell in Section 3 uses exactly one of the following statuses.

| Status | Meaning |
|--------|---------|
| **OWN** | The agent is the sole creator and owner. Only this agent may create this artifact. No other agent may write to it. |
| **CONSUME** | Read-only input. The agent reads and depends on this artifact but must never modify it. |
| **EXTEND** | The agent may enrich the artifact without changing its original intent. Ownership remains with the originating agent. Only explicitly granted on api-contracts.md for Backend Developer. |
| **REFERENCE** | The artifact is used for context only. No modifications permitted. Lower dependency than CONSUME. |
| **NONE** | The artifact is irrelevant to this stage. The agent must not read or touch it. |

---

## 2.1 Enforcement Rules

These rules apply to every agent, every execution, without exception.

```
BEFORE generating any artifact:
  1. Look up the artifact in Section 3.
  2. Find this agent's column.
  3. Status must be OWN to generate.
  4. If status is CONSUME, EXTEND, REFERENCE, or NONE:
       - Stop. Do not generate this artifact.
       - Identify the OWN agent from Section 3.
       - Record an ownership violation in:
           quality-report.md  (violation log)
           handoff-contract.md (Cross-Agent Dependencies)
           openlog.md          (Open Item with Category: Governance)
       - Reference the owning agent's artifact path instead of generating.
  5. EXTEND is the only exception: Backend Developer may append to
     endpoint-implementation.md as an addendum to api-contracts.md
     without overwriting the original.
```

---

## 3. Artifact Ownership Status Matrix

Columns: BA = Business Analyst | SA = Solution Architect | UX = UI/UX Developer | BE = Backend Developer | DB = Database Developer | QA = QA Engineer | RV = Reviewer | DO = DevOps & Release | DC = Documentation | SV = Supervisor

### 3.1 Business Analyst Artifacts

| Artifact | BA | SA | UX | BE | DB | QA | RV | DO | DC | SV |
|----------|----|----|----|----|----|----|----|----|----|----|
| requirements_spec.md | OWN | CONSUME | REFERENCE | REFERENCE | REFERENCE | REFERENCE | REFERENCE | REFERENCE | CONSUME | REFERENCE |
| user_stories.md | OWN | CONSUME | CONSUME | CONSUME | REFERENCE | CONSUME | REFERENCE | REFERENCE | CONSUME | REFERENCE |
| acceptance_criteria.md | OWN | CONSUME | REFERENCE | NONE | NONE | CONSUME | REFERENCE | NONE | REFERENCE | REFERENCE |
| non_functional_requirements.md | OWN | CONSUME | REFERENCE | REFERENCE | REFERENCE | CONSUME | REFERENCE | REFERENCE | REFERENCE | REFERENCE |
| ui_observations.md | OWN | CONSUME | CONSUME | NONE | NONE | REFERENCE | NONE | NONE | REFERENCE | NONE |
| traceability.md | OWN | CONSUME | NONE | NONE | NONE | CONSUME | CONSUME | NONE | CONSUME | REFERENCE |

### 3.2 Solution Architect Artifacts

| Artifact | BA | SA | UX | BE | DB | QA | RV | DO | DC | SV |
|----------|----|----|----|----|----|----|----|----|----|----|
| architecture-design.md | NONE | OWN | CONSUME | CONSUME | REFERENCE | REFERENCE | CONSUME | REFERENCE | CONSUME | REFERENCE |
| module-design.md | NONE | OWN | REFERENCE | CONSUME | CONSUME | REFERENCE | REFERENCE | NONE | REFERENCE | NONE |
| technology-stack.md | NONE | OWN | REFERENCE | CONSUME | CONSUME | REFERENCE | REFERENCE | CONSUME | CONSUME | REFERENCE |
| api-contracts.md | NONE | OWN | REFERENCE | EXTEND | REFERENCE | CONSUME | REFERENCE | REFERENCE | CONSUME | REFERENCE |
| security-architecture.md | NONE | OWN | NONE | CONSUME | NONE | CONSUME | CONSUME | CONSUME | REFERENCE | REFERENCE |
| deployment-architecture.md | NONE | OWN | NONE | NONE | NONE | NONE | REFERENCE | CONSUME | CONSUME | REFERENCE |
| architecture-decision-records.md | NONE | OWN | REFERENCE | REFERENCE | REFERENCE | REFERENCE | CONSUME | REFERENCE | CONSUME | REFERENCE |
| database-strategy.md | NONE | OWN | NONE | REFERENCE | CONSUME | NONE | REFERENCE | NONE | REFERENCE | NONE |

### 3.3 UI/UX Developer Artifacts

| Artifact | BA | SA | UX | BE | DB | QA | RV | DO | DC | SV |
|----------|----|----|----|----|----|----|----|----|----|----|
| ui-specification.md | NONE | REFERENCE | OWN | REFERENCE | NONE | CONSUME | REFERENCE | NONE | CONSUME | NONE |
| design-system.md | NONE | NONE | OWN | REFERENCE | NONE | REFERENCE | REFERENCE | NONE | CONSUME | NONE |
| component-specification.md | NONE | NONE | OWN | REFERENCE | NONE | CONSUME | REFERENCE | NONE | REFERENCE | NONE |
| interaction-flow.md | NONE | NONE | OWN | REFERENCE | NONE | CONSUME | REFERENCE | NONE | REFERENCE | NONE |
| accessibility-report.md | NONE | NONE | OWN | NONE | NONE | CONSUME | CONSUME | NONE | REFERENCE | NONE |
| frontend-handoff.md | NONE | NONE | OWN | CONSUME | NONE | REFERENCE | NONE | NONE | REFERENCE | NONE |

### 3.4 Backend Developer Artifacts

| Artifact | BA | SA | UX | BE | DB | QA | RV | DO | DC | SV |
|----------|----|----|----|----|----|----|----|----|----|----|
| backend-design.md | NONE | NONE | NONE | OWN | REFERENCE | CONSUME | REFERENCE | NONE | REFERENCE | NONE |
| endpoint-implementation.md | NONE | NONE | NONE | OWN | NONE | CONSUME | REFERENCE | NONE | NONE | NONE |
| business-logic.md | NONE | NONE | NONE | OWN | REFERENCE | CONSUME | CONSUME | NONE | REFERENCE | NONE |
| validation-rules.md | NONE | NONE | NONE | OWN | NONE | CONSUME | REFERENCE | NONE | NONE | NONE |
| integration-implementation.md | NONE | NONE | NONE | OWN | NONE | CONSUME | REFERENCE | REFERENCE | NONE | NONE |
| backend-development-report.md | NONE | NONE | NONE | OWN | NONE | REFERENCE | CONSUME | NONE | NONE | CONSUME |

### 3.5 Database Developer Artifacts

| Artifact | BA | SA | UX | BE | DB | QA | RV | DO | DC | SV |
|----------|----|----|----|----|----|----|----|----|----|----|
| database-schema.md | NONE | REFERENCE | NONE | REFERENCE | OWN | CONSUME | REFERENCE | REFERENCE | REFERENCE | REFERENCE |
| er-diagram.md | NONE | REFERENCE | NONE | REFERENCE | OWN | CONSUME | CONSUME | NONE | CONSUME | NONE |
| migration-plan.md | NONE | NONE | NONE | REFERENCE | OWN | CONSUME | REFERENCE | CONSUME | REFERENCE | NONE |
| indexing-strategy.md | NONE | NONE | NONE | REFERENCE | OWN | CONSUME | REFERENCE | NONE | NONE | NONE |
| seed-data-plan.md | NONE | NONE | NONE | NONE | OWN | CONSUME | NONE | NONE | NONE | NONE |
| database-report.md | NONE | NONE | NONE | NONE | OWN | REFERENCE | CONSUME | NONE | NONE | CONSUME |

### 3.6 QA Engineer Artifacts

| Artifact | BA | SA | UX | BE | DB | QA | RV | DO | DC | SV |
|----------|----|----|----|----|----|----|----|----|----|----|
| test-plan.md | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | NONE | REFERENCE | NONE |
| unit-test-cases.md | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | NONE | NONE | NONE |
| integration-test-cases.md | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | CONSUME | NONE | NONE |
| system-test-cases.md | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | NONE | NONE | NONE |
| regression-test-plan.md | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | NONE | NONE | NONE |
| test-execution-report.md | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | NONE | REFERENCE | CONSUME |

### 3.7 Reviewer Artifacts

| Artifact | BA | SA | UX | BE | DB | QA | RV | DO | DC | SV |
|----------|----|----|----|----|----|----|----|----|----|----|
| review-report.md | NONE | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | CONSUME | CONSUME |
| quality-scorecard.md | NONE | NONE | NONE | NONE | NONE | NONE | OWN | NONE | CONSUME | CONSUME |
| findings.md | NONE | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | REFERENCE | CONSUME |
| improvement-recommendations.md | NONE | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | CONSUME | CONSUME |

### 3.8 DevOps & Release Artifacts

| Artifact | BA | SA | UX | BE | DB | QA | RV | DO | DC | SV |
|----------|----|----|----|----|----|----|----|----|----|----|
| deployment-plan.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | NONE |
| ci-cd-pipeline.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | REFERENCE |
| infrastructure-specification.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | REFERENCE |
| monitoring-observability.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | REFERENCE |
| rollback-recovery-plan.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN | CONSUME | REFERENCE |
| release-report.md | NONE | NONE | NONE | NONE | NONE | NONE | REFERENCE | OWN | CONSUME | CONSUME |

### 3.9 Documentation Artifacts

| Artifact | BA | SA | UX | BE | DB | QA | RV | DO | DC | SV |
|----------|----|----|----|----|----|----|----|----|----|----|
| user-guide.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN | NONE |
| developer-guide.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN | NONE |
| api-documentation.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN | NONE |
| deployment-guide.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN | NONE |
| release-notes.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN | NONE |

### 3.10 Supervisor Artifacts

| Artifact | BA | SA | UX | BE | DB | QA | RV | DO | DC | SV |
|----------|----|----|----|----|----|----|----|----|----|----|
| workflow-status.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN |
| approval-queue.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN |
| execution-log.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN |
| supervisor-report.md | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | OWN |

### 3.11 Per-Agent Governance Artifacts (Scoped)

Each agent owns its own scoped instance. No other agent may write to another agent's governance artifacts.

| Artifact | Status for Owning Agent | Status for Supervisor | Status for Solution Architect | Status for All Others |
|----------|------------------------|----------------------|-------------------------------|----------------------|
| quality-report.md | OWN | CONSUME | CONSUME | NONE |
| handoff-contract.md | OWN | CONSUME | CONSUME | NONE |
| openlog.md | OWN | CONSUME | CONSUME | NONE |

---

## 4. Per-Agent Ownership Detail

---

### 4.1 Business Analyst

**Pipeline position:** 1

**Owns:**
- `requirements_spec.md`
- `user_stories.md`
- `acceptance_criteria.md`
- `non_functional_requirements.md`
- `ui_observations.md`
- `traceability.md`
- `quality_report.md`
- `handoff_contract.md` (BA-scoped)
- `openlog.md` (BA-scoped)

**Consumes:**
- `specification.md` (platform input)
- `figma_url.txt` (optional fallback only)
- `config.yaml` (optional)

Figma propagation rule:
- If a Figma URL exists in `specification.md`, Business Analyst must consume it directly and preserve it unchanged through `ui_observations.md` and `handoff_contract.md`.

**May Extend:** None.

**Must NOT generate:**
- API endpoints or HTTP method definitions
- REST contracts or OpenAPI fragments
- Database schema (physical or conceptual ER)
- SQL of any kind
- Technology stack decisions
- Architecture diagrams or component designs
- Deployment or infrastructure decisions
- Any code (frontend, backend, database, infrastructure)
- Artifacts owned by any other agent

**Boundary statement:** Business Analyst defines WHAT the business needs, never HOW to implement it.

---

### 4.2 Solution Architect

**Pipeline position:** 2

**Owns:**
- `architecture-design.md`
- `module-design.md`
- `technology-stack.md`
- `api-contracts.md`
- `security-architecture.md`
- `deployment-architecture.md`
- `architecture-decision-records.md`
- `database-strategy.md` (conceptual only)
- `quality-report.md`
- `handoff-contract.md` (SA-scoped)
- `openlog.md` (SA-scoped)

**Consumes:**
- `requirements_spec.md`
- `user_stories.md`
- `acceptance_criteria.md`
- `non_functional_requirements.md`
- `ui_observations.md`
- `traceability.md`
- `quality_report.md` (BA output, read-only)
- `handoff_contract.md` (BA output, read-only)
- `openlog.md` (BA output, read-only)
- `config.yaml`

**May Extend:** None.

**`database-strategy.md` scope — STRICTLY limited to:**
- Conceptual entity relationship model (named entities and high-level relationships only; no column definitions)
- Persistence strategy selection (e.g., relational, document, time-series)
- Data flow overview
- Transaction strategy (e.g., ACID, eventual consistency)
- Storage and partitioning strategy

**Must NOT generate:**
- Physical database schema (tables, columns, data types)
- `CREATE TABLE` statements or DDL of any kind
- Index definitions
- Migration scripts
- Seed data
- ORM model files
- Any code (frontend, backend, infrastructure)
- Artifacts owned by any other agent

**Boundary statement:** Solution Architect defines HOW the system is structured. Physical data design belongs exclusively to Database Developer.

---

### 4.3 UI/UX Developer

**Pipeline position:** 3a (parallel with Backend)

**Owns:**
- `ui-specification.md`
- `design-system.md`
- `component-specification.md`
- `interaction-flow.md`
- `accessibility-report.md`
- `frontend-handoff.md`
- `quality-report.md`
- `handoff-contract.md` (UIUX-scoped)
- `openlog.md` (UIUX-scoped)

**Consumes:**
- `architecture-design.md`
- `ui_observations.md`
- `user_stories.md`
- `api-contracts.md` (reference only — must not modify)

**May Extend:** None.

**Must NOT generate:**
- Backend API implementation or modification
- Database schema or queries
- Artifacts owned by any other agent

**Boundary statement:** UI/UX Developer implements the approved UI specification as production-ready frontend code. Business Analyst defines the UI requirements, Solution Architect defines the architecture, and downstream agents own their respective implementation layers.

---

### 4.4 Backend Developer

**Pipeline position:** 3b (parallel with UI/UX)

**Owns:**
- `backend-design.md`
- `endpoint-implementation.md`
- `validation-rules.md`
- `business-logic.md`
- `integration-implementation.md`
- `backend-development-report.md`
- `quality-report.md`
- `handoff-contract.md` (Backend-scoped)
- `openlog.md` (Backend-scoped)

**Consumes:**
- `architecture-design.md`
- `api-contracts.md` (implements; must not alter the contract document)
- `security-architecture.md`
- `user_stories.md`
- `coding-guidelines.md`

**May Extend:** `api-contracts.md` — Backend Developer may produce implementation notes or endpoint mapping artifacts as addendums but must never modify the published API contracts.

**Must NOT generate:**
- Modifications to `api-contracts.md`
- Database schema, DDL, migration scripts, ORM models or database design
- Frontend code, components, styling or UI specifications
- Business requirements or architectural decisions
- Artifacts owned by other agents

**Boundary statement:** Backend Developer implements the complete business layer from Business Analyst requirements and Solution Architect artifacts. It consumes published API contracts, implements controllers, services, DTOs, validation, authentication, authorization and business logic, but must not redefine business requirements, API contracts or database design.

---

### 4.5 Database Developer

**Pipeline position:** 4

**Owns:**
- `database-schema.md`
- `er-diagram.md`
- `migration-plan.md`
- `indexing-strategy.md`
- `seed-data-plan.md`
- `database-report.md`
- `quality-report.md`
- `handoff-contract.md` (DB-scoped)
- `openlog.md` (DB-scoped)

**Consumes:**
- `database-strategy.md` (from Solution Architect — conceptual guide only)
- `backend-design.md` (entity and data requirements)
- `service-design.md` (entity and data requirements)
- `api-contracts.md` (data shape reference)

**May Extend:** None.

**Must NOT:**
- Alter the conceptual data model or persistence strategy defined by the Solution Architect.
- Modify published API contracts.
- Produce frontend or backend application code.
- Redefine business requirements or architecture decisions.
- Modify artifacts owned by other agents.

**Boundary statement:** Database Developer implements the physical data layer from Business Analyst requirements and Solution Architect artifacts. It owns the implementation of schemas, tables, columns, keys, indexes, constraints, migrations, seed data, views, stored procedures/functions (when required), and ORM mappings, but must not redefine the conceptual data model, business rules, API contracts or architecture.
---

### 4.6 QA Engineer

**Pipeline position:** 5

**Owns:**
- `test-plan.md`
- `unit-test-cases.md`
- `integration-test-cases.md`
- `system-test-cases.md`
- `regression-test-plan.md`
- `test-execution-report.md`
- `quality-report.md`
- `handoff-contract.md` (QA-scoped)
- `openlog.md` (QA-scoped)

**Consumes:**
- `user_stories.md`
- `acceptance_criteria.md`
- `api-contracts.md`
- `ui-specification.md`
- `backend-design.md`
- `database-schema.md`
- `service-design.md`

**May Extend:** None.

**Must NOT:**
- Modify implementation artifacts (code, schema, contracts or specifications)
- Change business requirements or architecture
- Generate implementation or infrastructure artifacts
- Alter artifacts owned by other agents

**Boundary statement:** QA Engineer owns the complete testing lifecycle. It generates, configures and executes unit, integration, API, UI and end-to-end tests, collects evidence, measures quality and publishes validation results. It must not modify the artifacts it validates.

---

### 4.7 Reviewer

**Pipeline position:** 6

**Owns:**
- `review-report.md`
- `quality-scorecard.md`
- `findings.md`
- `improvement-recommendations.md`
- `quality-report.md`
- `handoff-contract.md` (Reviewer-scoped)
- `openlog.md` (Reviewer-scoped)

**Consumes:** All artifacts from all previous agents (read-only).

**May Extend:** None.

**Must NOT:**
- Generate implementation artifacts of any kind
- Modify artifacts owned by other agents
- Produce code, schema, architecture, specifications or infrastructure artifacts
- Substitute for any upstream agent's responsibilities

**Boundary statement:** Reviewer independently assesses all completed artifacts for completeness, consistency, quality, traceability and compliance with requirements, architecture and governance. It produces only review findings, recommendations and quality assessment artifacts. It never modifies the artifacts it reviews.
---

### 4.8 DevOps & Release

**Pipeline position:** 7

**Owns:**
- `deployment-plan.md`
- `ci-cd-pipeline.md`
- `infrastructure-specification.md`
- `monitoring-observability.md`
- `rollback-recovery-plan.md`
- `release-report.md`
- `quality-report.md`
- `handoff-contract.md` (DevOps-scoped)
- `openlog.md` (DevOps-scoped)

**Consumes:**
- `deployment-strategy.md` (from Solution Architect)
- `migration-plan.md` (from Database Developer)
- `review-report.md` (from Reviewer)
- All application artifacts (read-only, for packaging)

**May Extend:** None.

**Must NOT:**
- Redesign or modify application architecture
- Alter API contracts, database schema, or code
- Produce business logic or feature code
- Regenerate artifacts owned by Solution Architect

**Boundary statement:** DevOps & Release owns infrastructure and delivery pipeline. Application design belongs to upstream agents.

---

### 4.9 Documentation

**Pipeline position:** 8

**Owns:**
- `user-guide.md`
- `developer-guide.md`
- `api-documentation.md`
- `deployment-guide.md`
- `release-notes.md`
- `quality-report.md`
- `handoff-contract.md` (Docs-scoped)
- `openlog.md` (Docs-scoped)

**Consumes:** All artifacts from all prior agents (read-only synthesis).

**May Extend:** None.

**Must NOT:**
- Produce implementation artifacts (code, schema, infrastructure files)
- Alter or overwrite any artifact owned by another agent
- Make architecture or design decisions

**Boundary statement:** Documentation synthesizes all prior artifacts into human-readable guides. It does not produce or modify any implementation artifact.

---

### 4.10 Supervisor

**Pipeline position:** Orchestrator (all stages)

**Owns:**
- `workflow_state.json`
- `agent_directives.json`
- `execution_log.jsonl`
- `metrics.json`
- `progress_report.md`
- Approval requests and responses

**Consumes:** All agent events, handoff contracts, approval decisions.

**May Extend:** None (reads all; owns orchestration state only).

**Must NOT:**
- Produce business requirements, architecture, or implementation artifacts
- Override agent ownership of their respective artifacts

---

## 5. Handoff Sequence

```
specification.md
    │
    ▼
[Business Analyst]
    │  Produces: requirements_spec.md, user_stories.md, acceptance_criteria.md,
    │            non_functional_requirements.md, ui_observations.md, traceability.md
    ▼
[Solution Architect]
    │  Consumes: requirements_spec.md, user_stories.md, non_functional_requirements.md
    │  Produces: architecture-design.md, api-contracts.md, database-strategy.md,
    │            deployment-strategy.md, security-architecture.md, technology-decision-matrix.md
    ▼
    ├──────────────────────────────────┐
    ▼                                  ▼
[UI/UX Developer]              [Backend Developer]
    │  Consumes: architecture-design.md    │  Consumes: architecture-design.md,
    │            ui_observations.md        │            api-contracts.md,
    │  Produces: ui-specification.md,      │            security-architecture.md
    │            design-system.md,         │  Produces: backend-design.md,
    │            component-spec.md,        │            service-design.md,
    │            interaction-spec.md       │            endpoint-implementation-plan.md
    │                                      ▼
    │                         [Database Developer]
    │                              │  Consumes: database-strategy.md,
    │                              │            backend-design.md,
    │                              │            service-design.md
    │                              │  Produces: database-schema.md,
    │                              │            er-diagram.md,
    │                              │            migration-plan.md
    └──────────────┬───────────────┘
                   ▼
            [QA Engineer]
                     │  Consumes: user_stories.md, acceptance_criteria.md, api-contracts.md,
                   │            ui-specification.md, backend-design.md, database-schema.md
                   │  Produces: test-plan.md, test-cases.md, integration-tests.md, qa-report.md
                   ▼
             [Reviewer]
                   │  Consumes: all artifacts (read-only)
                   │  Produces: review-report.md, architecture-review.md,
                   │            quality-scorecard.md, improvement-recommendations.md
                   ▼
         [DevOps & Release]
                   │  Consumes: deployment-strategy.md, migration-plan.md, review-report.md
                   │  Produces: Dockerfile, docker-compose.yml, ci/cd workflows,
                   │            deployment-config.md, release-plan.md
                   ▼
          [Documentation]
                   │  Consumes: all artifacts (read-only synthesis)
                   │  Produces: user-guide.md, developer-guide.md, api-documentation.md,
                   │            deployment-guide.md, release-notes.md
                   ▼
                 DONE
```

---

## 6. Overlap Prevention Rules

The following pairs historically produced overlap. These rules are normative.

### 6.1 Business Analyst ↔ Solution Architect
- Business Analyst must not suggest specific endpoints, HTTP verbs, request/response payloads, or data schemas.
- Solution Architect must not re-analyze or rewrite business requirements; it consumes them.

### 6.2 Solution Architect ↔ Database Developer
- Solution Architect `database-strategy.md` is conceptual only: entity names, relationships, persistence strategy, transaction strategy.
- Database Developer owns all physical schema decisions: table names, columns, data types, indexes, constraints, migrations, seeds.
- If Solution Architect's database-strategy contains DDL, column definitions, or index definitions, those sections must be removed and deferred to Database Developer.

### 6.3 Solution Architect ↔ Backend Developer
- Backend Developer must not alter `api-contracts.md`. Deviations are recorded in `endpoint-implementation-plan.md` with a reference.
- Solution Architect must not produce service implementation details, validation logic, or error handling code.

### 6.4 UI/UX Developer ↔ Backend Developer
- UI/UX Developer produces design specifications; it does not produce code.
- Backend Developer implements services; it does not produce UI specifications.

### 6.5 QA Engineer ↔ All Implementation Agents
- QA Engineer does not modify any implementation artifact. Test code is owned exclusively by QA Engineer.
- QA Engineer's test artifacts are never overwritten by implementation agents.

### 6.6 Reviewer ↔ All Agents
- Reviewer produces only review and recommendation artifacts.
- No implementation agent may overwrite a Reviewer artifact.
- No Reviewer artifact may overwrite an implementation artifact.

### 6.7 DevOps ↔ Solution Architect
- Deployment infrastructure files are owned exclusively by DevOps & Release.
- Solution Architect's `deployment-strategy.md` is input guidance, not the final deployment configuration.

---

## 7. Conflict Resolution Protocol

When an agent detects it is about to produce an artifact owned by another agent:

```
1. STOP: Do not generate the artifact.
2. IDENTIFY: Locate the owning agent in Section 4 of this document.
3. REFERENCE: Add a reference entry in the current Handoff Contract:
     "Cross-Agent Dependency:
      Artifact: <artifact-name>
      Owner: <owning-agent>
      Action: Deferred. Will be consumed when published by <owning-agent>."
4. CONTINUE: Proceed with artifacts within your ownership scope.
5. DO NOT escalate to Supervisor unless the owning agent's artifact is missing
   and it is a required input — in that case, emit a Blocked event.
```

---

## 8. Related Contracts

| Contract | Relationship |
|----------|-------------|
| `artifact-contracts.md` | Defines artifact envelope, versioning, and lifecycle; this matrix defines ownership |
| `agent-contract.md` | Defines agent lifecycle; this matrix governs artifact scope within that lifecycle |
| `validation-contract.md` | Applies validation to artifacts; this matrix identifies which agent is responsible for passing validation |
| `event-contracts.md` | Events signal completion; this matrix determines what outputs trigger those events |
| `quality-report-contract.md` | Quality gates apply per artifact; this matrix identifies the accountable owner |

---

*End of Artifact Ownership Matrix — Contract Version 1.0.0*
