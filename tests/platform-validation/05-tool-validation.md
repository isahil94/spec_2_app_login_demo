# Purpose
Validate platform tooling and execution entry points used by developers and workflows.

# Scope
Python helper scripts, VS Code tasks, MCP server references, build/lint/test/format/documentation scripts, and workflow runner references.

# Prerequisites
- [ ] Tooling definitions are present.
- [ ] Required runtime dependencies are available.

# Validation Steps
- [ ] Verify Python helper script references resolve.
- [ ] Verify VS Code tasks reference existing commands/files.
- [ ] Verify MCP server references are resolvable.
- [ ] Verify build script references are valid.
- [ ] Verify lint script references are valid.
- [ ] Verify test script references are valid.
- [ ] Verify format script references are valid.
- [ ] Verify documentation script references are valid.
- [ ] Verify workflow runner references are valid.
- [ ] Verify no broken tool references across agents/chat modes/instructions.

# Expected Result
- [ ] No broken references.
- [ ] No missing dependencies in declared tool paths.

# Failure Conditions
- [ ] Missing script targets or task command targets.
- [ ] Broken MCP references.
- [ ] Unresolvable runner/tool links.

# Recovery Actions
- [ ] Correct invalid tool references.
- [ ] Restore missing scripts or update references to canonical files.
- [ ] Re-run tool validation after fixes.

# Pass / Fail Checklist
- [ ] PASS: Tooling validation succeeded.
- [ ] FAIL: One or more tooling checks failed.
- [ ] Blockers captured.
- [ ] Recovery actions assigned.

# Notes
- This validates integration and readiness, not script internals.
