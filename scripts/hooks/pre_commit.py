"""
Pre-commit hook implementation.

Runs before git commit to validate:
- Code formatting
- Linting
- Unit tests
- Schema validation
"""

import sys
from datetime import datetime
from pathlib import Path

from . import (
    ensure_log_dir,
    get_workspace_root,
    run_black,
    run_isort,
    run_pylint,
    run_pytest,
)


def log_result(message):
    """Log hook result."""
    log_dir = ensure_log_dir()
    log_file = log_dir / "pre-commit.log"
    
    timestamp = datetime.now().isoformat()
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def run_pre_commit_hook():
    """
    Run pre-commit validation.
    
    Returns:
        0 = All checks passed, allow commit
        1 = Some checks failed, block commit
    """
    print("\n╔════════════════════════════════════════╗")
    print("║      Pre-Commit Hook Validation      ║")
    print("╚════════════════════════════════════════╝\n")
    
    checks_passed = 0
    checks_failed = 0
    
    # 1. Format check (Black)
    code, _, err = run_black()
    if code == 0:
        checks_passed += 1
    else:
        checks_failed += 1
        print("ℹ  Fix formatting with: python scripts/format.py\n")
    
    # 2. Import sorting (isort)
    code, _, err = run_isort()
    if code == 0:
        checks_passed += 1
    else:
        checks_failed += 1
        print("ℹ  Fix imports with: python -m isort .\n")
    
    # 3. Linting
    code, _, err = run_pylint()
    if code == 0:
        checks_passed += 1
    else:
        checks_failed += 1
        print("ℹ  Check linting output above. Fix issues and try again.\n")
    
    # 4. Unit tests
    code, _, err = run_pytest()
    if code == 0:
        checks_passed += 1
    else:
        checks_failed += 1
        print("ℹ  Fix test failures and try again.\n")
    
    # Summary
    print("\n" + "─" * 40)
    print(f"Results: {checks_passed} passed, {checks_failed} failed")
    print("─" * 40 + "\n")
    
    if checks_failed > 0:
        print("❌ Pre-commit checks FAILED\n")
        print("   Fix the issues above and try again.\n")
        log_result(f"FAILED: {checks_failed} checks failed")
        return 1
    else:
        print("✓ Pre-commit checks PASSED\n")
        print("   Commit allowed.\n")
        log_result("SUCCESS: All checks passed")
        return 0


if __name__ == "__main__":
    sys.exit(run_pre_commit_hook())
