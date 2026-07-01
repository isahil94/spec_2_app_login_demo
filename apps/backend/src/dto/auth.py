from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class AuthRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    remember_me: Optional[bool] = False


class RegisterRequest(AuthRequest):
    display_name: str = Field(min_length=1, max_length=100)


class RecoverRequest(BaseModel):
    email: EmailStr


class ResetRequest(BaseModel):
    token: str = Field(min_length=1)
    new_password: str = Field(min_length=8)


class AuthResponse(BaseModel):
    user_id: str
    email: EmailStr
    display_name: str
    token: str
    expires_in: int
    roles: Optional[list[str]] = []
