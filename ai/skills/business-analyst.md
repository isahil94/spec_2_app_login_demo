# Business Analyst Skills

This document defines reusable capabilities for the Business Analyst agent in requirements analysis and documentation.

---

## Skill: Analyze Requirements

### Purpose (Analyze Requirements)

Extract structured business requirements from raw specifications, identifying goals, constraints, priorities, and assumptions.

### When to Use (Analyze Requirements)

- Processing initial business specifications
- Clarifying vague or ambiguous requirements
- Decomposing complex requirements into manageable components
- Identifying missing or conflicting requirements

### Inputs (Analyze Requirements)

- `specification` (string): Raw specification document or narrative
- `context` (object): Project context (industry, domain, users)
- `constraints` (array, optional): Known business constraints
- `existing_requirements` (array, optional): Previously documented requirements to extend

### Outputs (Analyze Requirements)

- `requirements` (array): Structured requirements list
- `business_goals` (array): High-level business objectives
- `constraints` (array): Identified constraints and limitations
- `assumptions` (array): Documented assumptions
- `open_questions` (array): Clarification questions for stakeholders
- `priority_matrix` (object): Requirements prioritized by impact and effort
- `non_functional_requirements` (array): Business-oriented quality expectations
- `stakeholder_analysis` (array): Stakeholder responsibilities, goals, pain points, and success criteria
- `glossary_terms` (array): Business glossary entries
- `ui_observations` (array): Observations from the provided design reference
- `business_capability_requirements` (array): Capability statements grouped by business domain
- `business_data_model` (array): Conceptual entities and relationships

### Dependencies (Analyze Requirements)

- Input specification must be readable
- Domain context should be available
- Stakeholder availability for clarification

### Execution Steps (Analyze Requirements)

1. Parse specification for explicit requirements
2. Identify implicit requirements from narrative
3. Extract business goals and success criteria
4. Document constraints and limitations
5. List assumptions made during analysis
6. Identify gaps and ambiguities
7. Prioritize requirements by business value using MoSCoW
8. Generate clarification questions
9. Document non-functional expectations, stakeholders, glossary, and Figma observations in business language only
10. Structure output for downstream agents
11. Verify no technical design or implementation details are present

### Validation Checklist (Analyze Requirements)

- [ ] All explicit requirements documented
- [ ] Business goals are SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
- [ ] Constraints are realistic and documented
- [ ] Assumptions are justified and explicit
- [ ] Open questions are clear and specific
- [ ] Requirements are free of implementation details
- [ ] Non-functional business expectations are documented separately
- [ ] Stakeholder analysis is complete
- [ ] Glossary entries are defined
- [ ] UI observations reference the provided design without redesigning it
- [ ] UI requirements include approved design alignment, responsive behavior, and accessibility expectations
- [ ] Validation rules are specified for every user input surface
- [ ] Data constraints, defaults, allowed values, required vs optional fields, uniqueness, and relationships are specified where applicable
- [ ] Feature-level business detail is complete for applicable workflows, permissions, state transitions, and scenarios
- [ ] No duplicate or conflicting requirements remain unresolved
- [ ] Authentication and authorization behavior is specified in business language
- [ ] Navigation, workflow, and state transitions are specified where applicable
- [ ] Success, failure, empty, loading, and exception scenarios are captured where applicable
- [ ] Permission and visibility rules are specified where applicable
- [ ] Business capability requirements are documented without API design
- [ ] Business data model is conceptual only
- [ ] No endpoints, HTTP methods, payloads, schemas, SQL, framework names, or architecture choices appear

### Success Criteria (Analyze Requirements)

- Clear, actionable requirements identified
- Ambiguities resolved or documented as questions
- Business value understood for each requirement
- Requirements support overall business goals

### Failure Conditions (Analyze Requirements)

- Specification insufficient to derive requirements
- Conflicting or contradictory requirements identified
- Critical information missing
- Requirements lack measurable success criteria

---

## Skill: Identify Business Rules

### Purpose (Identify Business Rules)

Extract and document the business rules, policies, validations, and constraints that govern the system's behavior.

### When to Use (Identify Business Rules)

- Defining validation rules for data entry
- Documenting business policy constraints
- Identifying workflows and decision points
- Defining error conditions and handling rules

### Inputs (Identify Business Rules)

- `requirements` (object): Analyzed requirements
- `domain_knowledge` (object, optional): Industry-specific rules
- `existing_rules` (array, optional): Previously documented rules
- `regulatory_constraints` (array, optional): Compliance requirements

### Outputs (Identify Business Rules)

- `business_rules` (array): Documented business rules
- `validation_rules` (array): Data validation requirements
- `workflow_rules` (array): Process and workflow constraints
- `decision_trees` (array): Business decision logic
- `rule_dependencies` (object): Rules that depend on other rules

### Dependencies (Identify Business Rules)

- Analyzed requirements available
- Domain expertise or documentation available

### Execution Steps (Identify Business Rules)

1. Extract business rules from requirements
2. Identify validation constraints
3. Map workflow and process rules
4. Document decision logic and conditions
5. Identify rule precedence and conflicts
6. Document rule triggers and effects
7. Identify rules that depend on other rules
8. Validate rules are enforceable

### Validation Checklist (Identify Business Rules)

