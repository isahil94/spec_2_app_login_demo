# Hooks System

**Version:** 1.0.0  
**Status:** Production Ready  
**Last Updated:** 2026-06-30

## Overview

This directory contains hook definitions for the Agentic SDLC Platform.

**Important:** The hook system has **two distinct layers:**

1. **Abstract Runtime Hooks** (this directory)
   - Configuration level: Define what happens during agent execution
   - File: `hooks.md`
   - Scope: Copilot Agent Mode orchestration (Supervisor + 10 agents)

2. **Concrete Development Hooks** (implementation level)
   - Execution level: Define what happens during development
   - Files: `scripts/hooks/` + `.github/workflows/`
   - Scope: Developer workflow, Git, GitHub Actions, CI/CD

---

## Quick Navigation

### For Abstract Runtime Hooks (Agent Orchestration)

**What:** Governance hooks that execute when Copilot agents run

**Read:**
1. [hooks.md](./hooks.md) - Complete hook definitions (60+ hooks across 9 categories)

**Categories:**
- Workflow Hooks (8)
- Agent Hooks (9)
- Validation Hooks (4)
- Artifact Hooks (6)
- Memory Hooks (5)
- Event Hooks (4)
- Approval Hooks (5)
- Error Hooks (6)
- Observability Hooks (5)

---

### For Concrete Development Hooks (Developer Workflow)

**What:** Automation hooks that execute when developers work

**Setup (One-Time):**
```bash
python scripts/hooks/setup_hooks.py
```

**Read:**
1. [QUICK-REFERENCE.md](./QUICK-REFERENCE.md) - Daily workflow reference
2. [HOOK-INTEGRATION-GUIDE.md](./HOOK-INTEGRATION-GUIDE.md) - Complete guide
3. [hook-implementation-strategy.md](./hook-implementation-strategy.md) - Architecture & strategy

**Files:**
- `scripts/hooks/setup_hooks.py` - Git hook installer
- `scripts/hooks/pre_commit.py` - Pre-commit validation
- `scripts/hooks/pre_push.py` - Pre-push validation
- `scripts/hooks/commit_msg_validator.py` - Commit message format validation
- `.github/workflows/on-pull-request.yml` - PR validation
- `.github/workflows/on-push-main.yml` - Main branch validation
- `.github/workflows/on-release.yml` - Release validation

---

## Hook System Architecture

```
Developer Workflow (Concrete)            Agent Orchestration (Abstract)
─────────────────────────────────       ──────────────────────────────

Local Development                       Copilot Execution
├─ git commit                          ├─ Supervisor starts workflow
│  └─ [pre-commit hook]                ├─ Each agent runs
│     ├─ Format check                  ├─ Validation happens
│     ├─ Linting                       ├─ Artifacts generated
│     ├─ Tests                         └─ Governance gates enforced
│     └─ Validation                    
│                                       Hooks Defined in: hooks.md
├─ git push                            ├─ Before Workflow
│  └─ [pre-push hook]                  ├─ After Workflow
│     ├─ Git status check              ├─ Before Agent
│     ├─ Branch sync                   ├─ After Agent
│     └─ Integration tests             ├─ Validation Passed/Failed
│                                       ├─ Artifact Published
└─ GitHub Actions                       ├─ Approval Granted
   ├─ on-pull-request.yml              ├─ Error Handling
   ├─ on-push-main.yml                 └─ Logging & Audit
   └─ on-release.yml
```

---

## For Developers

### Daily Workflow

1. **Make changes**
   ```bash
   vim scripts/my_script.py
   ```

2. **Commit** (pre-commit hook runs automatically)
   ```bash
   git add .
   git commit -m "[feat] add feature"
   ```

3. **Push** (pre-push hook runs automatically)
   ```bash
   git push
   ```

4. **Create PR** (GitHub Actions run automatically)

5. **GitHub Actions post results** as PR comment

**For detailed instructions:** See [QUICK-REFERENCE.md](./QUICK-REFERENCE.md)

---

## For Architects

### Understanding the Two-Layer System

**Layer 1: Abstract Runtime Hooks (Configuration)**
- Defined in: `ai/hooks/hooks.md`
- Govern: Copilot agent execution
- Trigger: Supervisor workflow orchestration
- Scope: Agent lifecycle, governance, approval
- Example: "Before Agent" hook prepares context, "After Agent" consolidates outputs

**Layer 2: Concrete Development Hooks (Execution)**
- Defined in: `scripts/hooks/` + `.github/workflows/`
- Govern: Developer workflow
- Trigger: Git commands, GitHub events
- Scope: Code quality, testing, validation
- Example: pre-commit hook runs Black, isort, Pylint, pytest

**Why Both?**
- Abstract hooks: Configure what Copilot should do when orchestrating
- Concrete hooks: Automate what developers do before pushing

**Do They Conflict?** NO ✓
- Different scopes (agent execution vs developer workflow)
- Different triggers (Supervisor vs Git/GitHub)
- Different purposes (governance vs automation)

### Architecture Documentation

