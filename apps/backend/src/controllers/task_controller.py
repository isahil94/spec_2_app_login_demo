from fastapi import APIRouter, Depends, HTTPException, Query, status

from apps.backend.src.db.database import SessionLocal
from apps.backend.src.dto.task import (
    TaskCreateRequest,
    TaskListResponse,
    TaskResponse,
    TaskUpdateRequest,
)
from apps.backend.src.middleware.auth import get_current_user
from apps.backend.src.services.task_service import (
    create_task,
    delete_task,
    get_task,
    list_tasks,
    update_task,
)

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create(payload: TaskCreateRequest, user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        task = create_task(db, owner_id=user.id, payload=payload.model_dump())
        return TaskResponse(**task.__dict__)
    finally:
        db.close()


@router.get("", response_model=TaskListResponse)
def list_all(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), user=Depends(get_current_user)):
    skip = (page - 1) * size
    db = SessionLocal()
    try:
        tasks, total = list_tasks(db, user_id=user.id, skip=skip, limit=size)
        return TaskListResponse(tasks=[TaskResponse(**task.__dict__) for task in tasks], total=total, page=page, size=size)
    finally:
        db.close()


@router.get("/{task_id}", response_model=TaskResponse)
def get_one(task_id: int, user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        task = get_task(db, task_id)
        if not task or task.owner_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return TaskResponse(**task.__dict__)
    finally:
        db.close()


@router.patch("/{task_id}", response_model=TaskResponse)
def update(task_id: int, payload: TaskUpdateRequest, user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        task = get_task(db, task_id)
        if not task or task.owner_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        task = update_task(db, task, payload.model_dump(exclude_none=True))
        return TaskResponse(**task.__dict__)
    finally:
        db.close()


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove(task_id: int, user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        task = get_task(db, task_id)
        if not task or task.owner_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        delete_task(db, task)
        return None
    finally:
        db.close()


@router.post("/{task_id}/archive", response_model=TaskResponse)
def archive(task_id: int, user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        task = get_task(db, task_id)
        if not task or task.owner_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        task = update_task(db, task, {"status": "archived"})
        return TaskResponse(**task.__dict__)
    finally:
        db.close()


@router.post("/{task_id}/restore", response_model=TaskResponse)
def restore(task_id: int, user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        task = get_task(db, task_id)
        if not task or task.owner_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        task = update_task(db, task, {"status": "todo"})
        return TaskResponse(**task.__dict__)
    finally:
        db.close()


@router.post("/{task_id}/duplicate", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def duplicate(task_id: int, user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        task = get_task(db, task_id)
        if not task or task.owner_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        payload = {
            "title": f"Copy of {task.title}",
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "due_date": task.due_date,
            "assignee_id": task.assignee_id,
        }
        duplicated = create_task(db, owner_id=user.id, payload=payload)
        return TaskResponse(**duplicated.__dict__)
    finally:
        db.close()
