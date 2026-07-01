# AI Tool Library

Complete tool definitions for the Agentic SDLC Platform.

**Version:** 1.0.0  
**Status:** Production Ready  
**Purpose:** Define available tools for Copilot agents

---

## Overview

The AI Tool Library provides a comprehensive, implementation-agnostic set of tool definitions for Copilot agents. These are NOT Python implementations—they define WHAT tools are available and WHEN to use them.

All tools execute through:
- MCP Servers (filesystem, git, github, database, browser)
- Existing Python helper scripts (format, lint, test, build)
- VS Code capabilities
- GitHub Actions

---

## Quick Reference

### Tools Available

| Tool | Domain | Purpose | Execution |
|------|--------|---------|-----------|
| **Terminal** | Commands | Run scripts and tools | Terminal MCP |
| **Filesystem** | Files | Read/write/search files | Filesystem MCP |
| **Git** | Version Control | Git operations | Git MCP |
| **GitHub** | Repository | GitHub API operations | GitHub MCP |
| **Testing** | Quality | Run tests, coverage | Terminal MCP + pytest |
| **Documentation** | Documentation | Generate and validate docs | Terminal MCP + Filesystem |
| **Code Analysis** | Quality | Lint, format, analyze | Terminal MCP + helpers |
| **Database** | Data | Query and manage database | Database MCP |
| **Browser** | UI | Browser automation | Playwright MCP (optional) |
| **Shared** | Guidance | Common best practices | Reference documentation |

---

## Tool Descriptions

### [terminal.md](terminal.md)

**Execute shell commands, scripts, and development tools.**

**Key Operations:**
- Run Python helper scripts (format.py, lint.py, test.py, build.py)
- Build applications
- Run formatters and linters
- Execute arbitrary commands

**Execution:** Terminal MCP Server  
**Dependencies:** Python, build tools from requirements.txt

---

### [filesystem.md](filesystem.md)

**Read, write, search, and manage files and directories.**

**Key Operations:**
- Read file contents (with line ranges)
- Write new files or update existing
- Search files by name or content pattern
- Create directories
- List directory contents

**Execution:** Filesystem MCP Server  
**Constraints:** All operations scoped to project root

---

### [git.md](git.md)

**Perform Git version control operations.**

**Key Operations:**
- Check repository status
- View diffs
- Commit changes
- Create/switch branches
- Restore files
- View commit history
- Create tags

**Execution:** Git MCP Server  
**Dependencies:** Git installation and configuration

---

### [github.md](github.md)

**Interact with GitHub API for repository management.**

**Key Operations:**
- Create and manage pull requests
- Create and manage issues
- Check workflow status
- Publish releases
- Trigger workflows
- View repository metadata

**Execution:** GitHub MCP Server  
**Dependencies:** GitHub authentication token

---

### [testing.md](testing.md)

**Execute test suites and generate coverage reports.**

**Key Operations:**
- Run unit tests
- Run integration tests
- Generate coverage reports
- Set coverage thresholds
- Generate test reports
- Filter and run specific tests

**Execution:** Terminal MCP + pytest  
**Dependencies:** pytest, pytest-cov

---

### [documentation.md](documentation.md)

**Generate, validate, and maintain documentation.**

**Key Operations:**
- Generate API documentation
- Validate README completeness
- Update README sections
- Generate changelogs
- Validate documentation structure
- Check for broken links

**Execution:** Terminal MCP + Filesystem  
**Dependencies:** Markdown tooling

---

### [code-analysis.md](code-analysis.md)

**Analyze code quality and apply formatting standards.**

**Key Operations:**
- Check code formatting (Black)
- Apply auto-formatting
- Check import organization (isort)
- Run linting (Pylint, Flake8)
- Run security checks (Bandit)
- Type checking (mypy)

**Execution:** Terminal MCP + Helper Scripts  
**Dependencies:** Black, isort, pylint, flake8, bandit, mypy

---

### [database.md](database.md)

**Inspect, query, and validate databases.**

**Key Operations:**
- Inspect database schemas
- Execute SQL queries
- Validate migrations
- Validate data integrity
- Create test data
- Generate schema documentation

**Execution:** Database MCP Server  
**Constraints:** Read-only for production databases

---

### [browser.md](browser.md)

**Automate browser interactions and validate UI.**

**Key Operations:**
- Navigate to URLs
- Click elements and fill forms
- Capture screenshots
- Validate UI elements
- Test user workflows
- Measure performance

**Execution:** Playwright MCP Server (optional, disabled by default)  
**Note:** Browser tool is optional, enable in .vscode/mcp.json if needed

---

### [shared.md](shared.md)

**Common guidance for all tools.**

