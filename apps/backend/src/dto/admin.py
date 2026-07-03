from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str = Field(min_length=1)


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class TeamCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=256)


class TeamResponse(BaseModel):
    id: int
    name: str
