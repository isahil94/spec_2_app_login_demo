# Hook Integration Strategy

**Version:** 1.0.0  
**Date:** 2026-06-30  
**Status:** Production Ready

## Overview

This document defines the practical implementation of development lifecycle hooks that automatically enforce code quality, testing, and documentation standards.

Hooks integrate with:
- **Git hooks** (local developer machine)
- **VS Code tasks** (during development)
- **GitHub Actions** (CI/CD pipeline)
- **Copilot chat modes** (human approvals)

## Architecture

```
Developer Actions          Hook Trigger              Implementation             Integration
─────────────────        ─────────────             ──────────────             ─────────────
git commit        →  pre-commit hook       →  run tests & lint       →  Block if fails
git push          →  pre-push hook         →  integration tests      →  Block if fails
PR created        →  GitHub Actions        →  run reviewer mode      →  Copilot chat
Push to main      →  GitHub Actions        →  run release checks     →  Copilot chat
VS Code save      →  File watcher          →  format + lint          →  On save
Project open      →  VS Code activation   →  validate environment   →  On startup
```

## Hook Categories

### 1. Local Development Hooks (Git Hooks)

**Location:** `.git/hooks/`

| Hook | Trigger | Validates | Blocks |
|------|---------|-----------|--------|
| `pre-commit` | `git commit` | Format, Lint, Tests | Yes |
| `pre-push` | `git push` | Integration Tests | Yes |
| `commit-msg` | `git commit` | Commit message format | Yes |

### 2. VS Code Hooks (Tasks & File Watchers)

**Location:** `.vscode/tasks.json`

| Hook | Trigger | Action | Blocks |
|------|---------|--------|--------|
| `On File Save` | File save | Format + Lint | No |
| `On Project Open` | Workspace open | Validate environment | No |

### 3. GitHub Hooks (Actions)

**Location:** `.github/workflows/`

| Workflow | Trigger | Action | Blocks |
|----------|---------|--------|--------|
| `on-pull-request.yml` | PR created | Run reviewer mode | Yes (PR checks) |
| `on-release.yml` | Release created | Verify artifacts | Yes (release checks) |
| `on-push-main.yml` | Push to main | Build & deploy | Yes (workflow) |

## Implementation Details

### Local Development Hooks

These hooks run on the developer's machine before committing or pushing.

#### `pre-commit` Hook
```
Runs before: git commit
Validates:
  1. Code formatting (Black, isort)
  2. Linting (ESLint, Pylint)
  3. Unit tests (pytest)
  4. Markdown validation
  5. Schema validation for JSON/YAML

Blocks commit if:
  - Tests fail
  - Linting errors > warnings
  - Markdown has broken links
  - Schema validation fails

Exit code:
  0 = Allow commit
  1 = Block commit (fix and try again)
```

#### `pre-push` Hook
```
Runs before: git push
Validates:
  1. All pre-commit checks pass
  2. Integration tests pass
  3. Build succeeds
  4. No uncommitted changes
  5. Branch is up-to-date

Blocks push if:
  - Integration tests fail
  - Build fails
  - Out of sync with remote

Exit code:
  0 = Allow push
  1 = Block push (fix and try again)
```

#### `commit-msg` Hook
```
Runs before: commit is finalized
Validates:
  1. Message is not empty
  2. First line ≤ 72 characters
  3. Format: [TYPE] brief message
  4. Types: feat, fix, docs, style, refactor, perf, test, chore

Blocks commit if:
  - Message is empty
  - Message doesn't match format

Exit code:
  0 = Allow commit
  1 = Block commit (edit message and retry)
```

### VS Code Integration

#### File Save Hook
```
On Save:
  1. Auto-format code (Black, Prettier)
  2. Auto-sort imports (isort)
  3. Run linter (show warnings, don't block)
  4. Validate YAML/JSON schema

Non-blocking:
  - Linting warnings shown in Problems panel
  - User can ignore and continue
  - Errors shown but not blocking
```

#### Project Open Hook
```
On Workspace Open:
  1. Validate Python environment
  2. Check required configuration files
  3. Validate MCP configuration
  4. Verify git hooks are installed
  5. Show status in status bar

Actions if failures:
  - Show warning in status bar
  - Suggest fixes in notification
  - Provide quick-fix commands
```

### GitHub Actions Integration

#### On Pull Request
```
When: PR is created or updated
Runs:
  1. Format check (Black, Prettier)
  2. Lint check (All linters)
  3. Security scan (Bandit, safety)
  4. Test coverage (pytest + coverage)
  5. Type checking (mypy, tsc)
  6. Invoke Reviewer chatmode via API

Blocks merge if:
  - Tests fail
  - Coverage drops
  - Security issues found
  - Type errors exist
```

