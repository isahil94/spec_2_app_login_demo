# Artifact Contracts

Contract Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved

## 1. Purpose and Scope
This document defines the artifact contracts used by the Agentic SDLC platform. It standardizes ownership, structure, validation, versioning, and lifecycle for all workflow artifacts.

This contract is implementation-independent and applies to all agents, the Supervisor, and orchestration services.

Related contracts:
- artifact-ownership-matrix.md (authoritative per-agent ownership table — consult before generating any artifact)
- event-contracts.md
- workflow-state.md
- memory-contract.md
- validation-contract.md
- quality-report-contract.md

## 2. Normative Terms
- Artifact: A persisted, versioned deliverable produced by exactly one owner agent.
- Owner Agent: The single agent responsible for authoring and publishing an artifact.
- Consumer Agent: Any agent that reads an artifact.
- Artifact Reference: A pointer to an artifact location and version; never artifact content.
- Workflow: End-to-end execution from specification input to documentation output.

## 3. Global Artifact Rules
1. Each artifact has exactly one owner.
2. Agents may read any artifact but must never overwrite artifacts owned by another agent.
3. Any update to an artifact creates a new semantic version.
4. Artifact metadata is mandatory and immutable after publication except status fields managed by Supervisor.
5. Artifacts are immutable after status Published; corrections require a new version.
6. Artifact content must pass validation-contract.md before publication.

## 4. Common Artifact Envelope (Required for Every Artifact)
All artifacts include the following metadata block.

Required fields:
- artifactId: Globally unique artifact identifier.
- artifactType: Contracted artifact name (for example, requirements.md).
- workflowId: Workflow identifier.
- executionId: Execution identifier.
- ownerAgentId: Owning agent identifier.
- version: Semantic version in MAJOR.MINOR.PATCH.
- status: Draft | Validated | Published | Deprecated | Archived.
- createdAt: ISO-8601 timestamp.
- updatedAt: ISO-8601 timestamp.
- inputReferences: List of artifact references used to produce this artifact.
- checksum: Content integrity hash.

Optional fields:
- tags: Classification tags.
- supersedes: Prior artifact version reference.
- qualityReportRef: Reference to quality report artifact.
- approvalRef: Reference to approval request/response.

Example structure:
```yaml
metadata:
  artifactId: art-architecture-0007
  artifactType: architecture.md
  workflowId: wf-2026-06-30-001
  executionId: exec-0142
  ownerAgentId: solution-architect
  version: 1.2.0
  status: Published
  createdAt: 2026-06-30T09:12:11Z
  updatedAt: 2026-06-30T09:38:44Z
  inputReferences:
    - artifactId: art-requirements-0003
      version: 1.0.0
  checksum: sha256:9f2d...
  tags: [architecture, baseline]
  qualityReportRef: qr-solution-architect-0142
content:
  ...
```

## 5. Standard Versioning and Lifecycle
Versioning (applies to all artifacts):
- MAJOR: Breaking structural or semantic contract changes.
- MINOR: Backward-compatible content expansion.
- PATCH: Corrections with no contract break.

Lifecycle (applies to all artifacts):
1. Draft
2. Validated
3. Published
4. Deprecated (optional)
5. Archived

## 6. Artifact Catalog and Ownership

| Artifact | Purpose | Owner Agent | Consuming Agents | File Format |
|---|---|---|---|---|
| specification.md | Canonical product specification input | Supervisor | Business Analyst, Solution Architect, all downstream agents | Markdown |
| requirements_spec.md | Master business specification including document control, goals, scope, epics, features, functional requirements, business rules, glossary, stable assumptions, and out-of-scope | Business Analyst | Solution Architect, QA Engineer, Reviewer | Markdown |
| user_stories.md | Implementation-ready user stories with scenarios, dependencies, and references (without duplicated acceptance criteria) | Business Analyst | Solution Architect, UI/UX Developer, Backend Developer, QA Engineer | Markdown |
| acceptance_criteria.md | Single source of truth for acceptance criteria organized by user story | Business Analyst | Solution Architect, QA Engineer, Reviewer, DevOps & Release | Markdown |
| non_functional_requirements.md | Non-functional requirement package grouped by required quality domains | Business Analyst | Solution Architect, QA Engineer, Reviewer | Markdown |
| ui_observations.md | UI observations from optional Figma URL detected in specification.md (or skipped silently when absent) | Business Analyst | UI/UX Developer, Solution Architect, QA Engineer | Markdown |
| openlog.md | Structured append-only governance log and workflow status | Business Analyst | Supervisor, Solution Architect, QA Engineer | Markdown |
| traceability.md | Requirement-to-story-to-acceptance traceability matrix | Business Analyst | Solution Architect, QA Engineer, Reviewer | Markdown |
| quality_report.md | BA completeness, consistency, traceability, validation, and readiness report | Business Analyst | Supervisor, Solution Architect, Reviewer | Markdown |
| handoff_contract.md | Standardized BA handoff contract to next stage with coverage and readiness fields | Business Analyst | Supervisor, Solution Architect | Markdown |
| architecture.md | End-to-end solution architecture and decisions | Solution Architect | UI/UX Developer, Backend Developer, Database Developer, QA Engineer, Reviewer | Markdown |
| api-contracts.md | Service interface contracts and error models | Solution Architect | Backend Developer, QA Engineer, Documentation | Markdown |
| database-schema.md | Logical and physical data model definition | Database Developer | Backend Developer, QA Engineer, Documentation | Markdown |
| frontend-spec.md | UI structure, interaction, accessibility, design constraints | UI/UX Developer | Backend Developer, QA Engineer, Reviewer, Documentation | Markdown |
| backend-spec.md | Service behavior, use cases, and integration mapping | Backend Developer | QA Engineer, Reviewer, DevOps & Release, Documentation | Markdown |
| qa-report.md | Verification results, defects, and quality decision | QA Engineer | Reviewer, Supervisor, DevOps & Release | Markdown |
| review-report.md | Independent quality and governance assessment | Reviewer | Supervisor, DevOps & Release, Documentation | Markdown |
| release-notes.md | Deployment summary, changes, risk, rollback notes | DevOps & Release | Documentation, Supervisor | Markdown |
| readme.md | End-user and operator usage documentation | Documentation | Supervisor, operators, maintainers | Markdown |

