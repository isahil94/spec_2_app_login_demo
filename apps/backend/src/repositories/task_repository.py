"""Task repository for data access."""

from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from src.models.models import Task, TaskStatus
from src.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """Repository for Task model."""

    def __init__(self, session: Session):
        """Initialize task repository."""
        super().__init__(session, Task)

    def create_task(
        self,
        title: str,
        owner_id: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.TODO,
        priority: str = "medium",
        assignee_id: Optional[str] = None,
        due_date: Optional[datetime] = None,
        team_id: Optional[str] = None,
    ) -> Task:
        """Create a new task."""
        task = Task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            owner_id=owner_id,
            assignee_id=assignee_id,
            due_date=due_date,
            team_id=team_id,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

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
    ) -> Tuple[List[Task], int]:
        """List tasks with filtering and pagination."""
        # Build query
        query = self.session.query(Task)

        # Visibility filter: user sees own tasks, assigned tasks, or team tasks
        from src.models.models import User

        user = self.session.query(User).filter(User.id == user_id).first()
        if user and user.role == "ADMIN":
            # Admin sees all tasks
            pass
        else:
            # Non-admin sees their own, assigned, or team tasks
            query = query.filter(
                or_(
                    Task.owner_id == user_id,
                    Task.assignee_id == user_id,
                )
            )

        # Apply filters
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Task.title.ilike(search_term),
                    Task.description.ilike(search_term),
                )
            )

        if status:
            query = query.filter(Task.status == status)

        if priority:
            query = query.filter(Task.priority == priority)

        if assignee_id:
            query = query.filter(Task.assignee_id == assignee_id)

        if owner_id:
            query = query.filter(Task.owner_id == owner_id)

        if due_date_from:
            query = query.filter(Task.due_date >= due_date_from)

        if due_date_to:
            query = query.filter(Task.due_date <= due_date_to)

        # Archive filter
        if archived is False:
            query = query.filter(Task.archived_at == None)
        elif archived is True:
            query = query.filter(Task.archived_at != None)

        # Get total count
        total = query.count()

        # Apply sorting
        if sort_by == "due_date":
            query = query.order_by(
                Task.due_date.desc() if order == "desc" else Task.due_date.asc()
            )
        elif sort_by == "priority":
            # Assuming priority is stored as string, sort by custom order
            query = query.order_by(
                Task.priority.desc() if order == "desc" else Task.priority.asc()
            )
        elif sort_by == "status":
            query = query.order_by(
                Task.status.desc() if order == "desc" else Task.status.asc()
            )
        elif sort_by == "created_date":
            query = query.order_by(
                Task.created_at.desc() if order == "desc" else Task.created_at.asc()
            )
        else:  # recently_updated
            query = query.order_by(
                Task.updated_at.desc() if order == "desc" else Task.updated_at.asc()
            )

        # Apply pagination
        tasks = query.offset(skip).limit(limit).all()
        return tasks, total

    def get_task_by_id(self, task_id: str, user_id: str) -> Optional[Task]:
        """Get task by ID with visibility check."""
        from src.models.models import User

        user = self.session.query(User).filter(User.id == user_id).first()
        query = self.session.query(Task).filter(Task.id == task_id)

        # Check visibility
        if user and user.role != "ADMIN":
            query = query.filter(
                or_(
                    Task.owner_id == user_id,
                    Task.assignee_id == user_id,
                )
            )

        return query.first()

    def get_user_tasks(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        """Get tasks owned or assigned to user."""
        return (
            self.session.query(Task)
            .filter(
                or_(
                    Task.owner_id == user_id,
                    Task.assignee_id == user_id,
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_overdue_tasks(self) -> List[Task]:
        """Get overdue tasks."""
        from datetime import datetime, timezone

        return (
            self.session.query(Task)
            .filter(
                and_(
                    Task.due_date < datetime.now(timezone.utc),
                    Task.status != TaskStatus.COMPLETED,
                    Task.archived_at == None,
                )
            )
            .all()
        )

    def archive_task(self, task_id: str) -> Optional[Task]:
        """Archive a task."""
        from datetime import datetime, timezone

        task = self.get_by_id(task_id)
        if task:
            task.archived_at = datetime.now(timezone.utc)
            self.session.commit()
            self.session.refresh(task)
        return task

    def restore_task(self, task_id: str) -> Optional[Task]:
        """Restore an archived task."""
        task = self.get_by_id(task_id)
        if task:
            task.archived_at = None
            self.session.commit()
            self.session.refresh(task)
        return task