**Coverage:**
- Tool selection strategy
- Security practices
- Validation patterns
- Error handling approach
- Logging best practices
- Tool chaining strategies
- Performance optimization
- Quality assurance
- Integration guidelines
- Common patterns
- Troubleshooting guide

---

## File Organization

```
ai/tools/
├── terminal.md            ← Command execution
├── filesystem.md          ← File operations
├── git.md                 ← Version control
├── github.md              ← Repository management
├── testing.md             ← Test execution
├── documentation.md       ← Documentation generation
├── code-analysis.md       ← Code quality
├── database.md            ← Database operations
├── browser.md             ← UI automation
├── shared.md              ← Common guidance
└── README.md              ← This file
```

---

## Usage Guide

### For Copilot Agents

Each agent can reference these tools in its instructions:

```markdown
## Available Tools

Use the following tools to accomplish tasks:

- **Terminal Tool** - Run scripts and commands
- **Filesystem Tool** - Read and write files
- **Git Tool** - Version control operations
- **GitHub Tool** - Repository management
- **Testing Tool** - Execute tests
- **Code Analysis Tool** - Check code quality
- **Documentation Tool** - Generate and validate docs
```

### For Skill Definitions

Skills can specify tool usage:

```yaml
Tools:
  - terminal: Run build process
  - testing: Execute tests
  - git: Commit changes
  - github: Create pull request
```

### For Workflow Documentation

Workflows can document tool chains:

```markdown
Workflow:
1. Filesystem: Read code
2. Code Analysis: Check quality
3. Testing: Run tests
4. Git: Commit
5. GitHub: Create PR
```

---

## Tool Execution Architecture

```
Agent Request
    ↓
Tool Dispatcher (reads tool definition)
    ↓
┌─────────────────────────────────┐
│ Tool Execution Layer            │
├─────────────────────────────────┤
│                                 │
│ ┌─ Terminal MCP ────────────────┤
│ │  (scripts, commands)          │
│ │                               │
│ ├─ Filesystem MCP ──────────────┤
│ │  (files, directories)         │
│ │                               │
│ ├─ Git MCP ─────────────────────┤
│ │  (version control)            │
│ │                               │
│ ├─ GitHub MCP ──────────────────┤
│ │  (repository API)             │
│ │                               │
│ ├─ Database MCP ────────────────┤
│ │  (database operations)        │
│ │                               │
│ └─ Playwright MCP ──────────────┤
│    (browser automation)         │
│                                 │
└─────────────────────────────────┘
    ↓
Result returned to Agent
```

---

## MCP Server Integration

### Enabled by Default

| Server | Configuration | Purpose |
|--------|---------------|---------|
| Filesystem | .vscode/mcp.json | File access |
| Git | .vscode/mcp.json | Version control |
| GitHub | .vscode/mcp.json | Repository API |
| Terminal | .vscode/mcp.json | Command execution |

### Optional (Disabled by Default)

| Server | Configuration | Purpose | Enable When |
|--------|---------------|---------|-------------|
| Database | .vscode/mcp.json | Database access | Needed for data operations |
| Playwright | .vscode/mcp.json | Browser automation | Needed for UI testing |

---

## Helper Scripts Integration

### Always Available

```
scripts/format.py    ← Code formatting (Black + isort)
scripts/lint.py      ← Code linting (Pylint + Flake8)
scripts/test.py      ← Test execution (pytest)
scripts/build.py     ← Build artifacts
```

### How Tools Use Them

- **Terminal Tool** - Can invoke directly: `python scripts/format.py`
- **Code Analysis Tool** - Uses Black/isort/Pylint via Terminal
- **Testing Tool** - Uses pytest via Terminal
- **Documentation Tool** - Can invoke helpers via Terminal

---

## Tool Selection Decision Tree

```
Task: Accomplish X

├─ Need to run a command?
│  └─ Use Terminal Tool
│
├─ Need to read/write files?
│  └─ Use Filesystem Tool
│
├─ Need to check git status or commit?
│  └─ Use Git Tool
│
├─ Need to create PR or check workflow?
│  └─ Use GitHub Tool
│
├─ Need to format or lint code?
│  └─ Use Code Analysis Tool
│
├─ Need to run tests?
│  └─ Use Testing Tool
│
├─ Need to document something?
│  └─ Use Documentation Tool
│
├─ Need to query database?
│  └─ Use Database Tool
│
└─ Need to test UI?
   └─ Use Browser Tool
```

---

## Common Workflows

### Code Commit Workflow
1. Filesystem: Read modified files
2. Code Analysis: Check formatting/linting
3. Testing: Run tests
4. Git: Check status
5. Git: Commit changes

### Feature Development Workflow
1. Filesystem: Read requirements
2. Terminal: Set up environment
3. Code Analysis: Validate code
4. Testing: Run tests
5. Git: Create feature branch
6. Git: Commit work
7. GitHub: Create pull request

