# Hook Setup & Usage Reference

Quick reference for setting up and using development hooks.

## Setup (One-Time)

### 1. Install Git Hooks

```bash
python scripts/hooks/setup_hooks.py
```

**Output:**
```
╔════════════════════════════════════════╗
║      Git Hook Setup                   ║
╚════════════════════════════════════════╝

Workspace: f:\Projects\Specs_to_APP

✓ Installed pre-commit
✓ Installed pre-push
✓ Installed commit-msg

────────────────────────────────────────
✓ All hooks installed successfully

Hooks are now active...
```

### 2. Verify Installation

```bash
ls -la .git/hooks/
# Should show:
# -rwxr-xr-x  pre-commit
# -rwxr-xr-x  pre-push
# -rwxr-xr-x  commit-msg
```

**Done!** Hooks are ready to use.

---

## Daily Workflow

### Make Changes

```bash
# Edit files
vim scripts/my_script.py

# Check status
git status
```

### Format & Lint (Optional)

```bash
# Auto-format code
python scripts/format.py

# Check imports
python -m isort .

# Lint
python -m pylint scripts/
```

**Note:** Pre-commit hook will do this automatically, but you can do it now to catch issues early.

### Run Tests (Optional)

```bash
# Run unit tests
python -m pytest tests/unit/ -v

# Run with coverage
python -m pytest tests/ --cov=scripts
```

**Note:** Pre-commit hook will also run tests.

### Commit

```bash
git add .

git commit -m "[feat] add new feature"
```

**Pre-commit hook runs automatically:**
```
▶ Format check (Black)... ✓
▶ Import sorting (isort)... ✓
▶ Linting (Pylint)... ✓
▶ Unit tests (pytest)... ✓

────────────────────────────────
Results: 4 passed, 0 failed
────────────────────────────────

✓ Pre-commit checks PASSED
   Commit allowed.
```

### Push

```bash
git push
```

**Pre-push hook runs automatically:**
```
▶ Checking for uncommitted changes... ✓
▶ Checking if branch is up-to-date... ✓
▶ Running integration tests... ✓

────────────────────────────────
Results: 3 passed, 0 failed
────────────────────────────────

✓ Pre-push checks PASSED
   Push allowed.
```

---

## Commit Message Format

### Required Format

```
[TYPE] Brief description
```

### Valid Types

| Type | Use Case | Example |
|------|----------|---------|
| `feat` | New feature | `[feat] add business analyst mode` |
| `fix` | Bug fix | `[fix] correct date parsing` |
| `docs` | Documentation | `[docs] update README with setup` |
| `style` | Code formatting | `[style] format constants` |
| `refactor` | Code refactoring | `[refactor] simplify validator` |
| `perf` | Performance improvement | `[perf] optimize query` |
| `test` | Test changes | `[test] add validator tests` |
| `chore` | Maintenance | `[chore] update dependencies` |

### Examples

```bash
git commit -m "[feat] add new validation"
git commit -m "[fix] correct error handling"
git commit -m "[docs] update CHANGELOG"
git commit -m "[test] add integration tests"
```

---

## If Hooks Fail

### Pre-Commit Hook Fails

**Symptom:**
```
▶ Format check (Black)... ✗
```

**Solution:**
```bash
# Auto-format code
python scripts/format.py

# Stage changes
git add .

# Try commit again
git commit -m "[fix] format changes"
```

---

### Pre-Push Hook Fails

**Symptom:**
```
▶ Checking if branch is up-to-date... ✗
   Your branch is 3 commits behind
```

**Solution:**
```bash
# Pull latest changes
git pull

# Try push again
git push
```

---

### Commit Message Fails

**Symptom:**
```
✗ Commit message is invalid
   Error: Invalid type 'feature'. Must be: feat, fix, ...
```

**Solution:**
```bash
# Use --amend to fix message
git commit --amend -m "[feat] add new feature"
```

---

## Emergency Overrides (Use Sparingly)

### Skip Pre-Commit Hook

```bash
git commit --no-verify -m "emergency fix"
```

⚠️ **Only use in emergencies** - skips all validation

### Skip Pre-Push Hook

```bash
git push --no-verify
```

⚠️ **Only use in emergencies** - skips integration tests

---

## Monitor Hooks

### View Hook Logs

```bash
# View pre-commit log
tail -f .vscode/hook-logs/pre-commit.log

# View pre-push log
tail -f .vscode/hook-logs/pre-push.log

# View commit-msg log
tail -f .vscode/hook-logs/commit-msg.log
```

### Check Recent Failures

```bash
# Find failures
grep "FAILED" .vscode/hook-logs/*.log

# Find successes
grep "SUCCESS" .vscode/hook-logs/*.log
```

---

## GitHub Actions

### Pull Request Validation

When you create a PR:
```
1. Quality Checks start
2. Test Suite runs
3. Configuration Validation runs
4. Summary comment posted

If all pass ✓ → PR can be merged
If any fail ✗ → PR blocked until fixed
```

### View PR Status

In GitHub:
```
Pull Request → Checks tab → [workflow name] → View logs
```

Or via CLI:
```bash
gh workflow view on-pull-request --log
```

### Push to Main

When code is merged to main:
```
1. Quality checks run
2. Full test suite runs
3. Docker image built
4. Security scan
5. Team notified
```

### Release

When release is created:
```
1. Version consistency validated
2. CHANGELOG checked
3. Build artifacts created
4. Docker image built
5. Release published
```

---

## Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| Hooks not running | `python scripts/hooks/setup_hooks.py` |
| Permission denied | `chmod +x .git/hooks/*` |
| Format errors | `python scripts/format.py` |
| Import errors | `python -m isort .` |
| Test failures | Run locally: `python -m pytest tests/` |
| Can't push | `git pull` first |
| Wrong commit message | `git commit --amend` |

---

## Performance Tips

- **Commit frequently:** Smaller commits are faster
- **Format often:** Pre-commit will catch fewer issues
- **Run tests locally:** Catch failures before pushing
- **Keep tests fast:** Don't include long-running tests
- **Use `--no-verify` only when necessary:** It skips important checks

---

## Help & Support

### Resources

- Full strategy: [hook-implementation-strategy.md](./hook-implementation-strategy.md)
- Integration guide: [HOOK-INTEGRATION-GUIDE.md](./HOOK-INTEGRATION-GUIDE.md)
- Scripts: [scripts/hooks/](../../scripts/hooks/)

### Check Configuration

```bash
# Validate all configuration

# Check hooks installed
ls -la .git/hooks/
```

### Common Questions

**Q: Can I commit without running hooks?**
A: Yes, use `git commit --no-verify`, but don't do this routinely.

**Q: How do I fix failed tests in a hook?**
A: Run `python -m pytest tests/ -v` locally, fix issues, then commit.

**Q: What if I made a mistake in the commit message?**
A: Use `git commit --amend -m "[TYPE] new message"`

**Q: How long does pre-commit take?**
A: Typically 15-30 seconds depending on code size and tests.

**Q: Can I modify the hooks?**
A: Yes, edit `scripts/hooks/*.py` then run `python scripts/hooks/setup_hooks.py`

---

**Last Updated:** 2026-06-30  
**Quick Reference Version:** 1.0.0
