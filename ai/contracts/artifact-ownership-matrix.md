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
| **EXTEND** | The agent may enrich the artifact without changing its original intent. Ownership remains with the originating agent. Only explicitly granted on api-specifications.md for Backend Developer. |
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
     endpoint-implementation.md as an addendum to api-specifications.md
     without overwriting the original.
```

---

## 3. Artifact Ownership Status Matrix

Columns: BA = Business Analyst | SA = Solution Architect | UX = UI/UX Developer | BE = Backend Developer | DB = Database Developer | QA = QA Engineer

### 3.1 Business Analyst Artifacts

| Artifact | BA | SA | UX | BE | DB | QA |
|----------|----|----|----|----|----|----|
| requirements_spec.md | OWN | CONSUME | REFERENCE | REFERENCE | REFERENCE | REFERENCE |
| user_stories.md | OWN | CONSUME | CONSUME | CONSUME | REFERENCE | CONSUME |
| acceptance_criteria.md | OWN | CONSUME | REFERENCE | CONSUME | NONE | CONSUME |
| non_functional_requirements.md | OWN | CONSUME | REFERENCE | REFERENCE | REFERENCE | CONSUME |
| ui_observations.md | OWN | CONSUME | CONSUME | NONE | NONE | REFERENCE |
| screen_elements.md | OWN | CONSUME | CONSUME | CONSUME | CONSUME | CONSUME |
| business_rules.md | OWN | CONSUME | CONSUME | CONSUME | CONSUME | CONSUME |
| data_requirements.md | OWN | CONSUME | CONSUME | CONSUME | CONSUME | CONSUME |
| glossary.md | OWN | CONSUME | CONSUME | CONSUME | CONSUME | CONSUME |
| traceability.md | OWN | CONSUME | NONE | CONSUME | NONE | CONSUME |
| personas.md | OWN | CONSUME | CONSUME | CONSUME | CONSUME | CONSUME |
| business_process_flows.md | OWN | CONSUME | CONSUME | CONSUME | CONSUME | CONSUME |
| figma_design_intake.md | OWN | CONSUME | CONSUME | NONE | NONE | NONE |

### 3.2 Solution Architect Artifacts

| Artifact | BA | SA | UX | BE | DB | QA |
|----------|----|----|----|----|----|----|
| architecture-design.md | NONE | OWN | CONSUME | CONSUME | REFERENCE | REFERENCE |
| module-design.md | NONE | OWN | CONSUME | CONSUME | CONSUME | CONSUME |
| tdd.md | NONE | OWN | CONSUME | CONSUME | CONSUME | CONSUME |
| lld.md | NONE | OWN | REFERENCE | CONSUME | CONSUME | REFERENCE |
| api-specifications.md | NONE | OWN | REFERENCE | EXTEND | REFERENCE | CONSUME |
| user-flow-specification.md | NONE | OWN | CONSUME | CONSUME | REFERENCE | CONSUME |
| data-dictionary.md | NONE | OWN | REFERENCE | CONSUME | CONSUME | CONSUME |
| security-architecture.md | NONE | OWN | NONE | CONSUME | NONE | CONSUME |
| deployment-architecture.md | NONE | OWN | NONE | NONE | NONE | NONE |
| architecture-decision-records.md | NONE | OWN | REFERENCE | REFERENCE | REFERENCE | REFERENCE |
| database-strategy.md | NONE | OWN | NONE | REFERENCE | CONSUME | NONE |
| technology-stack.md | NONE | OWN | CONSUME | CONSUME | CONSUME | CONSUME |

### 3.3 UI/UX Developer Artifacts

| Artifact | BA | SA | UX | BE | DB | QA |
|----------|----|----|----|----|----|----|
| ui-specification.md | NONE | REFERENCE | OWN | REFERENCE | NONE | CONSUME |
| design-system.md | NONE | NONE | OWN | REFERENCE | NONE | REFERENCE |
| component-specification.md | NONE | NONE | OWN | REFERENCE | NONE | CONSUME |
| interaction-flow.md | NONE | NONE | OWN | REFERENCE | NONE | CONSUME |
| accessibility-report.md | NONE | NONE | OWN | NONE | NONE | CONSUME |
| frontend-handoff.md | NONE | NONE | OWN | CONSUME | NONE | REFERENCE |

### 3.4 Backend Developer Artifacts

| Artifact | BA | SA | UX | BE | DB | QA |
|----------|----|----|----|----|----|----|
| backend-design.md | NONE | NONE | NONE | OWN | REFERENCE | CONSUME |
| endpoint-implementation.md | NONE | NONE | NONE | OWN | NONE | CONSUME |
| business-logic.md | NONE | NONE | NONE | OWN | REFERENCE | CONSUME |
| validation-rules.md | NONE | NONE | NONE | OWN | CONSUME | REFERENCE |
| integration-implementation.md | NONE | NONE | NONE | OWN | CONSUME | REFERENCE |
| backend-spec.md | NONE | NONE | NONE | OWN | CONSUME | REFERENCE |
| backend-development-report.md | NONE | NONE | NONE | OWN | NONE | REFERENCE |

### 3.5 Database Developer Artifacts

| Artifact | BA | SA | UX | BE | DB | QA |
|----------|----|----|----|----|----|----|
| database-schema.md | NONE | REFERENCE | NONE | REFERENCE | OWN | CONSUME |
| er-diagram.md | NONE | REFERENCE | NONE | REFERENCE | OWN | CONSUME |
| migration-plan.md | NONE | NONE | NONE | REFERENCE | OWN | CONSUME |
| indexing-strategy.md | NONE | NONE | NONE | REFERENCE | OWN | CONSUME |
| seed-data-plan.md | NONE | NONE | NONE | NONE | OWN | CONSUME |
| database-report.md | NONE | NONE | NONE | NONE | OWN | REFERENCE |

### 3.6 QA Engineer Artifacts

| Artifact | BA | SA | UX | BE | DB | QA |
|----------|----|----|----|----|----|----|
| test-plan.md | NONE | NONE | NONE | NONE | NONE | OWN |
| unit-test-cases.md | NONE | NONE | NONE | NONE | NONE | OWN |
| integration-test-cases.md | NONE | NONE | NONE | NONE | NONE | OWN |
| system-test-cases.md | NONE | NONE | NONE | NONE | NONE | OWN |
| regression-test-plan.md | NONE | NONE | NONE | NONE | NONE | OWN |
| test-execution-report.md | NONE | NONE | NONE | NONE | NONE | OWN |

### 3.7 Per-Agent Governance Artifacts (Scoped)

Each agent owns its own scoped instance. No other agent may write to another agent's governance artifacts.

| Artifact | Status for Owning Agent | Status for Solution Architect | Status for All Others |
|----------|------------------------|-------------------------------|----------------------|
| quality-report.md | OWN | CONSUME | NONE |
| handoff-contract.md | OWN | CONSUME | NONE |
| openlog.md | OWN | CONSUME | NONE |



## 4. Conflict Resolution Protocol

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

*End of Artifact Ownership Matrix — Contract Version 1.0.0*
