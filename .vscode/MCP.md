# MCP Server Configuration Guide

## Overview

This directory contains Model Context Protocol (MCP) server configuration for GitHub Copilot integration with the Agentic SDLC Platform.

## Files

- **`mcp.json`** - Main MCP server configuration (production-ready)

## What is MCP?

Model Context Protocol enables AI assistants (like GitHub Copilot) to securely interact with local tools and data through standardized interfaces.

In this project, MCP enables Copilot to:
- Read/write project files
- Access Git repository state
- Execute build/test/lint commands
- Query GitHub issues and PRs
- (Optionally) control Docker, databases, browsers

## Architecture

```
GitHub Copilot Chat
        ↓
    MCP Client
        ↓
   ├─ Filesystem Server (read/write files)
   ├─ Git Server (version control)
   ├─ Terminal Server (execute commands)
   ├─ GitHub Server (PR/issues)
   └─ Optional Servers (Docker, databases, etc.)
        ↓
   Local Development Environment
```

## Required Servers (Always Enabled)

### 1. Filesystem Server
**Purpose:** Read project files, write generated artifacts

**Capabilities:**
- Read files
- Write files  
- List directories
- Search files

**Security:**
- Sandboxed to allowed paths
- Restricted paths: `.git/objects`, `node_modules`, `.env`
- Rate limited: 100 reads, 20 writes, 50 searches per minute

**Use Cases:**
- Copilot reads specification files
- Copilot writes generated code to `artifacts/`
- Copilot searches for existing implementations

---

### 2. Git Server
**Purpose:** Version control operations

**Capabilities:**
- Get repository status
- View diffs
- Create commits
- Check branches
- View commit history

**Security:**
- Read-only operations allowed
- Restricted operations: `force_push`, `delete_branch`
- Rate limited: 30 diffs/minute, 10 commits/hour

**Use Cases:**
- Copilot checks if changes are staged
- Copilot reviews diffs before committing
- Copilot creates commits after code generation
- Copilot inspects branch history

---

### 3. Terminal Server
**Purpose:** Execute build, test, lint, and format commands

**Allowed Commands:**
```
npm, yarn, python, pip, eslint, black, pytest, 
docker, git, node, tsc, prettier
```

**Security:**
- Sandboxed execution
- 5-minute timeout per command
- Max 3 concurrent commands
- Restricted: `rm -rf /`, `sudo`, `chmod 777`, destructive commands
- Rate limited: 20 commands/minute
- Working directory locked to workspace root

**Use Cases:**
- Copilot runs tests after code generation
- Copilot formats code before commit
- Copilot runs linters
- Copilot builds Docker images

---

### 4. GitHub Server
**Purpose:** Integration with GitHub (requires authentication)

**Capabilities:**
- List pull requests
- List issues
- Get repository metadata
- Create pull requests

**Security:**
- Requires `GITHUB_TOKEN` environment variable
- Token-based authentication
- Allowed scopes: `repo:read`, `repo:write`
- Restricted scopes: `admin:repo_hook`, `delete_repo`
- Rate limited: 60 API calls/hour

**Use Cases:**
- Copilot checks existing PRs/issues
- Copilot creates pull requests with generated code
- Copilot reads repository metadata

---

## Optional Servers (Disabled by Default)

### Enable Playwright for UI Testing
```json
Move from optionalServers to mcpServers:
{
  "playwright": {
    "disabled": false,
    ...
  }
}
```

**Use when:** Building UI components, running browser automation tests

---

### Enable SQLite for Local Database Testing
```json
Move from optionalServers to mcpServers:
{
  "sqlite": {
    "disabled": false,
    "configuration": {
      "databasePath": "${workspaceFolder}/data/app.db"
    }
  }
}
```

**Requirements:** Database file must exist at specified path

**Use when:** Testing database layer with local SQLite

---

### Enable PostgreSQL for Production Database
```json
Move from optionalServers to mcpServers:
{
  "postgresql": {
    "disabled": false,
    ...
  }
}
```

**Requirements:** Environment variables must be set:
```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=app_db
export DB_USER=postgres
export DB_PASSWORD=<password>
```

**Use when:** Connected to production PostgreSQL database

---

### Enable Docker for Container Management
```json
Move from optionalServers to mcpServers:
{
  "docker": {
    "disabled": false,
    ...
  }
}
```

**Requirements:** Docker daemon must be running
```bash
docker ps  # Verify Docker is accessible
```

**Use when:** Building and deploying Docker containers

---

## Quick Start

### 1. Verify Prerequisites
```bash
# Check Node.js
node --version

# Check npm
npm --version

# Check Git
git --version
```

### 2. Install MCP CLI (Optional)
```bash
npm install -g @modelcontextprotocol/cli
```

