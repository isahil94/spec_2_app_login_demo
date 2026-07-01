import json
import uuid
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from apps.backend.src.domain.models import Comment, Notification, Task


def create_comment(db: Session, task: Task, author_id: str, content: str, mentions: List[str], attachments: List[str]) -> dict:
    comment_id = str(uuid.uuid4())
    comment = Comment(
        id=comment_id,
        task_id=task.id,
        author_id=author_id,
        content=content,
        mentions=json.dumps(mentions or []),
        attachments=json.dumps(attachments or []),
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    if mentions:
        for mention in mentions:
            notification = Notification(
                id=str(uuid.uuid4()),
                user_id=mention,
                type="mention",
                title="You were mentioned in a comment",
                message=f"You were mentioned in a comment on task {task.id}",
                related_task_id=task.id,
            )
            db.add(notification)
        db.commit()

    return {
        "comment_id": comment.id,
        "task_id": comment.task_id,
        "author_id": comment.author_id,
        "content": comment.content,
        "mentions": mentions,
        "attachments": attachments,
        "created_at": comment.created_at.isoformat(),
    }


def list_comments(db: Session, task_id: str) -> list[dict]:
    comments = db.query(Comment).filter(Comment.task_id == task_id).all()
    results = []
    for comment in comments:
        results.append(
            {
                "comment_id": comment.id,
                "task_id": comment.task_id,
                "author_id": comment.author_id,
                "content": comment.content,
                "mentions": json.loads(comment.mentions or "[]"),
                "attachments": json.loads(comment.attachments or "[]"),
                "created_at": comment.created_at.isoformat(),
            }
        )
    return results
