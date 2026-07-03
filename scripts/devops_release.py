#!/usr/bin/env python
"""
DevOps & Release Agent Script

Orchestrates DevOps and release operations for the Agentic SDLC Platform.
Builds artifacts, creates deployments, and prepares releases.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from agent_base import (
    AgentBase,
    display_agent_info,
    load_agent_definition,
    log_placeholder_execution,
    record_execution_state,
    validate_paths,
    validate_required_inputs,
)

REQUIRED_INPUT_ARTIFACTS = [
    'architecture/deployment-architecture.md',
    'architecture/technology-stack.md',
    'architecture/security-architecture.md',
    'tests/integration-test-cases.md',
    'review/review-report.md',
    'review/findings.md',
]


class DevOpsReleaseAgent(AgentBase):
    """DevOps & Release agent for building, testing, and deploying applications."""

    def __init__(self):
        super().__init__(
            name="DevOps & Release",
            agent_file=".github/agents/08-devops-release.md",
        )

    def run(self, input_path: Optional[str] = None, output_path: Optional[str] = None):
        """Execute DevOps & Release workflow."""
        self.logger.info("DevOps & Release Agent started")

        # Resolve default paths for stage-level incremental checks.
        input_p = Path(input_path) if input_path else self.workspace_root / "artifacts"
        output_p = Path(output_path) if output_path else self.workspace_root / "artifacts"
        validate_paths(input_path=input_p, output_path=output_p)

        missing_inputs = validate_required_inputs(input_p, REQUIRED_INPUT_ARTIFACTS)
        if missing_inputs:
            self.logger.warning(f"Missing recommended inputs: {', '.join(missing_inputs)}")

        agent_def = load_agent_definition('08-devops-release.md')
        metadata = agent_def['metadata']
        display_agent_info(metadata)

        status, input_signature, reason = self.get_execution_status(
            agent_id=metadata.get('id', 'devops_release'),
            input_path=input_p,
            output_path=output_p,
            include_paths=REQUIRED_INPUT_ARTIFACTS,
        )

        if status == 'SKIPPED':
            self.logger.info(f"Skipping DevOps artifact update: {reason}")
            return True

        self.logger.info(f"Proceeding with DevOps execution: {reason}")
        self.logger.info(f"Execution status: {status}")

        # Execute DevOps operations
        self.logger.info("Building project artifacts...")
        self.logger.info("Running quality checks...")
        self.logger.info("Packaging application...")
        self.logger.info("Preparing deployment...")

        log_placeholder_execution(
            agent_name=metadata.get('name', 'DevOps & Release'),
            input_path=str(input_p),
            output_path=str(output_p),
        )

        record_execution_state(
            agent_id=metadata.get('id', 'devops_release'),
            input_signature=input_signature,
            input_path=input_p,
            output_path=output_p,
        )
        self.logger.info("DevOps & Release workflow completed")

        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='DevOps & Release Agent - Build and release orchestration',
    )
    parser.add_argument('--input', type=str, help='Path to stage input artifacts')
    parser.add_argument('--output', type=str, help='Path to stage output artifacts')
    args = parser.parse_args()

    agent = DevOpsReleaseAgent()
    success = agent.run(input_path=args.input, output_path=args.output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
