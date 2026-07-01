# Purpose
Validate full repository integrity and structural consistency.

# Scope
Repository layout, naming conventions, canonical directories, and platform-level repository governance.

# Prerequisites
- [ ] Latest repository changes are pulled.
- [ ] Validation runner has read access to repository root.
- [ ] Canonical repository conventions are available for reference.

# Validation Steps
- [ ] Verify top-level structure is intact.
- [ ] Verify canonical directory naming and presence.
- [ ] Verify numbered agent files exist in ai/agents.
- [ ] Verify canonical chat modes exist in .github/chatmodes.
- [ ] Verify templates directory and template files exist.
- [ ] Verify contracts directory and contract files exist.
- [ ] Verify shared instructions exist.
- [ ] Verify prompts directory and expected prompts exist.
- [ ] Verify hooks directory and expected hook files exist.
- [ ] Verify skills directory and expected skill files exist.
- [ ] Verify scripts directory and expected scripts exist.
- [ ] Verify workflow-related directories and files exist.
- [ ] Verify VS Code tasks are defined and resolvable.
- [ ] Verify examples directory structure exists.
- [ ] Verify artifacts directory structure exists.
- [ ] Verify repository conventions are consistently applied.

# Expected Result
- [ ] 100% repository consistency.
- [ ] No missing canonical directories or required files.
- [ ] No duplicate or conflicting naming patterns.

# Failure Conditions
- [ ] Missing required directories or canonical files.
- [ ] Non-numbered duplicate agent definitions.
- [ ] Broken task or workflow references.
- [ ] Structural deviations from repository conventions.

# Recovery Actions
- [ ] Restore missing canonical files from source control.
- [ ] Remove duplicate or non-canonical files.
- [ ] Correct broken references and naming mismatches.
- [ ] Re-run repository validation after fixes.

# Pass / Fail Checklist
- [ ] PASS: All repository checks succeeded.
- [ ] FAIL: One or more repository checks failed.
- [ ] Blockers captured.
- [ ] Recovery actions assigned.

# Notes
- Keep changes minimal and in-place.
- Do not refactor unrelated structure during remediation.