#### On Release
```
When: Release is created
Validates:
  1. Version matches tag
  2. CHANGELOG.md is updated
  3. README.md is current
  4. Docker image builds
  5. All tests pass

Blocks release if:
  - Version mismatch
  - Changelog missing
  - Build fails
```

#### On Push to Main
```
When: Code pushed to main branch
Runs:
  1. All checks (same as PR)
  2. Build production Docker image
  3. Push image to registry (optional)
  4. Deploy to staging (optional)
  5. Run smoke tests

Blocks deployment if:
  - Checks fail
  - Build fails
  - Smoke tests fail
```

## File Structure

```
.git/hooks/                         ← Git hooks (created by script)
├── pre-commit
├── pre-push
└── commit-msg

.github/workflows/                  ← GitHub Actions
├── on-pull-request.yml
├── on-push-main.yml
└── on-release.yml

.vscode/
├── tasks.json                      ← Contains hook tasks
└── settings.json                   ← File watcher config

scripts/                            ← Hook implementation
├── hooks/
│   ├── __init__.py
│   ├── setup_hooks.py             ← Install git hooks
│   ├── pre_commit.py              ← pre-commit hook logic
│   ├── pre_push.py                ← pre-push hook logic
│   └── commit_msg_validator.py    ← commit-msg hook logic
├── validate/
│   ├── format_check.py
│   ├── lint_check.py
│   ├── test_runner.py
│   └── schema_validator.py
└── environment/
    └── validate_environment.py
```

## Integration with Existing Assets

### Reuse Python Scripts

Existing scripts are already in `scripts/`:
- `format.py` - Auto-format code
- `lint.py` - Check linting
- `test.py` - Run tests
- `build.py` - Build artifacts

**Hook implementation will:**
1. Import these scripts
2. Call their main functions
3. Pass through return codes
4. Add no duplicate logic

### Reuse VS Code Tasks

Existing tasks in `.vscode/tasks.json`:
- `build` - Build task
- `test` - Test task
- `lint` - Lint task
- `format` - Format task

**Hooks will:**
1. Call these tasks via `tasks: run` command
2. Reuse the exact same logic
3. No duplication

### Reuse MCP Servers

Existing MCP servers in `.vscode/mcp.json`:
- Filesystem - Write validation results
- Terminal - Run commands
- Git - Check status/diff
- GitHub - Create PRs

**Hooks will:**
1. Use Filesystem server to read/write validation data
2. Use Terminal to execute checks
3. Use Git to check status
4. Use GitHub to manage PRs/issues

### Reuse Chat Modes

Existing chat modes in `.github/chatmodes/`:
- reviewer.chatmode.md - Code review
- devops-release.chatmode.md - Release checks

**GitHub Actions will:**
1. Invoke Reviewer chat mode on PR
2. Invoke DevOps chat mode on release
3. Pass validation results as context
4. Wait for approval

## Setup Instructions

### 1. Install Git Hooks

```bash
# Run setup script (creates hooks in .git/hooks/)
python scripts/hooks/setup_hooks.py

# Verify hooks installed
ls -la .git/hooks/
# Should show: pre-commit, pre-push, commit-msg (executable)
```

### 2. Configure VS Code

**Already configured in:**
- `.vscode/settings.json` - File watchers
- `.vscode/tasks.json` - Hook tasks

**No additional configuration needed** - Works on project open.

### 3. Set Up GitHub Actions

```bash
# Create workflows directory (if not exists)
mkdir -p .github/workflows

# GitHub Actions workflows will auto-run on:
# - PR creation/update
# - Release creation
# - Push to main
```

## Hook Behavior

### Pre-Commit Hook Flow

```
Developer: git commit -m "feat: add feature"
         ↓
       [pre-commit hook runs]
         ↓
    1. Format check
       Black formatter
       isort for imports
       ✓ PASS
         ↓
    2. Lint check
       ESLint, Pylint
       ✓ PASS
         ↓
    3. Unit tests
       pytest coverage
       ✓ PASS
         ↓
    4. Markdown validation
       Link checks
       ✓ PASS
         ↓
    5. Schema validation
       YAML, JSON schema
       ✓ PASS
         ↓
    Commit is allowed ✓
```

### Pre-Commit Hook Failure

```
Developer: git commit -m "feat: add feature"
         ↓
       [pre-commit hook runs]
         ↓
    1. Format check
       FAIL: Files not formatted
       ✗ BLOCKED
         ↓
    Hook output:
    "Fix formatting with: python scripts/format.py"
         ↓
    Commit is blocked ✗
         ↓
Developer: python scripts/format.py
Developer: git add .
Developer: git commit -m "feat: add feature"
         ↓
    (Hook runs again, passes this time)
```

