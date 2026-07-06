# Hook Integration Guide

**Version:** 1.0.0  
**Status:** Production Ready

## Quick Start

### 1. Install Git Hooks (One-Time Setup)

```bash
# Run setup script
python scripts/hooks/setup_hooks.py

# Verify installation
ls -la .git/hooks/
# Should show: pre-commit, pre-push, commit-msg (all executable)
```

### 2. Development Workflow

```bash
# 1. Make changes
vim scripts/hooks/pre_commit.py

# 2. Check status
git status

# 3. Format and lint (optional - pre-commit will do this)
python scripts/format.py
python -m isort .

# 4. Commit
git commit -m "[feat] add new validation"
# Pre-commit hook runs automatically ✓

# 5. Push
git push
# Pre-push hook runs automatically ✓
```

### 3. GitHub Actions (Automatic)

- PR created → Runs validation + posts summary
- Code pushed to main → Runs full test suite + builds Docker
- Release created → Validates version + builds artifacts

---

## Hook Architecture

### Local Hooks (Your Machine)

```
git commit
    ↓
[pre-commit hook]
    ├─ Run Black formatter
    ├─ Run isort
    ├─ Run Pylint
    ├─ Run pytest
    └─ Block if any fail

git push
    ↓
[pre-push hook]
    ├─ Check git status
    ├─ Check branch is up-to-date
    ├─ Run integration tests
    └─ Block if any fail

[commit-msg hook]
    └─ Validate format: [TYPE] message
```

### GitHub Hooks (Remote)

```
PR Created
    ↓
[on-pull-request.yml]
    ├─ Format check
    ├─ Test suite
    ├─ Configuration validation
    └─ Post comment with results

Push to main
    ↓
[on-push-main.yml]
    ├─ Full test suite
    ├─ Build Docker image
    ├─ Security scan
    └─ Comment on commit

Release Created
    ↓
[on-release.yml]
    ├─ Validate version consistency
    ├─ Check CHANGELOG
    ├─ Build artifacts
    └─ Build Docker image
```

---

## Implementation Details

### Pre-Commit Hook

**File:** `.git/hooks/pre-commit` (created by setup script)

**What it does:**
1. Format check (Black) - Auto-formats code
2. Import sorting (isort) - Ensures consistent imports
3. Linting (Pylint) - Checks for errors
4. Unit tests (pytest) - Runs all unit tests

**Logs:** `.vscode/hook-logs/pre-commit.log`

**Exit codes:**
- `0` = All checks passed, commit allowed
- `1` = Some checks failed, commit blocked

**When it runs:**
```bash
git commit -m "message"
# Pre-commit hook runs automatically
```

**Skip if needed (emergencies only):**
```bash
git commit --no-verify -m "message"
```

---

### Pre-Push Hook

**File:** `.git/hooks/pre-push` (created by setup script)

**What it does:**
1. Check for uncommitted changes
2. Verify branch is up-to-date with remote
3. Run integration tests

**Logs:** `.vscode/hook-logs/pre-push.log`

**Exit codes:**
- `0` = All checks passed, push allowed
- `1` = Some checks failed, push blocked

**When it runs:**
```bash
git push
# Pre-push hook runs automatically
```

**Skip if needed (emergencies only):**
```bash
git push --no-verify
```

---

### Commit Message Validator

**File:** `.git/hooks/commit-msg` (created by setup script)

**What it validates:**
- Format: `[TYPE] Brief description`
- Message is not empty
- First line ≤ 72 characters
- Valid type (feat, fix, docs, style, refactor, perf, test, chore)

**Logs:** `.vscode/hook-logs/commit-msg.log`

**Valid formats:**
```
[feat] add business analyst mode
[fix] correct date parsing
[docs] update README with setup
[test] add validator tests
[chore] update dependencies
```

**Invalid formats (will be rejected):**
```
Add feature                          ✗ Missing [TYPE]
[feature] something                  ✗ Invalid type (must be "feat")
[feat] This is a very long message that exceeds 72 characters limit
                                     ✗ First line too long
[feat]                               ✗ Message content missing
```

---

### GitHub Actions Workflows

#### On Pull Request (on-pull-request.yml)

