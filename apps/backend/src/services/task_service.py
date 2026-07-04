"""Task management service."""

import json
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from src.models.models import Task, TaskStatus, User
from src.repositories.other_repositories import AuditRepository, CommentRepository
from src.repositories.task_repository import TaskRepository
from src.repositories.user_repository import UserRepository
from src.schemas.schemas import TaskCreate, TaskDTO, TaskUpdate
from src.utils.exceptions import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnprocessableError,
    ValidationError,
)


class TaskService:
    """Service for task management."""

    @staticmethod
    def _normalize_due_date(due_date: Optional[datetime]) -> Optional[datetime]:
        if due_date is None:
            return None
        if due_date.tzinfo is None:
            return due_date.replace(tzinfo=timezone.utc)
        return due_date.astimezone(timezone.utc)

    def __init__(self, session: Session):
        """Initialize task service."""
        self.session = session
        self.task_repo = TaskRepository(session)
        self.user_repo = UserRepository(session)
        self.comment_repo = CommentRepository(session)
        self.audit_repo = AuditRepository(session)

    def create_task(self, user_id: str, task_create: TaskCreate) -> TaskDTO:
        """Create a new task."""
        # Validate user exists
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        normalized_due_date = self._normalize_due_date(task_create.due_date)

        # Validate input
        if not task_create.title or len(task_create.title) > 100:
            raise ValidationError("Title is required and must be <= 100 characters")

        if task_create.description and len(task_create.description) > 2000:
            raise ValidationError("Description must be <= 2000 characters")

        # BR-007: Validate status
        valid_statuses = {
            TaskStatus.TODO,
            TaskStatus.IN_PROGRESS,
            TaskStatus.REVIEW,
            TaskStatus.COMPLETED,
            TaskStatus.BLOCKED,
        }
        if task_create.status not in valid_statuses:
            raise ValidationError(f"Invalid status: {task_create.status}")

        # Validate assignee if provided
        if task_create.assignee_id:
            assignee = self.user_repo.get_by_id(task_create.assignee_id)
            if not assignee:
                raise ValidationError("Assignee not found")

        # Create task
        task = self.task_repo.create_task(
            title=task_create.title,
            description=task_create.description,
            status=task_create.status,
            priority=task_create.priority,
            owner_id=user_id,
            assignee_id=task_create.assignee_id,
            due_date=normalized_due_date,
            team_id=task_create.team_id,
        )

        # Log audit
        self.audit_repo.log_action(user_id, "task_created", "task", task.id, task.id)

        return self._task_to_dto(task)

    def get_task(self, task_id: str, user_id: str) -> TaskDTO:
        """Get task by ID with visibility check."""
        task = self.task_repo.get_task_by_id(task_id, user_id)
        if not task:
            raise NotFoundError("Task not found or access denied")

        return self._task_to_dto(task)

    def update_task(
        self, task_id: str, user_id: str, task_update: TaskUpdate
    ) -> TaskDTO:
        """Update task."""
        # Get task with visibility check
        task = self.task_repo.get_task_by_id(task_id, user_id)
        if not task:
            raise NotFoundError("Task not found or access denied")

        # Get user for role check
        user = self.user_repo.get_by_id(user_id)

        # Check authorization: owner, assignee, or admin
        is_authorized = (
            user.role == "ADMIN"
            or task.owner_id == user_id
            or task.assignee_id == user_id
        )
        if not is_authorized:
            raise ForbiddenError("You do not have permission to update this task")

        # BR-004: Check if task is completed (only admin can edit)
        if task.status == TaskStatus.COMPLETED and user.role != "ADMIN":
            raise ForbiddenError("Cannot edit completed tasks")

        # BR-003: Check if task is archived (only admin can edit)
        if task.archived_at is not None and user.role != "ADMIN":
            raise ForbiddenError("Cannot edit archived tasks")

        # Validate updates
        if task_update.title is not None:
            if not task_update.title or len(task_update.title) > 100:
                raise ValidationError("Title must be between 1 and 100 characters")

        if task_update.description is not None:
            if len(task_update.description) > 2000:
                raise ValidationError("Description must be <= 2000 characters")

        normalized_due_date = self._normalize_due_date(task_update.due_date)

        # BR-006: Validate due date
        if normalized_due_date is not None:
            now = datetime.now(timezone.utc)
            if normalized_due_date < now:
                raise ValidationError("Due date cannot be in the past")

        # BR-007: Validate status transition
        if task_update.status is not None:
            valid_statuses = {
                TaskStatus.TODO,
                TaskStatus.IN_PROGRESS,
                TaskStatus.REVIEW,
                TaskStatus.COMPLETED,
                TaskStatus.BLOCKED,
            }
            if task_update.status not in valid_statuses:
                raise ValidationError(f"Invalid status: {task_update.status}")

        # Validate assignee if provided
        if task_update.assignee_id is not None:
            if (
                task_update.assignee_id
            ):  # Only validate if not None (not clearing assignee)
                assignee = self.user_repo.get_by_id(task_update.assignee_id)
                if not assignee:
                    raise ValidationError("Assignee not found")

        # Track changes for audit
        changes = {}
        for field in [
            "title",
            "description",
            "status",
            "priority",
            "assignee_id",
            "due_date",
        ]:
            new_value = getattr(task_update, field, None)
            if field == "due_date":
                new_value = normalized_due_date
            if new_value is not None:
                old_value = getattr(task, field)
                if old_value != new_value:
                    changes[field] = {"from": str(old_value), "to": str(new_value)}
                    setattr(task, field, new_value)

        # Update task
        task.updated_at = datetime.now(timezone.utc)
        self.session.commit()
        self.session.refresh(task)

        # Log audit with changes
        if changes:
            self.audit_repo.log_action(
                user_id, "task_updated", "task", task.id, task.id, json.dumps(changes)
            )

        return self._task_to_dto(task)

    def delete_task(self, task_id: str, user_id: str) -> bool:
        """Delete task (admin only - BR-002)."""
        # Get user
        user = self.user_repo.get_by_id(user_id)
        if not user or user.role != "ADMIN":
            raise ForbiddenError("Only administrators can delete tasks")

        # Get task
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")

        # Delete task
        self.task_repo.delete(task_id)

        # Log audit
        self.audit_repo.log_action(user_id, "task_deleted", "task", task_id, task_id)

        return True

    def archive_task(self, task_id: str, user_id: str) -> TaskDTO:
        """Archive a task (BR-003)."""
        # Get task with visibility check
        task = self.task_repo.get_task_by_id(task_id, user_id)
        if not task:
            raise NotFoundError("Task not found or access denied")

        # Get user
        user = self.user_repo.get_by_id(user_id)

        # Check authorization
        is_authorized = user.role == "ADMIN" or task.owner_id == user_id
        if not is_authorized:
            raise ForbiddenError("You do not have permission to archive this task")

        # Archive task
        task = self.task_repo.archive_task(task_id)

        # Log audit
        self.audit_repo.log_action(user_id, "task_archived", "task", task_id, task_id)

        return self._task_to_dto(task)

    def restore_task(self, task_id: str, user_id: str) -> TaskDTO:
        """Restore an archived task."""
        # Get user
        user = self.user_repo.get_by_id(user_id)

        # Get task (bypass normal visibility for restore)
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")

        # Check authorization
        is_authorized = user.role == "ADMIN" or task.owner_id == user_id
        if not is_authorized:
            raise ForbiddenError("You do not have permission to restore this task")

        # Restore task
        task = self.task_repo.restore_task(task_id)

        # Log audit
        self.audit_repo.log_action(user_id, "task_restored", "task", task_id, task_id)

        return self._task_to_dto(task)

    def duplicate_task(self, task_id: str, user_id: str) -> TaskDTO:
        """Create a duplicate of a task."""
        # Get task with visibility check
        task = self.task_repo.get_task_by_id(task_id, user_id)
        if not task:
            raise NotFoundError("Task not found or access denied")

        # Create duplicate
        new_task = self.task_repo.create_task(
            title=f"Copy of {task.title}",
            description=task.description,
            status=TaskStatus.TODO,
            priority=task.priority,
            owner_id=user_id,
            assignee_id=None,  # Clear assignee on duplicate
            due_date=task.due_date,
            team_id=task.team_id,
        )

        # Log audit
        self.audit_repo.log_action(
            user_id,
            "task_duplicated",
            "task",
            new_task.id,
            new_task.id,
            json.dumps({"original_task_id": task_id}),
        )

        return self._task_to_dto(new_task)

    def list_tasks(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee_id: Optional[str] = None,
        owner_id: Optional[str] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
        archived: Optional[bool] = False,
        sort_by: str = "recently_updated",
        order: str = "desc",
    ) -> Tuple[List[TaskDTO], int]:
        """List tasks with filtering."""
        tasks, total = self.task_repo.list_tasks(
            user_id=user_id,
            skip=skip,
            limit=limit,
            search=search,
            status=status,
            priority=priority,
            assignee_id=assignee_id,
            owner_id=owner_id,
            due_date_from=due_date_from,
            due_date_to=due_date_to,
            archived=archived,
            sort_by=sort_by,
            order=order,
        )

        # Convert to DTOs
        task_dtos = [self._task_to_dto(task) for task in tasks]

        return task_dtos, total

    def _task_to_dto(self, task: Task) -> TaskDTO:
        """Convert task to DTO."""
        from src.schemas.schemas import UserDTO

        return TaskDTO(
            task_id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            owner=UserDTO(
                user_id=task.owner.id,
                email=task.owner.email,
                full_name=task.owner.full_name,
                role=task.owner.role,
                created_at=task.owner.created_at,
            ),
            assignee=(
                UserDTO(
                    user_id=task.assignee.id,
                    email=task.assignee.email,
                    full_name=task.assignee.full_name,
                    role=task.assignee.role,
                    created_at=task.assignee.created_at,
                )
                if task.assignee
                else None
            ),
            due_date=task.due_date,
            archived_at=task.archived_at,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