### Release Workflow
1. Git: Check main branch status
2. Terminal: Build release
3. Testing: Run full suite
4. Documentation: Generate changelog
5. GitHub: Create release
6. Terminal: Deploy artifacts

### Code Review Workflow
1. GitHub: List pull requests
2. Filesystem: Read PR changes
3. Code Analysis: Check quality
4. Testing: Check test status
5. Git: Review diffs
6. GitHub: Add PR comments

---

## Best Practices

### ✓ DO

- ✓ Use existing helper scripts
- ✓ Follow tool documentation
- ✓ Chain tools logically
- ✓ Validate inputs and outputs
- ✓ Log tool operations
- ✓ Handle errors gracefully
- ✓ Use tools in parallel when possible
- ✓ Cache expensive results

### ✗ DON'T

- ✗ Create duplicate Python implementations
- ✗ Bypass tool definitions
- ✗ Ignore tool constraints
- ✗ Skip validation steps
- ✗ Hardcode sensitive data
- ✗ Chain too many tools (keep < 5)
- ✗ Ignore error messages
- ✗ Run tests multiple times unnecessarily

---

## Implementation Status

| Tool | Status | Lines | Coverage |
|------|--------|-------|----------|
| terminal.md | ✅ Ready | 200+ | Comprehensive |
| filesystem.md | ✅ Ready | 200+ | Comprehensive |
| git.md | ✅ Ready | 220+ | Complete |
| github.md | ✅ Ready | 220+ | Complete |
| testing.md | ✅ Ready | 220+ | Complete |
| documentation.md | ✅ Ready | 200+ | Complete |
| code-analysis.md | ✅ Ready | 220+ | Complete |
| database.md | ✅ Ready | 220+ | Complete |
| browser.md | ✅ Ready | 220+ | Complete |
| shared.md | ✅ Ready | 400+ | Comprehensive |

**Total:** 2,000+ lines of tool definitions  
**Format:** 100% Markdown  
**Python Code:** 0 lines (configuration-driven only)

---

## Integration with Project

### Copilot Instructions
Tools referenced in `.github/copilot-instructions.md`

### Agent Definitions
Agents can reference tools in `ai/agents/*.md`

### Chat Modes
Chat modes can include tool guidance in `.github/chatmodes/*.md`

### Skills
Skills can specify tool requirements in `ai/skills/*.md`

---

## Next Steps

### For Agents

1. **Reference in Instructions** - Add tool reference to agent definition
2. **Use in Workflows** - Include tool operations in tasks
3. **Chain Effectively** - Use tools in logical order
4. **Validate Results** - Check tool outputs before proceeding

### For Skills

1. **Specify Tool Requirements** - Document which tools are needed
2. **Provide Examples** - Show expected tool usage
3. **Handle Errors** - Document tool failure scenarios
4. **Document Outputs** - Show expected results

### For Team

1. **Review Tool Documentation** - Understand available tools
2. **Follow Best Practices** - Use guidance in shared.md
3. **Report Issues** - Provide feedback on tool effectiveness
4. **Suggest Improvements** - Request new tool capabilities

---

## FAQ

**Q: Can I create new tools?**  
A: Yes, follow the standard template (Purpose, When to Use, Operations, etc.) and add to ai/tools/

**Q: What if a tool doesn't support my use case?**  
A: Use Terminal Tool to run any custom command or script

**Q: How do I know which tool to use?**  
A: Use the decision tree above or check shared.md for patterns

**Q: Can I disable tools?**  
A: Yes, tools are optional. Disable in .vscode/mcp.json or agent instructions

**Q: How do tools integrate with Copilot?**  
A: Tools are reference definitions. Copilot Agent Mode handles actual execution via MCP servers

---

## Support & Resources

### Documentation
- **Tool Details** - Read individual tool files for specific operations
- **Best Practices** - See shared.md for common patterns
- **Examples** - Each tool includes usage examples

### Troubleshooting
- **Tool Not Working** - Check MCP server status
- **Unexpected Results** - Review tool constraints and inputs
- **Performance Issues** - See shared.md performance section
- **Integration Problems** - Check .vscode/mcp.json configuration

---

## Version History

**1.0.0** (2026-06-30) - Initial release
- 10 comprehensive tool definitions
- 2,000+ lines of documentation
- Full MCP server coverage
- Complete shared guidance
- Production ready

---

## Status

✅ **Production Ready**

All tools are fully documented, tested, and ready for use by Copilot agents.

---

**Created:** 2026-06-30  
**Version:** 1.0.0  
**Format:** Markdown  
**Implementation:** Configuration-Driven (NO Python code)  
**MCP Integration:** Full  
**Agent Ready:** Yes

---

See individual tool files for detailed usage information and examples.
