from typing import List, Optional

from pydantic import BaseModel, Field


class CommentCreateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=1000)
    mentions: Optional[List[str]] = []
    attachments: Optional[List[str]] = []


class CommentResponse(BaseModel):
    comment_id: str
    task_id: str
    author_id: str
    content: str
    mentions: Optional[List[str]] = []
    attachments: Optional[List[str]] = []
    created_at: str
