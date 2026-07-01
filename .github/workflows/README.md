# GitHub Actions CI/CD Pipeline

**Version:** 1.0.0  
**Status:** Production Ready  
**Created:** 2026-06-30

## Overview

This directory contains production-ready GitHub Actions workflows for the Agentic SDLC Platform. The CI/CD pipeline is designed to:

1. **Automate quality checks** on every push and pull request
2. **Validate project structure** and configurations
3. **Generate and validate** documentation
4. **Build and publish** releases

---

## Workflows

### 1. CI Pipeline (`ci.yml`)

**Purpose:** Run continuous integration checks on every push and pull request.

**Triggers:**
- Push to `main`, `develop`, or feature branches
- Pull requests to `main` or `develop`

**Jobs:**
- **Format Check** - Uses Black formatter
  - Reuses: Python's `black` module
  - Suggests: `python scripts/format.py`

- **Import Sort Check** - Uses isort
  - Reuses: Python's `isort` module
  - Suggests: `python scripts/format.py`

- **Linting** - Uses Pylint and Flake8
  - Reuses: Python's `pylint` module
  - Continues on error (warnings don't block)
  - Suggests: `python scripts/lint.py`

- **Unit Tests** - Runs pytest
  - Reuses: Python's `pytest` module
  - Generates: `test-results.xml`
  - Uploads: Test results as artifact

- **Coverage Report** - Generates coverage report
  - Reuses: `pytest --cov`
  - Uploads: Coverage to Codecov
  - Continues on error

**Features:**
- ✓ Caches pip dependencies for faster runs
- ✓ Parallel execution of independent jobs
- ✓ Python 3.11 pinned
- ✓ Continues on errors for non-critical checks
- ✓ Uploads artifacts for review

**Reused Assets:**
- `scripts/format.py` (via Black/isort)
- `scripts/lint.py` (via Pylint)
- `scripts/test.py` (via pytest)

---

### 2. Quality Assurance (`quality.yml`)

**Purpose:** Validate repository structure, configurations, and project assets.

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main` or `develop`

**Jobs:**
- **Repository Structure** - Validates required directories and files
  - Checks: `ai/`, `orchestration/`, `scripts/`, `.github/`, `docs/`
  - Fails: If any required directory/file is missing
  - Success: All core project assets present

- **YAML Validation** - Validates workflow and config YAML
  - Reuses: `yamllint`
  - Checks: `.github/workflows/`, `ai/` configs

- **JSON Validation** - Validates all JSON files
  - Reuses: Python's `json.tool`
  - Checks: `.vscode/mcp.json`, chat mode configs

- **Markdown Validation** - Checks Markdown syntax
  - Reuses: `markdownlint`
  - Checks: `*.md` files, broken links

- **AI Configuration** - Validates agent definitions and contracts
  - Checks: All 10 agent definitions present
  - Checks: 8 contract definitions present
  - Checks: 10 chat modes present
  - Fails: If any required AI asset is missing

- **Hook Configuration** - Validates hook definitions and implementations
  - Checks: `ai/hooks/hooks.md` exists
  - Checks: All 5 hook scripts present
  - Fails: If hook system is incomplete

- **MCP Configuration** - Validates Model Context Protocol setup
  - Checks: `.vscode/mcp.json` syntax
  - Runs: `.vscode/validate-mcp.js` validation script
  - Verifies: MCP servers are properly configured

**Features:**
- ✓ Comprehensive structure validation
- ✓ Multi-format validation (YAML, JSON, Markdown)
- ✓ AI-specific asset validation
- ✓ Configuration consistency checks
- ✓ Fails fast on critical validation errors

**Reused Assets:**
- MCP validation script: `.vscode/validate-mcp.js`
- Project configuration files

---

### 3. Documentation Validation (`documentation.yml`)

**Purpose:** Validate and maintain documentation quality.

**Triggers:**
- Push to `main` or `develop` (when `docs/**` or README changes)
- Pull requests affecting documentation
- Manual trigger via `workflow_dispatch`

**Jobs:**
- **README Validation** - Checks README.md completeness
  - Checks: File exists and has content
  - Suggests: Key sections (Overview, Features, Architecture, etc.)
  - Validates: Documentation completeness

- **Documentation Files** - Validates core documentation
  - Checks: `docs/` directory exists
  - Optional: `docs/architecture.md`
  - Optional: `docs/developer-guide.md`
  - Optional: `docs/project-structure.md`

- **Developer Guide** - Validates developer documentation
  - Checks: Setup, Architecture, Development, Testing sections
  - Optional: Not required but recommended

- **AI Configuration Documentation** - Validates AI-specific docs
  - Checks: Hook documentation (README, strategy, guides)
  - Checks: Copilot instructions
  - Verifies: Documentation is complete and non-empty

- **Markdown Format Check** - Validates Markdown formatting
  - Reuses: `markdownlint` and `prettier`
  - Non-blocking: Formatting issues don't block release

- **Workflow Documentation** - Checks for workflow documentation
  - Checks: Workflows referenced in docs
  - Suggests: Add workflow descriptions to README

**Features:**
- ✓ Validates core documentation
- ✓ Checks markdown formatting
- ✓ Uploads documentation artifacts
- ✓ Non-blocking for format issues
- ✓ Artifacts retained for 30 days

**Reused Assets:**
- None (uses standard Markdown validators)

---

### 4. Release Pipeline (`release.yml`)

**Purpose:** Validate, build, and publish releases.

**Triggers:**
- Release creation/publication
- Manual trigger with tag input

**Jobs:**
- **Prepare Release** - Extracts and validates version
  - Extracts: Tag from release or input
  - Outputs: Version and tag for subsequent jobs
  - Validates: Tag format

- **Validate Release** - Runs full validation suite
  - Format check: Black
  - Linting: Pylint
  - Tests: pytest
  - CHANGELOG: Validates release notes exist
  - Reuses: All code quality helpers
  - Fails: If validation fails (blocking)

- **Build Release** - Builds release artifacts
  - Reuses: `python -m build`
  - Outputs: `dist/` and `build/` directories
  - Uploads: Artifacts retained for 30 days

- **Generate Release Notes** - Extracts release notes from CHANGELOG
  - Extracts: Release notes for version
  - Generates: Release notes markdown
  - Outputs: Release notes for GitHub Release

- **Build Docker Image** - Builds Docker image (optional)
  - Checks: Dockerfile exists
  - Continues on error: Not required
  - Outputs: OCI image format

- **Publish Release** - Publishes GitHub Release
  - Requires: Validation to pass
  - Creates: GitHub Release with notes
  - Uploads: Build artifacts
  - Allows: Updates to existing releases

- **Release Notification** - Notifies team (optional)
  - Creates: Deployment event
  - Logs: Next steps
  - Continues on error

**Features:**
- ✓ Full validation before release
- ✓ Automated artifact building
- ✓ Release notes generation
- ✓ Optional Docker image building
- ✓ GitHub Release creation
- ✓ Blocking validation (fails if tests fail)

**Reused Assets:**
- `scripts/format.py` (via Black)
- `scripts/lint.py` (via Pylint)
- `scripts/test.py` (via pytest)

---

## Workflow Relationships

```
Code Push
├── CI Pipeline (ci.yml)
│   ├── Format Check
│   ├── Import Check
│   ├── Linting
│   └── Tests
│
├── Quality Assurance (quality.yml)
│   ├── Structure Validation
│   ├── Config Validation
│   ├── AI Assets Validation
│   └── Hook Validation
│
└── Documentation (documentation.yml) [on doc changes]
    ├── README Validation
    ├── Docs Validation
    └── Markdown Format

Release Trigger
└── Release Pipeline (release.yml)
    ├── Prepare
    ├── Validate (runs CI checks again)
    ├── Build
    ├── Release Notes
    ├── Docker Build (optional)
    ├── Publish
    └── Notify
```

---

## Reused Assets

### Helper Scripts

| Script | Used By | Purpose |
|--------|---------|---------|
| `scripts/format.py` | CI, Release | Code formatting (Black, isort) |
| `scripts/lint.py` | CI, Release | Code quality (Pylint, Flake8) |
| `scripts/test.py` | CI, Release | Testing (pytest, coverage) |
| `scripts/build.py` | Release | Package building |

### Configuration Files

| File | Used By | Purpose |
|------|---------|---------|
| `.vscode/mcp.json` | Quality | MCP server configuration |
| `.vscode/validate-mcp.js` | Quality | MCP validation |
| `.github/copilot-instructions.md` | Documentation | Copilot configuration |
| `ai/hooks/hooks.md` | Quality | Hook definitions |
| `CHANGELOG.md` | Release | Release notes source |

### AI Assets

| Asset | Validated By | Purpose |
|-------|--------------|---------|
| 10 Agent definitions | Quality | Supervisor orchestration |
| 8 Contract definitions | Quality | Interface contracts |
| 10 Chat modes | Quality | Copilot integration |
| 5 Hook implementations | Quality | Git/GitHub automation |

---

## Best Practices Implemented

### 1. **Fail Fast**
- Critical validations block the pipeline
- Non-critical checks continue on error
- Clear error messages guide remediation

### 2. **Caching**
- Pip dependency caching reduces run time
- Speeds up CI/CD execution
- Reduces GitHub Actions usage

### 3. **Modularity**
- Each job has single responsibility
- Jobs can run in parallel (no dependencies unless needed)
- Easy to add/remove validation jobs

### 4. **Artifact Management**
- Test results uploaded for review
- Coverage reports uploaded
- Build artifacts retained 30 days
- Documentation artifacts generated

### 5. **Concurrency**
- Previous runs cancelled on new push
- Prevents redundant workflow execution
- Saves CI/CD minutes

### 6. **No Duplication**
- Helper scripts reused across workflows
- Consistent validation logic
- Single source of truth for each check

### 7. **Documentation**
- Clear comments in YAML
- Job names describe purpose
- Step descriptions explain actions

### 8. **Error Handling**
- Continue-on-error for non-blocking checks
- Proper exit codes on failures
- Informative error messages

---

## Running Workflows Locally

### Test CI Pipeline Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Format code
python scripts/format.py

# Lint code
python scripts/lint.py

# Run tests
python scripts/test.py
```

### Test Quality Checks

```bash
# Validate YAML
yamllint .github/workflows/

# Validate JSON
python -m json.tool .vscode/mcp.json

# Validate project structure
ls -la ai/ orchestration/ scripts/ .github/
```

### Test Documentation

```bash
# Check markdown
markdownlint README.md docs/*.md

# Check links (manual)
grep -r "^\[.*\](.*\.md)" docs/ README.md
```

---

## GitHub Actions Permissions

Required permissions in repository settings:

```yaml
Permissions:
  - Contents: read/write (for releases)
  - Pull Requests: read/write (for PR comments)
  - Checks: read/write (for check runs)
```

## Secrets (Optional)

For enhanced functionality, add these secrets:

```yaml
CODECOV_TOKEN       # For Codecov integration
DOCKER_USERNAME     # For Docker Hub push
DOCKER_PASSWORD     # For Docker Hub push
SLACK_WEBHOOK_URL   # For Slack notifications
```

---

## Monitoring & Troubleshooting

### View Workflow Runs

1. Go to GitHub repository → **Actions**
2. Select workflow (CI, Quality, Documentation, Release)
3. View run details and logs

### Debug Failed Runs

```bash
# Download logs from GitHub
gh workflow run logs <RUN_ID>

# Or view in browser
https://github.com/<owner>/<repo>/actions/runs/<RUN_ID>
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Format check fails | Run `python scripts/format.py` locally |
| Lint errors | Run `python scripts/lint.py` and fix issues |
| Tests fail | Run `python -m pytest tests/` locally |
| Structure validation fails | Check required directories exist |
| AI asset missing | Verify `ai/agents/`, `ai/contracts/` files |
| MCP validation fails | Check `.vscode/mcp.json` syntax |

---

## Integration with Copilot Agent Mode

These workflows do NOT conflict with Copilot Agent Mode:

- ✓ Workflows validate CODE QUALITY and PROJECT STRUCTURE
- ✓ Copilot orchestrates AGENT EXECUTION
- ✓ No overlap in functionality
- ✓ Workflows provide validation DATA for chat modes

**Integration Points:**
- Quality checks can be invoked by chat modes
- Validation results passed to agents
- Release validation gates approvals
- Chat modes trigger manual workflow runs

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│          GitHub Actions CI/CD                  │
└─────────────────────────────────────────────────┘
                    ↓
        ┌───────────┬───────────┬────────────┐
        ↓           ↓           ↓            ↓
    ┌────────┐  ┌────────┐  ┌──────────┐  ┌────────┐
    │   CI   │  │Quality │  │   Docs   │  │Release │
    └────────┘  └────────┘  └──────────┘  └────────┘
        ↓           ↓           ↓            ↓
    Format      Structure    README      Validate
    Lint        Assets       Guides      Build
    Test        Configs      Format      Publish
    Coverage    Validation   Artifacts   Release
        ↓           ↓           ↓            ↓
    [Helper     [Config     [Markdown   [Helper
     Scripts]   Files]      Tools]      Scripts]
        ↓           ↓           ↓            ↓
    ┌─────────────────────────────────────────────┐
    │          Copilot Agent Mode                │
    │     (orchestration & approvals)            │
    └─────────────────────────────────────────────┘
```

---

## Performance Metrics

### Expected Run Times

| Workflow | Time | Notes |
|----------|------|-------|
| CI | 5-10 min | Depends on test count |
| Quality | 2-3 min | Fast structure checks |
| Documentation | 2-3 min | Markdown validation |
| Release | 10-15 min | Includes tests + build |

### Optimization Tips

1. **Cache pip dependencies** - Saves 1-2 minutes
2. **Parallel jobs** - CI jobs run in parallel
3. **Cancel redundant runs** - Concurrency enabled
4. **Skip non-essential** - Documentation optional
5. **Artifact cleanup** - 30-day retention

---

## Maintenance

### Adding New Checks

1. Update the appropriate workflow (ci.yml, quality.yml, etc.)
2. Add new job with clear name and description
3. Include comments explaining purpose
4. Test locally first
5. Commit with description of new validation

### Updating Dependencies

When `requirements.txt` changes:
1. Test locally: `pip install -r requirements.txt`
2. Commit updates
3. All workflows automatically use new versions
4. Monitor first CI run for compatibility

### Monitoring Workflow Health

```bash
# View workflow metrics
gh workflow list

# View recent runs
gh run list

# Check workflow status
gh workflow view ci.yml
```

---

## Next Steps

1. **Enable workflows** - Push to `main` or `develop` to trigger CI
2. **Monitor runs** - Go to Actions tab to watch workflows
3. **Set up secrets** (optional) - Add Codecov, Docker, Slack tokens
4. **Configure branch protection** - Require CI to pass before merge
5. **Integrate with Copilot** - Chat modes can reference workflow results

---

## Summary

✅ **Four production-ready workflows created:**
- **ci.yml** - Continuous integration (format, lint, test)
- **quality.yml** - Quality assurance (structure, configs, assets)
- **documentation.yml** - Documentation validation
- **release.yml** - Release pipeline (build, package, publish)

✅ **Best practices implemented:**
- Modular jobs with single responsibility
- Caching for performance
- No code duplication (reuse existing scripts)
- Clear error messages and reporting
- Artifact management
- Concurrency control

✅ **Copilot-compatible:**
- No conflicts with Agent Mode orchestration
- Validation data available for chat modes
- Approval gates integrated with release

---

**Status:** ✅ PRODUCTION READY  
**Version:** 1.0.0  
**Last Updated:** 2026-06-30

---

## File Reference

| File | Purpose | Status |
|------|---------|--------|
| `.github/workflows/ci.yml` | CI pipeline | ✅ Ready |
| `.github/workflows/quality.yml` | Quality validation | ✅ Ready |
| `.github/workflows/documentation.yml` | Doc validation | ✅ Ready |
| `.github/workflows/release.yml` | Release pipeline | ✅ Ready |

All workflows are production-ready and can be deployed immediately.
