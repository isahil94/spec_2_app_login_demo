from typing import Optional

from pydantic import BaseModel, Field


class ProjectCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: Optional[str] = Field(default=None, max_length=1000)


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
