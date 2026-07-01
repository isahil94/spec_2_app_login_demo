from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from apps.backend.db import get_db
from apps.backend.src.auth.security import get_current_user, require_role
from apps.backend.src.domain.models import Task, User
from apps.backend.src.dto.auth import (
    AuthRequest,
    AuthResponse,
    RecoverRequest,
    RegisterRequest,
    ResetRequest,
)
from apps.backend.src.dto.comment import CommentCreateRequest
from apps.backend.src.dto.project import ProjectCreateRequest, ProjectResponse
from apps.backend.src.dto.task import (
    TaskCreateRequest,
    TaskDetail,
    TaskStatusUpdateRequest,
    TaskSummary,
    TaskUpdateRequest,
)
from apps.backend.src.dto.team import TeamCreateRequest, TeamMembershipRequest
from apps.backend.src.dto.user import (
    ProfileUpdateRequest,
    SettingsUpdateRequest,
    UserProfileResponse,
)
from apps.backend.src.services.auth_service import (
    authenticate_user,
    create_token,
    register_user,
)
from apps.backend.src.services.comment_service import create_comment, list_comments
from apps.backend.src.services.notification_service import (
    list_notifications,
    mark_notification_read,
)
from apps.backend.src.services.project_service import create_project, get_project
from apps.backend.src.services.task_service import (
    archive_task,
    create_task,
    duplicate_task,
    get_task,
    list_tasks,
    restore_task,
    update_task,
    update_task_status,
)
from apps.backend.src.services.team_service import (
    add_team_member,
    create_team,
    get_team,
    list_teams,
    remove_team_member,
    update_team_member_role,
)
from apps.backend.src.services.user_service import (
    get_user_profile,
    update_profile,
    update_settings,
)

api_router = APIRouter()


