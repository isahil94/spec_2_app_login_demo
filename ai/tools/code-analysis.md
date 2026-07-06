# Code Analysis Tool

Analyze, lint, and format code to ensure quality and consistency.

---

## Purpose

Provide agents with the ability to analyze code quality, apply formatting standards, identify issues, and validate code consistency across the project.

---

## When to Use

- Checking code formatting
- Running linting analysis
- Identifying code issues
- Applying code formatting fixes
- Validating import organization
- Checking for security issues
- Analyzing complexity
- Before committing code

---

## Available Operations

### Formatting Operations
- Check code formatting (Black)
- Apply code formatting automatically
- Check import organization (isort)
- Fix import organization

### Linting Operations
- Run flake8 analysis (currently implemented)
- Run pylint checks (optional, future enhancement)
- Run security checks (bandit - optional, future enhancement)
- Run type checking (mypy - optional, future enhancement)
- Custom linting rules

### Analysis Operations
- Analyze code complexity
- Identify code duplicates
- Find unused imports
- Identify style violations
- Detect security vulnerabilities

### Validation Operations
- Validate code against standards
- Check import order
- Check line length
- Check naming conventions

---

## Inputs

### Format Check/Fix
- **Path** (required): File or directory to format
- **Check Only** (optional): Check without modifying (default: false)
- **Formatter** (optional): black/isort/all (default: all)

### Linting
- **Path** (required): File or directory to lint
- **Strict** (optional): Fail on warnings
- **Tool** (optional): pylint/flake8/bandit/mypy/all
- **Disable Rules** (optional): Rules to disable

### Analysis
- **Path** (required): File or directory
- **Type** (optional): complexity/duplicates/unused-imports

---

## Outputs

### Format Output
- **Status**: Success/Failure
- **Files Modified**: Number of files changed
- **Changes**: Line additions/deletions
- **Issues Found**: Format violations if check-only

### Linting Output
- **Issue Count**: Total issues found
- **By Severity**: Errors/Warnings/Info
- **By File**: Issues grouped by file
- **Suggestions**: Remediation suggestions
- **Exit Code**: 0 for success, non-zero for failures

### Analysis Output
- **Complexity Score**: Code complexity metrics
- **Duplicates**: Duplicate code blocks
- **Unused**: Unused imports/variables
- **Report**: Detailed analysis report

---

## Dependencies

- **Black** - Code formatter (implemented)
- **isort** - Import sorter (implemented)
- **Flake8** - Style and error checker (implemented)
- **Pylint** - Code quality checker (optional, future enhancement)
- **Bandit** - Security checker (optional, future enhancement)
- **mypy** - Type checker (optional, future enhancement)
- **scripts/format.py** - Formatting helper (Black + isort)
- **scripts/lint.py** - Linting helper (Flake8)
- **Terminal MCP** - For execution

---

## Execution

**Method:** Terminal MCP + Helper Scripts

**How it works:**
1. Agent specifies code analysis operation
2. Helper scripts execute (format.py, lint.py)
3. Formatters/linters run on project
4. Results parsed and formatted
5. Issues reported with locations
6. Suggestions provided for fixes

**Primary tools:** Black (formatter), Flake8 (linter)

---

## Constraints

- Operates on Python code only
- Formatting is destructive (modifies files)
- Large codebases may take time
- Some rules may conflict (require configuration)
- Type checking may have false positives
- Performance depends on project size

---

## Best Practices

### Before Formatting
- Commit current changes first
- Review what will be formatted
- Understand formatting rules
- Verify backups exist

### Formatting Standards
- Use Black for consistency
- Use isort for import ordering
- Configure formatter for project standards
- Apply formatting before committing
- Don't disable important rules lightly

### Linting Strategy
- Fix errors (should be blockers)
- Fix warnings (should be resolved)
- Review info messages
- Disable false positives with reasoning
- Document disabled rules

### Security Analysis
- Run security scans on dependencies
- Check for hardcoded secrets
- Review security warnings
- Validate input handling
- Check authentication/authorization

### Type Checking
- Enable mypy for type hints
- Use type hints in code
- Review type errors carefully
- Use type ignore comments sparingly
- Improve type coverage gradually

---

## Error Handling

### Common Failures

**Format Conflict**
- Cause: Code conflicts with format rules
- Recovery: Review format rules, adjust code
- Log: Conflicting patterns

**Linting Error**
- Cause: Code violates linting rules
- Recovery: Fix code according to rules
- Log: Rule violations and suggestions

**Security Issue**
- Cause: Security vulnerability detected
- Recovery: Fix vulnerability immediately
- Log: Issue type and severity

**Type Mismatch**
- Cause: Type checking failed
- Recovery: Add type hints, fix type issues
- Log: Type mismatch locations

**Configuration Error**
- Cause: Linter configuration invalid
- Recovery: Fix configuration, validate
- Log: Configuration errors

**Timeout**
- Cause: Analysis takes too long
- Recovery: Optimize code, split analysis
- Log: Analysis duration and threshold

---

## Tool Integration Examples

### Check Code Formatting
```
Code Analysis: Check formatting
Path: scripts/
Check Only: true
Purpose: Verify formatting compliance
Output: Violations found, exit code
```

### Apply Formatting
```
Code Analysis: Format code
Path: scripts/
Formatter: black, isort
Purpose: Auto-format code
Output: Files modified, changes
```

### Run Linting
```
Code Analysis: Lint
Path: scripts/
Tool: pylint, flake8
Purpose: Identify quality issues
Output: Issues by severity and file
```

### Security Check
```
Code Analysis: Security scan
Path: scripts/
Tool: bandit
Purpose: Find security vulnerabilities
Output: Vulnerabilities by severity
```

---

## See Also

- **Terminal Tool** - For running tools manually
- **Testing Tool** - For validating code works
- **Filesystem Tool** - For viewing code being analyzed
- **Git Tool** - For committing formatted code

Reference: `shared.md` for common guidance on tool chaining and integration.
