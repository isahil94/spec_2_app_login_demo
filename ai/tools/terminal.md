# Terminal Tool

Execute shell commands, scripts, and development tools.

---

## Purpose

Provide agents with the ability to run terminal commands, build scripts, tests, formatters, linters, and other command-line tools within the project environment.

---

## When to Use

- Executing build processes
- Running test suites
- Formatting code
- Running linting checks
- Executing helper scripts
- Running Git commands
- Installing dependencies
- Running documentation generators
- Any shell command execution needed for workflow

---

## Available Operations

### Script Execution
- Run Python helper scripts (`scripts/format.py`, `scripts/lint.py`, `scripts/test.py`, `scripts/build.py`)
- Run shell scripts
- Execute arbitrary commands

### Build Operations
- Build application
- Build Docker images
- Build documentation
- Build packages

### Development Tools
- Format code (Black, isort)
- Lint code (Pylint, Flake8)
- Run tests (pytest)
- Generate coverage reports
- Run security scans

### Utility Operations
- Check versions
- Install packages (pip)
- Copy files
- Create directories
- Print environment info

---

## Inputs

**Command**
- Type: string
- Description: Shell command to execute
- Required: yes

**Working Directory**
- Type: string
- Description: Directory to execute command in (defaults to project root)
- Required: no

**Timeout**
- Type: integer
- Description: Maximum execution time in seconds (defaults to 120)
- Required: no

**Fail on Error**
- Type: boolean
- Description: Whether to fail if command returns non-zero exit code
- Required: no (default: true)

---

## Outputs

**Exit Code**
- Type: integer
- Description: Command exit code (0 = success)

**Stdout**
- Type: string
- Description: Standard output from command

**Stderr**
- Type: string
- Description: Standard error output from command

**Duration**
- Type: float
- Description: Command execution time in seconds

---

## Dependencies

- **Terminal MCP Server** - Provides terminal execution capability
- **VS Code Terminal** - Built-in VS Code terminal
- **Python Interpreter** - For running Python scripts
- **Helper Scripts** - `scripts/format.py`, `scripts/lint.py`, `scripts/test.py`, `scripts/build.py`
- **Build Tools** - Black, isort, Pylint, Flake8, pytest, etc. (from `requirements.txt`)

---

## Execution

**Method:** Terminal MCP Server + VS Code Terminal

**How it works:**
1. Agent specifies terminal command
2. Terminal MCP server receives command
3. Command executes in project workspace
4. Output captured (stdout, stderr)
5. Exit code returned
6. Results available to agent

**Alternative:** VS Code Tasks (for predefined workflows)

---

## Constraints

- Commands execute in workspace context
- No root/elevated privileges (unless explicitly configured)
- Timeout enforcement (default 120 seconds)
- Command output buffered (large outputs may be truncated)
- No interactive input (non-interactive mode)
- Working directory must be within project

---

## Best Practices

### Script Selection
- Prefer using existing helper scripts (`scripts/format.py`, `scripts/lint.py`, etc.)
- Chain operations when possible (avoid multiple sequential commands)
- Use specific commands rather than generic shell operations

### Error Handling
- Always check exit codes
- Log full command before execution
- Capture and report all output
- Suggest remediation for common errors

### Performance
- Use timeouts to prevent hanging
- Run tests in parallel when supported
- Use caching where available
- Monitor long-running operations

### Logging
- Log the exact command being executed
- Include working directory
- Record start/end times
- Capture full output for debugging

### Security
- Sanitize command inputs
- Never execute user-supplied commands without validation
- Avoid shell injection vulnerabilities
- Log all commands executed

---

## Error Handling

### Common Failures

**Timeout**
- Cause: Command takes longer than timeout
- Recovery: Increase timeout, optimize command, split into smaller tasks
- Log: Record timeout and partial output

**Command Not Found**
- Cause: Script or binary not in PATH
- Recovery: Use full path, check installation, install dependencies
- Log: Suggest installation command

**Exit Code Non-Zero**
- Cause: Command failed (normal behavior for some tools)
- Recovery: Examine output, fix issue, retry
- Log: Full stdout and stderr

**Insufficient Permissions**
- Cause: User lacks permissions for operation
- Recovery: Check file permissions, adjust access, retry
- Log: Permission requirements

**Workspace Not Found**
- Cause: Project root not accessible
- Recovery: Verify project path, check access
- Log: Path and error details

---

## Tool Integration Examples

### Format Code
```
Terminal: python scripts/format.py
Purpose: Auto-format code to project standards
Output: Formatted files
```

### Run Tests
```
Terminal: python -m pytest tests/ -v
Purpose: Execute test suite
Output: Test results, exit code
```

### Lint Code
```
Terminal: python scripts/lint.py
Purpose: Check code quality
Output: Lint report, exit code
```

### Build Application
```
Terminal: python scripts/build.py
Purpose: Build release artifacts
Output: Build directory, artifacts
```

---

## See Also

- **Code Analysis Tool** - For linting and formatting
- **Testing Tool** - For test execution
- **Filesystem Tool** - For file operations
- **Git Tool** - For version control commands

Reference: `shared.md` for common guidance on tool chaining and security.
