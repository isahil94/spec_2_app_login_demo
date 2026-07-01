# Reviewer Skills

This document defines reusable capabilities for the Reviewer agent in code review and quality assessment.

---

## Skill: Review Code Quality

### Purpose
Assess code quality across multiple dimensions including readability, maintainability, performance, and security.

### When to Use
- Reviewing generated code before deployment
- Assessing code maintainability
- Identifying technical debt
- Preparing code for production

### Inputs
- `code` (object): Code to review
- `standards` (object): Coding standards and guidelines
- `quality_criteria` (object): Quality metrics and thresholds
- `context` (object, optional): Business context for code
- `previous_reviews` (array, optional): Prior review feedback

### Outputs
- `quality_score` (number): Overall code quality score
- `issues` (array): Quality issues found
- `recommendations` (array): Improvement suggestions
- `quality_report` (object): Detailed quality analysis
- `remediation_plan` (array): Steps to improve quality

### Dependencies
- Code available for review
- Standards and guidelines defined
- Quality criteria established

### Execution Steps
1. Run static analysis tools (see [ai/tools/code-analysis.md](../../ai/tools/code-analysis.md), or use scripts/lint.py)
2. Check coding standards compliance
3. Review code readability and style
4. Assess code maintainability
5. Identify code duplication
6. Check error handling
7. Assess performance implications
8. Review security considerations
9. Generate quality report

### Validation Checklist
- [ ] Code follows standards
- [ ] No obvious bugs
- [ ] Error handling present
- [ ] No security issues
- [ ] Performance acceptable
- [ ] Code is readable
- [ ] Test coverage adequate

### Success Criteria
- Code passes quality review
- Issues identified are prioritized
- Recommendations are actionable
- Quality score meets threshold
- Code ready for production

### Failure Conditions
- Code fails quality review
- Critical issues found
- Quality score below threshold
- Security issues present
- Performance concerns

---

## Skill: Validate Architecture

### Purpose
Verify that the implementation matches the architectural design and maintains intended structure and patterns.

### When to Use
- Reviewing component structure
- Validating layer separation
- Checking dependency patterns
- Ensuring architectural consistency

### Inputs
- `implementation` (object): Implemented code
- `architecture_spec` (object): Intended architecture
- `design_patterns` (array): Agreed patterns
- `component_contracts` (array): Component interfaces

### Outputs
- `architecture_assessment` (object): Overall assessment
- `deviations` (array): Deviations from intended architecture
- `violations` (array): Architecture violations
- `recommendations` (array): Architectural improvements
- `architecture_report` (object): Detailed analysis

### Dependencies
- Architecture specification available
- Implementation code available
- Design patterns documented

### Execution Steps
1. Map implementation to architecture
2. Check component boundaries
3. Validate layer separation
4. Check dependency direction
5. Verify patterns are applied
6. Check contract compliance
7. Identify architectural violations
8. Assess maintainability implications
9. Generate architecture report

### Validation Checklist
- [ ] Implementation matches architecture
- [ ] Component boundaries clear
- [ ] Layers properly separated
- [ ] Dependencies follow rules
- [ ] Patterns correctly applied
- [ ] No circular dependencies

### Success Criteria
- Implementation follows architecture
- Component boundaries maintained
- Patterns consistently applied
- Architecture enables maintenance
- No violations present

### Failure Conditions
- Implementation deviates from architecture
- Boundaries blurred
- Layers not separated
- Circular dependencies exist
- Patterns misapplied

---

## Skill: Validate Coding Standards

### Purpose
Ensure code conforms to established coding standards and conventions, maintaining consistency and readability.

### When to Use
- Reviewing generated code
- Ensuring team consistency
- Preparing code for merge
- Quality gate checking

### Inputs
- `code` (object): Code to validate
- `standards` (object): Coding standards document
- `style_guide` (object): Style guide to follow
- `lint_rules` (array, optional): Linting rules

### Outputs
- `compliance_score` (number): Standards compliance percentage
- `violations` (array): Standard violations found
- `style_issues` (array): Style guide violations
- `suggestions` (array): Improvement suggestions
- `compliance_report` (object): Detailed compliance analysis

### Dependencies
- Coding standards defined
- Style guide available
- Linting tools available (scripts/lint.py)

### Execution Steps
1. Run linting tools (scripts/lint.py)
2. Check naming conventions
3. Check formatting and indentation
4. Check comment/documentation standards
5. Check import/include organization
6. Check code organization
7. Verify test standards
8. Check documentation standards
9. Generate compliance report

### Validation Checklist
- [ ] Naming follows conventions
- [ ] Formatting is consistent
- [ ] Comments are present and clear
- [ ] Imports organized properly
- [ ] Code structured logically
- [ ] Documentation complete
- [ ] No linting errors

### Success Criteria
- Code passes linting
- Compliance score high
- No major violations
- Code consistent with team style
- Easy to maintain

### Failure Conditions
- Linting errors present
- Low compliance score
- Major violations found
- Inconsistent with team style
- Difficult to read/maintain

---

## Skill: Perform Final Review

### Purpose
Conduct comprehensive final review before release, verifying all aspects of the deliverable meet requirements and quality standards.

### When to Use
- Final verification before deployment
- Release gate review
- Acceptance sign-off
- Quality validation before production

### Inputs
- `deliverables` (array): All deliverables to review
- `requirements` (object): Original requirements
- `acceptance_criteria` (array): Criteria for acceptance
- `quality_standards` (object): Quality expectations
- `testing_results` (object, optional): Test results

### Outputs
- `final_assessment` (object): Overall assessment
- `requirements_met` (boolean): Requirements coverage
- `quality_met` (boolean): Quality standards met
- `ready_for_release` (boolean): Release readiness
- `release_notes` (object): Summary for release
- `outstanding_issues` (array, optional): Unresolved issues

### Dependencies
- All deliverables complete
- Testing finished
- Documentation prepared

### Execution Steps
1. Verify all deliverables present
2. Check requirements coverage
3. Verify testing completed
4. Review quality metrics
5. Assess documentation completeness
6. Review performance characteristics
7. Validate security measures
8. Check deployment readiness
9. Generate final assessment

### Validation Checklist
- [ ] All deliverables present
- [ ] All requirements met
- [ ] All tests passing
- [ ] Quality standards met
- [ ] Documentation complete
- [ ] Performance acceptable
- [ ] Security validated
- [ ] Deployment plan ready

### Success Criteria
- All deliverables complete
- All requirements satisfied
- Quality standards met
- Ready for production deployment
- Release approved

### Failure Conditions
- Missing deliverables
- Requirements not met
- Tests failing
- Quality below standard
- Not ready for production
