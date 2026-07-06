# Solution Architect Skills

This document defines reusable capabilities for the Solution Architect agent in system design and architecture.

---

## Skill: Design Solution Architecture

### Purpose
Create comprehensive system architecture that meets requirements while optimizing for scalability, maintainability, and performance.

### When to Use
- Creating initial system design from requirements
- Planning multi-component systems
- Defining system layers and boundaries
- Designing for non-functional requirements (performance, scalability, security)

### Inputs
- `requirements` (object): Business and technical requirements
- `constraints` (object): Technical, organizational, and environmental constraints
- `technology_stack` (array, optional): Approved technologies to use
- `existing_systems` (array, optional): Systems to integrate with
- `quality_attributes` (object): Non-functional requirements (scalability, security, etc.)

### Outputs
- `architecture_diagram` (string): Architecture visualization/description
- `layers` (array): Architectural layers and responsibilities
- `components` (array): Major system components
- `data_flow` (object): Data flow between components
- `deployment_model` (object): Deployment topology
- `scalability_plan` (object): Scaling strategy

### Dependencies
- Requirements clearly defined
- Technical constraints documented
- Technology preferences known

### Execution Steps
1. Analyze requirements and constraints
2. Identify system layers (presentation, business, data, infrastructure)
3. Define major components and responsibilities
4. Map data flows between components
5. Define integration points
6. Plan for scalability and performance
7. Consider security and reliability
8. Create architecture diagram
9. Document rationale for key decisions

### Validation Checklist
- [ ] Architecture addresses all requirements
- [ ] All BA artifacts are consumed and represented
- [ ] Every epic, feature, and user story is represented in architecture outputs
- [ ] All constraints are satisfied
- [ ] Components have clear responsibilities
- [ ] Data flows are unambiguous
- [ ] Scalability approach is documented
- [ ] Architecture aligns with approved tech stack
- [ ] Presentation, business, and data layer interactions are explicitly defined
- [ ] Cross-cutting concerns are fully addressed (logging, configuration, observability, auditing, performance)

### Success Criteria
- Architecture meets all functional requirements
- Non-functional requirements addressed
- Components are loosely coupled
- System can be deployed and tested
- Team understands architecture

### Failure Conditions
- Architecture doesn't meet requirements
- Violates technical constraints
- Components tightly coupled
- Scalability concerns unaddressed
- Too complex to implement

---

## Skill: Define Application Components

### Purpose
Break down the architecture into discrete, independently deployable components with clear interfaces and responsibilities.

### When to Use
- Defining component responsibilities and boundaries
- Planning component interactions
- Enabling sequential implementation handoffs
- Defining component APIs

### Inputs
- `architecture` (object): System architecture
- `requirements` (object): Functional and non-functional requirements
- `team_structure` (array, optional): Development team organization
- `deployment_constraints` (object, optional): Deployment limitations

### Outputs
- `components` (array): Detailed component definitions
- `component_interfaces` (object): Public APIs for each component
- `component_dependencies` (object): Dependencies between components
- `deployment_units` (array): How components map to deployable artifacts
- `ownership_map` (object): Which team owns each component

### Dependencies
- Architecture defined
- Requirements available
- Technology stack decided

### Execution Steps
1. Identify natural component boundaries from architecture
2. Assign responsibilities to components
3. Define component public interfaces
4. Identify component dependencies
5. Map components to deployment units
6. Define component communication protocols
7. Identify shared services or utilities
8. Plan component release cadence
9. Assign ownership to teams

### Validation Checklist
- [ ] Each component has clear, single responsibility
- [ ] Component interfaces are well-defined
- [ ] Dependencies are documented and minimal
- [ ] Components can be deployed independently
- [ ] Component boundaries are clear
- [ ] Communication between components is defined
- [ ] Module decomposition covers every epic and feature pathway
- [ ] Component, service, repository, and database responsibilities are explicit where applicable
- [ ] Navigation/workflow/state-transition responsibilities are explicit where applicable

