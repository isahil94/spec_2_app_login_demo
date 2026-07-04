"""Collaboration and Reporting services."""

from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.models.models import Task, TaskStatus
from src.repositories.other_repositories import AuditRepository, CommentRepository
from src.repositories.task_repository import TaskRepository
from src.repositories.user_repository import UserRepository
from src.schemas.schemas import CommentDTO, UserDTO
from src.utils.exceptions import ForbiddenError, NotFoundError, ValidationError


class CollaborationService:
    """Service for task collaboration (comments, attachments)."""

    def __init__(self, session: Session):
        """Initialize collaboration service."""
        self.session = session
        self.comment_repo = CommentRepository(session)
        self.task_repo = TaskRepository(session)
        self.user_repo = UserRepository(session)
        self.audit_repo = AuditRepository(session)

    def add_comment(self, task_id: str, user_id: str, content: str) -> CommentDTO:
        """Add a comment to a task."""
        # Validate content
        if not content or len(content.strip()) == 0:
            raise ValidationError("Comment content cannot be empty")

        # Get task with visibility check
        task = self.task_repo.get_task_by_id(task_id, user_id)
        if not task:
            raise NotFoundError("Task not found or access denied")

        # Create comment
        comment = self.comment_repo.create_comment(task_id, user_id, content)

        # Log audit
        self.audit_repo.log_action(
            user_id, "comment_added", "comment", comment.id, task_id
        )

        return self._comment_to_dto(comment)

    def get_task_comments(
        self, task_id: str, user_id: str, skip: int = 0, limit: int = 20
    ) -> Tuple[List[CommentDTO], int]:
        """Get comments for a task."""
        # Check task access
        task = self.task_repo.get_task_by_id(task_id, user_id)
        if not task:
            raise NotFoundError("Task not found or access denied")

        # Get comments
        comments, total = self.comment_repo.get_task_comments(task_id, skip, limit)

        # Convert to DTOs
        comment_dtos = [self._comment_to_dto(comment) for comment in comments]

        return comment_dtos, total

    def update_comment(
        self, task_id: str, comment_id: str, user_id: str, content: str
    ) -> CommentDTO:
        """Update a comment."""
        # Validate content
        if not content or len(content.strip()) == 0:
            raise ValidationError("Comment content cannot be empty")

        # Get comment
        comment = self.comment_repo.get_by_id(comment_id)
        if not comment:
            raise NotFoundError("Comment not found")

        # Check authorization (author or admin)
        user = self.user_repo.get_by_id(user_id)
        if comment.author_id != user_id and user.role != "ADMIN":
            raise ForbiddenError("You can only edit your own comments")

        # Update comment
        comment.content = content
        comment.updated_at = datetime.now(timezone.utc)
        self.session.commit()
        self.session.refresh(comment)

        # Log audit
        self.audit_repo.log_action(
            user_id, "comment_updated", "comment", comment_id, task_id
        )

        return self._comment_to_dto(comment)

    def delete_comment(self, task_id: str, comment_id: str, user_id: str) -> bool:
        """Delete a comment."""
        # Get comment
        comment = self.comment_repo.get_by_id(comment_id)
        if not comment:
            raise NotFoundError("Comment not found")

        # Check authorization (author or admin)
        user = self.user_repo.get_by_id(user_id)
        if comment.author_id != user_id and user.role != "ADMIN":
            raise ForbiddenError("You can only delete your own comments")

        # Delete comment
        self.comment_repo.delete(comment_id)

        # Log audit
        self.audit_repo.log_action(
            user_id, "comment_deleted", "comment", comment_id, task_id
        )

        return True

    def _comment_to_dto(self, comment) -> CommentDTO:
        """Convert comment to DTO."""
        return CommentDTO(
            comment_id=comment.id,
            author=UserDTO(
                user_id=comment.author.id,
                email=comment.author.email,
                full_name=comment.author.full_name,
                role=comment.author.role,
                created_at=comment.author.created_at,
            ),
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )


