# CI/CD Pipeline Integration Guide

**Date:** 2026-06-30  
**Version:** 1.0.0  
**Purpose:** Quick reference showing workflow-to-asset mapping

---

## Quick Reference

### Workflows Created

```
.github/workflows/
├── ci.yml               ← Continuous Integration (format, lint, test)
├── quality.yml          ← Quality Assurance (structure, config validation)
├── documentation.yml    ← Documentation Validation
├── release.yml          ← Release Pipeline
└── README.md            ← This documentation
```

---

## Workflow-to-Asset Mapping

### CI Pipeline (ci.yml)

```
ci.yml
├── Format Check
│   └── Reuses: Black (python -m black)
│       Helper: scripts/format.py
│       Suggestion: Run python scripts/format.py locally
│
├── Import Check
│   └── Reuses: isort (python -m isort)
│       Helper: scripts/format.py
│       Suggestion: Run python scripts/format.py locally
│
├── Linting
│   ├── Reuses: Pylint (python -m pylint)
│   │   Helper: scripts/lint.py
│   │   Suggestion: Run python scripts/lint.py locally
│   └── Reuses: Flake8 (python -m flake8)
│       Helper: scripts/lint.py
│
├── Unit Tests
│   └── Reuses: pytest (python -m pytest)
│       Helper: scripts/test.py
│       Suggestion: Run python scripts/test.py locally
│
└── Coverage
    └── Reuses: pytest --cov
        Helper: scripts/test.py
        Output: coverage.xml (uploaded)
```

**Dependencies:**
- `requirements.txt` (black, isort, pylint, flake8, pytest, pytest-cov)
- `scripts/format.py`
- `scripts/lint.py`
- `scripts/test.py`

**Artifacts Produced:**
- `test-results.xml` (uploaded to GitHub)
- `coverage.xml` (uploaded to Codecov)

---

### Quality Pipeline (quality.yml)

```
quality.yml
├── Repository Structure
│   └── Validates:
│       - .github/agents/ (10 agent definitions)
│       - ai/contracts/ (8 contract files)
│       - ai/hooks/ (hook definitions)
│       - orchestration/ (subsystems)
│       - scripts/ (helper scripts)
│       - .github/ (workflows, chat modes)
│       - docs/ (documentation)
│
├── YAML Validation
│   └── Reuses: yamllint
│       Checks: .github/workflows/, ai/
│
├── JSON Validation
│   └── Reuses: Python json.tool
│       Checks: .vscode/mcp.json, configs/
│
├── Markdown Validation
│   └── Reuses: markdownlint, prettier
│       Checks: *.md files
│
├── AI Configuration
│   ├── Validates:
│   │   - 10 agent definitions (.github/agents/*.md)
│   │   - 8 contract definitions (ai/contracts/*.md)
│   │   - 10 chat modes (.github/chatmodes/*.chatmode.md)
│   └── Fails: If any required asset missing
│
├── Hook Configuration
│   ├── Validates:
│   │   - ai/hooks/hooks.md (exists, has content)
│   │   - scripts/hooks/__init__.py
│   │   - scripts/hooks/setup_hooks.py
│   │   - scripts/hooks/pre_commit.py
│   │   - scripts/hooks/pre_push.py
│   │   - scripts/hooks/commit_msg_validator.py
│   └── Fails: If any hook script missing
│
└── MCP Configuration
    ├── Validates:
    │   - .vscode/mcp.json (valid JSON)
    │   - MCP server configuration
    │   - Runs: .vscode/validate-mcp.js
    └── Checks: All MCP servers properly configured
```

**Dependencies:**
- `yamllint`
- `markdownlint`
- `.vscode/validate-mcp.js`
- `ai/` directory structure
- `scripts/hooks/` implementations

**Validation Coverage:**
- ✓ Project structure
- ✓ All AI assets present
- ✓ All hook implementations present
- ✓ MCP configuration valid
- ✓ Fails if any required asset missing

---

### Documentation Pipeline (documentation.yml)

