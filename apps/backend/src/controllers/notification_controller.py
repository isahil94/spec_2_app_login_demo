from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.src.core.models import Notification
from apps.backend.src.db.database import SessionLocal
from apps.backend.src.dto.notification import (
    NotificationPreferenceRequest,
    NotificationResponse,
)
from apps.backend.src.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1", tags=["notifications"])


@router.get("/notifications", response_model=list[NotificationResponse])
def list_notifications(user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        records = db.query(Notification).filter(Notification.user_id == user.id).all()
        return [NotificationResponse(**record.__dict__) for record in records]
    finally:
        db.close()


@router.patch("/notifications/preferences", response_model=NotificationResponse)
def update_preferences(payload: NotificationPreferenceRequest, user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        record = (
            db.query(Notification)
            .filter(Notification.user_id == user.id, Notification.channel == payload.channel, Notification.trigger == payload.trigger)
            .first()
        )
        if not record:
            record = Notification(user_id=user.id, channel=payload.channel, trigger=payload.trigger, enabled=payload.enabled)
        else:
            record.enabled = payload.enabled
        db.add(record)
        db.commit()
        db.refresh(record)
        return NotificationResponse(**record.__dict__)
    finally:
        db.close()
