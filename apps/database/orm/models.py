import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    TEAM_LEAD = "TEAM_LEAD"
    TEAM_MEMBER = "TEAM_MEMBER"


class AccountStatus(str, enum.Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    DELETED = "deleted"


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MembershipRole(str, enum.Enum):
    TEAM_LEAD = "TEAM_LEAD"
    TEAM_MEMBER = "TEAM_MEMBER"


class NotificationDeliveryChannel(str, enum.Enum):
    IN_APP = "in_app"
    EMAIL = "email"
    BOTH = "both"


class NotificationEventType(str, enum.Enum):
    TASK_ASSIGNED = "task_assigned"
    TASK_STATUS_CHANGED = "task_status_changed"
    COMMENT_ADDED = "comment_added"
    MENTIONED_IN_COMMENT = "mentioned_in_comment"
    TASK_ARCHIVED = "task_archived"


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(254), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    contact_information = Column(String(200), nullable=True)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.TEAM_MEMBER)
    account_status = Column(
        SQLEnum(AccountStatus), nullable=False, default=AccountStatus.ACTIVE
    )
    theme = Column(String(10), nullable=False, default="system")
    language = Column(String(5), nullable=False, default="en")
    timezone = Column(String(50), nullable=False, default="UTC")
    notify_in_app = Column(Boolean, nullable=False, default=True)
    notify_email = Column(Boolean, nullable=False, default=False)
    privacy_preferences = Column(JSON, nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    account_locked_until = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    tasks_owned = relationship(
        "Task", back_populates="owner", foreign_keys="Task.owner_id"
    )
    tasks_assigned = relationship(
        "Task", back_populates="assignee", foreign_keys="Task.assignee_id"
    )
    comments = relationship("Comment", back_populates="author")
    notifications = relationship("Notification", back_populates="recipient")
    notification_preferences = relationship(
        "NotificationPreference", back_populates="user", uselist=False
    )
    teams = relationship("TeamMembership", back_populates="user")
    audit_entries = relationship("AuditEntry", back_populates="actor")


class Team(Base):
    __tablename__ = "teams"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    archived_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    owner = relationship("User", foreign_keys=[owner_id])
    members = relationship("TeamMembership", back_populates="team")
    tasks = relationship("Task", back_populates="team")

    __table_args__ = (
        Index("ix_teams_owner_id", "owner_id"),
        Index("ux_teams_name_owner", "owner_id", "name", unique=True),
    )


class TeamMembership(Base):
    __tablename__ = "team_membership"

    team_id = Column(String(36), ForeignKey("teams.id"), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    role = Column(
        SQLEnum(MembershipRole), nullable=False, default=MembershipRole.TEAM_MEMBER
    )
    joined_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="teams")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    description = Column(String(2000), nullable=True)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    priority = Column(
        SQLEnum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM
    )
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    assignee_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    team_id = Column(String(36), ForeignKey("teams.id"), nullable=True)
    due_date = Column(Date, nullable=True)
    version = Column(Integer, nullable=False, default=1)
    archived_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    owner = relationship("User", back_populates="tasks_owned", foreign_keys=[owner_id])
    assignee = relationship(
        "User", back_populates="tasks_assigned", foreign_keys=[assignee_id]
    )
    team = relationship("Team", back_populates="tasks")
    labels = relationship(
        "TaskLabel", back_populates="task", cascade="all, delete-orphan"
    )
    comments = relationship(
        "Comment", back_populates="task", cascade="all, delete-orphan"
    )
    attachments = relationship(
        "Attachment", back_populates="task", cascade="all, delete-orphan"
    )
    audit_entries = relationship(
        "AuditEntry", back_populates="task", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_tasks_owner_id", "owner_id"),
        Index("ix_tasks_assignee_id", "assignee_id"),
        Index("ix_tasks_team_id", "team_id"),
        Index("ix_tasks_status", "status"),
        Index("ix_tasks_priority", "priority"),
        Index("ix_tasks_due_date", "due_date"),
        Index("ix_tasks_archived_at", "archived_at"),
    )


class TaskLabel(Base):
    __tablename__ = "task_labels"

    task_id = Column(String(36), ForeignKey("tasks.id"), primary_key=True)
    label = Column(String(100), primary_key=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    task = relationship("Task", back_populates="labels")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=False, index=True)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    edit_history = Column(JSON, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)
    edited_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="comments", foreign_keys=[author_id])


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=False, index=True)
    uploader_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(1000), nullable=False)
    mime_type = Column(String(100), nullable=True)
    file_size = Column(Integer, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    task = relationship("Task", back_populates="attachments")
    uploader = relationship("User")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    recipient_id = Column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )
    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=True, index=True)
    actor_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    event_type = Column(SQLEnum(NotificationEventType), nullable=False)
    title = Column(String(100), nullable=False)
    message = Column(String(500), nullable=False)
    delivery_channel = Column(
        SQLEnum(NotificationDeliveryChannel),
        nullable=False,
        default=NotificationDeliveryChannel.IN_APP,
    )
    read_at = Column(DateTime(timezone=True), nullable=True)
    dismissed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    expires_at = Column(DateTime(timezone=True), nullable=True)

    recipient = relationship(
        "User", back_populates="notifications", foreign_keys=[recipient_id]
    )
    task = relationship("Task")
    actor = relationship("User", foreign_keys=[actor_id])


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(
        String(36), ForeignKey("users.id"), nullable=False, unique=True, index=True
    )
    in_app_notifications = Column(Boolean, nullable=False, default=True)
    email_notifications = Column(Boolean, nullable=False, default=False)
    task_assigned = Column(Boolean, nullable=False, default=True)
    task_status_changed = Column(Boolean, nullable=False, default=True)
    comment_added = Column(Boolean, nullable=False, default=True)
    mentioned_in_comment = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="notification_preferences")


class AuditEntry(Base):
    __tablename__ = "audit_entries"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    entity_type = Column(String(50), nullable=False, index=True)
    entity_id = Column(String(36), nullable=False, index=True)
    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=True, index=True)
    action = Column(String(50), nullable=False, index=True)
    actor_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    success = Column(Boolean, nullable=False, default=True)
    error_message = Column(String(500), nullable=True)
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    task = relationship("Task", back_populates="audit_entries")
    actor = relationship("User", back_populates="audit_entries")
