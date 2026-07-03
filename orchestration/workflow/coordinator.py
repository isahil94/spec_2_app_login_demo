"""
Workflow Coordinator

Main orchestrator for the SDLC workflow.

Coordinates:
1. Reading the specification
2. Initializing workflow state
3. Executing stages in order
4. Tracking artifacts
5. Managing approvals
6. Producing logs and summaries

Does NOT perform AI reasoning - only coordinates execution.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from orchestration.approval.approval_manager import ApprovalManager
from orchestration.artifact.artifact_manager import ArtifactManager
from orchestration.workflow.executor import ExecutionEngine, ExecutionResult
from orchestration.workflow.logging import ExecutionLogger
from orchestration.workflow.state import StageStatus, WorkflowStage, WorkflowState


class WorkflowCoordinator:
    """Main workflow coordinator"""

    def __init__(
        self,
        project_root: Path = None,
        state_dir: Path = None,
        log_dir: Path = None,
    ):
        """Initialize coordinator"""
        self.project_root = project_root or Path.cwd()
        self.state_dir = state_dir or self.project_root / "memory" / "workflow"
        self.log_dir = log_dir or self.project_root / "orchestration" / "logs"

        # Initialize components
        self.artifact_manager = ArtifactManager(self.project_root / "artifacts")
        self.approval_manager = ApprovalManager(
            self.project_root / "orchestration" / "approval"
        )
        self.execution_engine = ExecutionEngine(self.project_root)
        self.logger = ExecutionLogger(self.log_dir)

        # Workflow state
        self.state: Optional[WorkflowState] = None
        self.specification: str = ""

    def initialize_workflow(self, spec_file: Path, workflow_id: str) -> WorkflowState:
        """Initialize a new workflow from specification"""
        # Read specification
        with open(spec_file, "r") as f:
            self.specification = f.read()

        # Create workflow state
        self.state = WorkflowState(
            workflow_id=workflow_id,
            specification_file=str(spec_file),
        )

        # Save initial state
        self.state.save(self.state_dir / f"{workflow_id}.json")

        # Log workflow start
        self.logger.log_workflow_started(workflow_id, str(spec_file))

        return self.state

    def resume_workflow(self, workflow_id: str) -> WorkflowState:
        """Resume a previously saved workflow"""
        state_file = self.state_dir / f"{workflow_id}.json"

        if not state_file.exists():
            raise FileNotFoundError(f"Workflow state not found: {workflow_id}")

        self.state = WorkflowState.load(state_file)

        # Load specification
        with open(self.state.specification_file, "r") as f:
            self.specification = f.read()

        return self.state

    def execute_workflow(self, max_stages: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute the complete workflow

        Args:
            max_stages: Maximum number of stages to execute (for testing)

        Returns:
            Workflow execution summary
        """
        if not self.state:
            raise RuntimeError(
                "Workflow not initialized. Call initialize_workflow first."
            )

        execution_results: list[ExecutionResult] = []
        stages_executed = 0

        # Get execution order
        stages_to_execute = [
            WorkflowStage.BUSINESS_ANALYST,
            WorkflowStage.SOLUTION_ARCHITECT,
            WorkflowStage.UI_UX_DEVELOPER,
            WorkflowStage.BACKEND_DEVELOPER,
            WorkflowStage.DATABASE_DEVELOPER,
            WorkflowStage.QA_ENGINEER,
            WorkflowStage.REVIEWER,
            WorkflowStage.DOCUMENTATION,
            WorkflowStage.DEVOPS,
        ]

        for stage in stages_to_execute:
            if max_stages and stages_executed >= max_stages:
                break

            # Check if stage is already completed
            if self.state.stages[stage].status == StageStatus.COMPLETED:
                continue

            # Execute stage
            result = self._execute_stage(stage)
            execution_results.append(result)
            stages_executed += 1

            # Check for blockers
            if not result.success:
                self.logger.log_stage_failed(
                    self.state.workflow_id,
                    stage.value,
                    result.error or "Unknown error",
                    result.duration_seconds or 0,
                )

                # Mark workflow blocked
                self.state.mark_stage_blocked(stage, result.error or "Execution failed")
                self.state.save(self.state_dir / f"{self.state.workflow_id}.json")

                return self._generate_summary(execution_results)

        # Mark workflow completed
        self.state.mark_workflow_completed()
        self.state.save(self.state_dir / f"{self.state.workflow_id}.json")

        self.logger.log_workflow_completed(
            self.state.workflow_id,
            self.state.total_duration_seconds or 0,
        )

        return self._generate_summary(execution_results)

    def execute_stage(self, stage: WorkflowStage) -> ExecutionResult:
        """Execute a single stage"""
        if not self.state:
            raise RuntimeError("Workflow not initialized")

        return self._execute_stage(stage)

    def request_approval(
        self,
        stage: WorkflowStage,
        blocker_report: str,
        blocker_type: str = "validation_failure",
    ):
        """Request approval for a blocked stage"""
        approval_request = self.approval_manager.create_approval_request(
            workflow_id=self.state.workflow_id,
            stage=stage.value,
            blocker_report=blocker_report,
            blocker_type=blocker_type,
        )

        self.logger.log_approval_requested(
            self.state.workflow_id,
            stage.value,
            approval_request.approval_id,
            blocker_report,
        )

        self.state.add_approval_request(stage, blocker_report)
        self.state.save(self.state_dir / f"{self.state.workflow_id}.json")

    def approve_stage(self, stage: WorkflowStage, approved_by: str) -> bool:
        """Approve a blocked stage"""
        if not self.state:
            return False

        stage_exec = self.state.stages[stage]

        # Find matching approval request
        for approval in self.state.approval_queue:
            if approval["stage"] == stage.value and approval["status"] == "pending":
                self.approval_manager.approve_request(
                    approval_id=f"{self.state.workflow_id}-{stage.value}-{approval['requested_at']}",
                    approved_by=approved_by,
                )
                approval["status"] = "approved"

                self.state.mark_stage_approved(stage, approved_by)
                self.state.save(self.state_dir / f"{self.state.workflow_id}.json")

                self.logger.log_approval_approved(
                    self.state.workflow_id,
                    stage.value,
                    f"{self.state.workflow_id}-{stage.value}",
                    approved_by,
                )

                return True

        return False

    def reject_stage(self, stage: WorkflowStage, rejected_by: str, reason: str) -> bool:
        """Reject a blocked stage"""
        if not self.state:
            return False

        # Find matching approval request
        for approval in self.state.approval_queue:
            if approval["stage"] == stage.value and approval["status"] == "pending":
                self.approval_manager.reject_request(
                    approval_id=f"{self.state.workflow_id}-{stage.value}-{approval['requested_at']}",
                    approved_by=rejected_by,
                    notes=reason,
                )
                approval["status"] = "rejected"

                self.state.save(self.state_dir / f"{self.state.workflow_id}.json")

                self.logger.log_approval_rejected(
                    self.state.workflow_id,
                    stage.value,
                    f"{self.state.workflow_id}-{stage.value}",
                    rejected_by,
                )

                return True

        return False

    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status"""
        if not self.state:
            return {}

        return {
            "workflow_id": self.state.workflow_id,
            "status": self.state.status.value,
            "current_stage": self.state.current_stage.value,
            "started_at": (
                self.state.started_at.isoformat() if self.state.started_at else None
            ),
            "updated_at": self.state.updated_at.isoformat(),
            "approval_queue": self.state.approval_queue,
            "blocked_reason": self.state.blocked_reason,
            "stages": {
                stage.value: {
                    "status": execution.status.value,
                    "duration_seconds": execution.duration_seconds,
                    "output_artifacts": execution.output_artifacts,
                }
                for stage, execution in self.state.stages.items()
            },
        }

    def save_execution_log(self) -> Path:
        """Save execution log"""
        if not self.state:
            raise RuntimeError("No active workflow")

        return self.logger.save_workflow_log(self.state.workflow_id)

    def save_execution_summary(self) -> Path:
        """Save execution summary"""
        if not self.state:
            raise RuntimeError("No active workflow")

        return self.logger.save_workflow_summary(self.state.workflow_id)

    def _execute_stage(self, stage: WorkflowStage) -> ExecutionResult:
        """Internal stage execution"""
        stage_name = stage.value

        # Log stage start
        self.logger.log_stage_started(self.state.workflow_id, stage_name)

        # Mark stage in progress
        stage_config = self.execution_engine.get_stage_config(stage_name)
        if stage_config:
            self.state.mark_stage_in_progress(stage, stage_config.chat_mode)

        # Collect input artifacts, including optional inputs when available.
        input_artifacts = {}
        if self.specification:
            input_artifacts["specification"] = self.specification
            input_artifacts["specs/specification"] = self.specification
            input_artifacts["specs/specification.md"] = self.specification

        if stage_config:
            for artifact_name in (
                stage_config.input_artifacts + stage_config.optional_input_artifacts
            ):
                content = self._load_artifact_content(artifact_name)
                if content:
                    input_artifacts[artifact_name] = content

        # Execute stage
        result = self.execution_engine.execute_stage(
            stage_name=stage_name,
            input_artifacts=input_artifacts,
            specification=self.specification,
        )

        # Process results
        if result.success:
            # Save generated artifacts
            for artifact_name in result.artifacts:
                artifact_path = (
                    artifact_name
                    if artifact_name.startswith("artifacts/")
                    else f"artifacts/{artifact_name}"
                )
                self.logger.log_artifact_generated(
                    self.state.workflow_id,
                    stage_name,
                    artifact_name,
                    artifact_path,
                )

            # Mark stage completed
            self.state.mark_stage_completed(stage, result.artifacts)

            self.logger.log_stage_completed(
                self.state.workflow_id,
                stage_name,
                result.artifacts,
                result.duration_seconds or 0,
            )
        else:
            # Handle failure
            error_msg = result.error or "Unknown error"
            self.state.mark_stage_blocked(stage, error_msg)

            # Request approval if configured
            if stage_config and stage_config.requires_approval:
                self.request_approval(
                    stage,
                    blocker_report=error_msg,
                    blocker_type="execution_failure",
                )

        # Save state
        self.state.save(self.state_dir / f"{self.state.workflow_id}.json")

        return result

    def _load_artifact_content(self, artifact_ref: str) -> Optional[str]:
        """Load artifact content by direct path token relative to artifacts root."""
        artifacts_root = self.project_root / "artifacts"
        normalized = artifact_ref.strip().replace("\\", "/")
        candidate = artifacts_root / normalized

        if candidate.is_dir():
            return f"[directory:{normalized}]"

        if candidate.exists() and candidate.is_file():
            try:
                return candidate.read_text(encoding="utf-8")
            except OSError:
                return None

        markdown_candidate = Path(str(candidate) + ".md")
        if markdown_candidate.exists() and markdown_candidate.is_file():
            try:
                return markdown_candidate.read_text(encoding="utf-8")
            except OSError:
                return None

        # If the artifact is the specification or a spec-relative asset, try the spec directory.
        spec_dir = None
        if self.state and self.state.specification_file:
            spec_dir = Path(self.state.specification_file).parent

        if spec_dir:
            candidate = spec_dir / normalized
            if candidate.exists() and candidate.is_file():
                try:
                    return candidate.read_text(encoding="utf-8")
                except OSError:
                    return None

            markdown_candidate = Path(str(candidate) + ".md")
            if markdown_candidate.exists() and markdown_candidate.is_file():
                try:
                    return markdown_candidate.read_text(encoding="utf-8")
                except OSError:
                    return None

        if (
            normalized.lower() in {"specification", "specification.md"}
            and self.specification
        ):
            return self.specification

        return None

    def _generate_summary(self, results: list[ExecutionResult]) -> Dict[str, Any]:
        """Generate workflow execution summary"""
        return {
            "workflow_id": self.state.workflow_id if self.state else None,
            "status": self.state.status.value if self.state else "unknown",
            "current_stage": self.state.current_stage.value if self.state else None,
            "total_stages_executed": len(results),
            "successful_stages": sum(1 for r in results if r.success),
            "failed_stages": sum(1 for r in results if not r.success),
            "execution_summary": self.execution_engine.get_execution_summary(results),
            "artifact_summary": self.artifact_manager.get_all_artifacts_summary(),
            "approval_summary": self.approval_manager.get_approval_summary(),
            "state": self.state.to_dict() if self.state else None,
        }
