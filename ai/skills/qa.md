# QA Engineer Skills

This document defines reusable capabilities for the QA Engineer agent in testing and quality assurance.

## Strict QA Guardrails

The QA Engineer must not:
- Change or seed any data in the database.
- Change ports, endpoints, or other runtime configuration for testing.
- Modify implementation code outside of the test artifact area `artifacts/tests/`.
- Alter application behavior to make tests pass; instead, report defects and create test artifacts under `artifacts/tests/`.

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
3. If no matching test exists for the unit, create a new test case and place it in `artifacts/tests/test_scripts/backend_tests/unit/`
4. Write tests for happy path
5. Write tests for error cases
6. Write tests for boundary conditions
7. Write tests for edge cases
8. Set up test data and mocks
9. Run backend unit tests: `python artifacts/tests/test_scripts/run-all-tests.py --unit`
10. Verify all tests pass and measure code coverage

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

### Integration Testing Purpose
Create tests that verify multiple components work together correctly, validating system behavior end-to-end.

### When to Use Integration Tests
- Testing component interactions
- Testing API endpoints
- Testing workflows
- Verifying system integration

### Integration Test Inputs
- `components` (array): Components that integrate
- `workflows` (array): User workflows to test
- `api_specs` (array, optional): API endpoints to test
- `test_data` (object, optional): Data for integration tests
- `external_services` (array, optional): External dependencies

### Integration Test Outputs
- `integration_tests` (array): Integration test definitions
- `test_scenarios` (array): End-to-end test scenarios
- `test_data_setup` (object): How to prepare test data
- `mock_services` (array): Mock external dependencies
- `integration_report` (object): Integration test results

### Integration Test Dependencies
- Components available for testing
- Workflows documented
- API specs defined
- Test environment available

### Integration Test Steps
1. Identify component interactions to test
2. Map user workflows to test scenarios
3. If no integration or workflow test exists, generate a new Playwright E2E test and store it in `artifacts/tests/test_scripts/tests/persistence-*.spec.ts`
4. Create test data for scenarios (use `artifacts/tests/test_scripts/seed_data.py` to populate test database)
5. Set up test fixtures in Playwright test files
6. Write end-to-end tests validating API integrations
7. Test database persistence and interactions
8. Validate data flow across backend, frontend, and database layers
9. Run persistence E2E tests: `python artifacts/tests/test_scripts/run-all-tests.py --persistence`
10. Generate a full HTML QA summary at `artifacts/tests/qa-report.html` covering suite status, commands, exit codes, and detailed test-case results
11. Report integration test results with database verification

### Integration Test Validation
- [ ] All key workflows tested
- [ ] Component interactions verified
- [ ] Error handling tested
- [ ] Data flows correctly
- [ ] Performance acceptable
- [ ] External dependencies mocked

### Integration Test Success Criteria
- All integration tests pass
- Workflows execute correctly end-to-end
- Components integrate properly
- Performance meets requirements
- System behaves as expected

### Integration Test Failure Conditions
- Tests fail due to integration issues
- Workflows not working end-to-end
- Data lost or corrupted in flow
- Performance unacceptable
- Components incompatible

---

## Skill: Validate Authentication and Page Workflows

### Auth Workflow Validation Purpose
Validate critical user journeys across backend, frontend, and database layers,
ensuring authentication, input constraints, and page-level behavior meet the
documented requirements.

### When to Use Auth Validation
- Verifying signup and login flows
- Validating form rules and error handling
- Testing dashboard, project, task, comment, label, notification, and account pages
- Checking persistence and constraint behavior in the database

### Auth Validation Inputs
- `application_routes` (array): Backend endpoints and frontend routes to verify
- `business_rules` (array): Required validation rules and constraints
- `auth_scenarios` (array): Signup/login cases to exercise
- `page_flows` (array): Core user journeys and page states
- `static_analysis_context` (object, optional): Static analysis context (mypy/eslint/flake8 output)

### Auth Validation Outputs
- `workflow_validation_results` (object): Results for auth and page-flow checks
- `constraint_findings` (array): Missing or invalid validation findings
- `defect_report` (array): Issues discovered during workflow validation
- `recommendations` (array): Follow-up actions for failed scenarios

### Auth Validation Dependencies
- Application implementation available
- Requirements and acceptance criteria documented
- Static analysis tools available (mypy/eslint/flake8)

### Auth Validation Execution Steps
1. Run static analysis (mypy, eslint, flake8) for backend, frontend, and database code and capture results.
2. Generate Playwright E2E tests for acceptance criteria where appropriate; keep one spec file per feature and place in `artifacts/tests/test_scripts/tests/`.
3. Run generated Playwright tests automatically; capture and save failure screenshots to `artifacts/tests/e2e/screenshots`.
   - When a frontend or backend instance is already running, do not stop or restart the application.
     Use the local Playwright runner against the existing running services.
