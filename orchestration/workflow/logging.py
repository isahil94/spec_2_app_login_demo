"""
Execution Logging

Tracks all workflow execution events:
- Stage start/completion
- Artifact generation
- Approval requests
- Errors and blockers
- Performance metrics
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class EventType(Enum):
    """Types of workflow events"""
    WORKFLOW_STARTED = "workflow_started"
    STAGE_STARTED = "stage_started"
    STAGE_COMPLETED = "stage_completed"
    STAGE_FAILED = "stage_failed"
    ARTIFACT_GENERATED = "artifact_generated"
    APPROVAL_REQUESTED = "approval_requested"
    APPROVAL_APPROVED = "approval_approved"
    APPROVAL_REJECTED = "approval_rejected"
    WORKFLOW_BLOCKED = "workflow_blocked"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"


class WorkflowEvent:
    """Represents a workflow execution event"""

    def __init__(
        self,
        event_type: EventType,
        workflow_id: str,
        stage: Optional[str] = None,
        message: str = "",
        data: Optional[Dict[str, Any]] = None,
        severity: str = "info",
    ):
        self.event_id = f"{workflow_id}-{datetime.now().timestamp()}"
        self.event_type = event_type
        self.workflow_id = workflow_id
        self.stage = stage
        self.message = message
        self.data = data or {}
        self.severity = severity  # info, warning, error, critical
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "workflow_id": self.workflow_id,
            "stage": self.stage,
            "message": self.message,
            "severity": self.severity,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
        }

    def __str__(self) -> str:
        """String representation for logging"""
        timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        stage_str = f" [{self.stage}]" if self.stage else ""
        return f"{timestamp} {self.event_type.value}{stage_str}: {self.message}"


class ExecutionLogger:
    """Logs all workflow execution events"""

    def __init__(self, log_dir: Path = None):
        """Initialize logger"""
        self.log_dir = log_dir or Path("orchestration/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.events: List[WorkflowEvent] = []

    def log_event(
        self,
        event_type: EventType,
        workflow_id: str,
        stage: Optional[str] = None,
        message: str = "",
        data: Optional[Dict[str, Any]] = None,
        severity: str = "info",
    ) -> WorkflowEvent:
        """Log a workflow event"""
        event = WorkflowEvent(
            event_type=event_type,
            workflow_id=workflow_id,
            stage=stage,
            message=message,
            data=data,
            severity=severity,
        )

        self.events.append(event)
        self._write_event(event)
        self._print_event(event)

        return event

    def log_workflow_started(self, workflow_id: str, specification_file: str):
        """Log workflow start"""
        self.log_event(
            EventType.WORKFLOW_STARTED,
            workflow_id,
            message=f"Workflow started with specification: {specification_file}",
            data={"specification_file": specification_file},
        )

    def log_stage_started(self, workflow_id: str, stage: str):
        """Log stage start"""
        self.log_event(
            EventType.STAGE_STARTED,
            workflow_id,
            stage=stage,
            message=f"Starting stage: {stage}",
        )

    def log_stage_completed(
        self,
        workflow_id: str,
        stage: str,
        artifacts: List[str],
        duration_seconds: float,
    ):
        """Log stage completion"""
        self.log_event(
            EventType.STAGE_COMPLETED,
            workflow_id,
            stage=stage,
            message=f"Completed stage: {stage} ({duration_seconds:.2f}s)",
            data={
                "stage": stage,
                "artifacts": artifacts,
                "duration_seconds": duration_seconds,
            },
        )

    def log_stage_failed(
        self,
        workflow_id: str,
        stage: str,
        error: str,
        duration_seconds: float,
    ):
        """Log stage failure"""
        self.log_event(
            EventType.STAGE_FAILED,
            workflow_id,
            stage=stage,
            message=f"Failed stage: {stage} - {error}",
            data={
                "stage": stage,
                "error": error,
                "duration_seconds": duration_seconds,
            },
            severity="error",
        )

    def log_artifact_generated(
        self,
        workflow_id: str,
        stage: str,
        artifact_name: str,
        artifact_path: str,
    ):
        """Log artifact generation"""
        self.log_event(
            EventType.ARTIFACT_GENERATED,
            workflow_id,
            stage=stage,
            message=f"Generated artifact: {artifact_name}",
            data={
                "artifact_name": artifact_name,
                "artifact_path": artifact_path,
                "stage": stage,
            },
        )

    def log_approval_requested(
        self,
        workflow_id: str,
        stage: str,
        approval_id: str,
        blocker_report: str,
    ):
        """Log approval request"""
        self.log_event(
            EventType.APPROVAL_REQUESTED,
            workflow_id,
            stage=stage,
            message=f"Approval requested for stage: {stage}",
            data={
                "approval_id": approval_id,
                "stage": stage,
                "blocker_report_preview": blocker_report[:100],
            },
            severity="warning",
        )

    def log_approval_approved(
        self,
        workflow_id: str,
        stage: str,
        approval_id: str,
        approved_by: str,
    ):
        """Log approval"""
        self.log_event(
            EventType.APPROVAL_APPROVED,
            workflow_id,
            stage=stage,
            message=f"Approval granted for stage: {stage} by {approved_by}",
            data={
                "approval_id": approval_id,
                "stage": stage,
                "approved_by": approved_by,
            },
        )

    def log_approval_rejected(
        self,
        workflow_id: str,
        stage: str,
        approval_id: str,
        rejected_by: str,
    ):
        """Log approval rejection"""
        self.log_event(
            EventType.APPROVAL_REJECTED,
            workflow_id,
            stage=stage,
            message=f"Approval rejected for stage: {stage} by {rejected_by}",
            data={
                "approval_id": approval_id,
                "stage": stage,
                "rejected_by": rejected_by,
            },
            severity="error",
        )

    def log_workflow_blocked(
        self,
        workflow_id: str,
        stage: str,
        reason: str,
    ):
        """Log workflow blocked"""
        self.log_event(
            EventType.WORKFLOW_BLOCKED,
            workflow_id,
            stage=stage,
            message=f"Workflow blocked at stage: {stage}",
            data={"stage": stage, "reason": reason},
            severity="warning",
        )

    def log_workflow_completed(self, workflow_id: str, total_duration_seconds: float):
        """Log workflow completion"""
        self.log_event(
            EventType.WORKFLOW_COMPLETED,
            workflow_id,
            message=f"Workflow completed successfully ({total_duration_seconds:.2f}s)",
            data={"total_duration_seconds": total_duration_seconds},
        )

    def log_workflow_failed(self, workflow_id: str, reason: str):
        """Log workflow failure"""
        self.log_event(
            EventType.WORKFLOW_FAILED,
            workflow_id,
            message=f"Workflow failed: {reason}",
            data={"reason": reason},
            severity="critical",
        )

    def get_workflow_events(self, workflow_id: str) -> List[WorkflowEvent]:
        """Get all events for a workflow"""
        return [e for e in self.events if e.workflow_id == workflow_id]

    def get_stage_events(self, workflow_id: str, stage: str) -> List[WorkflowEvent]:
        """Get all events for a specific stage"""
        return [
            e for e in self.events
            if e.workflow_id == workflow_id and e.stage == stage
        ]

    def save_workflow_log(self, workflow_id: str) -> Path:
        """Save all events for a workflow to file"""
        events = self.get_workflow_events(workflow_id)
        log_file = self.log_dir / f"{workflow_id}-execution.jsonl"

        with open(log_file, "w") as f:
            for event in events:
                f.write(json.dumps(event.to_dict()) + "\n")

        return log_file

    def save_workflow_summary(self, workflow_id: str) -> Path:
        """Save summary of workflow execution"""
        events = self.get_workflow_events(workflow_id)

        summary = {
            "workflow_id": workflow_id,
            "generated_at": datetime.now().isoformat(),
            "total_events": len(events),
            "events_by_type": {},
            "events_by_stage": {},
            "critical_events": [],
            "timeline": [],
        }

        # Count by type
        for event_type in EventType:
            count = sum(1 for e in events if e.event_type == event_type)
            if count > 0:
                summary["events_by_type"][event_type.value] = count

        # Count by stage
        for event in events:
            if event.stage:
                if event.stage not in summary["events_by_stage"]:
                    summary["events_by_stage"][event.stage] = 0
                summary["events_by_stage"][event.stage] += 1

        # Critical events
        critical = [e for e in events if e.severity in ["error", "critical"]]
        summary["critical_events"] = [
            {
                "type": e.event_type.value,
                "stage": e.stage,
                "message": e.message,
                "timestamp": e.timestamp.isoformat(),
            }
            for e in critical
        ]

        # Timeline
        summary["timeline"] = [
            {
                "timestamp": e.timestamp.isoformat(),
                "event": e.event_type.value,
                "stage": e.stage,
                "message": e.message,
            }
            for e in events
        ]

        summary_file = self.log_dir / f"{workflow_id}-summary.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        return summary_file

    def _write_event(self, event: WorkflowEvent):
        """Write event to log file"""
        event_file = self.log_dir / f"{event.workflow_id}.jsonl"

        with open(event_file, "a") as f:
            f.write(json.dumps(event.to_dict()) + "\n")

    def _print_event(self, event: WorkflowEvent):
        """Print event to console"""
        # Color codes for terminal
        colors = {
            "info": "\033[94m",      # Blue
            "warning": "\033[93m",   # Yellow
            "error": "\033[91m",     # Red
            "critical": "\033[95m",  # Magenta
        }
        reset = "\033[0m"

        color = colors.get(event.severity, reset)
        print(f"{color}{event}{reset}")
