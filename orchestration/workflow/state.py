"""
Workflow State Management

Tracks the current state of the SDLC workflow, including:
- Current stage
- Stage status (pending, in-progress, completed, blocked)
- Artifact locations
- Approval requirements
- Execution history
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
import json
from pathlib import Path


class WorkflowStage(Enum):
    """SDLC workflow stages in execution order"""
    SPECIFICATION = "specification"
    BUSINESS_ANALYST = "business-analyst"
    SOLUTION_ARCHITECT = "solution-architect"
    UI_UX_DEVELOPER = "ui-ux-developer"
    BACKEND_DEVELOPER = "backend-developer"
    DATABASE_DEVELOPER = "database-developer"
    QA_ENGINEER = "qa-engineer"
    REVIEWER = "reviewer"
    DOCUMENTATION = "documentation"
    DEVOPS = "devops"
    COMPLETED = "completed"


class StageStatus(Enum):
    """Status of a workflow stage"""
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class StageExecution:
    """Tracks execution of a single workflow stage"""
    stage: WorkflowStage
    status: StageStatus = StageStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    chat_mode: Optional[str] = None
    input_artifacts: List[str] = field(default_factory=list)
    output_artifacts: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    requires_approval: bool = False
    approved_by: Optional[str] = None
    approval_time: Optional[datetime] = None
    notes: str = ""
    retries: int = 0
    max_retries: int = 3

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "stage": self.stage.value,
            "status": self.status.value,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "chat_mode": self.chat_mode,
            "input_artifacts": self.input_artifacts,
            "output_artifacts": self.output_artifacts,
            "error_message": self.error_message,
            "requires_approval": self.requires_approval,
            "approved_by": self.approved_by,
            "approval_time": self.approval_time.isoformat() if self.approval_time else None,
            "notes": self.notes,
            "retries": self.retries,
        }


@dataclass
class WorkflowState:
    """Complete workflow state"""
    workflow_id: str
    specification_file: str
    status: StageStatus = StageStatus.PENDING
    current_stage: WorkflowStage = WorkflowStage.SPECIFICATION
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_duration_seconds: Optional[float] = None
    stages: Dict[WorkflowStage, StageExecution] = field(default_factory=dict)
    approval_queue: List[Dict[str, Any]] = field(default_factory=list)
    blocked_reason: Optional[str] = None

    def __post_init__(self):
        """Initialize all stages"""
        if not self.stages:
            for stage in WorkflowStage:
                self.stages[stage] = StageExecution(stage=stage)

    def get_stage_execution(self, stage: WorkflowStage) -> StageExecution:
        """Get execution record for a stage"""
        return self.stages[stage]

    def mark_stage_in_progress(self, stage: WorkflowStage, chat_mode: str):
        """Mark stage as in-progress"""
        execution = self.stages[stage]
        execution.status = StageStatus.IN_PROGRESS
        execution.start_time = datetime.now()
        execution.chat_mode = chat_mode
        self.current_stage = stage
        self.status = StageStatus.IN_PROGRESS
        self.updated_at = datetime.now()
        if not self.started_at:
            self.started_at = datetime.now()

    def mark_stage_completed(self, stage: WorkflowStage, output_artifacts: List[str] = None):
        """Mark stage as completed"""
        execution = self.stages[stage]
        execution.status = StageStatus.COMPLETED
        execution.end_time = datetime.now()
        if execution.start_time:
            execution.duration_seconds = (
                execution.end_time - execution.start_time
            ).total_seconds()
        if output_artifacts:
            execution.output_artifacts = output_artifacts
        self.updated_at = datetime.now()

    def mark_stage_blocked(self, stage: WorkflowStage, reason: str, requires_approval: bool = True):
        """Mark stage as blocked"""
        execution = self.stages[stage]
        execution.status = StageStatus.BLOCKED
        execution.end_time = datetime.now()
        execution.error_message = reason
        execution.requires_approval = requires_approval
        self.blocked_reason = reason
        self.status = StageStatus.BLOCKED
        self.updated_at = datetime.now()

    def mark_stage_approved(self, stage: WorkflowStage, approved_by: str):
        """Mark stage as approved"""
        execution = self.stages[stage]
        execution.status = StageStatus.APPROVED
        execution.approved_by = approved_by
        execution.approval_time = datetime.now()
        self.blocked_reason = None
        self.updated_at = datetime.now()

    def add_approval_request(self, stage: WorkflowStage, blocker_report: str):
        """Add to approval queue"""
        self.approval_queue.append({
            "stage": stage.value,
            "requested_at": datetime.now().isoformat(),
            "blocker_report": blocker_report,
            "status": "pending",
        })

    def mark_workflow_completed(self):
        """Mark entire workflow as completed"""
        self.current_stage = WorkflowStage.COMPLETED
        self.status = StageStatus.COMPLETED
        self.completed_at = datetime.now()
        if self.started_at:
            self.total_duration_seconds = (
                self.completed_at - self.started_at
            ).total_seconds()
        self.updated_at = datetime.now()

    def get_next_stage(self) -> Optional[WorkflowStage]:
        """Get next stage to execute"""
        stages_order = list(WorkflowStage)
        current_index = stages_order.index(self.current_stage)
        if current_index < len(stages_order) - 1:
            return stages_order[current_index + 1]
        return None

    def is_workflow_complete(self) -> bool:
        """Check if workflow is complete"""
        return self.current_stage == WorkflowStage.COMPLETED

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "workflow_id": self.workflow_id,
            "specification_file": self.specification_file,
            "status": self.status.value,
            "current_stage": self.current_stage.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "total_duration_seconds": self.total_duration_seconds,
            "stages": {
                stage.value: execution.to_dict()
                for stage, execution in self.stages.items()
            },
            "approval_queue": self.approval_queue,
            "blocked_reason": self.blocked_reason,
        }

    def save(self, file_path: Path):
        """Persist state to file"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @staticmethod
    def load(file_path: Path) -> "WorkflowState":
        """Load state from file"""
        with open(file_path, "r") as f:
            data = json.load(f)

        state = WorkflowState(
            workflow_id=data["workflow_id"],
            specification_file=data["specification_file"],
            status=StageStatus[data["status"].upper()],
            current_stage=WorkflowStage(data["current_stage"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            started_at=datetime.fromisoformat(data["started_at"]) if data.get("started_at") else None,
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
            total_duration_seconds=data.get("total_duration_seconds"),
            approval_queue=data.get("approval_queue", []),
            blocked_reason=data.get("blocked_reason"),
        )

        # Restore stage executions
        for stage_name, stage_data in data["stages"].items():
            stage = WorkflowStage(stage_name)
            execution = StageExecution(
                stage=stage,
                status=StageStatus[stage_data["status"].upper()],
                start_time=datetime.fromisoformat(stage_data["start_time"]) if stage_data.get("start_time") else None,
                end_time=datetime.fromisoformat(stage_data["end_time"]) if stage_data.get("end_time") else None,
                duration_seconds=stage_data.get("duration_seconds"),
                chat_mode=stage_data.get("chat_mode"),
                input_artifacts=stage_data.get("input_artifacts", []),
                output_artifacts=stage_data.get("output_artifacts", []),
                error_message=stage_data.get("error_message"),
                requires_approval=stage_data.get("requires_approval", False),
                approved_by=stage_data.get("approved_by"),
                approval_time=datetime.fromisoformat(stage_data["approval_time"]) if stage_data.get("approval_time") else None,
                notes=stage_data.get("notes", ""),
                retries=stage_data.get("retries", 0),
            )
            state.stages[stage] = execution

        return state
