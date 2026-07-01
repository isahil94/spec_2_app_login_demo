#!/usr/bin/env python
"""
Test Script

Executes the project's test suite using pytest.
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


def run_tests(verbose: bool = False, coverage: bool = False) -> int:
    """
    Execute test suite.
    
    Args:
        verbose: Enable verbose output
        coverage: Generate coverage report
        
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        workspace_root = Path(__file__).parent.parent
        tests_dir = workspace_root / 'tests'
        
        if not tests_dir.exists():
            logger.warning(f"Tests directory not found: {tests_dir}")
            logger.info("Test suite is ready for implementation")
            return 0
        
        logger.info("Running test suite...")
        
        # Build pytest command
        cmd = ['python', '-m', 'pytest', str(tests_dir), '-v', '--tb=short']
        
        if coverage:
            cmd.extend(['--cov', '--cov-report=html'])
        
        if verbose:
            cmd.append('-vv')
        
        logger.info(f"Executing: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, cwd=str(workspace_root))
        
        if result.returncode == 0:
            logger.info("All tests passed!")
        else:
            logger.error("Some tests failed")
        
        return result.returncode
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Project Test Script',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Generate coverage report'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logging('test', level=log_level)
    
    # Execute tests
    exit_code = run_tests(verbose=args.verbose, coverage=args.coverage)
    sys.exit(exit_code)
