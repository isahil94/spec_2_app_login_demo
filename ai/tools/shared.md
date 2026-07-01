# Shared Tool Guidance

Common guidance for tool usage across all tools.

---

## Tool Selection Strategy

### When to Chain Multiple Tools

Agents should chain tools when performing complex workflows:

1. **Read configuration** (Filesystem)
2. **Validate format** (Code Analysis)
3. **Execute tests** (Testing)
4. **Commit changes** (Git)
5. **Create PR** (GitHub)

### Avoid Unnecessary Tool Calls

- Don't read files you don't need
- Don't run tests multiple times
- Cache results between calls
- Batch operations when possible

### Performance Optimization

- Run independent tools in parallel
- Use fast checks first (fail fast)
- Cache expensive operations
- Avoid redundant operations
- Monitor tool execution time

---

## Security Practices

### Input Validation

All tool inputs must be validated:
- Validate file paths are within project root
- Validate URLs are appropriate
- Validate command inputs for injection
- Sanitize user-supplied data
- Reject suspicious inputs

### Access Control

- Respect file permissions
- Don't bypass security checks
- Use appropriate database user/role
- Validate API token permissions
- Log all access attempts

### Secrets Management

Never expose secrets in:
- Log output
- Tool error messages
- Cached results
- Documentation
- Error reports

Use environment variables and secret vaults:
- GitHub secrets for API tokens
- MCP server configuration for credentials
- Local `.env` files (never commit)
- Credential helpers for passwords

---

## Validation Practices

### Verify Inputs

Before using tool results:
- Validate output format
- Check for errors/warnings
- Verify no unexpected changes
- Confirm operation success
- Validate state changes

### Cross-Validate Results

Use multiple approaches when critical:
- Run tests after deployment
- Check both Git and GitHub status
- Validate both locally and remotely
- Use multiple validation tools

### Fail Safely

- Always check exit codes
- Validate before proceeding
- Stop on critical errors
- Report issues clearly
- Provide recovery steps

---

## Error Handling Strategy

### Classification

Errors fall into categories:

**Recoverable Errors**
- Format issues (can be auto-fixed)
- Missing files (can be created)
- Type errors (can be corrected)

**Warning Errors**
- Coverage below threshold (non-blocking)
- Deprecated APIs (warn but proceed)
- Style violations (non-critical)

**Critical Errors**
- Test failures (blocking)
- Security vulnerabilities (blocking)
- Build failures (blocking)

### Recovery Steps

For each error type:
1. Classify severity
2. Provide clear error message
3. Suggest remediation
4. Offer retry or abort
5. Log for debugging

### Logging

Always log:
- Tool name and operation
- Input parameters
- Start/end timestamps
- Exit code or status
- Any errors or warnings
- Resource usage (if relevant)

---

## Logging Best Practices

### Structured Logging

Log entries should include:
- **Timestamp** - When operation occurred
- **Tool** - Which tool was invoked
- **Operation** - What was being done
- **Status** - Success/failure/warning
- **Duration** - How long it took
- **Resources** - Files, queries, or commands
- **Result** - What happened
- **Error** - Error message if failed

### Log Levels

- **DEBUG** - Detailed diagnostic info
- **INFO** - General informational messages
- **WARN** - Warning messages (recoverable issues)
- **ERROR** - Error messages (failures)
- **CRITICAL** - Critical failures (must stop)

### What to Log

✓ Tool invocation and parameters  
✓ Execution start and end times  
✓ Exit codes and status  
✓ File paths and operations  
✓ Configuration being used  
✓ Any warnings or issues  
✓ Summary statistics  

✗ Sensitive data (passwords, tokens)  
✗ Full file contents (use summaries)  
✗ Credentials (use placeholder)  
✗ Personally identifiable information  

---

## Tool Chaining

### Effective Chains

Good tool chains follow logical workflows:

**Code Review Chain:**
1. Read code (Filesystem)
2. Analyze code quality (Code Analysis)
3. Run tests (Testing)
4. Check coverage (Testing)

**Commit Chain:**
1. Check status (Git)
2. Review changes (Git - diff)
3. Format code (Code Analysis)
4. Commit (Git)
5. Push (GitHub)

**Release Chain:**
1. Validate (Quality - all checks)
2. Build (Terminal)
3. Test (Testing)
4. Create release (GitHub)
5. Deploy (Terminal)

### Avoid Anti-Patterns

