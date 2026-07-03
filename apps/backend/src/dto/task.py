from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=256)
    description: Optional[str] = None
    priority: Optional[str] = Field(default="medium")
    status: Optional[str] = Field(default="todo")
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    assignee_id: Optional[int]
    owner_id: int
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int
    page: int
    size: int