**Triggers:** When PR is created or updated

**What it checks:**
```
1. Quality Checks
   ├─ Black formatter (format compliance)
   ├─ isort (import sorting)
   ├─ Pylint (linting)
   ├─ Bandit (security)
   └─ mypy (type checking)

2. Test Suite
   ├─ Unit tests (pytest)
   ├─ Integration tests
   ├─ Test coverage (≥ 80%)
   └─ Upload to Codecov

3. Configuration Validation
   ├─ MCP configuration
   ├─ YAML syntax
   ├─ JSON schema
   └─ Repository structure

4. PR Summary
   └─ Post comment with results
```

**Result:**
- All pass → PR marked as approved for merge
- Any fail → PR blocked until fixed

---

#### On Push to Main (on-push-main.yml)

**Triggers:** When code is pushed to main branch (after PR merge)

**What it does:**
```
1. Quality Checks
   ├─ Format check
   ├─ Import sorting
   └─ Linting

2. Full Test Suite
   ├─ All unit tests
   ├─ All integration tests
   └─ Coverage ≥ 80%

3. Build
   ├─ Build Docker image
   └─ Build platform image

4. Security
   ├─ Bandit scan
   └─ Safety check (dependencies)

5. Documentation
   ├─ Check README.md
   ├─ Check CHANGELOG.md
   └─ Validate markdown links

6. Notifications
   └─ Comment on commit
```

**Result:**
- All pass → Changes merged and deployed
- Any fail → Team is notified

---

#### On Release (on-release.yml)

**Triggers:** When release is published

**What it validates:**
```
1. Validate Release
   ├─ Version consistency
   │  ├─ pyproject.toml
   │  └─ __init__.py
   ├─ CHANGELOG.md updated
   ├─ README.md present
   └─ Full test suite passes

2. Build Release Artifacts
   ├─ Build distribution
   └─ Generate wheel

3. Build Docker Image
   └─ Build and push image

4. Generate Release Notes
   └─ Extract from CHANGELOG

5. Publish Release
   ├─ Update GitHub release
   ├─ Create deployment
   └─ Slack notification
```

**Result:**
- All pass → Release is published and deployed
- Any fail → Release validation fails

---

## Reusing Existing Scripts

The hooks **reuse** existing Python scripts in `scripts/`:

| Script | Used By |
|--------|---------|
| `scripts/format.py` | pre-commit hook + GitHub Actions |
| `scripts/lint.py` | pre-commit hook + GitHub Actions |
| `scripts/test.py` | pre-commit hook + GitHub Actions |
| `scripts/build.py` | GitHub Actions |

**No duplicate logic** - hooks call these scripts directly.

---

## Integrating with Copilot Chat Modes

### On Pull Request

Copilot can be invoked to validate PR quality. To add this:

1. **Manual Validation** (Current):
   ```
   In Copilot Chat:
   @chatmode qa-engineer "Validate PR #123"
   ```

2. **Automated via API** (Advanced):
   Add to `.github/workflows/on-pull-request.yml`:
   ```yaml
   - name: Invoke Copilot QA Workflow
     run: |
       # Requires Copilot API token
       # Calls the QA chat mode with PR context
       python scripts/hooks/invoke_qa.py
   ```

### On Release

Copilot can verify release artifacts:

1. **Manual Verification** (Current):
   ```
   In Copilot Chat:
   @chatmode devops-release "Verify release v1.0.0"
   ```

2. **Automated** (Advanced):
   Add to `.github/workflows/on-release.yml`:
   ```yaml
   - name: Verify Release with Copilot
     run: |
       python scripts/hooks/verify_release.py
   ```

---

## Monitoring Hooks

### View Local Hook Logs

```bash
# Real-time monitoring
tail -f .vscode/hook-logs/pre-commit.log
tail -f .vscode/hook-logs/pre-push.log
tail -f .vscode/hook-logs/commit-msg.log

# View specific error
grep "FAILED" .vscode/hook-logs/pre-commit.log
```

### View GitHub Actions Logs

**In VS Code:**
```
Ctrl+Shift+P → GitHub: View Workflow Runs
```

**In GitHub Web UI:**
```
Repository → Actions → [Workflow Name] → [Run] → View logs
```

