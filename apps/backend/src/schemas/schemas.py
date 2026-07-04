"""Pydantic schemas for API requests/responses."""

from datetime import date, datetime, time, timezone
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.models.models import TaskPriority, TaskStatus, UserRole


# User Schemas
class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    """User creation schema."""

    password: str = Field(..., min_length=8)


class UserDTO(UserBase):
    """User DTO for responses."""

    user_id: str = Field(alias="id")
    role: UserRole
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class UserResponse(UserDTO):
    """User response schema."""

    pass


# Task Schemas
class TaskCreate(BaseModel):
    """Task creation schema."""

    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=2000)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee_id: Optional[str] = Field(None, alias="assigneeId")
    due_date: Optional[datetime] = Field(None, alias="dueDate")
    team_id: Optional[str] = Field(None, alias="teamId")

    model_config = {"populate_by_name": True}

    @field_validator("due_date", mode="before")
    @classmethod
    def normalize_due_date_value(cls, value):
        if value is None or isinstance(value, datetime):
            return value

        if isinstance(value, date):
            return datetime.combine(value, time.max, tzinfo=timezone.utc)

        if isinstance(value, str):
            text = value.strip()
            if not text:
                return None

            if "T" not in text and " " not in text and len(text) == 10:
                try:
                    parsed_date = date.fromisoformat(text)
                    return datetime.combine(parsed_date, time.max, tzinfo=timezone.utc)
                except ValueError:
                    pass

            try:
                parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    return parsed.replace(tzinfo=timezone.utc)
                return parsed
            except ValueError:
                return value

        return value


class TaskUpdate(BaseModel):
    """Task update schema."""

    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee_id: Optional[str] = Field(None, alias="assigneeId")
    due_date: Optional[datetime] = Field(None, alias="dueDate")

    model_config = {"populate_by_name": True}

    @field_validator("due_date", mode="before")
    @classmethod
    def normalize_due_date_value(cls, value):
        if value is None or isinstance(value, datetime):
            return value

        if isinstance(value, date):
            return datetime.combine(value, time.max, tzinfo=timezone.utc)

        if isinstance(value, str):
            text = value.strip()
            if not text:
                return None

            if "T" not in text and " " not in text and len(text) == 10:
                try:
                    parsed_date = date.fromisoformat(text)
                    return datetime.combine(parsed_date, time.max, tzinfo=timezone.utc)
                except ValueError:
                    pass

            try:
                parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    return parsed.replace(tzinfo=timezone.utc)
                return parsed
            except ValueError:
                return value

        return value


class TaskDTO(BaseModel):
    """Task DTO for responses."""

    task_id: str = Field(alias="id")
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    owner: UserDTO
    assignee: Optional[UserDTO] = None
    due_date: Optional[datetime]
    archived_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# Comment Schemas
class CommentCreate(BaseModel):
    """Comment creation schema."""

    content: str = Field(..., min_length=1)


class CommentDTO(BaseModel):
    """Comment DTO for responses."""

    comment_id: str = Field(alias="id")
    author: UserDTO
    content: str
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# Team Schemas
class TeamCreate(BaseModel):
    """Team creation schema."""

    name: str
    description: Optional[str] = None


class TeamDTO(BaseModel):
    """Team DTO for responses."""

    team_id: str = Field(alias="id")
    name: str
    description: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# Authentication Schemas
class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str
    remember_me: bool = False


class TokenResponse(BaseModel):
    """Token response schema."""

    token: str
    expires_in: int
    user: UserDTO


class RegisterRequest(BaseModel):
    """Registration request schema."""

    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., alias="fullName")

    model_config = {
        "populate_by_name": True,
    }


class ProfileUpdateRequest(BaseModel):
    """Profile update schema."""

    full_name: Optional[str] = Field(None, alias="fullName")
    contact_information: Optional[str] = Field(None, alias="contactInformation")

    model_config = {"populate_by_name": True}


class NotificationsUpdateRequest(BaseModel):
    """Notification update schema."""

    in_app: Optional[bool] = Field(None, alias="inApp")
    email: Optional[bool] = Field(None, alias="email")

    model_config = {"populate_by_name": True}


class Theme(str, Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class Privacy(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"


class SettingsUpdateRequest(BaseModel):
    """Settings update schema."""

    theme: Optional[Theme] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    privacy: Optional[Privacy] = None
    notifications: Optional[NotificationsUpdateRequest] = None

    model_config = {"populate_by_name": True}


class PasswordChangeRequest(BaseModel):
    """Password change schema."""

    current_password: str = Field(..., alias="currentPassword", min_length=8)
    new_password: str = Field(..., alias="newPassword", min_length=8)

    model_config = {"populate_by_name": True}


class RecoverPasswordRequest(BaseModel):
    """Password recovery request schema."""

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Password reset request schema."""

    token: str
    new_password: str = Field(..., min_length=8)


# Notification Schemas
class NotificationPreferenceDTO(BaseModel):
    """Notification preference DTO."""

    task_assigned: bool = True
    task_created: bool = True
    comment_added: bool = True
    task_completed: bool = True


class NotificationDTO(BaseModel):
    """Notification DTO."""

    notification_id: str = Field(alias="id")
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# Response Wrappers
class DataResponse(BaseModel):
    """Generic data response wrapper."""

    data: dict


class ListResponse(BaseModel):
    """List response wrapper."""

    data: dict
    pagination: Optional[dict] = None


class ErrorDetail(BaseModel):
    """Error detail schema."""

    field: Optional[str] = None
    issue: str


class ErrorResponse(BaseModel):
    """Error response schema."""

    code: str
    message: str
    details: Optional[List[ErrorDetail]] = None
    timestamp: datetime
    request_id: str
