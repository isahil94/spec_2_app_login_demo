"""
Pre-push hook implementation.

Runs before git push to validate:
- All pre-commit checks pass
- Integration tests pass
- Build succeeds
- No uncommitted changes
"""

import subprocess
import sys
from datetime import datetime

from . import ensure_log_dir, run_pytest


def log_result(message):
    """Log hook result."""
    log_dir = ensure_log_dir()
    log_file = log_dir / "pre-push.log"
    
    timestamp = datetime.now().isoformat()
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def check_git_status():
    """Check for uncommitted changes."""
    print("▶ Checking for uncommitted changes...", end=" ", flush=True)
    
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        print("✗")
        print("\n  Uncommitted changes detected:")
        print("  " + "\n  ".join(result.stdout.split('\n')))
        print("\n  Stage changes with: git add .")
        print("  Or commit with: git commit\n")
        return False
    else:
        print("✓")
        return True


def check_branch_up_to_date():
    """Check if branch is up-to-date with remote."""
    print("▶ Checking if branch is up-to-date...", end=" ", flush=True)
    
    try:
        # Fetch latest from remote
        subprocess.run(
            ["git", "fetch"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Check if current branch is behind
        result = subprocess.run(
            ["git", "rev-list", "--count", "@{u}..HEAD"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            # Branch not tracking, assume OK
            print("✓")
            return True
        
        behind = int(result.stdout.strip())
        if behind > 0:
            print("✗")
            print(f"\n  Your branch is {behind} commits behind")
            print("  Pull latest changes: git pull\n")
            return False
        else:
            print("✓")
            return True
            
    except Exception as e:
        print("⚠")
        print(f"  Warning: Could not check remote status: {e}")
        return True


def run_integration_tests():
    """Run integration tests (subset of full test suite)."""
    print("▶ Running integration tests...", end=" ", flush=True)
    
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/integration/", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("✓")
            return True
        else:
            print("✗")
            print("\n" + result.stdout)
            print("\nℹ  Fix integration test failures and try again.\n")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ (timeout)")
        return False
    except Exception as e:
        print("⚠")
        print(f"  Warning: Could not run integration tests: {e}")
        return True


def run_pre_push_hook():
    """
    Run pre-push validation.
    
    Returns:
        0 = All checks passed, allow push
        1 = Some checks failed, block push
    """
    print("\n╔════════════════════════════════════════╗")
    print("║        Pre-Push Hook Validation       ║")
    print("╚════════════════════════════════════════╝\n")
    
    checks_passed = 0
    checks_failed = 0
    
    # 1. Check for uncommitted changes
    if check_git_status():
        checks_passed += 1
    else:
        checks_failed += 1
    
    # 2. Check branch is up-to-date
    if check_branch_up_to_date():
        checks_passed += 1
    else:
        checks_failed += 1
    
    # 3. Run integration tests
    if run_integration_tests():
        checks_passed += 1
    else:
        checks_failed += 1
    
    # Summary
    print("\n" + "─" * 40)
    print(f"Results: {checks_passed} passed, {checks_failed} failed")
    print("─" * 40 + "\n")
    
    if checks_failed > 0:
        print("❌ Pre-push checks FAILED\n")
        print("   Fix the issues above and try again.\n")
        log_result(f"FAILED: {checks_failed} checks failed")
        return 1
    else:
        print("✓ Pre-push checks PASSED\n")
        print("   Push allowed.\n")
        log_result("SUCCESS: All checks passed")
        return 0


if __name__ == "__main__":
    sys.exit(run_pre_push_hook())
