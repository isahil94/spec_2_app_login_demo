"""
Approval Checkpoint System

Manages approval requests when a workflow stage is blocked.

Workflows emit approval requests that are stored for review.
Once approved, the workflow can resume from the blocked stage.
"""

import json
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class ApprovalStatus(Enum):
    """Status of an approval request"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ApprovalRequest:
    """Represents an approval request"""

    def __init__(
        self,
        approval_id: str,
        workflow_id: str,
        stage: str,
        blocker_report: str,
        blocker_type: str = "validation_failure",
        severity: str = "high",
        required_approval_roles: List[str] = None,
    ):
        self.approval_id = approval_id
        self.workflow_id = workflow_id
        self.stage = stage
        self.blocker_report = blocker_report
        self.blocker_type = blocker_type  # validation_failure, manual_review, etc.
        self.severity = severity  # low, medium, high, critical
        self.required_approval_roles = required_approval_roles or ["reviewer", "architect"]
        self.status = ApprovalStatus.PENDING
        self.created_at = datetime.now()
        self.expires_at = datetime.now() + timedelta(days=7)  # 7 day expiry
        self.approved_by = None
        self.approved_at = None
        self.approval_notes = None
        self.decision_notes = None

    def approve(self, approved_by: str, notes: str = ""):
        """Approve the request"""
        self.status = ApprovalStatus.APPROVED
        self.approved_by = approved_by
        self.approved_at = datetime.now()
        self.decision_notes = notes

    def reject(self, approved_by: str, notes: str = ""):
        """Reject the request"""
        self.status = ApprovalStatus.REJECTED
        self.approved_by = approved_by
        self.approved_at = datetime.now()
        self.decision_notes = notes

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "approval_id": self.approval_id,
            "workflow_id": self.workflow_id,
            "stage": self.stage,
            "blocker_report": self.blocker_report,
            "blocker_type": self.blocker_type,
            "severity": self.severity,
            "required_approval_roles": self.required_approval_roles,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "decision_notes": self.decision_notes,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ApprovalRequest":
        """Create from dictionary"""
        request = ApprovalRequest(
            approval_id=data["approval_id"],
            workflow_id=data["workflow_id"],
            stage=data["stage"],
            blocker_report=data["blocker_report"],
            blocker_type=data.get("blocker_type", "validation_failure"),
            severity=data.get("severity", "high"),
            required_approval_roles=data.get("required_approval_roles", []),
        )
        request.status = ApprovalStatus(data["status"])
        request.created_at = datetime.fromisoformat(data["created_at"])
        request.expires_at = datetime.fromisoformat(data["expires_at"])
        request.approved_by = data.get("approved_by")
        request.approved_at = datetime.fromisoformat(data["approved_at"]) if data.get("approved_at") else None
        request.decision_notes = data.get("decision_notes")
        return request


class ApprovalManager:
    """Manages approval requests throughout the workflow"""

    def __init__(self, approval_dir: Path = None):
        """Initialize approval manager"""
        self.approval_dir = approval_dir or Path("orchestration/approval")
        self.approval_dir.mkdir(parents=True, exist_ok=True)
        self.pending_dir = self.approval_dir / "pending"
        self.approved_dir = self.approval_dir / "approved"
        self.rejected_dir = self.approval_dir / "rejected"

        for dir_path in [self.pending_dir, self.approved_dir, self.rejected_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def create_approval_request(
        self,
        workflow_id: str,
        stage: str,
        blocker_report: str,
        blocker_type: str = "validation_failure",
        severity: str = "high",
        required_approval_roles: List[str] = None,
    ) -> ApprovalRequest:
        """Create and store an approval request"""
        approval_id = f"{workflow_id}-{stage}-{datetime.now().timestamp()}"

        request = ApprovalRequest(
            approval_id=approval_id,
            workflow_id=workflow_id,
            stage=stage,
            blocker_report=blocker_report,
            blocker_type=blocker_type,
            severity=severity,
            required_approval_roles=required_approval_roles or ["reviewer"],
        )

        # Save to pending
        self._save_request(request, self.pending_dir)

        return request

    def get_pending_approvals(self) -> List[ApprovalRequest]:
        """Get all pending approval requests"""
        requests = []
        for file_path in self.pending_dir.glob("*.json"):
            with open(file_path, "r") as f:
                data = json.load(f)
            requests.append(ApprovalRequest.from_dict(data))
        return sorted(requests, key=lambda r: r.created_at)

    def get_pending_approvals_for_workflow(self, workflow_id: str) -> List[ApprovalRequest]:
        """Get pending approvals for a specific workflow"""
        all_pending = self.get_pending_approvals()
        return [r for r in all_pending if r.workflow_id == workflow_id]

    def approve_request(self, approval_id: str, approved_by: str, notes: str = "") -> bool:
        """Approve a request"""
        request = self._load_request(approval_id, self.pending_dir)
        if not request:
            return False

        request.approve(approved_by, notes)
        self._move_request(request, self.pending_dir, self.approved_dir)
        return True

    def reject_request(self, approval_id: str, approved_by: str, notes: str = "") -> bool:
        """Reject a request"""
        request = self._load_request(approval_id, self.pending_dir)
        if not request:
            return False

        request.reject(approved_by, notes)
        self._move_request(request, self.pending_dir, self.rejected_dir)
        return True

    def is_approved(self, approval_id: str) -> bool:
        """Check if request is approved"""
        request = self._load_request(approval_id, self.approved_dir)
        return request is not None

    def is_rejected(self, approval_id: str) -> bool:
        """Check if request is rejected"""
        request = self._load_request(approval_id, self.rejected_dir)
        return request is not None

    def get_approval_summary(self) -> Dict[str, Any]:
        """Get summary of all approvals"""
        pending = self.get_pending_approvals()
        approved = self._load_all_requests(self.approved_dir)
        rejected = self._load_all_requests(self.rejected_dir)

        return {
            "generated_at": datetime.now().isoformat(),
            "pending_count": len(pending),
            "approved_count": len(approved),
            "rejected_count": len(rejected),
            "pending": [r.to_dict() for r in pending],
            "approved": [r.to_dict() for r in approved[-10:]],  # Last 10
            "rejected": [r.to_dict() for r in rejected[-10:]],  # Last 10
        }

    def _save_request(self, request: ApprovalRequest, directory: Path):
        """Save request to directory"""
        file_path = directory / f"{request.approval_id}.json"
        with open(file_path, "w") as f:
            json.dump(request.to_dict(), f, indent=2)

    def _load_request(self, approval_id: str, directory: Path) -> Optional[ApprovalRequest]:
        """Load request from directory"""
        file_path = directory / f"{approval_id}.json"
        if not file_path.exists():
            return None

        with open(file_path, "r") as f:
            data = json.load(f)

        return ApprovalRequest.from_dict(data)

    def _load_all_requests(self, directory: Path) -> List[ApprovalRequest]:
        """Load all requests from directory"""
        requests = []
        for file_path in directory.glob("*.json"):
            with open(file_path, "r") as f:
                data = json.load(f)
            requests.append(ApprovalRequest.from_dict(data))
        return requests

    def _move_request(self, request: ApprovalRequest, from_dir: Path, to_dir: Path):
        """Move request between directories"""
        old_file = from_dir / f"{request.approval_id}.json"
        new_file = to_dir / f"{request.approval_id}.json"

        if old_file.exists():
            old_file.rename(new_file)
        else:
            self._save_request(request, to_dir)