### GitHub Actions PR Flow

```
Developer: Pushes branch and creates PR
         ↓
    [GitHub Actions triggered]
         ↓
    1. Format check
       Black, Prettier
         ↓
    2. Lint check
       ESLint, Pylint
         ↓
    3. Security scan
       Bandit, safety
         ↓
    4. Test coverage
       pytest --cov
         ↓
    5. Type checking
       mypy, tsc
         ↓
    6. Invoke Reviewer chatmode
       Copilot reviews code
       Posts review as PR comment
         ↓
    If all pass: PR can be merged ✓
    If any fail: PR blocked until fixed ✗
```

## Configuration

### Commit Message Format

```
[TYPE] brief description

[body - optional]

[footer - optional]
```

**Valid types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Code formatting
- `refactor` - Code refactoring
- `perf` - Performance improvement
- `test` - Test additions/changes
- `chore` - Maintenance

**Examples:**
```
[feat] add business analyst mode
[fix] correct date calculation in BA
[docs] update README with MCP setup
[test] add tests for BA validation
```

### Skip Hooks (If Needed)

**Skip pre-commit hook:**
```bash
git commit --no-verify -m "message"
# Use ONLY for emergencies, not normal workflow
```

**Skip pre-push hook:**
```bash
git push --no-verify
# Use ONLY for emergencies, not normal workflow
```

**Note:** Use `--no-verify` only in emergencies. Normal development should always run hooks.

## Monitoring

### Local Hook Logs

Hooks create local logs in:
```
.vscode/hook-logs/
├── pre-commit.log
├── pre-push.log
└── commit-msg.log
```

View recent failures:
```bash
tail -f .vscode/hook-logs/pre-commit.log
```

### GitHub Actions Logs

View in GitHub:
```
Repository → Actions → [Workflow name] → [Run] → View logs
```

Or via CLI:
```bash
gh workflow view [workflow-name] --log
```

## Troubleshooting

### Hooks Not Running

```bash
# Check if hooks are executable
ls -la .git/hooks/
# Should show: -rwxr-xr-x (executable)

# If not executable, fix it:
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
chmod +x .git/hooks/commit-msg

# Re-run setup
python scripts/hooks/setup_hooks.py
```

### Hook Fails Unexpectedly

```bash
# Run hook manually to debug
.git/hooks/pre-commit

# Check logs
cat .vscode/hook-logs/pre-commit.log

# Check Python environment
python -c "import sys; print(sys.executable)"

# Verify dependencies
pip list | grep pytest black pylint
```

### GitHub Actions Not Triggering

```bash
# Check workflows in .github/workflows/
ls -la .github/workflows/

# Verify YAML syntax
python -m yaml .github/workflows/on-pull-request.yml

# Check Actions settings in GitHub:
Settings → Actions → General → Workflow permissions
  → Should allow "Read and write permissions"
```

## Best Practices

### For Developers

✅ **DO:**
- Run tests locally before pushing
- Write descriptive commit messages
- Check linting output before committing
- Keep commits small and focused

❌ **DON'T:**
- Use `--no-verify` routinely
- Commit large files
- Ignore pre-commit warnings
- Push failing tests

### For CI/CD

✅ **DO:**
- Run same checks locally and in CI
- Block merges on test failure
- Keep workflows fast (< 10 min)
- Archive logs for debugging

❌ **DON'T:**
- Have different rules locally vs CI
- Allow merges with failing checks
- Run unnecessary checks
- Leave failed jobs hanging

## Maintenance

### Update Hooks

When adding new checks:
```bash
# 1. Update script (scripts/hooks/pre_commit.py)
# 2. Reinstall hooks
python scripts/hooks/setup_hooks.py
# 3. Verify on test commit
git commit --dry-run
```

### Monitor Performance

Track hook execution time:
```bash
# View logs
cat .vscode/hook-logs/pre-commit.log | grep "duration"

# If > 30 seconds, optimize by:
- Parallelizing checks
- Caching results
- Running subset locally
```

### Update Policies

Review hooks quarterly:
- [ ] Check failure rates
- [ ] Review skipped hooks (--no-verify usage)
- [ ] Identify slow checks
- [ ] Update validation rules
- [ ] Document new requirements

## Next Steps

1. **Create hook scripts** (`scripts/hooks/*.py`)
2. **Create setup script** (`scripts/hooks/setup_hooks.py`)
3. **Create GitHub Actions workflows** (`.github/workflows/`)
4. **Test locally** with sample commits
5. **Document in team wiki** with common issues
6. **Monitor** hook performance and failures

---

**Status:** Ready for Implementation  
**Owner:** Platform Team  
**Last Updated:** 2026-06-30
