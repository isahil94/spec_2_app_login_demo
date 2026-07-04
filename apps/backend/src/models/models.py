"""Domain models for the Task Management System."""

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db.database import Base


class TaskStatus(str, Enum):
    """Task status enum."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class TaskPriority(str, Enum):
    """Task priority enum."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class UserRole(str, Enum):
    """User role enum."""

    ADMIN = "ADMIN"
    TEAM_LEAD = "TEAM_LEAD"
    TEAM_MEMBER = "TEAM_MEMBER"


# Association table for team members
team_members = Table(
    "team_members",
    Base.metadata,
    Column("user_id", String(36), ForeignKey("users.id")),
    Column("team_id", String(36), ForeignKey("teams.id")),
)

# Association table for task history
task_history = Table(
    "task_history",
    Base.metadata,
    Column("id", String(36), primary_key=True),
    Column("task_id", String(36), ForeignKey("tasks.id")),
    Column("action", String(50)),
    Column("actor_id", String(36), ForeignKey("users.id")),
    Column("details", Text),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.TEAM_MEMBER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    contact_information = Column(Text, nullable=True)
    theme = Column(String(20), nullable=True)
    language = Column(String(32), nullable=True)
    timezone = Column(String(64), nullable=True)
    privacy = Column(String(32), nullable=True)
    notifications_in_app = Column(Boolean, nullable=True)
    notifications_email = Column(Boolean, nullable=True)

    # Relationships
    tasks_owned = relationship(
        "Task", back_populates="owner", foreign_keys="Task.owner_id"
    )
    tasks_assigned = relationship(
        "Task", back_populates="assignee", foreign_keys="Task.assignee_id"
    )
    comments = relationship("Comment", back_populates="author")
    teams = relationship("Team", secondary=team_members, back_populates="members")


class Team(Base):
    """Team model."""

    __tablename__ = "teams"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    members = relationship("User", secondary=team_members, back_populates="teams")
    tasks = relationship("Task", back_populates="team")


class Task(Base):
    """Task model."""

    __tablename__ = "tasks"
    __table_args__ = (
        Index("ix_task_owner_id", "owner_id"),
        Index("ix_task_assignee_id", "assignee_id"),
        Index("ix_task_status", "status"),
        Index("ix_task_team_id", "team_id"),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(
        SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False
    )
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    assignee_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    team_id = Column(String(36), ForeignKey("teams.id"), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    archived_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    owner = relationship("User", back_populates="tasks_owned", foreign_keys=[owner_id])
    assignee = relationship(
        "User", back_populates="tasks_assigned", foreign_keys=[assignee_id]
    )
    team = relationship("Team", back_populates="tasks")
    comments = relationship(
        "Comment", back_populates="task", cascade="all, delete-orphan"
    )
    audit_entries = relationship(
        "AuditEntry", back_populates="task", cascade="all, delete-orphan"
    )


class Comment(Base):
    """Comment model."""

    __tablename__ = "comments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=False, index=True)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="comments")


class Notification(Base):
    """Notification model."""

    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(
        String(50), nullable=False
    )  # task_created, task_assigned, comment_added, etc.
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class NotificationPreference(Base):
    """User notification preferences."""

    __tablename__ = "notification_preferences"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(
        String(36), ForeignKey("users.id"), nullable=False, unique=True, index=True
    )
    task_assigned = Column(Boolean, default=True)
    task_created = Column(Boolean, default=True)
    comment_added = Column(Boolean, default=True)
    task_completed = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class AuditEntry(Base):
    """Audit log entry (immutable)."""

    __tablename__ = "audit_entries"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)  # task, user, comment, etc.
    entity_id = Column(String(36), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relationships
    task = relationship("Task", back_populates="audit_entries")