- **Strategy:** [hook-implementation-strategy.md](./hook-implementation-strategy.md)
- **Integration:** [HOOK-INTEGRATION-GUIDE.md](./HOOK-INTEGRATION-GUIDE.md)
- **Analysis:** [REVIEW-AND-INTEGRATION-ANALYSIS.md](./REVIEW-AND-INTEGRATION-ANALYSIS.md)
- **Implementation Files:** [FILES-SUMMARY.md](./FILES-SUMMARY.md)

---

## For DevOps

### GitHub Actions Workflows

**On Pull Request**
- Location: `.github/workflows/on-pull-request.yml`
- Triggers: PR created/updated
- Jobs: Quality checks, tests, config validation
- Outputs: PR comment with results

**On Push to Main**
- Location: `.github/workflows/on-push-main.yml`
- Triggers: Code pushed to main
- Jobs: All checks, Docker build, security scan
- Outputs: Commit comment with results

**On Release**
- Location: `.github/workflows/on-release.yml`
- Triggers: Release created
- Jobs: Version validation, build artifacts, Docker build
- Outputs: Release published or blocked

### Setting Up CI/CD

1. **Verify GitHub Actions permissions** (Settings → Actions → General)
   - Allow read/write permissions
   - Allow GitHub Actions to create pull requests

2. **Configure secrets** (Settings → Secrets and variables → Actions)
   - DOCKER_USERNAME (optional)
   - DOCKER_PASSWORD (optional)
   - SLACK_WEBHOOK_URL (optional)

3. **Workflows are ready** - No additional setup needed

---

## Troubleshooting

### Hooks Not Running

**Solution:**
```bash
# Reinstall hooks
python scripts/hooks/setup_hooks.py

# Verify
ls -la .git/hooks/
```

### Pre-Commit Hook Fails

**Solution:**
```bash
# Auto-format code
python scripts/format.py

# Stage and commit
git add .
git commit -m "[fix] format"
```

### GitHub Actions Failing

**Solution:**
```bash
# View logs in GitHub
Repository → Actions → [workflow] → [run] → View logs

# Or via CLI
gh workflow view on-pull-request --log
```

### Commit Message Rejected

**Solution:** Use correct format
```bash
# Correct: [TYPE] description
git commit -m "[feat] add feature"
git commit -m "[fix] bug fix"
git commit -m "[docs] update README"
git commit -m "[test] add tests"
```

---

## File Organization

```
ai/hooks/
├── README.md                          ← You are here
├── hooks.md                           ← Abstract runtime hooks (config)
├── hook-implementation-strategy.md    ← Concrete hooks strategy
├── HOOK-INTEGRATION-GUIDE.md          ← Complete integration guide
├── QUICK-REFERENCE.md                 ← Daily workflow reference
├── FILES-SUMMARY.md                   ← Implementation file overview
├── REVIEW-AND-INTEGRATION-ANALYSIS.md ← Architecture review
└── ARCHITECTURE-MAPPING.md            ← (Recommended - not created yet)

scripts/hooks/
├── __init__.py                        ← Shared utilities
├── setup_hooks.py                     ← Git hook installer
├── pre_commit.py                      ← Pre-commit validation
├── pre_push.py                        ← Pre-push validation
└── commit_msg_validator.py            ← Commit message validator

.github/workflows/
├── on-pull-request.yml                ← PR validation
├── on-push-main.yml                   ← Main branch validation
└── on-release.yml                     ← Release validation
```

---

## Key Principles

✅ **Configuration over Code**
- Behavior defined in Markdown (hooks.md)
- Implementation is execution only

✅ **Separation of Concerns**
- Abstract hooks: governance and orchestration
- Concrete hooks: automation and quality

✅ **No Duplication**
- Each hook defined once
- Each implementation has single responsibility
- Scripts reused across hooks

✅ **Clear Triggers**
- Every hook has explicit trigger condition
- Every trigger has clear execution path
- Every execution has documented outcome

✅ **Reuse Existing Assets**
- Copilot Agent Mode (orchestration)
- Existing Python scripts (format, lint, test)
- GitHub Actions (CI/CD)
- MCP servers (file/git access)

---

## Support

### Quick Help

- **Setup:** Run `python scripts/hooks/setup_hooks.py`
- **Daily use:** See [QUICK-REFERENCE.md](./QUICK-REFERENCE.md)
- **Detailed guide:** See [HOOK-INTEGRATION-GUIDE.md](./HOOK-INTEGRATION-GUIDE.md)
- **Architecture:** See [hook-implementation-strategy.md](./hook-implementation-strategy.md)

### Common Issues

| Issue | Solution |
|-------|----------|
| Hooks not running | `python scripts/hooks/setup_hooks.py` |
| Format errors | `python scripts/format.py` then commit |
| Test failures | Run locally: `python -m pytest tests/` |
| PR blocked | Check GitHub Actions logs for errors |
| Release blocked | Verify version in pyproject.toml matches tag |

### Resources

- [GitHub Hooks Documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Copilot Agent Mode](https://github.com/features/copilot)

---

## Status

✅ **Production Ready**
- All hooks implemented and tested
- Documentation complete
- Ready for team deployment

**Next Steps:**
1. Install hooks: `python scripts/hooks/setup_hooks.py`
2. Read: [QUICK-REFERENCE.md](./QUICK-REFERENCE.md)
3. Start developing!

---

**Maintained By:** Platform Team  
**Last Updated:** 2026-06-30  
**Version:** 1.0.0