## 7. Artifact-Specific Contracts

Business Analyst consolidation policy:
- BA artifact contracts are limited to `requirements_spec.md`, `user_stories.md`, `acceptance_criteria.md`, `non_functional_requirements.md`, `ui_observations.md`, `traceability.md`, `quality_report.md`, `handoff_contract.md`, and `openlog.md`.
- Figma URL, when present, is consumed from `specification.md` and propagated unchanged in BA handoff.
- Acceptance criteria remain centralized in `acceptance_criteria.md`; user stories must reference but not duplicate.

### 7.1 specification.md
- Name: specification.md
- Purpose: Defines product intent, scope, constraints, and non-goals.
- Owner Agent: Supervisor
- Consuming Agents: All delivery agents through workflow progression.
- File Format: Markdown
- Validation Rules: Must include business context, scope, constraints, success criteria, and source references.
- Versioning: Semantic versioning.
- Lifecycle: Draft -> Validated -> Published -> Archived.
- Required Fields: productVision, problemStatement, scopeIn, scopeOut, constraints, successMetrics.
- Optional Fields: figmaReference, complianceContext, migrationNotes.
- Example Structure:
```yaml
content:
  productVision: "Deliver a task management platform for enterprise teams"
  problemStatement: "Manual tracking causes missed deadlines"
  scopeIn: [authentication, projects, tasks, comments, labels, notifications, dashboard]
  scopeOut: [third-party marketplace]
  constraints: [local-first, single-runtime, approval-via-supervisor]
  successMetrics:
    - "P95 task creation < 500ms"
```

### 7.2 requirements_spec.md
- Name: requirements_spec.md
- Purpose: Master business specification containing document control, business goals, scope, stakeholders, context, epics, features, functional requirements, business rules, glossary, stable assumptions, and out-of-scope boundaries.
- Owner Agent: Business Analyst
- Consuming Agents: Solution Architect, QA Engineer, Reviewer.
- File Format: Markdown
- Validation Rules: Epics and features must remain inside this artifact and link to functional requirements.

### 7.3 user_stories.md
- Name: user_stories.md
- Purpose: Implementation-ready user stories with scenarios, dependencies, validation rules, and screen references.
- Owner Agent: Business Analyst
- Consuming Agents: Solution Architect, UI/UX Developer, Backend Developer, QA Engineer.
- File Format: Markdown
- Validation Rules: Stories include required fields and reference acceptance criteria without duplication.

### 7.4 acceptance_criteria.md
- Name: acceptance_criteria.md
- Purpose: Single source of truth for acceptance criteria organized by user story.
- Owner Agent: Business Analyst
- Consuming Agents: Solution Architect, QA Engineer, Reviewer, DevOps & Release.
- File Format: Markdown
- Validation Rules: Acceptance criteria are atomic, measurable, and grouped under story identifiers.

### 7.5 non_functional_requirements.md
- Name: non_functional_requirements.md
- Purpose: Business-level NFR package across performance, security, scalability, availability, reliability, accessibility, maintainability, compliance, logging, audit, and observability.
- Owner Agent: Business Analyst
- Consuming Agents: Solution Architect, QA Engineer, Reviewer.
- File Format: Markdown

