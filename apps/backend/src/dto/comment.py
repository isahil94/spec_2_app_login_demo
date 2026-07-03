from datetime import datetime

from pydantic import BaseModel, Field


class CommentRequest(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class CommentResponse(BaseModel):
    id: int
    task_id: int
    author_id: int
    content: str
    created_at: datetime
