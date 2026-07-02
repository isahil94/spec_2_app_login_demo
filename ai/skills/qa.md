# QA Engineer Skills

This document defines reusable capabilities for the QA Engineer agent in testing and quality assurance.

---

## Skill: Generate Unit Tests

### Purpose
Create unit tests that verify individual components function correctly in isolation, providing fast feedback on code correctness.

### When to Use
- Testing business logic functions
- Testing service methods
- Testing utility functions
- Verifying code meets specifications

### Inputs
- `implementation` (object): Code/components to test
- `requirements` (array): Requirements the code must meet
- `edge_cases` (array, optional): Known edge cases to test
- `test_framework` (string, optional): Testing framework to use
- `coverage_target` (number, optional): Target code coverage percentage

### Outputs
- `unit_tests` (array): Unit test definitions
- `test_cases` (array): Individual test cases
- `test_data` (object): Mock data for tests
- `test_utilities` (array): Helper functions for testing
- `coverage_report` (object): Code coverage analysis

### Dependencies
- Implementation code available
- Requirements documented
- Testing framework chosen

### Execution Steps
1. Analyze code/components to test
2. Identify testable units (functions, methods, classes)
3. If no matching test exists for the unit, create a new test case and place it in the appropriate QA artifact path under `artifacts/tests/`
4. Write tests for happy path
5. Write tests for error cases
6. Write tests for boundary conditions
7. Write tests for edge cases
8. Set up test data and mocks
9. Run tests and verify passing
10. Measure and report code coverage

### Validation Checklist
- [ ] Tests are independent and isolated
- [ ] Each test verifies one thing
- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases tested
- [ ] Code coverage >= target percentage

### Success Criteria
- All tests pass
- Code coverage meets target
- Tests execute quickly
- Tests are maintainable
- New code has test coverage

### Failure Conditions
- Tests are flaky or unreliable
- Coverage below target
- Missing edge cases
- Tests slow to execute
- New code lacks tests

---

## Skill: Generate Integration Tests

### Purpose
Create tests that verify multiple components work together correctly, validating system behavior end-to-end.

### When to Use
- Testing component interactions
- Testing API endpoints
- Testing workflows
- Verifying system integration

### Inputs
- `components` (array): Components that integrate
- `workflows` (array): User workflows to test
- `api_specs` (array, optional): API endpoints to test
- `test_data` (object, optional): Data for integration tests
- `external_services` (array, optional): External dependencies

### Outputs
- `integration_tests` (array): Integration test definitions
- `test_scenarios` (array): End-to-end test scenarios
- `test_data_setup` (object): How to prepare test data
- `mock_services` (array): Mock external dependencies
- `integration_report` (object): Integration test results

### Dependencies
- Components available for testing
- Workflows documented
- API specs defined
- Test environment available

### Execution Steps
1. Identify component interactions to test
2. Map user workflows to test scenarios
3. If no integration or workflow test exists, generate a new one and store it in the relevant QA artifact folder under `artifacts/tests/`
4. Create test data for scenarios
5. Set up mocks for external dependencies
6. Write end-to-end tests for workflows
7. Test API integrations
8. Test database interactions
9. Validate data flow across components
10. Report integration test results

### Validation Checklist
- [ ] All key workflows tested
- [ ] Component interactions verified
- [ ] Error handling tested
- [ ] Data flows correctly
- [ ] Performance acceptable
- [ ] External dependencies mocked

### Success Criteria
- All integration tests pass
- Workflows execute correctly end-to-end
- Components integrate properly
- Performance meets requirements
- System behaves as expected

### Failure Conditions
- Tests fail due to integration issues
- Workflows not working end-to-end
- Data lost or corrupted in flow
- Performance unacceptable
- Components incompatible

---

## Skill: Validate Authentication and Page Workflows

### Purpose
Validate critical user journeys across backend, frontend, and database layers, ensuring authentication, input constraints, and page-level behavior meet the documented requirements.