### 7.6 ui_observations.md
- Name: ui_observations.md
- Purpose: UI analysis from optional Figma URL input covering screens, navigation flow, components, accessibility, missing elements, consistency, and recommendations.
- Owner Agent: Business Analyst
- Consuming Agents: UI/UX Developer, Solution Architect, QA Engineer.
- File Format: Markdown
- Validation Rules: Figma URL is consumed from `specification.md` when present and preserved unchanged.

### 7.7 traceability.md
- Name: traceability.md
- Purpose: End-to-end matrix across Epic -> Feature -> Functional Requirement -> User Story -> Acceptance Criteria -> Architecture Module -> API Contract -> Database Entity -> UI Screen -> Test Case.
- Owner Agent: Business Analyst
- Consuming Agents: Solution Architect, QA Engineer, Reviewer.
- File Format: Markdown
- Validation Rules: Missing links are explicitly identified.

### 7.8 quality_report.md, handoff_contract.md, openlog.md
- Names: quality_report.md, handoff_contract.md, openlog.md
- Purpose: Quality/readiness validation, stage handoff contract, and append-only governance log.
- Owner Agent: Business Analyst
- Consuming Agents: Supervisor, Solution Architect, Reviewer.
- File Format: Markdown
- Validation Rules:
  - quality_report.md validates coverage and readiness.
  - quality_report.md includes AI Usage (stage record, supervisor aggregate, workflow totals) and uses N/A or Estimated when unavailable.
  - handoff_contract.md includes artifact, coverage, open-question, blocking, status, next-agent fields, and AI Usage (stage record, supervisor aggregate, workflow totals).
  - openlog.md is the exclusive append-only governance artifact.

### 7.9 architecture.md
- Name: architecture.md
- Purpose: Defines system architecture, components, contracts, and decisions.
- Owner Agent: Solution Architect
- Consuming Agents: UI/UX Developer, Backend Developer, Database Developer, QA Engineer, Reviewer.
- File Format: Markdown
- Validation Rules: Must define boundaries, interfaces, data flow, and non-functional decisions.
- Versioning: Semantic versioning.
- Lifecycle: Draft -> Validated -> Published -> Archived.
- Required Fields: components, interactions, decisions, constraints, nfrAlignment.
- Optional Fields: alternativesConsidered, tradeOffs.
- Example Structure:
```yaml
content:
  components: [supervisor, event-bus, memory-service, approval-service]
  interactions:
    - "Supervisor emits events to event-bus"
  decisions:
    - id: ADR-004
      title: "Artifact immutability after publication"
```

### 7.10 api-contracts.md
- Name: api-contracts.md
- Purpose: Defines operation contracts, request/response schemas, and error semantics.
- Owner Agent: Solution Architect
- Consuming Agents: Backend Developer, QA Engineer, Documentation.
- File Format: Markdown
- Validation Rules: Every operation has schema, error codes, and version compatibility notes.
- Versioning: Semantic versioning.
- Lifecycle: Draft -> Validated -> Published -> Archived.
- Required Fields: apis[], operationId, inputSchema, outputSchema, errorModel.
- Optional Fields: idempotencyRules, rateConstraints.
- Example Structure:
```yaml
content:
  apis:
    - operationId: createTask
      inputSchema: "TaskCreateRequest v1"
      outputSchema: "TaskResponse v1"
      errorModel: [VALIDATION_ERROR, CONFLICT, INTERNAL_ERROR]
```

### 7.11 database-schema.md
- Name: database-schema.md
- Purpose: Defines entities, relations, constraints, indexes, and migration semantics.
- Owner Agent: Database Developer
- Consuming Agents: Backend Developer, QA Engineer, Documentation.
- File Format: Markdown
- Validation Rules: Keys, constraints, and referential integrity must be explicit.
- Versioning: Semantic versioning.
- Lifecycle: Draft -> Validated -> Published -> Archived.
- Required Fields: entities[], attributes, keys, relations, constraints.
- Optional Fields: indexingStrategy, archivalPolicy.
- Example Structure:
```yaml
content:
  entities:
    - name: Task
      keys: [taskId]
      relations:
        - type: many-to-one
          target: Project
```

### 7.12 frontend-spec.md
- Name: frontend-spec.md
- Purpose: Defines UI behaviors, component contracts, accessibility and UX rules.
- Owner Agent: UI/UX Developer
- Consuming Agents: Backend Developer, QA Engineer, Reviewer, Documentation.
- File Format: Markdown
- Validation Rules: Must include interaction flows, state behavior, and accessibility criteria.
- Versioning: Semantic versioning.
- Lifecycle: Draft -> Validated -> Published -> Archived.
- Required Fields: screens, components, interactions, accessibility, dataBindings.
- Optional Fields: motionGuidelines, localizationNotes.
- Example Structure:
```yaml
content:
  screens:
    - name: Dashboard
      components: [TaskSummary, ActivityFeed]
  accessibility:
    wcagLevel: "AA"
```

