from datetime import datetime
from typing import Optional

from apps.backend.src.core.models import Task


def create_task(db, owner_id: int, payload: dict) -> Task:
    task = Task(
        title=payload["title"],
        description=payload.get("description"),
        priority=payload.get("priority", "medium"),
        status=payload.get("status", "todo"),
        assignee_id=payload.get("assignee_id"),
        owner_id=owner_id,
        due_date=payload.get("due_date"),
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks(db, user_id: int, skip: int = 0, limit: int = 20):
    query = db.query(Task).filter(Task.owner_id == user_id)
    total = query.count()
    tasks = query.offset(skip).limit(limit).all()
    return tasks, total


def update_task(db, task: Task, payload: dict):
    for key, value in payload.items():
        if hasattr(task, key) and value is not None:
            setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db, task: Task):
    db.delete(task)
    db.commit()
