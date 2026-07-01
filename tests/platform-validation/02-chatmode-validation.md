# Purpose
Validate all canonical chat modes for integrity, linkage, and expected governance behavior.

# Scope
Supervisor, Business Analyst, Solution Architect, UI/UX Developer, Backend Developer, Database Developer, QA Engineer, Reviewer, Documentation, and DevOps chat modes.

# Prerequisites
- [ ] All canonical chat mode files are present.
- [ ] Numbered agent definitions are available.
- [ ] Referenced skills, templates, contracts, and instructions exist.

# Validation Steps
- [ ] Validate supervisor.chatmode.md loads and resolves references.
- [ ] Validate business-analyst.chatmode.md loads and resolves references.
- [ ] Validate solution-architect.chatmode.md loads and resolves references.
- [ ] Validate ui-ux-developer.chatmode.md loads and resolves references.
- [ ] Validate backend-developer.chatmode.md loads and resolves references.
- [ ] Validate database-developer.chatmode.md loads and resolves references.
- [ ] Validate qa-engineer.chatmode.md loads and resolves references.
- [ ] Validate reviewer.chatmode.md loads and resolves references.
- [ ] Validate documentation.chatmode.md loads and resolves references.
- [ ] Validate devops-release.chatmode.md loads and resolves references.
- [ ] Verify each chat mode references the correct numbered agent.
- [ ] Verify each chat mode references existing skills.
- [ ] Verify each chat mode references templates and contracts correctly.
- [ ] Verify instruction references resolve.
- [ ] Verify expected artifact ownership alignment.
- [ ] Verify expected downstream handoff alignment.

# Expected Result
- [ ] Every canonical chat mode loads successfully.
- [ ] No broken references across agents, skills, templates, contracts, or instructions.
- [ ] Ownership and handoff intent match platform governance.

# Failure Conditions
- [ ] Missing or broken chat mode references.
- [ ] Incorrect agent mapping.
- [ ] Ownership or handoff inconsistencies.

# Recovery Actions
- [ ] Correct invalid references in-place.
- [ ] Align chat mode links to canonical numbered agents.
- [ ] Re-run chat mode validation after corrections.

# Pass / Fail Checklist
- [ ] PASS: All chat mode validations succeeded.
- [ ] FAIL: One or more chat mode validations failed.
- [ ] Blockers captured.
- [ ] Recovery actions assigned.

# Notes
- Validate each chat mode individually and then as a full set.