```
documentation.yml
├── README Validation
│   └── Checks:
│       - README.md exists
│       - Has content
│       - Contains key sections
│
├── Documentation Files
│   └── Checks:
│       - docs/ directory exists
│       - Optional: docs/architecture.md
│       - Optional: docs/developer-guide.md
│       - Optional: docs/project-structure.md
│
├── Developer Guide
│   └── Checks:
│       - docs/developer-guide.md structure
│       - Expected sections: Setup, Architecture, Development, Testing
│
├── AI Documentation
│   ├── Checks:
│   │   - ai/hooks/README.md
│   │   - ai/hooks/hooks.md
│   │   - ai/hooks/hook-implementation-strategy.md
│   │   - ai/hooks/HOOK-INTEGRATION-GUIDE.md
│   │   - ai/hooks/QUICK-REFERENCE.md
│   │   - .github/copilot-instructions.md
│   └── Validates: Content length (not empty)
│
├── Markdown Format Check
│   └── Reuses:
│       - markdownlint (syntax)
│       - prettier (formatting)
│
└── Workflow Documentation
    └── Checks: Workflows referenced in docs
```

**Validation Coverage:**
- ✓ README completeness
- ✓ Documentation directory exists
- ✓ Hook documentation present
- ✓ Markdown formatting
- ✓ Non-blocking validation

**Artifacts Produced:**
- Documentation snapshot (30-day retention)

---

### Release Pipeline (release.yml)

```
release.yml
├── Prepare Release
│   └── Extracts: Version from release tag or manual input
│       Output: version, tag (used by all jobs)
│
├── Validate Release
│   ├── Reuses: Black (python -m black)
│   │   Helper: scripts/format.py
│   ├── Reuses: Pylint (python -m pylint)
│   │   Helper: scripts/lint.py
│   ├── Reuses: pytest (python -m pytest)
│   │   Helper: scripts/test.py
│   ├── Checks: CHANGELOG.md has release entry
│   └── Fails: If any validation fails (BLOCKING)
│
├── Build Release
│   ├── Reuses: python -m build
│   │   Helper: scripts/build.py
│   └── Produces:
│       - dist/ directory
│       - build/ directory
│       - Uploaded as artifacts (30-day retention)
│
├── Generate Release Notes
│   ├── Extracts: CHANGELOG.md release section
│   ├── Generates: release-notes.md
│   └── Produces: Markdown for GitHub Release
│
├── Build Docker Image (optional)
│   ├── Checks: Dockerfile exists
│   ├── Skips: If no Dockerfile
│   └── Produces: OCI image (optional)
│
├── Publish Release
│   ├── Requires: Validation passed
│   ├── Creates: GitHub Release
│   ├── Attaches: Build artifacts
│   └── Updates: GitHub Release page
│
└── Release Notification
    └── Logs: Success and next steps
```

**Dependencies:**
- `requirements.txt` (build, black, isort, pylint, flake8, pytest)
- `scripts/format.py`
- `scripts/lint.py`
- `scripts/test.py`
- `scripts/build.py`
- `CHANGELOG.md` (optional)
- `Dockerfile` (optional)
- `pyproject.toml` (optional)

**Validation Coverage:**
- ✓ Code quality checks
- ✓ All tests pass
- ✓ Coverage minimum met
- ✓ CHANGELOG updated
- ✓ Version consistency

**Artifacts Produced:**
- `dist/` (Python packages)
- `build/` (Build artifacts)
- Docker image (optional)
- GitHub Release with notes

---

## Helper Script Usage

### scripts/format.py

**Used By:**
- ci.yml (suggestion in output)
- release.yml (via Black)

**Commands:**
```bash
# Format check
python scripts/format.py --check

# Auto-format
python scripts/format.py --fix
```

**Reused Tools:**
- Black (code formatting)
- isort (import sorting)

---

### scripts/lint.py

**Used By:**
- ci.yml (suggestion in output)
- release.yml (via Pylint)

**Commands:**
```bash
# Linting check
python scripts/lint.py

# Fix issues
python scripts/lint.py --fix
```

**Reused Tools:**
- Pylint (code quality)
- Flake8 (linting)

---

### scripts/test.py

**Used By:**
- ci.yml (unit tests, coverage)
- release.yml (validation tests)

