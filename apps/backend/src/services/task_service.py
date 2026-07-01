import json
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from apps.backend.src.domain.models import Comment, Task

ALLOWED_STATUSES = ["Todo", "In Progress", "Review", "Completed", "Blocked"]
ALLOWED_PRIORITIES = ["Low", "Medium", "High", "Critical"]
STATUS_TRANSITIONS = {
    "Todo": ["In Progress", "Blocked"],
    "In Progress": ["Review", "Blocked", "Completed"],
    "Review": ["Completed", "Blocked"],
    "Blocked": ["Todo", "In Progress"],
    "Completed": [],
}


def serialize_list(text: Optional[str]) -> List[str]:
    if not text:
        return []
    try:
        return json.loads(text)
    except Exception:
        return [item.strip() for item in text.split(",") if item.strip()]


def serialize_json(text: Optional[str]) -> dict:
    if not text:
        return {}
    try:
        return json.loads(text)
    except Exception:
        return {}


def task_to_summary(task: Task) -> dict:
    return {
        "task_id": task.id,
        "title": task.title,
        "status": task.status,
        "priority": task.priority,
        "assignee_id": task.assignee_id,
        "team_id": task.team_id,
        "due_date": task.due_date,
        "archived": task.archived,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
    }


def task_to_detail(task: Task) -> dict:
    return {
        **task_to_summary(task),
        "description": task.description,
        "labels": serialize_list(task.labels),
        "creator_id": task.creator_id,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "history_summary": "",
        "comments_count": len(task.comments or []),
        "attachments": serialize_list(task.attachments),
    }


def create_task(db: Session, task_data: dict) -> dict:
    if task_data["status"] not in ALLOWED_STATUSES:
        raise ValueError("Invalid status")
    if task_data["priority"] not in ALLOWED_PRIORITIES:
        raise ValueError("Invalid priority")

    task_id = str(uuid.uuid4())
    task = Task(
        id=task_id,
        title=task_data["title"],
        description=task_data.get("description"),
        status=task_data["status"],
        priority=task_data["priority"],
        assignee_id=task_data.get("assignee_id"),
        team_id=task_data.get("team_id"),
        due_date=task_data.get("due_date").isoformat() if task_data.get("due_date") else None,
        labels=json.dumps(task_data.get("labels") or []),
        attachments=json.dumps(task_data.get("attachments") or []),
        archived=False,
        creator_id=task_data["creator_id"],
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task_to_detail(task)


def get_task(db: Session, task_id: str) -> Optional[dict]:
    task = db.query(Task).filter(Task.id == task_id).first()
    return task_to_detail(task) if task else None


def update_task(db: Session, task: Task, updates: dict) -> dict:
    if updates.get("status") and updates["status"] not in ALLOWED_STATUSES:
        raise ValueError("Invalid status")
    if updates.get("priority") and updates["priority"] not in ALLOWED_PRIORITIES:
        raise ValueError("Invalid priority")

    for field, value in updates.items():
        if value is None:
            continue
        if field == "labels":
            setattr(task, field, json.dumps(value))
        elif field == "attachments":
            setattr(task, field, json.dumps(value))
        elif field == "due_date":
            setattr(task, field, value.isoformat() if value else None)
        else:
            setattr(task, field, value)

    task.updated_at = datetime.utcnow()
    db.add(task)
    db.commit()
    db.refresh(task)
    return task_to_detail(task)


def archive_task(db: Session, task: Task) -> dict:
    task.archived = True
    db.add(task)
    db.commit()
    db.refresh(task)
    return task_to_detail(task)


def restore_task(db: Session, task: Task) -> dict:
    task.archived = False
    db.add(task)
    db.commit()
    db.refresh(task)
    return task_to_detail(task)


def duplicate_task(db: Session, task: Task) -> dict:
    duplicate_id = str(uuid.uuid4())
    duplicate = Task(
        id=duplicate_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        assignee_id=task.assignee_id,
        team_id=task.team_id,
        due_date=task.due_date,
        labels=task.labels,
        attachments=task.attachments,
        archived=False,
        creator_id=task.creator_id,
    )
    db.add(duplicate)
    db.commit()
    db.refresh(duplicate)
    return task_to_detail(duplicate)


def update_task_status(db: Session, task: Task, status: str, comment: str | None = None) -> dict:
    if status not in ALLOWED_STATUSES:
        raise ValueError("Invalid status")
    allowed = STATUS_TRANSITIONS.get(task.status, [])
    if status not in allowed and task.status != status:
        raise ValueError("Status transition not allowed")
    task.status = status
    task.updated_at = datetime.utcnow()
    db.add(task)
    db.commit()
    db.refresh(task)
    return task_to_detail(task)


def list_tasks(db: Session, filters: dict) -> dict:
    query = db.query(Task).filter(Task.archived == False)
    if filters.get("status"):
        query = query.filter(Task.status == filters["status"])
    if filters.get("priority"):
        query = query.filter(Task.priority == filters["priority"])
    if filters.get("team_id"):
        query = query.filter(Task.team_id == filters["team_id"])
    if filters.get("assignee_id"):
        query = query.filter(Task.assignee_id == filters["assignee_id"])
    tasks = query.all()
    return {
        "items": [task_to_summary(task) for task in tasks],
        "total_count": len(tasks),
        "page": 1,
        "page_size": len(tasks),
    }