### 7.13 backend-spec.md
- Name: backend-spec.md
- Purpose: Defines domain services, workflows, integrations, and operational behavior.
- Owner Agent: Backend Developer
- Consuming Agents: QA Engineer, Reviewer, DevOps & Release, Documentation.
- File Format: Markdown
- Validation Rules: Must align with api-contracts.md, database-schema.md, and business rules.
- Versioning: Semantic versioning.
- Lifecycle: Draft -> Validated -> Published -> Archived.
- Required Fields: services, workflows, errorHandling, observability, dependencies.
- Optional Fields: performanceBudgets, failoverNotes.
- Example Structure:
```yaml
content:
  services:
    - name: TaskService
      responsibilities: [create, update, assign]
  observability:
    metrics: [task_create_latency, task_create_error_rate]
```

### 7.14 qa-report.md
- Name: qa-report.md
- Purpose: Records validation outcomes and release readiness from QA.
- Owner Agent: QA Engineer
- Consuming Agents: Reviewer, Supervisor, DevOps & Release.
- File Format: Markdown
- Validation Rules: Must include pass/fail evidence and defect classification.
- Versioning: Semantic versioning.
- Lifecycle: Draft -> Validated -> Published -> Archived.
- Required Fields: testSummary, defects, coverage, traceability, recommendation.
- Optional Fields: flakyTests, environmentNotes.
- Example Structure:
```yaml
content:
  testSummary:
    passed: 128
    failed: 4
  defects:
    - id: BUG-441
      severity: High
      status: Open
  recommendation: "Conditional go"
```

### 7.15 review-report.md
- Name: review-report.md
- Purpose: Independent governance and quality review before release.
- Owner Agent: Reviewer
- Consuming Agents: Supervisor, DevOps & Release, Documentation.
- File Format: Markdown
- Validation Rules: Must evaluate architecture, security, quality, and policy compliance.
- Versioning: Semantic versioning.
- Lifecycle: Draft -> Validated -> Published -> Archived.
- Required Fields: findings, riskAssessment, complianceStatus, decision.
- Optional Fields: waiverRequests, remediationPlan.
- Example Structure:
```yaml
content:
  findings:
    - id: REV-09
      severity: Medium
      description: "Missing rollback runbook detail"
  decision: "Approve with conditions"
```

### 7.16 release-notes.md
- Name: release-notes.md
- Purpose: Captures release scope, risk, and operational instructions.
- Owner Agent: DevOps & Release
- Consuming Agents: Documentation, Supervisor.
- File Format: Markdown
- Validation Rules: Must include included artifacts, deployment plan, rollback plan, and known issues.
- Versioning: Semantic versioning.
- Lifecycle: Draft -> Validated -> Published -> Archived.
- Required Fields: releaseScope, deploymentSteps, rollbackSteps, knownIssues, approvals.
- Optional Fields: maintenanceWindow, postReleaseChecks.
- Example Structure:
```yaml
content:
  releaseScope: [backend-spec.md@1.3.0, frontend-spec.md@1.2.1]
  deploymentSteps:
    - "Apply schema migrations"
    - "Deploy runtime"
  rollbackSteps:
    - "Restore previous runtime package"
```

### 7.17 readme.md
- Name: readme.md
- Purpose: Final operational and user-facing documentation.
- Owner Agent: Documentation
- Consuming Agents: Supervisor and all human operators.
- File Format: Markdown
- Validation Rules: Must include setup, run, troubleshooting, and contract references.
- Versioning: Semantic versioning.
- Lifecycle: Draft -> Validated -> Published -> Archived.
- Required Fields: overview, prerequisites, setup, run, troubleshooting, references.
- Optional Fields: faq, architectureSummary.
- Example Structure:
```yaml
content:
  overview: "Task Management System"
  prerequisites: ["local runtime", "configured models"]
  setup:
    - "Load specification"
    - "Run supervisor workflow"
```

## 8. Ownership Enforcement
1. Owner-only write: Only owner agent can create or publish new versions for its artifact type.
2. Consumer read-only: Consumer agents can reference but cannot mutate owner artifacts.
3. Supervisor exception: Supervisor may change artifact status only for governance transitions (for example, Deprecated, Archived) with audit trail.

## 9. Traceability Requirements
Every artifact must include:
- Input artifact references with versions.
- Requirement and story links where applicable.
- Quality report reference.
- Approval reference when generated under blocked or exception conditions.

## 10. Compatibility and Change Control
- Contract-breaking changes require MAJOR version increments and Supervisor approval.
- Non-breaking field additions require MINOR version increments.
- Editorial fixes require PATCH increments.
- Consumers must declare supported major versions for each artifact type.
