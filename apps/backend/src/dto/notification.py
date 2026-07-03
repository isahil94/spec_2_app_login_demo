from pydantic import BaseModel, Field


class NotificationPreferenceRequest(BaseModel):
    channel: str = Field(min_length=1, max_length=50)
    trigger: str = Field(min_length=1, max_length=100)
    enabled: bool


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    channel: str
    trigger: str
    enabled: bool
