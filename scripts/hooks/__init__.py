"""
Hook implementation utilities.

Provides reusable functions for validation, formatting, and testing
used by git hooks and CI/CD pipelines.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description, allow_fail=False):
    """
    Run a command and return result.
    
    Args:
        cmd: Command list (e.g., ['python', '-m', 'black', '.'])
        description: Human-readable description
        allow_fail: If True, don't exit on failure
        
    Returns:
        (exit_code, stdout, stderr)
    """
    print(f"▶ {description}...", end=" ", flush=True)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("✓")
            return (0, result.stdout, result.stderr)
        else:
            print("✗")
            if allow_fail:
                return (result.returncode, result.stdout, result.stderr)
            else:
                print(result.stderr or result.stdout)
                return (result.returncode, result.stdout, result.stderr)
                
    except subprocess.TimeoutExpired:
        print("✗ (timeout)")
        if not allow_fail:
            sys.exit(1)
        return (1, "", "Timeout")
    except Exception as e:
        print("✗ (error)")
        if not allow_fail:
            sys.exit(1)
        return (1, "", str(e))


def run_black(target="."):
    """Run Black formatter."""
    return run_command(
        ["python", "-m", "black", "--check", "--quiet", target],
        "Format check (Black)",
        allow_fail=True
    )


def run_isort(target="."):
    """Run isort (import sorting)."""
    return run_command(
        ["python", "-m", "isort", "--check-only", "--quiet", target],
        "Import sorting (isort)",
        allow_fail=True
    )


def run_pylint():
    """Run Pylint."""
    return run_command(
        ["python", "-m", "pylint", "scripts/", "--disable=all", "--enable=E,F"],
        "Linting (Pylint)",
        allow_fail=True
    )


def run_pytest():
    """Run pytest."""
    return run_command(
        ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
        "Unit tests (pytest)",
        allow_fail=True
    )


def run_pytest_cov():
    """Run pytest with coverage."""
    return run_command(
        ["python", "-m", "pytest", "tests/", "--cov=scripts", "--cov-fail-under=80"],
        "Test coverage",
        allow_fail=True
    )


def validate_commit_message(message):
    """
    Validate commit message format.
    
    Format: [TYPE] brief message
    
    Types: feat, fix, docs, style, refactor, perf, test, chore
    """
    valid_types = ["feat", "fix", "docs", "style", "refactor", "perf", "test", "chore"]
    
    lines = message.strip().split('\n')
    first_line = lines[0]
    
    # Check format
    if not first_line.startswith('['):
        return False, "Message must start with [TYPE]"
    
    if ']' not in first_line:
        return False, "Message must have closing ]"
    
    # Extract type
    bracket_end = first_line.index(']')
    msg_type = first_line[1:bracket_end]
    
    if msg_type not in valid_types:
        return False, f"Invalid type '{msg_type}'. Must be: {', '.join(valid_types)}"
    
    # Check first line length
    if len(first_line) > 72:
        return False, "First line must be ≤ 72 characters"
    
    # Check message content
    if len(first_line) <= bracket_end + 2:
        return False, "Message content is empty"
    
    return True, "Valid"


def get_workspace_root():
    """Get workspace root directory."""
    return Path(__file__).parent.parent.parent


def ensure_log_dir():
    """Ensure log directory exists."""
    log_dir = get_workspace_root() / ".vscode" / "hook-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir
