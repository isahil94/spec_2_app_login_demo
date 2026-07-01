# Prompt Engineering Standard

Document Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved and Mandatory  
Authority: Prompt Engineering Council  
Scope: All prompt templates under the platform runtime

## 1. Purpose
This document defines the official standard for prompt engineering across the platform. It governs how prompt templates are designed, versioned, reviewed, tested, optimized, and evolved.

Role of prompts in this platform:
- Prompts are runtime execution templates.
- Prompts guide task framing, output framing, and reasoning discipline.
- Prompts do not define platform policy, agent identity, or hard governance constraints.

Boundary definitions:
- Agent Definition: stable role contract describing mission, scope, and responsibilities.
- Prompt Template: versioned execution template used by runtime for a specific agent role and context.
- Instructions: global behavioral guidance applied across agents.
- Guardrails: mandatory non-negotiable constraints that override prompts.
- Skills: reusable capability contracts describing what agents can do.
- Hooks: runtime lifecycle execution points that inject common behavior.

Why prompts are versioned separately from agents:
- Agent identity should remain stable while prompt execution strategy improves.
- Prompt iteration should be controlled without redefining role ownership.
- Compatibility and rollback are easier when template changes are isolated.
- Auditability improves when template evolution is independent and traceable.

## 2. Prompt Architecture
The runtime assembles a final prompt from multiple governed layers.

Component responsibilities:
- Global Instructions: baseline platform behavior and shared execution expectations.
- Guardrails: hard safety, governance, quality, and compliance boundaries.
- Agent Definition: role-specific mission, responsibilities, and outputs.
- Versioned Prompt Template: task execution framing for the current run.
- Workflow Context: stage, state, dependencies, and goals for current lifecycle step.
- Memory: historical context, previous decisions, and continuity references.
- Artifacts: upstream deliverables and current target outputs.
- Runtime Variables: execution metadata and dynamic context values.

Conceptual prompt assembly flow:
1. Load global governance layers.
2. Load agent role definition.
3. Load selected prompt template version.
4. Attach workflow and execution context.
5. Attach relevant memory and artifacts.
6. Inject runtime variables.
7. Produce final assembled prompt payload.

Assembly rule:
- Higher-order governance constraints always override template preferences.

## 3. Prompt Directory Structure
Standard structure:

```text
ai/prompts/
    README.md
    supervisor/
        v1.0.md
        CHANGELOG.md
    business-analyst/
        v1.0.md
        CHANGELOG.md
    solution-architect/
        v1.0.md
        CHANGELOG.md
    ui-ux-developer/
        v1.0.md
        CHANGELOG.md
    backend-developer/
        v1.0.md
        CHANGELOG.md
    database-developer/
        v1.0.md
        CHANGELOG.md
    qa-engineer/
        v1.0.md
        CHANGELOG.md
    reviewer/
        v1.0.md
        CHANGELOG.md
    devops-release/
        v1.0.md
        CHANGELOG.md
    documentation/
        v1.0.md
        CHANGELOG.md
```

File purposes:
- README.md: authoritative platform-wide prompt engineering standard.
- v1.0.md: one concrete template version for a specific role.
- CHANGELOG.md: version history and rationale for changes.

Structure governance:
- One folder per agent role.
- One changelog per role prompt family.
- Version files must remain immutable once released.

## 4. Prompt Versioning Strategy
Versioning follows semantic intent.

Major versions:
- Introduce significant structural changes or behavior framing shifts.
- May require controlled migration planning.

Minor versions:
- Add compatible capabilities, clarity improvements, or scoped enhancements.
- Preserve existing intent and compatibility expectations.

Patch versions:
- Correct defects, ambiguity, wording errors, or minor quality issues.
- Must not alter core behavioral intent.

Backward compatibility:
- New versions should not break active workflows without governed migration.
- Existing stable workflows may continue on prior compatible versions.

Deprecation:
- Deprecated versions remain traceable and documented.
- Deprecation should include replacement guidance and timeline.

Replacement strategy:
- Promote new versions through controlled rollout.
- Keep prior versions available during migration windows.

When to create a new version:
- Meaningful change in execution expectations.
- New required output framing.
- Significant quality or determinism improvement.
- Governance-driven correction requiring explicit traceability.

## 5. Prompt Composition
Recommended template structure for all role prompts:
- Purpose: scope and intent of the template.
- Execution Context: situational boundaries and stage relevance.
- Primary Objective: what must be achieved.
- Execution Expectations: mandatory behavior and output discipline.
- Reasoning Guidance: controlled reasoning principles.
- Artifact Expectations: required deliverable shape and quality.
- Quality Expectations: acceptance thresholds and readiness indicators.
- Completion Requirements: explicit done criteria.