4. Review authentication requirements for signup and login workflows.
5. If the required workflow or validation test is missing, generate a new Playwright test case and publish it in `artifacts/tests/test_scripts/tests/`.
6. Exercise signup scenarios with missing email, invalid email, weak password, duplicate user, and valid data via Playwright.
7. Exercise login scenarios with unknown users, missing credentials, wrong password, and correct credentials via Playwright.
8. Validate core pages and flows for required-field checks, empty states, and successful completion paths via Playwright.
9. Confirm database constraints and persistence behavior for invalid or missing data (query DB directly at `apps/data/task_management.db` where needed).
10. Run all frontend E2E tests: `python artifacts/tests/test_scripts/run-all-tests.py --frontend`
11. Record failures, expected behavior, and remediation guidance.

### Auth Validation Checklist
- [ ] Missing input produces the expected validation error
- [ ] Invalid input fails safely and clearly
- [ ] Correct input proceeds to the expected success state
- [ ] Unknown user and wrong credentials are rejected appropriately
- [ ] Core pages expose the correct UX for empty/error/success states
- [ ] Database constraints are enforced or reported clearly
- [ ] Static analysis completed and Playwright tests executed; issues reviewed

### Auth Validation Success Criteria
- Authentication and page workflows behave according to documented requirements
- Invalid input is rejected with clear feedback
- Valid input reaches the expected success state
- Database and UI behavior remain consistent with the contract

### Auth Validation Failure Conditions
- Missing validation for required fields
- Authentication flows allow invalid accounts or leak incorrect state
- Page workflows fail without clear error handling
- Database constraints are not enforced or not surfaced
- Static analysis issues remain unresolved

---

## Skill: Generate Playwright E2E Tests

### Playwright Purpose
Generate maintainable Playwright end-to-end tests from user stories and acceptance criteria,
run tests, and capture failure artifacts.

### Playwright When to Use
- When an explicit user story or acceptance criterion requires an end-to-end verification
- For critical workflows (authentication, navigation, data persistence)

