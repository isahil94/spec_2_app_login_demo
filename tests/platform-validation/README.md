# Platform Validation Framework

## Purpose
Provide a reusable, manual validation suite for full-platform integrity, consistency, and readiness after configuration or code changes.

## Validation Order
1. 01-repository-validation.md
2. 02-chatmode-validation.md
3. 03-agent-validation.md
4. 04-skill-validation.md
5. 05-tool-validation.md
6. 06-template-validation.md
7. 07-contract-validation.md
8. 08-hook-validation.md
9. 09-workflow-validation.md
10. 10-artifact-validation.md
11. 11-observability-validation.md
12. 12-end-to-end-validation.md
13. regression-checklist.md

## How To Execute
- Review prerequisites in each validation document.
- Execute checks in sequence.
- Mark each checklist item as pass or fail.
- Record blockers and remediation actions.
- Complete overall status in regression-checklist.md.

## Completion Criteria
- All category checklists are completed.
- No unresolved blocking failures remain.
- Regression checklist is marked PASS.

## Notes
- This suite validates platform behavior and governance, not application unit logic.
- Keep validation evidence concise and auditable.
