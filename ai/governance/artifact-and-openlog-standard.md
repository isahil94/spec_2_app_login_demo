# Artifact and OpenLog Governance Standard

Document Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved  
Authority: Platform AI Governance Council

This document defines the shared standards for artifact ownership, handoffs, openlog management, and workflow governance across all agents and workflows.

## 5.1 Universal Handoff Contract (Mandatory)
Every agent output must end with a Handoff Contract section based on `ai/templates/handoff-contract.md`, including blocked paths.

Required structure:

1. Current Stage
- Agent and stage name.
- Execution outcome: completed, blocked, failed, or approval-required.

2. Inputs Consumed
- Artifacts and memory references consumed in this execution.
- Any missing required inputs.

3. Artifacts Produced
- Artifacts produced or updated, each marked: Generated | Updated | Not Applicable.

4. Artifacts Updated
- Any upstream artifacts read but not owned.

5. Next Agent(s)
- Primary next agent.
- Parallel agents if any.
- Preconditions before start.

6. Workflow Status
- READY | BLOCKED | WAITING_FOR_APPROVAL | FAILED
- Reason if not READY.

7. Dependencies
- Hard dependencies resolved.
- Soft dependencies and unresolved blockers.

8. Artifact Summary
- Table of each artifact: Generated | Already Exists | Not Applicable.

9. OpenLog Summary
- Blocking issues count.
- Approval required: Yes | No.
- See openlog.md for full detail.

10. Ready For Next Stage
- Readiness: Yes | No | Conditional.
- Conditions if Conditional.

Validation checklist:
- [ ] Required artifacts generated or marked Not Applicable.
- [ ] quality_report.md, handoff_contract.md, and openlog.md produced.
- [ ] No separate open-questions.md, assumptions.md, risks.md, approval-log.md, decision-log.md, or escalation-log.md created.
- [ ] Artifact ownership boundaries respected.
- [ ] Workflow Status reflects openlog.md state.

## 5.2 Universal OpenLog Standard (Mandatory)
Every agent must produce exactly one `openlog.md` artifact per execution. This is the ONLY governance artifact consumed by the Supervisor for workflow decisions and Human-in-the-Loop approvals.

`openlog.md` consolidates all of the following into a single append-only artifact:
- Open questions, assumptions, risks, decisions, escalations
- Governance violations (artifact ownership breaches)
- Human approval requests and final resolutions

Template: `ai/templates/openlog.md`

**Append-only rule (non-negotiable):**
Entries are never deleted or overwritten; each state change is appended with a timestamp.

**Open Question Lifecycle (mandatory sequence):**
```
NEW → UNDER_REVIEW → WAITING_FOR_APPROVAL → APPROVED/REJECTED → RESOLVED → CLOSED
```
No state may be skipped. The Lifecycle Status field drives all Supervisor routing.

**Mandatory OpenLog entry fields:**
- Entry ID
- Workflow ID
- Correlation ID
- Date
- Category
- Title
- Question
- Reason
- Priority
- Impact
- Blocking (Yes/No)
- Approval Required (Yes/No)
- Default Assumption
- Owner Agent
- Target Stage
- Related Artifact(s)
- Related Requirement(s)
- Related User Story(ies)
- Potential Risk
- Status
- Resolution
- Decision
- Decision By
- Decision Date

**Mandatory compact Workflow Status fields:**
- Workflow ID
- Current Stage
- Current State
- Open Items
- Blocking Items
- Pending HITL
- Next Agent
- Supervisor Action

**Priority vs Impact (both mandatory and independent):**
- Priority: urgency of decision (Critical | High | Medium | Low)
- Impact: combined outcome impact if unresolved (High | Medium | Low)

**Mandatory rules:**
1. Never create separate open-questions.md, assumptions.md, risks.md, approval-log.md, decision-log.md, or escalation-log.md files.
2. Every open question, assumption, risk, decision, escalation, and governance violation must appear in openlog.md.
3. The Summary Workflow Status field is the Supervisor routing field.

