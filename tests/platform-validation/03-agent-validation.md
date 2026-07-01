# Purpose
Validate every numbered agent definition for responsibilities, contracts, and workflow readiness.

# Scope
00-supervisor through 09-documentation agent files.

# Prerequisites
- [ ] All numbered agent files are present.
- [ ] Referenced contracts, templates, and instructions are available.
- [ ] Artifact ownership matrix is current.

# Validation Steps
- [ ] Validate 00-supervisor responsibilities, inputs, outputs, and governance references.
- [ ] Validate 01-business-analyst responsibilities, inputs, outputs, and governance references.
- [ ] Validate 02-solution-architect responsibilities, inputs, outputs, and governance references.
- [ ] Validate 03-ui-ux-developer responsibilities, inputs, outputs, and governance references.
- [ ] Validate 04-backend-developer responsibilities, inputs, outputs, and governance references.
- [ ] Validate 05-database-developer responsibilities, inputs, outputs, and governance references.
- [ ] Validate 06-qa-engineer responsibilities, inputs, outputs, and governance references.
- [ ] Validate 07-reviewer responsibilities, inputs, outputs, and governance references.
- [ ] Validate 08-devops-release responsibilities, inputs, outputs, and governance references.
- [ ] Validate 09-documentation responsibilities, inputs, outputs, and governance references.
- [ ] Verify owned artifacts are correct per matrix.
- [ ] Verify consumed artifacts are correct per matrix.
- [ ] Verify handoff contract usage is defined.
- [ ] Verify openlog usage is defined.
- [ ] Verify quality report requirement is defined.
- [ ] Verify logging, audit, and observability requirements are defined.
- [ ] Verify workflow compliance and stage boundaries are defined.

# Expected Result
- [ ] All agents are structurally valid and governance-compliant.
- [ ] Ownership, consumption, and handoff definitions are consistent.

# Failure Conditions
- [ ] Missing required sections in agent definitions.
- [ ] Ownership conflicts or invalid artifact declarations.
- [ ] Missing workflow, openlog, or quality requirements.

# Recovery Actions
- [ ] Correct inconsistent agent references in-place.
- [ ] Align ownership and handoff definitions with contracts.
- [ ] Re-run full agent validation after updates.

# Pass / Fail Checklist
- [ ] PASS: All numbered agents validated successfully.
- [ ] FAIL: One or more agent validations failed.
- [ ] Blockers captured.
- [ ] Recovery actions assigned.

# Notes
- Do not validate non-canonical duplicate agent files.