**Commands:**
```bash
# Run tests
python scripts/test.py

# With coverage
python scripts/test.py --coverage

# Verbose
python scripts/test.py --verbose
```

**Reused Tools:**
- pytest (testing framework)
- pytest-cov (coverage measurement)

---

### scripts/build.py

**Used By:**
- release.yml (artifact building)

**Commands:**
```bash
# Build release
python scripts/build.py

# Build with options
python scripts/build.py --version 1.0.0
```

**Reused Tools:**
- Python `build` module (packaging)

---

## Configuration Files Used

### .vscode/mcp.json

**Purpose:** MCP server configuration  
**Used By:** quality.yml (validation)  
**Validation:** JSON syntax + MCP server configuration  
**Required:** Yes (for Copilot integration)

### ai/hooks/hooks.md

**Purpose:** Abstract hook definitions  
**Used By:** quality.yml (validation)  
**Validation:** File exists, has content  
**Required:** Yes (hook system)

### .github/agents/*.md

**Purpose:** Agent definitions (10 files)  
**Used By:** quality.yml (validation)  
**Validation:** All 10 agents present  
**Required:** Yes (platform core)

### ai/contracts/*.md

**Purpose:** Contract definitions (8 files)  
**Used By:** quality.yml (validation)  
**Validation:** All 8 contracts present  
**Required:** Yes (governance)

### .github/chatmodes/*.chatmode.md

**Purpose:** Chat mode configurations (10 files)  
**Used By:** quality.yml (validation)  
**Validation:** All 10 chat modes present  
**Required:** Yes (Copilot integration)

### scripts/hooks/*.py

**Purpose:** Hook implementations (5 files)  
**Used By:** quality.yml (validation)  
**Validation:** All 5 scripts present  
**Required:** Yes (development automation)

### CHANGELOG.md

**Purpose:** Release notes source  
**Used By:** release.yml (release notes extraction)  
**Validation:** Release entry for version  
**Required:** Optional (but recommended)

### Dockerfile

**Purpose:** Container configuration  
**Used By:** release.yml (Docker image build)  
**Validation:** File exists (optional)  
**Required:** Optional

---

## Workflow Execution Flow

```
Developer Pushes Code
        ↓
GitHub Events Trigger
        ↓
    ┌───┴───────────────────┐
    ↓                       ↓
  CI.yml              quality.yml
  ├── format            ├── structure
  ├── imports           ├── yaml
  ├── lint              ├── json
  ├── tests             ├── markdown
  └── coverage          ├── ai-config
                        ├── hooks
                        └── mcp
        ↓                       ↓
   Results             Results
    (if PR)              (always)
        ↓                       ↓
  PR Comment          Commit Status
        ↓
   documentation.yml (if doc changes)
   ├── readme
   ├── docs
   ├── developer-guide
   ├── ai-docs
   ├── markdown-format
   └── workflow-docs

Release Tags Trigger
        ↓
   release.yml
   ├── prepare
   ├── validate (runs CI checks again)
   ├── build
   ├── release-notes
   ├── docker (optional)
   ├── publish
   └── notify
        ↓
   GitHub Release Created
```

---

## Failure Scenarios

### CI Pipeline Fails

**Cause:** Code quality check failed  
**Remediation:**
```bash
python scripts/format.py --fix    # Fix formatting
python scripts/lint.py --fix      # Fix lint issues
python -m pytest tests/           # Re-run tests locally
```

### Quality Pipeline Fails

**Cause:** Missing required asset or structure issue  
**Remediation:**
```bash
# Check structure
ls -la .github/agents/ ai/contracts/ scripts/hooks/

# Validate MCP config
node .vscode/validate-mcp.js

# Validate agent definitions
ls -la .github/agents/ | wc -l  # Should be 10
```

### Documentation Pipeline Fails

**Cause:** README or documentation missing  
**Remediation:**
- Verify `README.md` exists
- Add missing documentation to `docs/`
- Ensure `docs/architecture.md` exists

### Release Pipeline Fails

