#!/usr/bin/env python
"""
Format Script

Applies code formatting using Black and isort.
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


def run_formatting(check_only: bool = False) -> int:
    """
    Apply code formatting.
    
    Args:
        check_only: Check formatting without applying changes
        
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        workspace_root = Path(__file__).parent.parent
        
        logger.info("Applying code formatting...")
        
        # Try to run isort
        try:
            cmd_isort = ['python', '-m', 'isort', '.']
            if check_only:
                cmd_isort.append('--check-only')
            
            logger.info("Organizing imports with isort...")
            subprocess.run(cmd_isort, cwd=str(workspace_root), capture_output=True)
        except Exception as e:
            logger.debug(f"isort not available: {e}")
        
        # Try to run black
        try:
            cmd_black = ['python', '-m', 'black', '.', '--line-length=100']
            if check_only:
                cmd_black.append('--check')
            
            logger.info("Formatting code with Black...")
            result = subprocess.run(cmd_black, cwd=str(workspace_root))
            
            if result.returncode == 0:
                logger.info("Code formatting completed successfully!")
            else:
                logger.warning("Some files were not formatted")
            
            return result.returncode
        except Exception as e:
            logger.warning(f"Black not available: {e}")
            logger.info("Code formatting is ready for configuration")
            return 0
        
    except Exception as e:
        logger.error(f"Formatting failed: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Code Formatting Script',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check formatting without applying changes'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logging('format', level=log_level)
    
    # Execute formatting
    exit_code = run_formatting(check_only=args.check)
    sys.exit(exit_code)
