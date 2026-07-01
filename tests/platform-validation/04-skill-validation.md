# Purpose
Validate skill catalog integrity, references, and consistency across the platform.

# Scope
All skill definitions under ai/skills and all references from agents and chat modes.

# Prerequisites
- [ ] Skill files are available.
- [ ] Referencing agents and chat modes are available.

# Validation Steps
- [ ] Verify each skill file exists.
- [ ] Verify each referenced skill resolves from agents/chat modes.
- [ ] Verify naming consistency across skill definitions and references.
- [ ] Verify tool references in skills are valid.
- [ ] Verify no duplicate skills exist under alternate names.
- [ ] Verify no broken relative links in skill files.

# Expected Result
- [ ] Skills are complete, uniquely named, and reference-safe.
- [ ] No broken links or unresolved skill references.

# Failure Conditions
- [ ] Missing skill files.
- [ ] Unresolved skill references.
- [ ] Duplicate or conflicting skill naming.
- [ ] Broken links or invalid tool references.

# Recovery Actions
- [ ] Fix broken references and link targets.
- [ ] Consolidate duplicate skill definitions.
- [ ] Re-run skill validation after remediation.

# Pass / Fail Checklist
- [ ] PASS: All skill checks succeeded.
- [ ] FAIL: One or more skill checks failed.
- [ ] Blockers captured.
- [ ] Recovery actions assigned.

# Notes
- Preserve canonical skill naming and file placement.
