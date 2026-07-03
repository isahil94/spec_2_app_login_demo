#!/usr/bin/env python
"""
Run Complete SDLC Workflow (configuration-driven).

Executes the workflow through WorkflowCoordinator and Markdown agent definitions.
No per-agent execution scripts are invoked.
"""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestration.workflow.coordinator import WorkflowCoordinator

logger = logging.getLogger(__name__)


def setup_logging(level: int = logging.INFO) -> None:
    """Configure basic logging."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def default_spec_path(workspace_root: Path) -> Path:
    """Resolve default specification path."""
    candidates = [
        workspace_root / "examples" / "task-management" / "specification.md",
        workspace_root / "specification.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def run_pipeline(spec_file: Path, workflow_id: str, max_stages: int | None = None) -> int:
    """Initialize and execute workflow coordinator."""
    coordinator = WorkflowCoordinator(project_root=Path(__file__).parent.parent)

    state_file = coordinator.state_dir / f"{workflow_id}.json"
    if state_file.exists():
        coordinator.resume_workflow(workflow_id)
        logger.info("Resumed workflow: %s", workflow_id)
    else:
        coordinator.initialize_workflow(spec_file, workflow_id)
        logger.info("Initialized workflow: %s", workflow_id)

    summary = coordinator.execute_workflow(max_stages=max_stages)
    coordinator.save_execution_log()
    coordinator.save_execution_summary()

    print("\n" + "=" * 70)
    print("SDLC PIPELINE EXECUTION SUMMARY")
    print("=" * 70)
    print(f"Workflow ID: {summary.get('workflow_id')}")
    print(f"Status: {summary.get('status')}")
    print(f"Stages Executed: {summary.get('total_stages_executed', 0)}")
    print(f"Successful: {summary.get('successful_stages', 0)}")
    print(f"Failed: {summary.get('failed_stages', 0)}")
    print("=" * 70)

    return 0 if summary.get("failed_stages", 0) == 0 else 1


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Execute configuration-driven SDLC workflow from Markdown agent definitions.",
    )
    parser.add_argument("--input", type=str, help="Specification path")
    parser.add_argument("--workflow-id", type=str, default="wf-default", help="Workflow ID")
    parser.add_argument("--max-stages", type=int, help="Maximum number of stages to execute")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    setup_logging(logging.DEBUG if args.verbose else logging.INFO)

    workspace_root = Path(__file__).parent.parent
    spec_file = Path(args.input) if args.input else default_spec_path(workspace_root)
    if not spec_file.exists():
        logger.error("Specification file not found: %s", spec_file)
        return 1

    return run_pipeline(spec_file=spec_file, workflow_id=args.workflow_id, max_stages=args.max_stages)


if __name__ == "__main__":
    sys.exit(main())