### 3. Test Individual Servers
```bash
# Test filesystem
npx @modelcontextprotocol/server-filesystem .

# Test git
npx @modelcontextprotocol/server-git .

# Test terminal
npx @modelcontextprotocol/server-bash
```

### 4. Reload VS Code
After modifying `mcp.json`, reload VS Code:
- `Ctrl+Shift+P` → "Developer: Reload Window"

### 5. Verify in Copilot Chat
Ask Copilot:
```
@chatmode supervisor "What MCP servers are available?"
```

Copilot should respond with a list of configured servers.

---

## Configuration Best Practices

### Security

✅ **DO:**
- Keep `enabled: false` for unused optional servers
- Use environment variables for sensitive data
- Review MCP audit log regularly
- Use minimal necessary permissions
- Enable sandboxing (default)

❌ **DON'T:**
- Set `enabled: true` for optional servers you don't use
- Commit tokens or passwords to git
- Disable rate limiting
- Allow arbitrary command execution
- Trust unsigned servers

### Maintenance

1. **Review audit log monthly:**
   ```
   .vscode/mcp-audit.log
   ```

2. **Update MCP servers regularly:**
   ```bash
   npm update -g @modelcontextprotocol/server-*
   ```

3. **Test after updates:**
   ```
   @chatmode supervisor "Test MCP connectivity"
   ```

### Troubleshooting

**"MCP server not found"**
→ Install the server: `npm install -g @modelcontextprotocol/server-<name>`

**"Permission denied" errors**
→ Verify allowed paths in filesystem server configuration

**"Command not found"**
→ Check that command is in allowed commands list and in PATH

**"Rate limit exceeded"**
→ Check mcp-audit.log; increase rate limits if needed

**"Authentication failed"**
→ For GitHub, verify `GITHUB_TOKEN` environment variable

---

## Integration with Chat Modes

Each chat mode can access MCP servers:

### Business Analyst Mode
```
Reads: specification files (filesystem)
Writes: requirements-spec.md (filesystem)
Checks: Git status (git)
```

### Solution Architect Mode
```
Reads: requirements from BA (filesystem)
Writes: API contracts (filesystem)
Creates: commits (git)
```

### UI/UX Developer Mode
```
Tests: Components with Playwright (optional)
Commits: Changes (git)
Runs: Tests (terminal)
```

### Backend Developer Mode
```
Runs: Tests (terminal)
Queries: Database (optional: postgres/sqlite)
Creates: Pull requests (github)
```

### QA Engineer Mode
```
Reads: Test files (filesystem)
Writes: Test reports (filesystem)
Runs: Test suite (terminal)
Queries: Code coverage (terminal)
```

### Reviewer Mode
```
Reads: All code (filesystem)
Checks: Diffs (git)
Runs: Linters (terminal)
Queries: GitHub issues (github)
```

### DevOps Mode
```
Builds: Docker image (docker - optional)
Runs: Build commands (terminal)
Creates: Commits (git)
```

---

## Production Deployment

### Before Going Live

1. ✓ All required servers configured
2. ✓ Security restrictions in place
3. ✓ Rate limits appropriate for workload
4. ✓ MCP audit log enabled
5. ✓ Environment variables secured
6. ✓ Optional servers tested individually
7. ✓ Team trained on MCP concepts

### Monitoring

Check audit log:
```bash
tail -f .vscode/mcp-audit.log
```

Expected entries:
- Successful file reads/writes
- Git operations
- Terminal command execution
- Rate limit enforcements

Unexpected entries:
- Denied file access (check allowedPaths)
- Restricted command attempts
- Authentication failures

---

## Advanced Configuration

### Custom Rate Limits

Adjust in `mcp.json` for your team's needs:

```json
"rateLimits": {
  "fileReadsPerMinute": 200,      // Increase for large codebases
  "fileWritesPerMinute": 50,      // Increase for heavy generation
  "searchQueriesPerMinute": 100   // Increase for search-heavy workflows
}
```

### Custom Allowed Paths

Add project-specific paths:

```json
"allowedPaths": [
  "${workspaceFolder}",
  "${workspaceFolder}/artifacts",
  "${workspaceFolder}/generated",   // Add custom path
  "/mnt/shared/specs"               // Add external path
]
```

### Custom Allowed Commands

Add tools your team uses:

```json
"allowedCommands": [
  "npm", "yarn", "python", "pip",
  "myCustomTool",    // Add custom command
  "docker-compose"   // Add variant
]
```

---

## Reference

- [MCP Specification](https://modelcontextprotocol.io/)
- [GitHub Copilot Agent Mode](https://github.com/features/copilot)
- [VS Code Extension API](https://code.visualstudio.com/api)

---

**Last Updated:** 2026-06-30  
**Status:** Production Ready  
**Maintained By:** Agentic SDLC Platform Team