**Deterministic Supervisor routing rules:**
Supervisor decisions must depend only on: Blocking, Approval Required, Status, Priority.
- Blocking = Yes AND Approval Required = Yes AND Status = WAITING_FOR_APPROVAL → WAITING_FOR_APPROVAL: pause, Human Approval Request.
- Blocking = Yes AND Status IN (NEW, UNDER_REVIEW, APPROVED, REJECTED) → BLOCKED: pause, resolve internally.
- Multiple blocking items: process by Priority (Critical > High > Medium > Low).
- No blocking items → READY: continue automatically.
- Unrecoverable → FAILED: escalate to recovery path.

**Human Approval post-processing:**
After Human decision, Supervisor appends to the item's History in openlog.md:
- Lifecycle Status: APPROVED or REJECTED
- Decision By, Decision Date, Resolution
The originating agent then progresses to RESOLVED → CLOSED.

## 5.2.1 AI Usage Tracking (Mandatory)
Agents must include an AI Usage section in both `quality_report.md` and `handoff_contract.md`.

AI Usage policy:
- Metadata only.
- No narrative explanations.

Populate when available, otherwise use `N/A` or `Estimated`:
- Workflow ID
- Correlation ID
- Agent Name
- Stage Name
- Model Name
- Model Provider
- Session ID
- Start Time
- End Time
- Duration
- Input Tokens
- Output Tokens
- Total Tokens
- Estimated Cost
- Retry Count
- Status
- Blocking Reason

Supervisor aggregate (per workflow):
- Agent
- Model
- Duration
- Input
- Output
- Total Tokens
- Estimated Cost
- Status

Workflow totals:
- Total Agents
- Successful
- Failed
- Blocked
- Total Duration
- Total Input Tokens
- Total Output Tokens
- Total Tokens
- Estimated Total Cost

## 5.2.2 Mandatory Schema Sections for All Agents
Every agent must use identical required section structure for the following artifacts:

1. `openlog.md`
- Workflow Status
- Open Items (entries containing all mandatory OpenLog fields)

2. `handoff_contract.md`
- Workflow Context (Workflow ID, Correlation ID, Agent, Stage)
- Artifacts Produced
- Artifact Status (Created/Updated/Skipped)
- OpenLog Summary
- AI Usage Summary
- Workflow Status
- Next Agent

3. `quality_report.md`
- Validation Summary
- Coverage Summary
- OpenLog Summary
- AI Usage Summary
- Confidence Score
- Readiness
- Blocking Issues

## 5.3 Artifact-First Response Policy (Mandatory)
All agents must persist outputs to owned artifact files before presenting any response content.

Response mode requirements:

1. Do not return full inline analysis, full requirement bodies, or full design/code content in chat responses.
2. Update or create required artifacts first.
3. Return only an execution summary containing:
- Updated artifact paths
- Per-artifact status (created, updated, unchanged, blocked)
- Open Question Summary values
- Workflow Status
- Next Agent or approval path
4. If artifact write fails, report the failure explicitly and do not present generated content as final.
5. Handoff Contract remains required but must reference artifact locations instead of restating artifact bodies.

Forbidden response pattern:
- Long-form inline deliverables that are not persisted as artifacts.

Required response pattern:
- Artifact update confirmation with concise operational summary.

## 5.4 Business Analyst Separation of Responsibilities (Mandatory)
When acting as Business Analyst, outputs must describe WHAT the business needs and must not describe HOW implementation is performed.

This section applies specifically to Business Analyst. For all other agents, see `ai/contracts/artifact-ownership-matrix.md` for their respective scope boundaries.

Business Analyst allowed output categories:
- Business goals and stakeholders
- Functional and non-functional requirements
- Business rules, user stories, use cases, acceptance criteria
- MoSCoW prioritization and traceability
- Risks, assumptions, open questions
- Business capability requirements
- Figma-based UI observations
- Conceptual business data model

Business Analyst required artifact package (16 total):
1. requirements_spec.md
2. user_stories.md
3. acceptance_criteria.md
4. non_functional_requirements.md
5. ui_observations.md
6. figma_design_intake.md
7. screen_elements.md
8. personas.md
9. business_process_flows.md
10. business_rules.md
11. data_requirements.md
12. glossary.md
13. traceability.md
14. quality_report.md
15. handoff_contract.md
16. openlog.md

