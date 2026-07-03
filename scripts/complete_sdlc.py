#!/usr/bin/env python
"""
Complete SDLC Pipeline Script (configuration-driven).

Runs the full workflow via WorkflowCoordinator using Markdown agent definitions.
No per-agent Python execution scripts are invoked.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestration.workflow.coordinator import WorkflowCoordinator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def default_spec_path(workspace_root: Path) -> Path:
    candidates = [
        workspace_root / "examples" / "task-management" / "specification.md",
        workspace_root / "specification.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def main() -> int:
    workspace_root = Path(__file__).parent.parent
    coordinator = WorkflowCoordinator(project_root=workspace_root)

    workflow_id = f"wf-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    spec_file = default_spec_path(workspace_root)

    if not spec_file.exists():
        logger.error("Specification file not found: %s", spec_file)
        return 1

    logger.info("Starting configuration-driven SDLC pipeline")
    logger.info("Workflow ID: %s", workflow_id)

    coordinator.initialize_workflow(spec_file=spec_file, workflow_id=workflow_id)
    summary = coordinator.execute_workflow()
    coordinator.save_execution_log()
    coordinator.save_execution_summary()

    logger.info("Pipeline status: %s", summary.get("status"))
    logger.info("Stages executed: %s", summary.get("total_stages_executed", 0))
    logger.info("Successful stages: %s", summary.get("successful_stages", 0))
    logger.info("Failed stages: %s", summary.get("failed_stages", 0))

    return 0 if summary.get("failed_stages", 0) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
