from typing import List

from sqlalchemy.orm import Session

from apps.backend.src.domain.models import Notification


def list_notifications(db: Session, user_id: str) -> dict:
    items = db.query(Notification).filter(Notification.user_id == user_id).all()
    return {
        "items": [
            {
                "notification_id": notification.id,
                "type": notification.type,
                "title": notification.title,
                "message": notification.message,
                "created_at": notification.created_at.isoformat(),
                "read": notification.read,
                "related_task_id": notification.related_task_id,
            }
            for notification in items
        ],
        "unread_count": sum(1 for notification in items if not notification.read),
    }


def mark_notification_read(db: Session, notification_id: str, user_id: str) -> dict:
    notification = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()
    if not notification:
        raise ValueError("Notification not found")
    notification.read = True
    db.commit()
    return {
        "notification_id": notification.id,
        "status": "read",
    }