**Cause:** Validation failed before release  
**Remediation:**
```bash
# Fix code quality
python scripts/format.py --fix
python scripts/lint.py --fix

# Run full test suite
python -m pytest tests/

# Update CHANGELOG
# Add release notes for version

# Re-trigger release
# Create new release tag
```

---

## Performance Optimization

### CI Pipeline Optimization

✓ **Caching:** Pip dependencies cached (saves 1-2 min)  
✓ **Parallel:** Format, imports, linting run in parallel  
✓ **Coverage:** Optional (non-blocking)  
✓ **Expected Time:** 5-10 minutes

### Quality Pipeline Optimization

✓ **Fast Checks:** Structure validation very fast (< 1 min)  
✓ **No Dependencies:** Jobs run in parallel  
✓ **Expected Time:** 2-3 minutes

### Documentation Pipeline Optimization

✓ **Trigger:** Only runs on doc changes  
✓ **Non-blocking:** Format checks don't fail  
✓ **Expected Time:** 2-3 minutes

### Release Pipeline Optimization

✓ **Caching:** Pip dependencies cached  
✓ **Parallel:** Some jobs can run parallel  
✓ **Expected Time:** 10-15 minutes (includes all tests)

---

## Integration with Copilot Agent Mode

### How Workflows Support Copilot

1. **Validation Data**
   - Workflows validate project structure
   - Results available for Copilot agents
   - Agents can reference validation status

2. **Quality Gates**
   - Release validation blocks unsafe deployments
   - Ensures agent outputs meet quality standards
   - Approvals integrated with workflow status

3. **Configuration Validation**
   - Workflows validate agent definitions
   - Verify contracts are in place
   - Check Copilot chat modes configured

4. **No Orchestration**
   - Workflows do NOT orchestrate agents
   - Copilot maintains control
   - Workflows provide validation only

### Copilot Integration Points

```
Copilot Agent Mode (orchestration)
        ↓
   Supervisor
        ↓
   ┌───────────┬───────────┬─────────────┐
   ↓           ↓           ↓             ↓
 BA        Architect     Developers   QA Engineer
   ↓           ↓           ↓             ↓
 [Agents generate code and artifacts]
        ↓
GitHub Actions CI/CD
   ├── Validate structure
   ├── Check quality
   ├── Test code
   └── Build release
        ↓
[Validation data available to Copilot]
        ↓
Approval decisions informed by CI/CD status
```

---

## Maintenance Tasks

### Weekly

- [ ] Monitor workflow run times
- [ ] Review failed runs
- [ ] Check coverage trends

### Monthly

- [ ] Review workflow configuration
- [ ] Update dependencies in requirements.txt
- [ ] Test disaster recovery

### Quarterly

- [ ] Audit security practices
- [ ] Review performance metrics
- [ ] Plan CI/CD improvements

---

## Quick Start

### Enable CI/CD

1. **Push code to main branch**
   ```bash
   git add .
   git commit -m "[ci] add workflows"
   git push origin main
   ```

2. **Watch workflows run**
   - Go to GitHub → Actions
   - See ci.yml, quality.yml running
   - Check results

3. **Fix any failures**
   ```bash
   python scripts/format.py --fix
   python scripts/lint.py --fix
   git add .
   git commit -m "[fix] resolve CI errors"
   git push
   ```

4. **Create release (optional)**
   ```bash
   # Tag a release
   git tag v1.0.0
   git push origin v1.0.0
   
   # Or create via GitHub UI
   # Go to Releases → Create
   ```

---

## Summary

✅ **Four workflows created:**
- ci.yml (continuous integration)
- quality.yml (quality assurance)
- documentation.yml (documentation validation)
- release.yml (release pipeline)

✅ **Reuse pattern:**
- All workflows reuse existing helper scripts
- No duplication of validation logic
- Single source of truth for each check

✅ **Integration:**
- Works alongside Copilot Agent Mode
- Validates project structure
- Ensures code quality
- Manages releases

✅ **Best practices:**
- Modular jobs
- Parallel execution
- Caching enabled
- Clear error messages
- Comprehensive validation

---

**Status:** ✅ PRODUCTION READY  
**Version:** 1.0.0  
**Last Updated:** 2026-06-30