Business Analyst completion contract:
- Every Epic, Feature, and User Story must be covered by complete business requirements.
- Each Feature must define applicable business rules, validation rules, permissions, visibility rules, workflow/state transitions, scenario behavior, and data constraints where relevant.
- Every Functional Requirement must map to one or more User Stories.
- Every User Story must have measurable Acceptance Criteria covering happy path, alternate path, validation, error, edge, authorization, and state transitions.
- UI behavior must be specified as business requirements without implementation detail.
- No duplicate or conflicting requirements may remain unresolved.

Business Analyst consolidation rule:
- Merge overview, goals, scope, stakeholder summary, functional requirements, epics, features, user story summary, business rules summary, business capability requirements, conceptual business data model, stable assumptions, risks, and glossary into requirements_spec.md.
- Do not split these into separate BA artifacts.

Figma propagation rule:
- If a Figma URL exists anywhere in `specification.md`, consume it automatically as an input.
- Preserve the URL unchanged through BA outputs.
- Do not ask for the Figma URL again.

Duplication control rule:
- Keep acceptance criteria centralized in `acceptance_criteria.md`.
- `user_stories.md` may reference acceptance criteria IDs but must not duplicate criteria content.

Business Analyst prohibited output categories:
- API endpoints and HTTP methods
- Request/response payloads, DTOs, schemas
- Authentication implementation choices (JWT, OAuth, token strategy)
- Technology or framework selections
- Architecture or component design decisions
- Physical database design (tables, columns, indexes, SQL, migrations)
- Implementation logic, deployment, CI/CD, infrastructure details

If prohibited content appears, the affected section is invalid and must be regenerated before publication.

Handoff contract constraints:

1. Do not restate entire artifact contents.
2. Keep the handoff concise and evidence-based.
3. Keep wording role-appropriate.
4. Do not claim outputs, validations, events, or updates that did not occur.
5. If execution is blocked, the handoff contract must still be complete.

## 10. Artifact Rules
Artifacts are governed deliverables, not informal notes.

1. Ownership
Each artifact type has exactly one owner. Before generating any artifact, every agent must consult `ai/contracts/artifact-ownership-matrix.md` to confirm ownership. Generating an artifact owned by another agent is a critical guardrail violation.

2. Ownership Verification (Mandatory Pre-Generation Check)
Before producing any artifact:
  a. Confirm the artifact type appears in your Owns list in `ai/contracts/artifact-ownership-matrix.md`.
  b. Confirm the artifact type does NOT appear in another agent's Owns list.
  c. If check (a) fails: stop, identify the owning agent, record a Cross-Agent Dependency in the Handoff Contract, and do not generate the artifact.
  d. Only extend artifacts explicitly marked as May Extend = Yes in the matrix.

3. Versioning
All updates must follow approved version semantics.

4. Publishing
Only validated and complete artifacts may be published.

5. Validation
Artifacts must pass structure, dependency, and contract checks.

6. Traceability
Each artifact must reference relevant upstream sources.

7. Dependencies
Dependencies must be explicit, resolvable, and compatible.

8. Retention
Follow retention and archival policy. Do not delete arbitrarily.

Artifact discipline expectations:

1. No orphan artifacts without lineage.
2. No anonymous artifacts without ownership metadata.
3. No publish action without readiness evidence.
4. No downstream dependency unlock on invalid outputs.
5. No agent generates artifacts outside its ownership scope in `ai/contracts/artifact-ownership-matrix.md`.

## 11. Memory Rules
Memory stores context continuity and execution history.

1. Workflow memory
Maintain workflow-level pointers and lifecycle context references.

2. Shared memory
Store cross-stage context safely and consistently.

3. Execution history
Record retries, outcomes, and transition rationale.

4. Context retrieval
Read relevant memory before decision-making.

5. Memory updates
Write deterministic, scoped, and attributable updates.

6. Consistency
Prevent stale, conflicting, or untraceable memory state.

Memory safety rules:

1. Do not write outside authorized scope.
2. Do not replace validated context with speculative notes.
3. Do not omit memory updates required for recovery and audit.

---

**Inheritance Rule:** Every agent must load sections 5.1-5.4, 10, and 11 from this document before execution. This is mandatory and non-negotiable.