### When to Use
- Verifying signup and login flows
- Validating form rules and error handling
- Testing dashboard, project, task, comment, label, notification, and account pages
- Checking persistence and constraint behavior in the database

### Inputs
- `application_routes` (array): Backend endpoints and frontend routes to verify
- `business_rules` (array): Required validation rules and constraints
- `auth_scenarios` (array): Signup/login cases to exercise
- `page_flows` (array): Core user journeys and page states
- `static_analysis_context` (object, optional): Static analysis context (mypy/eslint/flake8 output)

### Outputs
- `workflow_validation_results` (object): Results for auth and page-flow checks
- `constraint_findings` (array): Missing or invalid validation findings
- `defect_report` (array): Issues discovered during workflow validation
- `recommendations` (array): Follow-up actions for failed scenarios

### Dependencies
- Application implementation available
- Requirements and acceptance criteria documented
- Static analysis tools available (mypy/eslint/flake8)

### Execution Steps
1. Run static analysis (mypy, eslint, flake8) for backend, frontend, and database code and capture results.
2. Generate Playwright E2E tests for acceptance criteria where appropriate; keep one spec file per feature and place under the repository's E2E test folder (e.g., `tests/e2e`).
3. Run generated Playwright tests automatically; capture and save failure screenshots to `artifacts/tests/e2e/screenshots`.
4. Review authentication requirements for signup and login.
5. If the required workflow or validation test is missing, generate a new Playwright test case and publish it under `artifacts/tests/`.
6. Exercise signup scenarios with missing email, invalid email, weak password, duplicate user, and valid data via Playwright.
7. Exercise login scenarios with unknown users, missing credentials, wrong password, and correct credentials via Playwright.
8. Validate core pages and flows for required-field checks, empty states, and successful completion paths via Playwright.
9. Confirm database constraints and persistence behavior for invalid or missing data (query DB directly where needed).
10. Record failures, expected behavior, and remediation guidance.

### Validation Checklist
- [ ] Missing input produces the expected validation error
- [ ] Invalid input fails safely and clearly
- [ ] Correct input proceeds to the expected success state
- [ ] Unknown user and wrong credentials are rejected appropriately
- [ ] Core pages expose the correct UX for empty/error/success states
- [ ] Database constraints are enforced or reported clearly
- [ ] Static analysis completed and Playwright tests executed; issues reviewed

### Success Criteria
- Authentication and page workflows behave according to documented requirements
- Invalid input is rejected with clear feedback
- Valid input reaches the expected success state
- Database and UI behavior remain consistent with the contract

### Failure Conditions
- Missing validation for required fields
- Authentication flows allow invalid accounts or leak incorrect state
- Page workflows fail without clear error handling
- Database constraints are not enforced or not surfaced
- Static analysis issues remain unresolved

---

## Skill: Generate Playwright E2E Tests

### Purpose
Generate maintainable Playwright end-to-end tests from user stories and acceptance criteria, run tests, and capture failure artifacts.

### When to Use
- When an explicit user story or acceptance criterion requires an end-to-end verification
- For critical workflows (authentication, navigation, data persistence)

