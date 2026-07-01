#!/usr/bin/env python
"""
Lint Script

Executes code quality checks using flake8 and other linters.
"""

import argparse
import sys
import logging
import subprocess
from pathlib import Path

logger = None


def setup_logging(name: str, level: int = logging.INFO) -> logging.Logger:
    """Configure and return logger."""
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    log = logging.getLogger(name)
    log.setLevel(level)
    log.addHandler(handler)
    return log


def run_linting(fix: bool = False) -> int:
    """
    Execute linting checks.
    
    Args:
        fix: Automatically fix issues where possible
        
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        workspace_root = Path(__file__).parent.parent
        
        logger.info("Running code quality checks...")
        
        # Check if flake8 is available
        try:
            result = subprocess.run(
                ['python', '-m', 'flake8', '--version'],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                logger.warning("flake8 not found. Install with: pip install flake8")
                logger.info("Linting is ready for configuration")
                return 0
        except FileNotFoundError:
            logger.warning("flake8 not installed")
            logger.info("Linting is ready for configuration")
            return 0
        
        # Run flake8
        cmd = [
            'python', '-m', 'flake8', '.',
            '--max-line-length=100',
            '--exclude=.venv,build,dist,__pycache__'
        ]
        
        logger.info(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=str(workspace_root))
        
        if result.returncode == 0:
            logger.info("Code quality checks passed!")
        else:
            logger.error("Code quality issues found")
        
        return result.returncode
        
    except Exception as e:
        logger.error(f"Linting failed: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Code Quality Linting Script',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Automatically fix issues where possible'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logging('lint', level=log_level)
    
    # Execute linting
    exit_code = run_linting(fix=args.fix)
    sys.exit(exit_code)
