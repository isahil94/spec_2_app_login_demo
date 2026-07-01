# Backend Developer Skills

This document defines reusable capabilities for the Backend Developer agent in API and business logic implementation.

---

## Skill: Generate REST APIs

### Purpose
Create REST API specifications and implementations that expose business functionality through standardized endpoints.

### When to Use
- Converting business features to API endpoints
- Designing resource-based interfaces
- Creating endpoints for CRUD operations
- Planning API request/response formats

### Inputs
- `features` (array): Business features to expose
- `data_model` (object): System data model
- `api_spec` (object): API specification/contract
- `authentication_model` (object, optional): Auth requirements

### Outputs
- `endpoints` (array): Defined REST endpoints
- `request_schemas` (array): Request body/query/param schemas
- `response_schemas` (array): Response body schemas
- `error_responses` (array): Error response definitions
- `endpoint_documentation` (object): Endpoint-by-endpoint docs

### Dependencies
- Features and requirements clear
- Data model defined
- API contract specified

### Execution Steps
1. Map features to resources and endpoints
2. Define HTTP methods for each operation
3. Specify request parameters and bodies
4. Define response formats
5. Plan error responses and codes
6. Add pagination and filtering where appropriate
7. Define authentication/authorization per endpoint
8. Document rate limiting if applicable
9. Create comprehensive endpoint documentation

### Validation Checklist
- [ ] All features have corresponding endpoints
- [ ] Methods follow REST conventions (GET, POST, PUT, DELETE)
- [ ] Request/response schemas are well-defined
- [ ] Error responses are comprehensive
- [ ] Authentication is specified for each endpoint
- [ ] Documentation is clear and complete

### Success Criteria
- API fully implements required features
- Clients can use API from documentation alone
- API is RESTful and follows conventions
- Error handling is clear
- Performance meets requirements

### Failure Conditions
- Features incomplete in API
- API doesn't follow REST conventions
- Documentation missing or unclear
- Authentication/authorization issues
- Performance unacceptable

---

## Skill: Generate Business Services

### Purpose
Create business logic components that encapsulate domain logic, making it reusable, testable, and independent of technical details.

### When to Use
- Implementing business rules and workflows
- Creating reusable business components
- Separating business logic from infrastructure
- Building domain models

### Inputs
- `business_rules` (array): Rules to implement
- `workflows` (array, optional): Workflows and processes
- `data_model` (object): System data model
- `external_services` (array, optional): Services to integrate with

### Outputs
- `services` (array): Business service definitions
- `service_interfaces` (object): Service method signatures
- `service_implementations` (array): Implementation strategies
- `service_dependencies` (object): Service interdependencies
- `workflow_definitions` (array): Implemented workflows

### Dependencies
- Business rules clearly documented
- Data model defined
- External service contracts available

### Execution Steps
1. Identify business domains and entities
2. Group related business rules into services
3. Define service responsibilities
4. Create service interfaces/contracts
5. Plan service interactions
6. Identify external service dependencies
7. Define error handling per service
8. Plan service state management
9. Create service documentation

### Validation Checklist
- [ ] Services have single, clear responsibility
- [ ] Services are reusable across features
- [ ] Business rules are implemented correctly
- [ ] Service interfaces are clear
- [ ] Dependencies are documented
- [ ] Error handling is comprehensive

### Success Criteria
- Business logic is encapsulated in services
- Services are independently testable
- Business rules are correctly implemented
- Services enable code reuse
- New features can reuse existing services

### Failure Conditions
- Business logic scattered throughout codebase
- Services tightly coupled
- Business rules violated in implementation
- Service contracts unclear
- Cannot reuse services for new features

---

## Skill: Implement Validation Rules

### Purpose
Create validation logic that ensures data integrity and business rule compliance at the application level.

### When to Use
- Validating form inputs
- Enforcing data constraints
- Checking business rule compliance
- Validating API requests

### Inputs
- `business_rules` (array): Rules that must be validated
- `data_model` (object): Data model and field definitions
- `constraints` (array): Business constraints
- `valid_examples` (array, optional): Examples of valid data
- `invalid_examples` (array, optional): Examples of invalid data

### Outputs
- `validators` (array): Validation functions/rules
- `validation_rules` (object): Specific validation logic
- `error_messages` (object): User-friendly error messages
- `validation_test_cases` (array): Test cases for validators
- `validation_documentation` (string): Validation rules documentation

### Dependencies
- Business rules documented
- Data model defined
- Constraints understood

### Execution Steps
1. Identify all validation requirements
2. Create field-level validators
3. Create business rule validators
4. Define validation error messages
5. Plan validation at multiple layers
6. Create validation test cases
7. Document validation rules
8. Consider performance of validation
9. Plan custom validation for complex rules

### Validation Checklist
- [ ] All business rules have validators
- [ ] Field constraints are validated
- [ ] Error messages are user-friendly and clear
- [ ] Validation test cases pass
- [ ] Invalid data is caught
- [ ] Valid data passes through

### Success Criteria
- Invalid data is rejected before processing
- Valid data is accepted correctly
- Error messages guide users
- Validation is performant
- Business rules are enforced

### Failure Conditions
- Invalid data passes through
- Valid data is incorrectly rejected
- Error messages confusing or unhelpful
- Validation too slow
- Business rules not enforced

---

## Skill: Implement Error Handling

### Purpose
Create comprehensive error handling that gracefully manages failures, recovers when possible, and provides useful feedback.

### When to Use
- Handling expected errors (invalid input, resource not found)
- Handling unexpected errors (service failures, database errors)
- Creating error response formats
- Planning error recovery strategies

### Inputs
- `features` (array): Features that could fail
- `external_dependencies` (array): Third-party services that could fail
- `error_scenarios` (array): Identified error conditions
- `user_context` (object, optional): User-facing vs. system errors

### Outputs
- `error_categories` (array): Categorized error types
- `error_responses` (array): Error response formats
- `error_handling_strategies` (object): How to handle each error type
- `retry_policies` (object): Retry logic for transient failures
- `error_recovery_procedures` (array): How to recover from failures

### Dependencies
- Features and error scenarios identified
- External dependencies documented
- Error response format specified

### Execution Steps
1. Identify all possible error scenarios
2. Categorize errors (client error, server error, external, etc.)
3. Define error response format
4. Create error codes and messages
5. Plan retry logic for transient failures
6. Define recovery procedures
7. Plan error logging and monitoring
8. Create error handling test cases
9. Document error handling strategy

### Validation Checklist
- [ ] All known error scenarios handled
- [ ] Error messages are helpful and clear
- [ ] Retry logic works for transient failures
- [ ] System recovers gracefully from failures
- [ ] Sensitive information not exposed in errors
- [ ] Error handling is consistent

### Success Criteria
- System handles errors gracefully
- Users understand what went wrong
- Transient failures are retried and recovered
- Error messages enable troubleshooting
- System doesn't crash on unexpected errors

### Failure Conditions
- Errors not handled cause system crash
- Error messages are confusing
- No retry for transient failures
- Sensitive info exposed in errors
- System stuck in error state