### Inputs
- `user_story` (object): User story with acceptance criteria and scenarios
- `local_url` (string): Local URL where the feature is deployed (e.g., http://localhost:5173/feature)
- `selectors` (object, optional): DOM selectors or page object hints

### Outputs
- Playwright spec file saved under `tests/e2e/<feature-name>.spec.ts` or `.js`
- Failure screenshots saved under `artifacts/tests/e2e/screenshots`\
- `ui-live-test-report.md` summarizing execution results and links to screenshots

### Execution Steps
1. Parse the `user_story` and extract Gherkin-style scenarios.
2. Generate a Playwright spec file (one per feature) that implements the scenarios using Playwright test API and page objects where helpful.
3. Run Playwright tests automatically using the project's Playwright setup (or install Playwright if missing in a controlled manner).
4. On test failures, save screenshots and the test trace to `artifacts/tests/e2e/screenshots`.
5. Produce `ui-live-test-report.md` with pass/fail, failure screenshots, and rerun commands.

### Validation Checklist
- [ ] One spec file per feature is created
- [ ] Tests implement acceptance criteria exactly (no invented flows)
- [ ] Failure screenshots captured for each failed test
- [ ] Report includes target user story and local URL

### Success Criteria
- Playwright tests run and report results automatically
- Failure artifacts are stored and linked from reports
- Tests are maintainable and aligned with feature names

---

## Skill: Generate Test Data

### Purpose
Create realistic test data that exercises the system under realistic conditions and edge cases.

### When to Use
- Populating test databases
- Creating realistic user scenarios
- Testing with large datasets
- Testing error conditions

### Inputs
- `data_model` (object): System data model
- `test_scenarios` (array): Test scenarios requiring data
- `scale_expectations` (object, optional): How much data to generate
- `data_constraints` (array, optional): Business rules for data
- `edge_cases` (array, optional): Edge cases to cover

### Outputs
- `test_datasets` (array): Generated test data
- `data_generation_scripts` (array): Scripts to generate data
- `data_documentation` (object): Documentation of test data
- `seed_data` (object): Initial seed data for tests
- `edge_case_data` (array): Data for edge case testing

### Dependencies
- Data model defined
- Test scenarios documented
- Database schema available

### Execution Steps
1. Understand test data needs for each scenario
2. Create realistic sample data
3. Generate edge case data
4. Create large datasets for performance testing
5. Implement data generation scripts
6. Validate generated data matches constraints
7. Document test data usage
8. Create data seeding procedures
9. Plan data cleanup after tests

### Validation Checklist
- [ ] Data matches business rules
- [ ] Edge cases covered
- [ ] Large datasets generated efficiently
- [ ] Data is realistic and representative
- [ ] Data can be regenerated consistently
- [ ] Data can be cleaned up after tests

### Success Criteria
- Tests have realistic data to work with
- Edge cases have corresponding data
- Performance tests have adequate volume
- Data generation is reproducible
- Data cleanup is automated

### Failure Conditions
- Data violates business rules
- Edge cases not covered
- Data generation is slow
- Cannot reproduce test conditions
- Data cleanup leaves artifacts

---

## Skill: Validate Test Coverage

### Purpose
Measure and analyze test coverage to ensure adequate testing and identify untested code paths.

### When to Use
- Reviewing test completeness
- Identifying gaps in testing
- Meeting coverage requirements
- Improving test quality

### Inputs
- `implementation` (object): Code to analyze
- `tests` (array): Test suite
- `coverage_targets` (object): Coverage goals by metric
- `critical_paths` (array, optional): Paths that must be tested

### Outputs
- `coverage_metrics` (object): Line, branch, path coverage
- `coverage_gaps` (array): Untested code paths
- `coverage_report` (object): Detailed coverage analysis
- `recommendations` (array): What to test next
- `coverage_visualization` (string): Coverage report format

### Dependencies
- Code and tests available
- Coverage tool configured
- Coverage targets defined

### Execution Steps
1. Run coverage tool on test suite
2. Analyze line coverage
3. Analyze branch coverage
4. Analyze path coverage for critical code
5. Identify untested code paths
6. Determine why paths are untested
7. Recommend tests for gaps
8. Generate coverage report
9. Track coverage over time

### Validation Checklist
- [ ] Coverage tool properly configured
- [ ] All test runs captured
- [ ] Coverage meets targets
- [ ] Critical paths have coverage
- [ ] Coverage report is accurate
- [ ] Trends tracked over time

### Success Criteria
- Coverage meets or exceeds targets
- Critical code paths tested
- Coverage trends improve
- New code has test coverage
- Defects caught by tests

### Failure Conditions
- Coverage below targets
- Critical paths untested
- Coverage gaps growing
- New code lacks tests
- False sense of coverage
