"""
Commit message validator hook.

Validates commit message format before finalization.

Required format:
  [TYPE] Brief description

Valid types:
  - feat: New feature
  - fix: Bug fix
  - docs: Documentation
  - style: Code style/formatting
  - refactor: Code refactoring
  - perf: Performance improvement
  - test: Test additions/changes
  - chore: Maintenance/build
"""

import sys
from datetime import datetime
from pathlib import Path

from . import ensure_log_dir, validate_commit_message


def log_result(message):
    """Log hook result."""
    log_dir = ensure_log_dir()
    log_file = log_dir / "commit-msg.log"
    
    timestamp = datetime.now().isoformat()
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def run_commit_msg_hook(message_file):
    """
    Validate commit message.
    
    Args:
        message_file: Path to commit message file
        
    Returns:
        0 = Message valid, allow commit
        1 = Message invalid, block commit
    """
    try:
        with open(message_file, 'r') as f:
            message = f.read()
    except Exception as e:
        print(f"✗ Error reading commit message: {e}")
        return 1
    
    print("\n╔════════════════════════════════════════╗")
    print("║    Commit Message Validation          ║")
    print("╚════════════════════════════════════════╝\n")
    
    # Validate message
    valid, reason = validate_commit_message(message)
    
    if valid:
        print(f"✓ Commit message is valid\n")
        print(f"  Message: {message.split(chr(10))[0]}\n")
        log_result(f"SUCCESS: {message.split(chr(10))[0]}")
        return 0
    else:
        print(f"✗ Commit message is invalid\n")
        print(f"  Error: {reason}\n")
        print("  Required format:")
        print("    [TYPE] Brief description\n")
        print("  Valid types:")
        print("    feat, fix, docs, style, refactor, perf, test, chore\n")
        print("  Examples:")
        print("    [feat] add business analyst mode")
        print("    [fix] correct date calculation")
        print("    [docs] update README")
        print("    [test] add validator tests\n")
        log_result(f"FAILED: {reason}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: commit_msg_validator.py <commit-message-file>")
        sys.exit(1)
    
    sys.exit(run_commit_msg_hook(sys.argv[1]))