### Playwright Inputs
- `user_story` (object): User story with acceptance criteria and scenarios
- `local_url` (string): Local URL where the feature is deployed (for example,
  <http://localhost:5173/feature>)
- `selectors` (object, optional): DOM selectors or page object hints

### Playwright Outputs
- Playwright spec file saved under `tests/e2e/<feature-name>.spec.ts` or `.js`
- Failure screenshots saved under `artifacts/tests/e2e/screenshots`\
- `ui-live-test-report.md` summarizing execution results and links to screenshots

### Playwright Execution Steps
1. Parse the `user_story` and extract Gherkin-style scenarios.
2. Generate a Playwright spec file (one per feature) in
   `artifacts/tests/test_scripts/tests/<feature-name>.spec.ts` that implements the scenarios
   using Playwright test API and page objects where helpful.
3. Run Playwright tests automatically using the project's Playwright setup from `apps/frontend` directory.
4. On test failures, save screenshots and the test trace to `artifacts/tests/e2e/screenshots`.
5. Use master test runner: `python artifacts/tests/test_scripts/run-all-tests.py --frontend` to execute all frontend E2E tests.
6. Produce `ui-live-test-report.md` with pass/fail, failure screenshots, and rerun commands.
7. Generate a full HTML QA report at `artifacts/tests/qa-report.html` after the run so the overall results are available in a shareable format.

### Playwright Validation Checklist
- [ ] One spec file per feature is created
- [ ] Tests implement acceptance criteria exactly (no invented flows)
- [ ] Failure screenshots captured for each failed test
- [ ] Report includes target user story and local URL

### Playwright Success Criteria
- Playwright tests run and report results automatically
- Failure artifacts are stored and linked from reports
- Tests are maintainable and aligned with feature names

---

## Skill: Generate Test Data

### Test Data Purpose
Create realistic test data that exercises the system under realistic conditions and edge cases.

### Test Data When to Use
- Populating test databases
- Creating realistic user scenarios
- Testing with large datasets
- Testing error conditions

### Test Data Inputs
- `data_model` (object): System data model
- `test_scenarios` (array): Test scenarios requiring data
- `scale_expectations` (object, optional): How much data to generate
- `data_constraints` (array, optional): Business rules for data
- `edge_cases` (array, optional): Edge cases to cover

### Test Data Outputs
- `test_datasets` (array): Generated test data
- `data_generation_scripts` (array): Scripts to generate data
- `data_documentation` (object): Documentation of test data
- `seed_data` (object): Initial seed data for tests
- `edge_case_data` (array): Data for edge case testing

### Test Data Dependencies
- Data model defined
- Test scenarios documented
- Database schema available

### Test Data Execution Steps
1. Understand test data needs for each scenario
2. Create realistic sample data in `artifacts/tests/test_scripts/seed_data.py`
3. Generate edge case data (e.g., multiple users, complex task workflows, comment threads)
4. Create large datasets for performance testing
5. Implement data generation functions in seed_data.py
6. Validate generated data matches business constraints
7. Document test data usage and scenarios covered
8. Create data seeding procedures using: `python artifacts/tests/test_scripts/seed_data.py`
9. Store database at `apps/data/task_management.db`
10. Plan data cleanup or database reset procedures

### Test Data Validation Checklist
- [ ] Data matches business rules
- [ ] Edge cases covered
- [ ] Large datasets generated efficiently
- [ ] Data is realistic and representative
- [ ] Data can be regenerated consistently
- [ ] Data can be cleaned up after tests

### Test Data Success Criteria
- Tests have realistic data to work with
- Edge cases have corresponding data
- Performance tests have adequate volume
- Data generation is reproducible
- Data cleanup is automated

### Test Data Failure Conditions
- Data violates business rules
- Edge cases not covered
- Data generation is slow
- Cannot reproduce test conditions
- Data cleanup leaves artifacts

---

## Skill: Validate Test Coverage

### Coverage Purpose
Measure and analyze test coverage to ensure adequate testing and identify untested code paths.

### Coverage When to Use
- Reviewing test completeness
- Identifying gaps in testing
- Meeting coverage requirements
- Improving test quality

### Coverage Inputs
- `implementation` (object): Code to analyze
- `tests` (array): Test suite
- `coverage_targets` (object): Coverage goals by metric
- `critical_paths` (array, optional): Paths that must be tested

### Coverage Outputs
- `coverage_metrics` (object): Line, branch, path coverage
- `coverage_gaps` (array): Untested code paths
- `coverage_report` (object): Detailed coverage analysis
- `recommendations` (array): What to test next
- `coverage_visualization` (string): Coverage report format

### Coverage Dependencies
- Code and tests available
- Coverage tool configured
- Coverage targets defined

### Coverage Execution Steps
1. Run full test suite using master runner: `python artifacts/tests/test_scripts/run-all-tests.py --all`
2. Collect coverage metrics from backend unit tests using: `python -m pytest artifacts/tests/test_scripts/backend_tests/unit --cov=apps.backend.src --cov-report=html`
3. Analyze line coverage results
4. Analyze branch coverage for critical services
5. Identify untested code paths from coverage reports
6. Determine why critical paths are untested
7. Recommend unit/integration tests for gaps
8. Generate HTML coverage report in `htmlcov/index.html`
9. Track coverage over time and require coverage for new code

### Coverage Validation Checklist
- [ ] Coverage tool properly configured
- [ ] All test runs captured
- [ ] Coverage meets targets
- [ ] Critical paths have coverage
- [ ] Coverage report is accurate
- [ ] Trends tracked over time

### Coverage Success Criteria
- Coverage meets or exceeds targets
- Critical code paths tested
- Coverage trends improve
- New code has test coverage
- Defects caught by tests

### Coverage Failure Conditions
- Coverage below targets
- Critical paths untested
- Coverage gaps growing
- New code lacks tests
- False sense of coverage

---

## Skill: Run Comprehensive Test Suite (Master Test Runner)

### Master Runner Purpose
Execute all test types (backend unit, persistence E2E, frontend E2E) in a coordinated,
automated manner with centralized reporting and health checks.

### Master Runner When to Use
- Full QA validation across all layers (backend, frontend, database)
- Pre-deployment verification
- Regression testing after changes
- Continuous integration and continuous deployment (CI/CD)
- Validating complete system functionality

### Master Runner Inputs
- `test_type` (string, optional): Specific test type to run ("unit", "persistence", "frontend", "all")
- `environment_config` (object, optional): Backend URL, database path, frontend port
- `include_coverage` (boolean, optional): Generate code coverage reports

### Master Runner Outputs
- `test_execution_summary` (object): Pass/fail counts by test type
- `test_results_detailed` (array): Individual test results
- `failure_artifacts` (array): Screenshots and logs for failures
- `coverage_report` (object, optional): Code coverage metrics if requested
- `test_report.md` (file): Markdown summary of execution

### Master Runner Dependencies
- Backend running on `http://localhost:8001`
- Database at `apps/data/task_management.db`
- Frontend test suite available at `apps/frontend/`
- Backend test suite available at `artifacts/tests/test_scripts/backend_tests/unit/`
- Master test runner available at `artifacts/tests/test_scripts/run-all-tests.py`

### Master Runner Execution Steps
1. Execute master test runner with requested scope:
   - **All tests (default):** `python artifacts/tests/test_scripts/run-all-tests.py --all`
   - **Backend unit tests only:** `python artifacts/tests/test_scripts/run-all-tests.py --unit`
   - **Persistence E2E tests only:** `python artifacts/tests/test_scripts/run-all-tests.py --persistence`
   - **Frontend E2E tests only:** `python artifacts/tests/test_scripts/run-all-tests.py --frontend`
2. Verify prerequisites (backend health, database availability, dependencies installed)
3. Auto-seed database if tests require it (seed_data.py runs automatically)
4. Collect individual test results with pass/fail status
5. Capture failure screenshots for E2E tests
6. Generate colored status output for easy interpretation
7. Summarize execution with total tests, passed, and failed counts
8. Exit with success code (0) if all tests pass, failure code (1) if any test fails
9. Generate optional code coverage report if `--coverage` flag used
10. Publish final test report with links to artifacts

### Master Runner Validation Checklist
- [ ] Backend server is running and responsive
- [ ] Database file exists and is accessible
- [ ] All test dependencies installed (pytest, Playwright, npm packages)
- [ ] Test scripts are executable
- [ ] Results clearly show pass/fail for each test type
- [ ] Failures include diagnostic information (screenshots, logs)
- [ ] Summary report accessible and human-readable
- [ ] Exit codes properly indicate success/failure

### Master Runner Success Criteria
- All requested tests execute without errors
- Pass/fail status accurately reflects test results
- Any failures include diagnostic artifacts (screenshots, error logs)
- Execution completes within timeout (30 min for --all)
- Reports are clear and actionable
- Exit code 0 when all tests pass, 1 when failures exist

### Master Runner Failure Conditions
- Backend service unavailable
- Database cannot be accessed or is corrupted
- Test timeout without completion
- Unclear or missing failure diagnostics
- Exit code does not reflect actual test results
- Reports missing or unreadable

### Test Execution Matrix

| Command | Backend Unit | Persistence E2E | Frontend E2E | Estimated Time |
| --- | --- | --- | --- | --- |
| `--unit` | ✅ | ❌ | ❌ | ~10s |
| `--persistence` | ❌ | ✅ | ❌ | ~2-3m |
| `--frontend` | ❌ | ❌ | ✅ | ~5-10m |
| `--all` (default) | ✅ | ✅ | ✅ | ~15-20m |

### Integration with QA Agent Workflow

1. **Before running tests:**
   - Verify backend is running: `curl http://localhost:8001/api/v1/health`
   - Check database exists: `ls -la apps/data/task_management.db`
   - Seed test data if needed: `python artifacts/tests/test_scripts/seed_data.py`

2. **Run comprehensive tests:**
   - Execute: `python artifacts/tests/test_scripts/run-all-tests.py --all`
   - Monitor output for colored status indicators (✓ PASSED, ✗ FAILED)
   - Wait for completion (full suite ~15-20 minutes)

3. **After tests complete:**
   - Review summary output with pass/fail counts
   - If failures exist, examine screenshots in `artifacts/tests/e2e/screenshots/`
   - If backend tests fail, check `artifacts/tests/test_scripts/backend_tests/unit/` for issues
   - If persistence tests fail, verify database at `apps/data/task_management.db`
   - If frontend tests fail, check browser compatibility and selector changes

4. **Generate report:**
   - Full results displayed in terminal with colored output
   - Failure details link to specific artifacts
   - Exit code: 0 (success) or 1 (failure) for CI/CD integration

### Related Files and Locations

**Test Scripts:**
- Master runner: `artifacts/tests/test_scripts/run-all-tests.py`
- Integration tests: `artifacts/tests/test_scripts/run-integration-tests.py`
- Platform-specific runners: `.bat` and `.sh` versions in same directory

**Test Suites:**
- Backend unit tests: `artifacts/tests/test_scripts/backend_tests/unit/`
- Persistence E2E tests: `artifacts/tests/test_scripts/tests/persistence-integration.spec.ts`
- Frontend E2E tests: `artifacts/tests/test_scripts/tests/*.spec.ts` (~12 test files, ~120 tests)

**Test Data:**
- Seed script: `artifacts/tests/test_scripts/seed_data.py`
- Test database: `apps/data/task_management.db`

**Documentation:**
- Test scripts README: `artifacts/tests/test_scripts/README.md`
- API documentation: `docs/api-documentation.md`
- Integration testing guide: `docs/integration-testing-guide.md`