@api_router.post("/auth/register", response_model=AuthResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    try:
        result = register_user(db, request.email, request.password, request.display_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result


@api_router.post("/auth/login", response_model=AuthResponse)
def login(request: AuthRequest, db: Session = Depends(get_db)):
    try:
        auth = authenticate_user(db, request.email, request.password)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    token_data = create_token(auth["user_id"], auth["roles"])
    return {
        "user_id": auth["user_id"],
        "email": auth["email"],
        "display_name": auth["display_name"],
        "token": token_data["token"],
        "expires_in": token_data["expires_in"],
        "roles": auth["roles"],
    }


@api_router.get("/users/me", response_model=UserProfileResponse)
def read_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_user_profile(db, current_user["user_id"])
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile


@api_router.put("/users/me", response_model=UserProfileResponse)
def update_profile_endpoint(
    request: ProfileUpdateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(id=current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return update_profile(db, user, request.model_dump(exclude_none=True))


@api_router.get("/users/settings", response_model=UserProfileResponse)
def read_settings(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_user_profile(db, current_user["user_id"])
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile


@api_router.put("/users/settings", response_model=UserProfileResponse)
def update_settings_endpoint(
    request: SettingsUpdateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(id=current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return update_settings(db, user, request.model_dump(exclude_none=True))


@api_router.get("/tasks")
def get_tasks(
    status: str | None = None,
    priority: str | None = None,
    assignee_id: str | None = None,
    team_id: str | None = None,
    db: Session = Depends(get_db),
):
    return list_tasks(db, {"status": status, "priority": priority, "assignee_id": assignee_id, "team_id": team_id})


@api_router.post("/tasks", response_model=TaskDetail)
def create_task_endpoint(
    request: TaskCreateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = request.model_dump()
    data["creator_id"] = current_user["user_id"]
    try:
        return create_task(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@api_router.get("/tasks/{task_id}", response_model=TaskDetail)
def get_task_endpoint(task_id: str, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@api_router.post("/projects", response_model=ProjectResponse)
def create_project_endpoint(request: ProjectCreateRequest, db: Session = Depends(get_db)):
    try:
        return create_project(db, request.name, request.description)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@api_router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project_endpoint(project_id: str, db: Session = Depends(get_db)):
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@api_router.post("/auth/recover")
def recover_password(request: RecoverRequest):
    return {"status": "ok", "message": "If the email exists, recovery instructions were sent."}


@api_router.post("/auth/reset")
def reset_password(request: ResetRequest):
    return {"status": "ok", "message": "Password reset completed."}


@api_router.put("/tasks/{task_id}", response_model=TaskDetail)
def update_task_endpoint(
    task_id: str,
    request: TaskUpdateRequest,
    db: Session = Depends(get_db),
):
    task_obj = db.query(Task).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        return update_task(db, task_obj, request.model_dump(exclude_none=True))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@api_router.post("/tasks/{task_id}/archive", response_model=TaskDetail)
def archive_task_endpoint(task_id: str, db: Session = Depends(get_db)):
    task_obj = db.query(Task).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    return archive_task(db, task_obj)


@api_router.post("/tasks/{task_id}/restore", response_model=TaskDetail)
def restore_task_endpoint(task_id: str, db: Session = Depends(get_db)):
    task_obj = db.query(Task).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    return restore_task(db, task_obj)


@api_router.post("/tasks/{task_id}/duplicate", response_model=TaskDetail)
def duplicate_task_endpoint(task_id: str, db: Session = Depends(get_db)):
    task_obj = db.query(Task).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    return duplicate_task(db, task_obj)


@api_router.post("/tasks/{task_id}/status", response_model=TaskDetail)
def update_task_status_endpoint(task_id: str, request: TaskStatusUpdateRequest, db: Session = Depends(get_db)):
    task_obj = db.query(Task).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        return update_task_status(db, task_obj, request.status, request.comment)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@api_router.get("/tasks/{task_id}/comments")
def get_comments(task_id: str, db: Session = Depends(get_db)):
    return list_comments(db, task_id)


@api_router.post("/tasks/{task_id}/comments")
def create_comment_endpoint(
    task_id: str,
    request: CommentCreateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task_obj = db.query(Task).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    return create_comment(db, task_obj, current_user["user_id"], request.content, request.mentions, request.attachments)


@api_router.get("/teams")
def get_all_teams(db: Session = Depends(get_db)):
    return list_teams(db)


@api_router.post("/teams")
def create_team_endpoint(request: TeamCreateRequest, db: Session = Depends(get_db)):
    return create_team(db, request.name, request.description, request.lead_user_id)


@api_router.get("/teams/{team_id}")
def get_team_endpoint(team_id: str, db: Session = Depends(get_db)):
    team = get_team(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@api_router.post("/teams/{team_id}/members")
def add_team_member_endpoint(request: TeamMembershipRequest, team_id: str, db: Session = Depends(get_db)):
    return add_team_member(db, team_id, request.user_id, request.role)


@api_router.put("/teams/{team_id}/members/{user_id}")
def update_team_member_endpoint(request: TeamMembershipRequest, team_id: str, user_id: str, db: Session = Depends(get_db)):
    return update_team_member_role(db, team_id, user_id, request.role)


@api_router.delete("/teams/{team_id}/members/{user_id}")
def remove_team_member_endpoint(team_id: str, user_id: str, db: Session = Depends(get_db)):
    return remove_team_member(db, team_id, user_id)


@api_router.get("/notifications")
def get_notifications(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return list_notifications(db, current_user["user_id"])


@api_router.post("/notifications/{notification_id}/read")
def mark_notification_read_endpoint(notification_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return mark_notification_read(db, notification_id, current_user["user_id"])
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@api_router.get("/dashboard")
def get_dashboard(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return {
        "totals": {},
        "overdue_count": 0,
        "upcoming_due_tasks": [],
        "completion_summary": {},
    }


@api_router.get("/reports")
def get_reports(team_id: str | None = None, from_date: str | None = None, to_date: str | None = None, type: str | None = None, db: Session = Depends(get_db)):
    return {"reports": [], "team_id": team_id, "from_date": from_date, "to_date": to_date, "type": type}


@api_router.get("/reports/team/{team_id}")
def get_team_report(team_id: str, db: Session = Depends(get_db)):
    return {"team_id": team_id, "workload": {}, "completion_metrics": {}}