- [ ] Rules are explicit and measurable
- [ ] Rules are enforceable by system
- [ ] Rule conflicts identified and resolved
- [ ] Dependencies mapped correctly
- [ ] Edge cases considered
- [ ] Rules align with requirements
- [ ] Each feature has sufficient business rules for implementation
- [ ] Workflow and state-transition rules are explicit where applicable
- [ ] Permission and visibility rules are explicit where applicable

### Success Criteria (Identify Business Rules)

- All business rules identified and documented
- Rules are unambiguous and actionable
- Conflicts resolved explicitly
- Rules ready for implementation

### Failure Conditions (Identify Business Rules)

- Critical rules missing or unclear
- Conflicting rules cannot be resolved
- Rules contradict requirements
- Enforcement mechanism unclear

---

## Skill: Create User Stories

### Purpose (Create User Stories)

Decompose requirements into user stories following the narrative format, enabling focused development iterations.

### When to Use (Create User Stories)

- Breaking down large features into business-deliverable units
- Creating work items for development teams
- Planning iterative delivery
- Enabling user-centered design

### Inputs (Create User Stories)

- `features` (array): High-level features from requirements
- `user_personas` (array, optional): User profiles and roles
- `business_goals` (array): Business objectives
- `constraints` (array, optional): Known constraints

### Outputs (Create User Stories)

- `user_stories` (array): Formatted user stories
- `story_map` (object): Hierarchical story organization
- `acceptance_criteria` (object): Criteria for each story
- `story_dependencies` (array): Story interdependencies
- `story_estimates` (object, optional): Effort estimates

### Dependencies (Create User Stories)

- Features clearly defined
- User personas or roles understood
- Business context available

### Execution Steps (Create User Stories)

1. Identify user personas or roles
2. Decompose features into atomic stories
3. Write stories in "As a [role], I want [action], so that [benefit]" format
4. Define acceptance criteria for each story
5. Identify story dependencies
6. Organize stories into workflow or product backlog
7. Flag complex or risky stories
8. Document assumptions for each story

### Validation Checklist (Create User Stories)

- [ ] Each story is independent and testable
- [ ] Acceptance criteria are SMART
- [ ] Stories fit within typical sprint timeframe
- [ ] User value is clear for each story
- [ ] Dependencies are documented
- [ ] Business risks and assumptions are identified
- [ ] Every implementation-critical requirement maps to one or more user stories
- [ ] Every story references functional requirements and acceptance criteria
- [ ] Validation and auth behavior are explicit where applicable
- [ ] Every epic is fully decomposed into feature-backed stories
- [ ] Every feature is fully decomposed into complete user stories
- [ ] Navigation/workflow and state-transition behavior are explicit where applicable

### Success Criteria (Create User Stories)

- Stories ready for development team
- Acceptance criteria enable testing
- Team can estimate story effort
- Stories support overall delivery roadmap

### Failure Conditions (Create User Stories)

- Stories are too vague to implement
- Acceptance criteria missing or unclear
- Story dependencies create bottlenecks
- Stories lack clear user value

---

## Skill: Define Acceptance Criteria

### Purpose (Define Acceptance Criteria)

Create measurable, testable conditions that determine when a requirement or story is complete and ready for acceptance.

### When to Use (Define Acceptance Criteria)

- Defining conditions for story completion
- Specifying test cases for QA
- Creating contracts between developers and stakeholders
- Enabling automated testing

### Inputs (Define Acceptance Criteria)

- `user_story` (object): User story requiring acceptance criteria
- `business_rules` (array, optional): Applicable business rules
- `test_scenarios` (array, optional): Known test scenarios
- `quality_standards` (object, optional): Project quality expectations

### Outputs (Define Acceptance Criteria)

- `acceptance_criteria` (array): Testable acceptance conditions
- `test_cases` (array): Concrete test scenarios
- `edge_cases` (array): Identified edge cases
- `failure_modes` (array): How the feature could fail
- `gherkin_scenarios` (array): BDD format scenarios

### Dependencies (Define Acceptance Criteria)

- User story clearly defined
- Business context understood
- Quality standards defined

### Execution Steps (Define Acceptance Criteria)

1. Extract requirements from user story
2. Identify happy path scenarios
3. Define error and edge cases
4. Write acceptance criteria in testable format
5. Generate BDD Gherkin scenarios
6. Identify test data requirements
7. Document failure modes
8. Validate criteria are measurable

### Validation Checklist (Define Acceptance Criteria)

- [ ] Criteria are specific and measurable
- [ ] Criteria cover happy path and error paths
- [ ] Criteria are testable without implementation knowledge
- [ ] Edge cases are included
- [ ] Gherkin scenarios are properly formatted
- [ ] Criteria align with business rules
- [ ] Validation behavior is covered for all relevant input flows
- [ ] Authentication and authorization outcomes are covered where applicable
- [ ] QA can derive direct test cases from criteria without additional interpretation
- [ ] Success, failure, empty, loading, and exception behaviors are covered where applicable
- [ ] State-transition outcomes are explicitly testable where applicable

### Success Criteria (Define Acceptance Criteria)

- Clear acceptance criteria enable QA testing
- Developers understand completion requirements
- All scenarios can be tested automatically
- Stakeholders can verify completion

### Failure Conditions (Define Acceptance Criteria)

- Criteria are subjective or unmeasurable
- Critical scenarios missing
- Criteria conflict with business rules
- Testing approach unclear