class ReportingService:
    """Service for dashboard and reporting."""

    def __init__(self, session: Session):
        """Initialize reporting service."""
        self.session = session
        self.task_repo = TaskRepository(session)
        self.user_repo = UserRepository(session)

    def _get_date_series(self, days: int = 7) -> list[datetime]:
        """Create a list of dates ending today."""
        today = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        return [today - timedelta(days=i) for i in reversed(range(days))]

    def _count_tasks_by_date(
        self, tasks: list[Task], date_field: str
    ) -> dict[str, int]:
        """Count tasks grouped by date field."""
        counts: dict[str, int] = {}
        for task in tasks:
            task_date = getattr(task, date_field)
            if task_date:
                normalized_date = self._normalize_datetime(task_date)
                date_key = normalized_date.date().isoformat()
                counts[date_key] = counts.get(date_key, 0) + 1
        return counts

    def _normalize_datetime(self, value: datetime) -> datetime:
        """Normalize a datetime to UTC-aware form."""
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    def get_dashboard_metrics(self, user_id: str) -> dict:
        """Get dashboard metrics for a user."""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        now = datetime.now(timezone.utc)

        # Get user's tasks
        user_tasks, _ = self.task_repo.list_tasks(user_id, skip=0, limit=1000)

        total_tasks = len(user_tasks)
        completed_tasks = len(
            [t for t in user_tasks if t.status == TaskStatus.COMPLETED]
        )
        pending_tasks = total_tasks - completed_tasks

        # Get overdue tasks
        overdue_tasks = len(
            [
                t
                for t in user_tasks
                if t.due_date
                and self._normalize_datetime(t.due_date) < now
                and t.status != TaskStatus.COMPLETED
            ]
        )

        # Get due today tasks
        due_today_tasks = len(
            [
                t
                for t in user_tasks
                if t.due_date
                and self._normalize_datetime(t.due_date).date() == now.date()
                and t.status != TaskStatus.COMPLETED
            ]
        )

        # Build activity metrics
        date_series = self._get_date_series(days=7)
        daily_counts = self._count_tasks_by_date(user_tasks, "created_at")
        completed_counts = self._count_tasks_by_date(
            [t for t in user_tasks if t.status == TaskStatus.COMPLETED], "updated_at"
        )

        activity_series = [
            {
                "date": date.isoformat(),
                "created": daily_counts.get(date.date().isoformat(), 0),
                "completed": completed_counts.get(date.date().isoformat(), 0),
            }
            for date in date_series
        ]

        upcoming_tasks = sorted(
            [
                t
                for t in user_tasks
                if t.due_date
                and self._normalize_datetime(t.due_date) >= now
                and self._normalize_datetime(t.due_date) <= now + timedelta(days=7)
                and t.status != TaskStatus.COMPLETED
            ],
            key=lambda t: self._normalize_datetime(t.due_date),
        )[:5]

        upcoming_deadlines = []
        for task in upcoming_tasks:
            due_date = self._normalize_datetime(task.due_date)
            upcoming_deadlines.append(
                {
                    "task_id": task.id,
                    "title": task.title,
                    "due_date": due_date.isoformat(),
                    "when": due_date.date().isoformat(),
                    "status": task.status,
                }
            )

        recent_activity = [
            {
                "task_id": task.id,
                "title": task.title,
                "action": (
                    "Completed" if task.status == TaskStatus.COMPLETED else "Updated"
                ),
                "when": task.updated_at.isoformat(),
                "status": task.status,
            }
            for task in sorted(user_tasks, key=lambda t: t.updated_at, reverse=True)[:5]
        ]

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "overdue_tasks": overdue_tasks,
            "due_today_tasks": due_today_tasks,
            "completion_rate": round(
                (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2
            ),
            "activity_series": activity_series,
            "recent_activity": recent_activity,
            "upcoming_deadlines": upcoming_deadlines,
        }
