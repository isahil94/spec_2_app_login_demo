"""
Orchestration Package

Coordinates the Agentic SDLC workflow execution.

Components:
- workflow: State management, execution, logging, coordination
- artifact: Artifact management
- approval: Approval checkpoint management
- observability: Monitoring and metrics
"""

from orchestration.approval.approval_manager import ApprovalManager
from orchestration.artifact.artifact_manager import ArtifactManager
from orchestration.workflow.executor import ExecutionEngine
from orchestration.workflow.logging import ExecutionLogger
from orchestration.workflow.state import StageStatus, WorkflowStage, WorkflowState

__all__ = [
    "WorkflowState",
    "WorkflowStage",
    "StageStatus",
    "ExecutionEngine",
    "ArtifactManager",
    "ApprovalManager",
    "ExecutionLogger",
]
