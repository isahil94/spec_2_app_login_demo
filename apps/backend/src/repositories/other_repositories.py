"""Comment, Team, Notification, and Audit repositories."""

from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session
from src.models.models import AuditEntry, Comment, Notification, Team
from src.repositories.base import BaseRepository


class CommentRepository(BaseRepository[Comment]):
    """Repository for Comment model."""

    def __init__(self, session: Session):
        """Initialize comment repository."""
        super().__init__(session, Comment)

    def create_comment(self, task_id: str, author_id: str, content: str) -> Comment:
        """Create a comment."""
        comment = Comment(task_id=task_id, author_id=author_id, content=content)
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def get_task_comments(
        self, task_id: str, skip: int = 0, limit: int = 20
    ) -> Tuple[List[Comment], int]:
        """Get comments for a task with pagination."""
        query = (
            self.session.query(Comment)
            .filter(Comment.task_id == task_id)
            .order_by(Comment.created_at.desc())
        )
        total = query.count()
        comments = query.offset(skip).limit(limit).all()
        return comments, total


class TeamRepository(BaseRepository[Team]):
    """Repository for Team model."""

    def __init__(self, session: Session):
        """Initialize team repository."""
        super().__init__(session, Team)

    def create_team(self, name: str, description: Optional[str] = None) -> Team:
        """Create a team."""
        team = Team(name=name, description=description)
        self.session.add(team)
        self.session.commit()
        self.session.refresh(team)
        return team

    def get_user_teams(self, user_id: str) -> List[Team]:
        """Get teams a user belongs to."""
        from src.models.models import User

        user = self.session.query(User).filter(User.id == user_id).first()
        return user.teams if user else []


class NotificationRepository(BaseRepository[Notification]):
    """Repository for Notification model."""

    def __init__(self, session: Session):
        """Initialize notification repository."""
        super().__init__(session, Notification)

    def create_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: str,
        task_id: Optional[str] = None,
    ) -> Notification:
        """Create a notification."""
        notification = Notification(
            user_id=user_id,
            task_id=task_id,
            title=title,
            message=message,
            notification_type=notification_type,
        )
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return notification

    def get_user_notifications(
        self, user_id: str, skip: int = 0, limit: int = 20
    ) -> Tuple[List[Notification], int]:
        """Get user notifications with pagination."""
        query = (
            self.session.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )
        total = query.count()
        notifications = query.offset(skip).limit(limit).all()
        return notifications, total

    def mark_as_read(self, notification_id: str) -> Optional[Notification]:
        """Mark notification as read."""
        notification = self.get_by_id(notification_id)
        if notification:
            notification.is_read = True
            self.session.commit()
            self.session.refresh(notification)
        return notification


class AuditRepository(BaseRepository[AuditEntry]):
    """Repository for Audit entries (immutable log)."""

    def __init__(self, session: Session):
        """Initialize audit repository."""
        super().__init__(session, AuditEntry)

    def log_action(
        self,
        user_id: str,
        action: str,
        entity_type: str,
        entity_id: str,
        task_id: Optional[str] = None,
        details: Optional[str] = None,
    ) -> AuditEntry:
        """Log an audit entry."""
        entry = AuditEntry(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            task_id=task_id,
            details=details,
        )
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return entry

    def get_task_history(self, task_id: str) -> List[AuditEntry]:
        """Get audit history for a task."""
        return (
            self.session.query(AuditEntry)
            .filter(AuditEntry.task_id == task_id)
            .order_by(AuditEntry.created_at.desc())
            .all()
        )
