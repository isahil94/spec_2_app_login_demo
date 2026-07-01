from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskSummary(BaseModel):
    task_id: str
    title: str
    status: str
    priority: str
    assignee_id: Optional[str] = None
    team_id: Optional[str] = None
    due_date: Optional[date] = None
    archived: bool
    updated_at: Optional[str] = None


class TaskDetail(TaskSummary):
    description: Optional[str] = None
    labels: Optional[List[str]] = []
    creator_id: str
    created_at: Optional[str] = None
    history_summary: Optional[str] = None
    comments_count: int = 0
    attachments: Optional[List[str]] = []


class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: str
    priority: str
    assignee_id: Optional[str] = None
    due_date: Optional[date] = None
    labels: Optional[List[str]] = []
    team_id: str
    attachments: Optional[List[str]] = []


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee_id: Optional[str] = None
    due_date: Optional[date] = None
    labels: Optional[List[str]] = None
    team_id: Optional[str] = None
    attachments: Optional[List[str]] = None


class TaskStatusUpdateRequest(BaseModel):
    status: str
    comment: Optional[str] = None
