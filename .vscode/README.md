# VS Code Configuration for Agentic SDLC Platform

This directory contains all VS Code configuration files for the Agentic SDLC Platform, including settings, tasks, extensions, and Model Context Protocol (MCP) servers.

## Files Overview

### Core Configuration

| File | Purpose |
|------|---------|
| **settings.json** | Python environment, formatting, linting, testing configuration |
| **extensions.json** | Recommended extensions (Copilot, Python, MCP, etc.) |
| **launch.json** | Debug configurations for Python and Node scripts |
| **tasks.json** | Automation tasks (build, test, format, lint, utility tasks) |


### Chat Modes

See [../.github/chatmodes/](../.github/chatmodes/) for 10 specialized Copilot chat modes.

---

## Quick Start

### 1. Install Recommended Extensions
```bash
# Option A: Manual install from marketplace
# - GitHub Copilot
# - Python
# - Type checking tools (mypy or equivalent)
# - Black Formatter
# - isort
# - Pytest

# Option B: VS Code will prompt automatically
# Check: Extensions panel → Recommended tab
```

### 2. Configure Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start Using Copilot
```
In VS Code Chat:
@chatmode supervisor "Show me the workflow"

Then:
@chatmode business-analyst "Analyze spec.md"
```

---

## Settings Configuration

### Python Settings (`settings.json`)

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.formatting.provider": "black",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

**What it does:**
- Sets Python interpreter to virtual environment
- Auto-formats code with Black on save
- Configures isort for import sorting
- Enables pytest discovery

---

## Tasks Configuration

### Available Tasks

Run via: `Ctrl+Shift+P` → "Tasks: Run Task"

| Task | Command | Purpose |
|------|---------|---------|
| **Build** | `npm run build` | Run tests and linting |
| **Test** | `pytest` | Run pytest test suite |
| **Lint** | `eslint . --ext .js` | Check code quality |
| **Format** | `black .` + `isort .` | Auto-format all code |
| **SDLC Entry** | `@chatmode supervisor` | Start and route SDLC workflow directly in Copilot Agent Mode |

### Example: Run All Tests
```
Ctrl+Shift+P → Tasks: Run Task → Test
```

---


## Chat Modes

### Available Agents (10 Total)

Each agent is a specialized Copilot chat mode:

1. **Supervisor** (@chatmode supervisor)
   - Orchestrates entire workflow
   - Manages approvals and gates

2. **Business Analyst** (@chatmode business-analyst)
   - Analyzes requirements
   - Creates user stories

3. **Solution Architect** (@chatmode solution-architect)
   - Designs system architecture
   - Creates API contracts
   - [APPROVAL GATE]

4. **UI/UX Developer** (@chatmode ui-ux-developer)
   - Builds React components
   - Creates pages and routing

5. **Backend Developer** (@chatmode backend-developer)
   - Implements API endpoints
   - Creates services

6. **Database Developer** (@chatmode database-developer)
   - Designs database schema
   - Creates migrations

7. **QA Engineer** (@chatmode qa-engineer)
   - Generates tests
   - Reports coverage

8. **DevOps & Release** (@chatmode devops-release)
   - Creates Dockerfile
   - Builds image

10. **Documentation** (@chatmode documentation)
    - Generates README
    - Creates API docs

### Using Chat Modes

```
In VS Code Chat:

1. Start with supervisor:
   @chatmode supervisor "Start building app"

2. Or jump to specific agent:
   @chatmode business-analyst "Analyze the spec"

3. Or parallel execution:
   @chatmode ui-ux-developer "Build frontend"
   @chatmode backend-developer "Build backend"
   @chatmode database-developer "Design database"
```

---

## Development Workflow

### Standard Workflow

```
1. Create spec.md (or use example)
2. Run: python main.py --spec=spec.md
3. In Copilot Chat: @chatmode supervisor "Start"
4. Answer approval gates (2 total)
5. Wait for generation (30-45 min)
6. Check results in artifacts/
7. Run: docker run -p 5000:5000 app:latest
```

### Debug Workflow

```
1. Enable debug mode:
   F5 (or Debug: Start Debugging)

2. Breakpoints in Python scripts:
   Click line number to set breakpoint

3. Debug Copilot interaction:
   Ctrl+Shift+P → Output: Focus Output (MCP)

```

### Testing Workflow

```
1. Run all tests:
   Ctrl+Shift+P → Tasks: Run Task → Test

2. Run specific test:
   Ctrl+Shift+P → Python: Debug Tests

3. Check coverage:
   pytest --cov=

4. View in UI:
   coverage html && open htmlcov/index.html
```

---

## Troubleshooting

### Tasks Not Running

Check:
1. **Python interpreter set:**
   ```
   Ctrl+Shift+P → Python: Select Interpreter
   ```

2. **Virtual environment activated:**
   ```bash
   which python  # Should show venv path
   ```

3. **Dependencies installed:**
   ```bash
   pip install -r requirements.txt
   ```

### Copilot Not Responding

Check:
1. **GitHub Copilot extension installed:**
   ```
   Extensions → Search "Copilot" → Install
   ```

2. **Signed in to GitHub:**
   ```
   Ctrl+Shift+P → Copilot: Sign In
   ```

3. **Chat enabled:**
   ```
   Ctrl+Shift+P → Copilot: Open Chat
   ```

---

## Production Checklist

Before deploying:

- [ ] Python interpreter configured
- [ ] Required extensions installed
- [ ] Security settings reviewed
- [ ] Rate limits appropriate
- [ ] Optional servers disabled (unless needed)
- [ ] Environment variables secured (.env in .gitignore)
- [ ] Team trained on workflows
- [ ] Backup plan documented

---

## Reference

- [GitHub Copilot Agent Mode](https://github.com/features/copilot)
- [VS Code Tasks Documentation](https://code.visualstudio.com/docs/editor/tasks)
- [VS Code Debugging](https://code.visualstudio.com/docs/editor/debugging)

---

## Support

### External Resources
- GitHub: https://github.com/modelcontextprotocol/
- VS Code: https://code.visualstudio.com/
- Python: https://www.python.org/

---

**Last Updated:** 2026-06-30  
**Status:** Production Ready  
**Maintained By:** Agentic SDLC Platform Team
