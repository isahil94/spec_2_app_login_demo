# Purpose
Validate reusable template integrity and downstream compatibility.

# Scope
All artifact templates in ai/templates relevant to platform lifecycle.

# Prerequisites
- [ ] Template files are available.
- [ ] Contract and agent ownership definitions are available.

# Validation Steps
- [ ] Verify required artifact templates exist.
- [ ] Verify template naming consistency with artifact conventions.
- [ ] Verify required sections are present in each template.
- [ ] Verify template structure is reusable and non-project-specific.
- [ ] Verify template references to contracts/instructions are valid.
- [ ] Verify downstream compatibility with consuming stages.

# Expected Result
- [ ] Templates are consistent, complete, and reusable.
- [ ] No template mismatches with expected artifact structure.

# Failure Conditions
- [ ] Missing required templates.
- [ ] Naming mismatches against artifact conventions.
- [ ] Missing required sections.
- [ ] Broken template references.

# Recovery Actions
- [ ] Correct template structure and references in-place.
- [ ] Align templates with current artifact ownership and contracts.
- [ ] Re-run template validation after corrections.

# Pass / Fail Checklist
- [ ] PASS: All template validations succeeded.
- [ ] FAIL: One or more template validations failed.
- [ ] Blockers captured.
- [ ] Recovery actions assigned.

# Notes
- Keep templates concise and implementation-agnostic.
