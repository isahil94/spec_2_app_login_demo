#!/usr/bin/env python
"""
Build Script

Orchestrates the project build process.
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


def validate_structure() -> bool:
    """
    Validate repository structure has required directories and files.
    
    Returns:
        True if structure is valid, False otherwise
    """
    workspace_root = Path(__file__).parent.parent
    required_items = {
        'directories': [
            '.github',
            'ai/agents',
            'ai/contracts',
            'ai/skills',
            'ai/tools',
            'ai/prompts',
            'scripts',
            'orchestration',
            'apps',
            'artifacts'
        ],
        'files': [
            'requirements.txt',
            'README.md',
            '.github/copilot-instructions.md',
            'pyproject.toml'
        ]
    }
    
    # Check directories
    for dir_path in required_items['directories']:
        full_path = workspace_root / dir_path
        if not full_path.exists():
            logger.error(f"❌ Missing directory: {dir_path}")
            return False
        if not full_path.is_dir():
            logger.error(f"❌ Not a directory: {dir_path}")
            return False
    
    # Check files
    for file_path in required_items['files']:
        full_path = workspace_root / file_path
        if not full_path.exists():
            logger.warning(f"⚠️  Missing file: {file_path}")
            # Don't fail on missing files, just warn
    
    logger.info("✅ Repository structure validated")
    return True


def run_build() -> int:
    """
    Execute build process.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        logger.info("🔨 Starting build process...")
        
        # Validate repository structure
        logger.info("📋 Validating repository structure...")
        if not validate_structure():
            logger.error("Repository structure validation failed")
            return 1
        
        # Verify key configuration files exist
        logger.info("📝 Checking configuration files...")
        workspace_root = Path(__file__).parent.parent
        config_files = [
            'requirements.txt',
            '.github/copilot-instructions.md',
            'ai/agents/00-supervisor.md'
        ]
        
        missing_configs = []
        for config in config_files:
            if not (workspace_root / config).exists():
                missing_configs.append(config)
        
        if missing_configs:
            logger.warning(f"⚠️  Missing configuration files: {', '.join(missing_configs)}")
        else:
            logger.info("✅ All configuration files present")
        
        # Check artifact directories
        logger.info("📂 Verifying artifact directories...")
        artifact_stages = ['requirements', 'architecture', 'design', 'frontend', 'backend', 
                          'database', 'tests', 'documentation', 'planning']
        artifacts_dir = workspace_root / 'artifacts'
        
        for stage in artifact_stages:
            stage_dir = artifacts_dir / stage
            if not stage_dir.exists():
                stage_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"📁 Created artifact directory: artifacts/{stage}")
        
        logger.info("✅ All artifact directories ready")
        
        # Summary
        logger.info("")
        logger.info("=" * 60)
        logger.info("✓ Build completed successfully")
        logger.info("=" * 60)
        logger.info("Repository is ready for agent execution")
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Build failed: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Project Build Script',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logging('build', level=log_level)
    
    # Execute build
    exit_code = run_build()
    sys.exit(exit_code)
