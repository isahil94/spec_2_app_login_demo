from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.src.core.models import Comment, Task
from apps.backend.src.db.database import SessionLocal
from apps.backend.src.dto.comment import CommentRequest, CommentResponse
from apps.backend.src.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/tasks", tags=["comments"])


@router.post("/{task_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def add_comment(task_id: int, payload: CommentRequest, user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task or task.owner_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        comment = Comment(task_id=task_id, author_id=user.id, content=payload.content)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return CommentResponse(**comment.__dict__)
    finally:
        db.close()