### Success Criteria
- Teams can implement components in the defined sequential order
- Components can be tested independently
- Components can be deployed on different cadences
- System integrates properly

### Failure Conditions
- Component responsibilities overlap
- Circular dependencies exist
- Components too tightly coupled
- Component boundaries unclear
- Communication protocol undefined

---

## Skill: Define API Contracts

### Purpose
Specify contracts for component communication, enabling independent development and testing of integrated components.

### When to Use
- Defining REST API endpoints
- Specifying message formats
- Defining event schemas
- Planning integrations

### Inputs
- `components` (array): System components
- `data_model` (object): System data model
- `integration_points` (array): Where components interact
- `communication_patterns` (array): Sync/async, request-response/events, etc.

### Outputs
- `api_specs` (array): API specifications (OpenAPI, AsyncAPI, etc.)
- `data_contracts` (array): Request/response schemas
- `error_contracts` (array): Error response formats
- `integration_examples` (array): Example integrations
- `versioning_strategy` (object): API versioning approach

### Dependencies
- Components defined
- Data model known
- Communication patterns decided

### Execution Steps
1. Identify component communication needs
2. Define API endpoints or message topics
3. Specify request/response schemas
4. Document error responses
5. Define authentication/authorization requirements
6. Plan API versioning strategy
7. Create OpenAPI/AsyncAPI specifications
8. Provide integration examples
9. Document breaking change policy

### Validation Checklist
- [ ] APIs are well-specified and machine-readable
- [ ] Request/response schemas are complete
- [ ] Error cases documented
- [ ] Authentication approach defined
- [ ] Versioning strategy clear
- [ ] APIs follow REST/async conventions
- [ ] Data contracts are complete and mapped to interfaces
- [ ] Integration contracts are complete and unambiguous
- [ ] Validation and authorization constraints are defined as architecture requirements
- [ ] Traceability to requirements, features, and stories is complete

### Success Criteria
- Developers can implement from spec without clarification
- Clients can integrate without implementation details
- APIs are testable and mockable
- API specifications are version-controlled

### Failure Conditions
- Specifications ambiguous or incomplete
- Schema definitions invalid
- Error handling undefined
- Breaking changes not managed
- APIs too loosely specified

---

## Skill: Select Design Patterns

### Purpose
Identify and recommend appropriate design patterns that solve common architectural problems and align with team capabilities.

### When to Use
- Solving recurring design problems
- Improving code maintainability and testability
- Enabling code reuse
- Establishing team conventions

### Inputs
- `problems_to_solve` (array): Specific design challenges
- `component` (object): Component applying patterns
- `team_experience` (object, optional): Team familiarity with patterns
- `language_platform` (string, optional): Programming context

### Outputs
- `recommended_patterns` (array): Suggested design patterns
- `pattern_justification` (object): Why each pattern fits
- `pattern_examples` (array): Code or pseudocode examples
- `trade_offs` (object): Benefits and drawbacks of each pattern
- `implementation_guide` (object): How to implement patterns

### Dependencies
- Design problems clearly identified
- Team capabilities understood
- Technical constraints known

### Execution Steps
1. Analyze design problems
2. Identify candidate patterns that address problems
3. Evaluate patterns against team capabilities
4. Document pattern selection rationale
5. Provide implementation examples
6. Document potential trade-offs
7. Suggest when to use vs. avoid each pattern
8. Create team guidelines for pattern usage

### Validation Checklist
- [ ] Patterns solve identified problems
- [ ] Patterns are appropriate for team skill level
- [ ] Trade-offs are clearly documented
- [ ] Examples are clear and applicable
- [ ] Guidelines help team decision-making
- [ ] Patterns don't introduce unnecessary complexity

### Success Criteria
- Patterns improve code quality and maintainability
- Team understands when to apply patterns
- Consistent pattern usage across codebase
- Reduced time to implement common scenarios

### Failure Conditions
- Patterns add unnecessary complexity
- Team lacks skills to implement patterns
- Wrong patterns selected for problems
- Implementation examples unclear or wrong