❌ Don't repeat identical operations  
❌ Don't chain too many operations (>5)  
❌ Don't ignore intermediate errors  
❌ Don't skip validation steps  
❌ Don't run tests multiple times  

---

## Performance Considerations

### Optimization Strategies

**Fail Fast**
- Run quick checks first
- Stop on critical errors
- Don't continue after failures

**Parallel Execution**
- Run independent tools in parallel
- Execute tests in parallel
- Combine validations

**Caching**
- Cache file contents
- Reuse lint/format results
- Remember test results

**Batching**
- Batch file operations
- Combine validations
- Group similar operations

### Performance Monitoring

Track execution time for:
- Individual tool calls
- Complete workflows
- Test suites
- Build processes

Alert if:
- Single tool exceeds threshold
- Workflow slows down significantly
- Tests take too long
- Build time increases

---

## Quality Assurance

### Pre-Operation Checks

Before executing critical operations:
- [ ] Verify inputs are valid
- [ ] Check permissions
- [ ] Validate configuration
- [ ] Confirm desired operation
- [ ] Have backup/recovery plan

### Post-Operation Validation

After executing operations:
- [ ] Verify exit code
- [ ] Check for errors
- [ ] Validate output format
- [ ] Confirm state changes
- [ ] Log results

### Health Checks

Regular health checks:
- [ ] MCP servers responding
- [ ] Connections stable
- [ ] Resources available
- [ ] Configurations valid
- [ ] Tools functional

---

## Integration Guidelines

### Tool Dependencies

Respect tool dependencies:

```
Testing Tool
    ↓ (requires)
Terminal Tool
    ↓ (uses)
Code Analysis Tool
    ↓ (reads)
Filesystem Tool
```

### Execution Model

Sequential execution for dependent operations:
```
1. Filesystem Tool (read files)
2. Code Analysis Tool (check quality)
3. Terminal Tool (run scripts)
4. Testing Tool (run tests)
5. Git Tool (commit)
6. GitHub Tool (create PR)
```

Parallel execution for independent operations:
```
Code Analysis Tool
    ↘
      → Testing Tool → Combined Results
    ↗
Documentation Tool
```

---

## Common Patterns

### Validate Before Commit

```
1. Filesystem: Read modified files
2. Code Analysis: Check formatting
3. Testing: Run tests
4. Git: Commit if all pass
```

### Pre-PR Checks

```
1. Code Analysis: Lint and format
2. Testing: Run full suite
3. Coverage: Check coverage threshold
4. Documentation: Validate docs
5. GitHub: Create PR
```

### Release Workflow

```
1. Git: Create release branch
2. Terminal: Build and test
3. Documentation: Generate changelog
4. GitHub: Create release
5. Terminal: Deploy artifacts
```

---

## Troubleshooting

### General Approach

When a tool operation fails:

1. **Check inputs** - Are parameters valid?
2. **Review logs** - What error was reported?
3. **Verify state** - What changed before failure?
4. **Check dependencies** - Are required tools working?
5. **Retry safely** - Attempt recovery
6. **Escalate** - Report if unrecoverable

### Common Issues

**Tool not responding**
- Check MCP server status
- Verify network connectivity
- Review server logs

**Unexpected output format**
- Verify tool version
- Check output parsing
- Try alternative approach

**Performance degradation**
- Check resource usage
- Review system load
- Optimize tool parameters

**Permission issues**
- Check user permissions
- Verify file/directory access
- Request elevated privileges

---

## Best Practices Summary

✓ **Validate** - Check inputs and outputs  
✓ **Fail Fast** - Stop on errors  
✓ **Log** - Record all operations  
✓ **Chain Wisely** - Logical workflows  
✓ **Secure** - Protect sensitive data  
✓ **Efficient** - Optimize performance  
✓ **Document** - Explain decisions  
✓ **Test** - Verify operations work  
✓ **Monitor** - Track execution  
✓ **Recover** - Handle failures gracefully  

---

## See Also

Refer to specific tool documentation for detailed usage:
- `terminal.md` - Execute commands
- `filesystem.md` - File operations
- `git.md` - Version control
- `github.md` - Repository management
- `testing.md` - Test execution
- `documentation.md` - Documentation
- `code-analysis.md` - Code quality
- `database.md` - Database operations
- `browser.md` - UI automation

---

## Questions?

For tool usage questions:
1. Check specific tool documentation
2. Review tool integration examples
3. Check this shared guidance
4. Review agent instructions
5. Check project README

All tools integrate with GitHub Copilot Agent Mode and follow configuration-driven architecture principles.
