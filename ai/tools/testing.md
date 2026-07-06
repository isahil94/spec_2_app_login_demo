# Testing Tool

Execute test suites, generate coverage reports, and validate code quality through testing.

---

## Purpose

Provide agents with the ability to run unit tests, integration tests, and coverage analysis to ensure code quality and prevent regressions.

---

## When to Use

- Before committing code
- Before creating pull requests
- During CI/CD pipeline
- Validating requirements implementation
- Measuring code coverage
- Debugging test failures
- Running specific test suites
- Generating test reports

---

## Available Operations

### Test Execution
- Run all unit tests
- Run specific test file
- Run tests matching pattern
- Run integration tests
- Run in verbose mode
- Stop on first failure

### Coverage Analysis
- Generate coverage report
- Show coverage by file
- Show coverage by function
- Measure branch coverage
- Generate HTML coverage report
- Set coverage minimum threshold

### Test Reporting
- Generate test report (XML, JSON)
- Show test statistics
- List failed tests
- Show test execution time
- Generate test timeline

### Test Filtering
- Run tests by name pattern
- Run tests by marker/tag
- Run only failed tests
- Run tests by module

---

## Inputs

### Test Execution
- **Test Path** (optional): Specific test file or directory
- **Pattern** (optional): Pattern to match test names
- **Verbose** (optional): Verbose output
- **Stop on Failure** (optional): Stop on first failure
- **Workers** (optional): Number of parallel workers

### Coverage
- **Minimum** (optional): Minimum coverage percentage (default: 80)
- **Report Format** (optional): xml/html/term (default: term)
- **Include** (optional): Modules to include (default: all)

### Reporting
- **Format** (optional): Output format (xml, json, html)
- **Output File** (optional): Write report to file

---

## Outputs

### Test Results
- **Passed**: Number of passed tests
- **Failed**: Number of failed tests
- **Skipped**: Number of skipped tests
- **Errors**: Number of errors
- **Duration**: Total execution time
- **Exit Code**: 0 for success, non-zero for failure

### Coverage Report
- **Total Coverage**: Overall coverage percentage
- **By File**: Coverage for each module
- **Uncovered Lines**: Lines not covered by tests
- **Coverage Minimum Met**: Boolean

### Detailed Output
- **Failed Test Names**: Names of failed tests
- **Error Messages**: Failure messages and tracebacks
- **Test Output**: Captured print/log output

---

## Dependencies

- **pytest** - Python testing framework
- **pytest-cov** - Coverage plugin for pytest
- **scripts/test.py** - Helper script for test execution
- **Terminal MCP** - For command execution

---

## Execution

**Method:** Terminal MCP + `scripts/test.py` Helper Script

**How it works:**
1. Agent invokes testing tool with parameters
2. Helper script receives test configuration
3. pytest executes tests in project
4. Coverage data collected
5. Reports generated
6. Results returned to agent

**Test framework:** pytest (configured in `pyproject.toml` or inline)

---

## Constraints

- Tests must be in `tests/` directory
- Test files must match `test_*.py` or `*_test.py` pattern
- Coverage minimum enforced (default 80%)
- Large test suites may take time
- Tests must be deterministic
- Tests should be isolated (no dependencies between tests)

---

## Best Practices

### Test Organization
- Organize tests by module (mirror source structure)
- Use descriptive test names
- Keep tests small and focused
- Use fixtures for setup/teardown
- Group related tests in classes

### Coverage Strategy
- Aim for high coverage (80%+)
- Cover happy paths and error cases
- Test edge cases and boundaries
- Don't test library code
- Don't test simple getters/setters

### Performance
- Run fast tests first
- Use parallel execution for speed
- Mock external dependencies
- Use fixtures for reuse
- Skip slow tests during development

### Debugging
- Use verbose output to see test details
- Run single failing test to debug
- Use print statements or logging
- Use pytest --pdb to debug interactively
- Review test failure output carefully

### CI/CD Integration
- Always run tests before commit
- Run tests on every PR
- Generate coverage reports
- Enforce minimum coverage
- Report test metrics

---

## Error Handling

### Common Failures

**Test Not Found**
- Cause: Specified test file/pattern doesn't exist
- Recovery: Verify test path, check file naming
- Log: Searched locations and patterns

**Import Error**
- Cause: Missing dependencies or import issues
- Recovery: Install dependencies, fix imports
- Log: Missing modules and suggestions

**Test Failure**
- Cause: Assertion failed or exception raised
- Recovery: Review failure output, fix code, re-run
- Log: Full failure traceback

**Coverage Below Minimum**
- Cause: Coverage percentage below threshold
- Recovery: Write more tests, review coverage report
- Log: Coverage percentage and requirements

**Timeout**
- Cause: Test takes too long
- Recovery: Optimize code, use mocks, split test
- Log: Test name and timeout value

**Setup/Teardown Error**
- Cause: Error in test fixture
- Recovery: Review fixture code, fix setup/teardown
- Log: Fixture name and error

---

## Tool Integration Examples

### Run All Tests
```
Testing: Run all tests
Verbose: true
Purpose: Verify all functionality works
Output: Test results, exit code
```

### Generate Coverage Report
```
Testing: Generate coverage
Minimum: 80%
Format: html
Purpose: Check coverage completeness
Output: Coverage percentage, report
```

### Run Tests Before Commit
```
Testing: Run tests
Pattern: test_*
Stop on Failure: true
Purpose: Validate changes before commit
Output: Pass/fail, duration
```

### Debug Failed Test
```
Testing: Run test
Path: tests/test_feature.py::test_specific
Verbose: true
Purpose: Investigate failure
Output: Full test output, traceback
```

---

## See Also

- **Code Analysis Tool** - For code quality beyond tests
- **Terminal Tool** - For manual test execution
- **GitHub Tool** - For reporting test status on PRs

Reference: `shared.md` for common guidance on test integration and reporting.