Composition rules:
- Keep sections explicit and consistently ordered.
- Keep requirements measurable and non-ambiguous.
- Keep role scope clear to avoid cross-role bleed.

## 6. Runtime Variables
Runtime variables provide dynamic context at execution time.

Common variable categories:
- Workflow ID
- Current Stage
- Agent Name
- Inputs
- Artifacts
- Memory
- Configuration
- Platform Settings
- Execution Metadata

Injection principles:
- Variables must be reliable and current.
- Variable meaning must be stable across versions.
- Variable availability assumptions must be explicit.
- Missing critical variables must trigger controlled failure handling.

Safety expectations:
- Variables must not bypass governance boundaries.
- Sensitive values must be handled under security policy.

## 7. Prompt Design Principles
Clarity:
- Use precise language and explicit expectations.

Determinism:
- Equivalent context should produce equivalent output framing.

Minimal ambiguity:
- Avoid vague instruction phrasing and implied assumptions.

Consistency:
- Use standard structure, terminology, and severity language.

Reusability:
- Design templates to work across repeated executions in same role scope.

Maintainability:
- Keep templates modular and easy to update safely.

Modularity:
- Separate concerns clearly so updates are low-risk.

Production readiness:
- Templates must support enterprise quality, traceability, and auditability.

## 8. Prompt Review Process
Every prompt version must pass formal review before release.

Review criteria:
- Correctness: template intent aligns with role and workflow objective.
- Clarity: instructions are precise and unambiguous.
- Consistency: structure and terminology align with platform standards.
- Compliance with instructions: role-level and global instruction alignment.
- Compliance with guardrails: no conflict with hard governance constraints.
- Artifact alignment: output expectations match artifact contracts.
- Agent alignment: template reinforces role boundaries and responsibilities.

Review outcomes:
- Approved
- Approved with required corrections
- Rejected with remediation actions

## 9. Prompt Testing
Prompt validation is mandatory before adoption.

Testing scope:
- Functional testing: verify intended behavior framing.
- Regression testing: ensure previously stable behavior is preserved.
- Output quality evaluation: confirm quality and readiness framing is adequate.
- Determinism checks: confirm stable outcomes under equivalent context.
- Compatibility checks: verify compatibility with runtime assembly inputs.

Testing expectations:
- Test outcomes must be evidence-backed.
- Critical failures block release.
- Release readiness requires explicit pass decision.

## 10. Prompt Optimization
Prompt evolution must be controlled and evidence-driven.

Optimization practices:
- Continuous improvement through measured iterations.
- Performance monitoring of output quality and reliability.
- Feedback incorporation from review and runtime outcomes.
- Version comparisons to evaluate measurable benefit.
- Controlled experimentation with bounded impact and rollback readiness.

Optimization guardrails:
- Never optimize at the expense of governance compliance.
- Never introduce uncontrolled prompt drift.

## 11. Prompt Changelog Policy
Each role prompt folder must include a CHANGELOG.md.

Each entry should include:
- Version identifier
- Date
- Summary of changes
- Reason for change
- Compatibility notes
- Rollout or migration notes when relevant

Standard change labels:
- Added
- Changed
- Improved
- Fixed
- Deprecated
- Removed

Changelog quality rules:
- Entries must be factual and concise.
- Claims must be traceable to actual template changes.

## 12. Best Practices
- Keep prompts role-specific and scope-bound.
- Prefer explicit constraints over implied assumptions.
- Keep completion criteria measurable.
- Keep artifact expectations concrete and consistent.
- Keep prompts concise enough for reliable runtime use.
- Reuse proven section structures across prompt families.
- Align every template with instructions and guardrails.
- Preserve backward compatibility where possible.
- Treat changelogs as governance artifacts, not optional notes.
- Validate before release and monitor after release.

## 13. Common Mistakes
- Duplicating agent definitions inside prompt templates.
- Embedding business logic that belongs in architecture or code artifacts.
- Ignoring guardrail constraints.
- Creating overly long templates that reduce clarity.
- Hardcoding workflow assumptions that break in other stages.
- Breaking backward compatibility without migration policy.
- Mixing role scope and causing cross-agent responsibility bleed.
- Publishing prompt changes without testing and review evidence.

## 14. Future Evolution
New prompt versions should be introduced through controlled, compatible evolution.

Evolution approach:
- Add improvements incrementally and version explicitly.
- Preserve stable behavior contracts for active workflows.
- Support side-by-side version operation during migration.
- Deprecate with clear timelines and replacement guidance.
- Maintain complete traceability for audits and rollback.

Stability commitment:
- Prompt templates evolve continuously, but governance, safety, and role integrity remain constant.

This document is the authoritative standard governing all prompt templates in the platform.