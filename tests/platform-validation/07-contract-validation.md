# Purpose
Validate platform contracts for ownership, consumption, governance, and workflow consistency.

# Scope
artifact-manifest, artifact-ownership-matrix, workflow-contract, and repository-conventions contract coverage.

# Prerequisites
- [ ] Contract files are available and current.
- [ ] Template and agent definitions are available for cross-checking.

# Validation Steps
- [ ] Validate artifact-manifest contract coverage.
- [ ] Validate artifact-ownership-matrix ownership definitions.
- [ ] Validate workflow-contract sequencing and stage expectations.
- [ ] Validate repository-conventions contract alignment.
- [ ] Verify ownership status usage is consistent: Own, Consume, Extend, Reference.
- [ ] Verify artifact ownership and consumption consistency.
- [ ] Verify handoff consistency across contracts.
- [ ] Verify workflow consistency across contracts.
- [ ] Verify Figma propagation requirements are defined consistently.
- [ ] Verify OpenLog governance requirements are defined consistently.

# Expected Result
- [ ] Contract set is internally consistent and complete.
- [ ] No ownership, workflow, or governance contradictions.

# Failure Conditions
- [ ] Missing contract coverage for required categories.
- [ ] Ownership status contradictions.
- [ ] Handoff or workflow contract mismatches.
- [ ] Missing Figma or OpenLog governance clauses.

# Recovery Actions
- [ ] Align contract language and status definitions.
- [ ] Resolve ownership and handoff inconsistencies.
- [ ] Re-run contract validation after updates.

# Pass / Fail Checklist
- [ ] PASS: All contract checks succeeded.
- [ ] FAIL: One or more contract checks failed.
- [ ] Blockers captured.
- [ ] Recovery actions assigned.

# Notes
- Keep contract terminology canonical and stable.