**Via CLI:**
```bash
gh workflow view on-pull-request --log
gh run view <run-id> --log
```

---

## Troubleshooting

### Hooks Not Running

**Symptom:** Git commits without running pre-commit hook

**Solutions:**
```bash
# 1. Check if hooks exist
ls -la .git/hooks/pre-commit

# 2. Check if executable
stat .git/hooks/pre-commit
# Should show: -rwxr-xr-x (755)

# 3. Fix permissions
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
chmod +x .git/hooks/commit-msg

# 4. Reinstall hooks
python scripts/hooks/setup_hooks.py
```

### Pre-Commit Hook Fails

**Symptom:** Commit is blocked by hook

**Common reasons:**
```
1. Format issues
   Solution: python scripts/format.py

2. Linting errors
   Solution: Fix errors shown in output

3. Test failure
   Solution: Fix failing tests, run locally first

4. Import sorting
   Solution: python -m isort .
```

### Pre-Push Hook Blocks Push

**Symptom:** Push is blocked

**Common reasons:**
```
1. Branch out of sync
   Solution: git pull

2. Uncommitted changes
   Solution: git add . && git commit

3. Integration tests fail
   Solution: Run locally: python -m pytest tests/integration/
```

### GitHub Actions Failing

**Symptom:** PR checks failing

**Debugging:**
```bash
# View logs
gh workflow view on-pull-request --log

# Run checks locally
python scripts/format.py
python -m pylint scripts/
python -m pytest tests/
```

---

## Best Practices

### For Developers

✅ **DO:**
- Commit frequently with meaningful messages
- Format code before committing (hooks will catch issues)
- Run tests locally before pushing
- Read error messages from hooks carefully

❌ **DON'T:**
- Use `--no-verify` routinely
- Skip hooks to commit broken code
- Push directly to main (use PR workflow)
- Ignore linting warnings

### For Code Review

✅ **DO:**
- Check GitHub Actions results before merging PR
- Verify all checks pass (green checkmarks)
- Read Copilot review if available
- Comment on failing checks

❌ **DON'T:**
- Merge with failing checks
- Force merge if tests fail
- Ignore security warnings

### For Releases

✅ **DO:**
- Update version consistently
- Update CHANGELOG.md
- Run release workflow
- Verify all artifacts built

❌ **DON'T:**
- Tag releases without updating version
- Create releases from develop branch
- Skip validation checks

---

## Performance

### Typical Hook Execution Times

| Hook | Time | Notes |
|------|------|-------|
| pre-commit | 15-30s | Depends on code size, tests |
| pre-push | 30-60s | Includes integration tests |
| commit-msg | < 1s | Very fast |

**Total pre-commit workflow:** ~45 seconds

**Tips to speed up:**
- Keep test files small and fast
- Use pytest fixtures efficiently
- Cache dependencies locally
- Run only affected tests

---

## Configuration

### Enable/Disable Hooks

**All hooks are required by default.**

To temporarily disable:
```bash
# Skip pre-commit hook
git commit --no-verify

# Skip pre-push hook
git push --no-verify
```

**Note:** Use only in emergencies. Normal workflow should always run hooks.

### Modify Hook Behavior

Edit hook implementation files:
```
scripts/hooks/
├── pre_commit.py       ← Edit to add/remove checks
├── pre_push.py         ← Edit push validation
└── commit_msg_validator.py  ← Edit message format
```

After changes, reinstall:
```bash
python scripts/hooks/setup_hooks.py
```

---

## Next Steps

1. **Install hooks:** `python scripts/hooks/setup_hooks.py`
2. **Test locally:** Make a commit and watch pre-commit hook run
3. **Create PR:** Push a feature branch and create PR
4. **Monitor:** Watch GitHub Actions run validation
5. **Release:** Tag a release and watch release workflow

---

## Support

### Resources

- [Hook Strategy Document](./hook-implementation-strategy.md)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Git Hooks Docs](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)

### Getting Help

Check logs:
```bash
cat .vscode/hook-logs/*.log
```

Run validation:
```bash
```

---

**Last Updated:** 2026-06-30  
**Status:** Production Ready  
**Maintained By:** Platform Team
