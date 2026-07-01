from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserProfileResponse(BaseModel):
    user_id: str
    email: EmailStr
    display_name: str
    roles: List[str]
    teams: List[str]
    preferences: dict


class ProfileUpdateRequest(BaseModel):
    display_name: Optional[str] = Field(default=None, max_length=100)
    avatar_url: Optional[str] = Field(default=None)
    time_zone: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)


class SettingsUpdateRequest(BaseModel):
    notification_preferences: Optional[dict] = None
    theme: Optional[str] = None
    time_zone: Optional[str] = None
    language: Optional[str] = None
