from typing import Optional

from pydantic import BaseModel, Field


class TeamSummary(BaseModel):
    team_id: str
    name: str
    description: Optional[str] = None
    lead_user_id: str


class TeamCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: Optional[str] = None
    lead_user_id: str


class TeamMembershipRequest(BaseModel):
    user_id: str
    role: str


class TeamMemberResponse(BaseModel):
    user_id: str
    role: str
