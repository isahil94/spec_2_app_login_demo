"""Main FastAPI application."""

import os
import sys
import uuid
from datetime import datetime, timezone
from typing import Optional

# Add backend directory to path so src can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import Body, Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.config.settings import settings
from src.db.database import get_db, init_db
from src.models.models import UserRole
from src.repositories.other_repositories import TeamRepository
from src.repositories.user_repository import UserRepository
from src.schemas.schemas import (
    CommentCreate,
    LoginRequest,
    PasswordChangeRequest,
    ProfileUpdateRequest,
    RegisterRequest,
    SettingsUpdateRequest,
    TaskCreate,
    TaskUpdate,
)
from src.services.auth_service import AuthService
from src.services.collaboration_service import CollaborationService, ReportingService
from src.services.task_service import TaskService
from src.utils.exceptions import (
    ApplicationError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)
from src.utils.jwt import decode_access_token
from src.utils.password import hash_password, verify_password

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
)

# Add CORS middleware
# Allow the local frontend origins used by the browser-based flows.
origins = [
    "http://localhost:3000",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4173",
    "http://127.0.0.1:4174",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get current user
async def get_current_user(
    authorization: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    """Get current authenticated user from JWT token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Missing or invalid authorization header"
        )

    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload["user_id"]


# Error handler
@app.exception_handler(ApplicationError)
async def application_error_handler(request, exc: ApplicationError):
    """Handle application errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "requestId": str(uuid.uuid4()),
            }
        },
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


# Auth endpoints
@app.post("/api/v1/auth/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        auth_service = AuthService(db)
        user = auth_service.register(request.email, request.password, request.full_name)
        return {
            "data": {
                "userId": user.user_id,
                "email": user.email,
                "fullName": user.full_name,
                "role": user.role,
                "createdAt": user.created_at,
            }
        }
    except ApplicationError as e:
        raise e


@app.post("/api/v1/auth/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return token."""
    try:
        auth_service = AuthService(db)
        token, expires_in, user = auth_service.login(request.email, request.password)
        return {
            "data": {
                "token": token,
                "expiresIn": expires_in,
                "user": {
                    "userId": user.user_id,
                    "email": user.email,
                    "fullName": user.full_name,
                    "role": user.role,
                },
            }
        }
    except ApplicationError as e:
        raise e


@app.get("/api/v1/users/{user_id}/profile")
async def get_user_profile(
    user_id: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a user's public profile data."""
    try:
        user_repo = UserRepository(db)
        profile_user = user_repo.get_by_id(user_id)
        if not profile_user:
            raise NotFoundError("User not found")
        if current_user != profile_user.id:
            raise ForbiddenError("You do not have access to this profile")

        return {
            "data": {
                "userId": profile_user.id,
                "fullName": profile_user.full_name,
                "email": profile_user.email,
                "contactInformation": profile_user.contact_information,
            }
        }
    except ApplicationError as e:
        raise e


@app.get("/api/v1/users")
async def list_active_users(
    current_user: str = Depends(get_current_user), db: Session = Depends(get_db)
):
    """List active users for task assignment."""
    try:
        user_repo = UserRepository(db)
        users = user_repo.get_active_users()
        return {
            "data": {
                "users": [
                    {
                        "userId": user.id,
                        "email": user.email,
                        "fullName": user.full_name,
                        "role": user.role,
                    }
                    for user in users
                ]
            }
        }
    except ApplicationError as e:
        raise e


@app.get("/api/v1/users/{user_id}/settings")
async def get_user_settings(
    user_id: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get the signed-in user's settings."""
    try:
        user_repo = UserRepository(db)
        profile_user = user_repo.get_by_id(user_id)
        if not profile_user:
            raise NotFoundError("User not found")
        if current_user != profile_user.id:
            raise ForbiddenError("You do not have access to this profile")

        return {
            "data": {
                "userId": profile_user.id,
                "theme": profile_user.theme or "system",
                "language": profile_user.language or "en",
                "timezone": profile_user.timezone or "UTC",
                "privacy": profile_user.privacy or "private",
                "notifications": {
                    "inApp": (
                        profile_user.notifications_in_app
                        if profile_user.notifications_in_app is not None
                        else True
                    ),
                    "email": (
                        profile_user.notifications_email
                        if profile_user.notifications_email is not None
                        else True
                    ),
                },
            }
        }
    except ApplicationError as e:
        raise e


@app.patch("/api/v1/users/{user_id}/profile")
async def update_user_profile(
    user_id: str,
    profile_data: ProfileUpdateRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update the signed-in user's profile data."""
    try:
        user_repo = UserRepository(db)
        profile_user = user_repo.get_by_id(user_id)
        if not profile_user:
            raise NotFoundError("User not found")
        if current_user != profile_user.id:
            raise ForbiddenError("You do not have access to this profile")

        if profile_data.full_name is not None:
            profile_user.full_name = profile_data.full_name
        if profile_data.contact_information is not None:
            profile_user.contact_information = profile_data.contact_information

        db.commit()
        db.refresh(profile_user)

        return {
            "data": {
                "userId": profile_user.id,
                "fullName": profile_user.full_name,
                "email": profile_user.email,
                "contactInformation": profile_user.contact_information,
            }
        }
    except ApplicationError as e:
        raise e


@app.patch("/api/v1/users/{user_id}/settings")
async def update_user_settings(
    user_id: str,
    settings_data: SettingsUpdateRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update the signed-in user's settings."""
    try:
        user_repo = UserRepository(db)
        profile_user = user_repo.get_by_id(user_id)
        if not profile_user:
            raise NotFoundError("User not found")
        if current_user != profile_user.id:
            raise ForbiddenError("You do not have access to this profile")

        if settings_data.theme is not None:
            profile_user.theme = settings_data.theme
        if settings_data.language is not None:
            profile_user.language = settings_data.language
        if settings_data.timezone is not None:
            profile_user.timezone = settings_data.timezone
        if settings_data.privacy is not None:
            profile_user.privacy = settings_data.privacy
        if settings_data.notifications is not None:
            if settings_data.notifications.in_app is not None:
                profile_user.notifications_in_app = settings_data.notifications.in_app
            if settings_data.notifications.email is not None:
                profile_user.notifications_email = settings_data.notifications.email

        db.commit()
        db.refresh(profile_user)

        return {
            "data": {
                "userId": profile_user.id,
                "theme": profile_user.theme or "system",
                "language": profile_user.language or "en",
                "timezone": profile_user.timezone or "UTC",
                "privacy": profile_user.privacy or "private",
                "notifications": {
                    "inApp": (
                        profile_user.notifications_in_app
                        if profile_user.notifications_in_app is not None
                        else True
                    ),
                    "email": (
                        profile_user.notifications_email
                        if profile_user.notifications_email is not None
                        else True
                    ),
                },
            }
        }
    except ApplicationError as e:
        raise e


@app.post("/api/v1/users/{user_id}/change-password")
async def change_user_password(
    user_id: str,
    password_data: PasswordChangeRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change the signed-in user's password."""
    try:
        user_repo = UserRepository(db)
        profile_user = user_repo.get_by_id(user_id)
        if not profile_user:
            raise NotFoundError("User not found")
        if current_user != profile_user.id:
            raise ForbiddenError("You do not have access to this profile")

        if not verify_password(
            password_data.current_password, profile_user.password_hash
        ):
            raise UnauthorizedError("Current password is incorrect")

        profile_user.password_hash = hash_password(password_data.new_password)
        db.commit()

        return {"data": {"message": "Password changed successfully"}}
    except ApplicationError as e:
        raise e


@app.post("/api/v1/auth/logout")
async def logout(
    current_user: str = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Logout user."""
    try:
        auth_service = AuthService(db)
        auth_service.logout(current_user)
        return {"data": {"message": "Logged out successfully"}}
    except ApplicationError as e:
        raise e


# Admin / User management endpoints (minimal implementations)
@app.post("/api/v1/admin/users/invite")
async def admin_invite_user(
    payload: dict = Body(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user_repo = UserRepository(db)
        invoker = user_repo.get_by_id(current_user)
        if not invoker or invoker.role != UserRole.ADMIN:
            raise ForbiddenError("Administrator privileges required")

        email = payload.get("email")
        full_name = (
            payload.get("fullName") or payload.get("full_name") or "Invited User"
        )
        role = payload.get("role") or UserRole.TEAM_MEMBER

        # Create with temporary password
        temp_pw = "TempInvitePass123!"
        pw_hash = hash_password(temp_pw)
        user = user_repo.create_user(email, pw_hash, full_name, role=role)

        return {
            "data": {
                "userId": user.id,
                "email": user.email,
                "fullName": user.full_name,
                "role": user.role,
            }
        }
    except ApplicationError as e:
        raise e


@app.patch("/api/v1/admin/users/{user_id}/disable")
async def admin_disable_user(
    user_id: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user_repo = UserRepository(db)
        invoker = user_repo.get_by_id(current_user)
        if not invoker or invoker.role != UserRole.ADMIN:
            raise ForbiddenError("Administrator privileges required")

        target = user_repo.get_by_id(user_id)
        if not target:
            raise NotFoundError("User not found")
        target.is_active = False
        db.commit()
        return {"data": {"userId": target.id, "isActive": target.is_active}}
    except ApplicationError as e:
        raise e


@app.patch("/api/v1/admin/users/{user_id}/enable")
async def admin_enable_user(
    user_id: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user_repo = UserRepository(db)
        invoker = user_repo.get_by_id(current_user)
        if not invoker or invoker.role != UserRole.ADMIN:
            raise ForbiddenError("Administrator privileges required")

        target = user_repo.get_by_id(user_id)
        if not target:
            raise NotFoundError("User not found")
        target.is_active = True
        db.commit()
        return {"data": {"userId": target.id, "isActive": target.is_active}}
    except ApplicationError as e:
        raise e


@app.delete("/api/v1/admin/users/{user_id}")
async def admin_delete_user(
    user_id: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user_repo = UserRepository(db)
        invoker = user_repo.get_by_id(current_user)
        if not invoker or invoker.role != UserRole.ADMIN:
            raise ForbiddenError("Administrator privileges required")

        deleted = user_repo.delete(user_id)
        if not deleted:
            raise NotFoundError("User not found")
        return {"data": {"deleted": True}}
    except ApplicationError as e:
        raise e


@app.post("/api/v1/admin/users/{user_id}/assign-role")
async def admin_assign_role(
    user_id: str,
    payload: dict = Body(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user_repo = UserRepository(db)
        invoker = user_repo.get_by_id(current_user)
        if not invoker or invoker.role != UserRole.ADMIN:
            raise ForbiddenError("Administrator privileges required")

        role = payload.get("role")
        target = user_repo.get_by_id(user_id)
        if not target:
            raise NotFoundError("User not found")
        target.role = role
        db.commit()
        db.refresh(target)
        return {"data": {"userId": target.id, "role": target.role}}
    except ApplicationError as e:
        raise e


@app.post("/api/v1/admin/teams/{team_id}/add-member")
async def admin_add_team_member(
    team_id: str,
    payload: dict = Body(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user_repo = UserRepository(db)
        team_repo = TeamRepository(db)
        invoker = user_repo.get_by_id(current_user)
        if not invoker or invoker.role != UserRole.ADMIN:
            raise ForbiddenError("Administrator privileges required")

        user_id = payload.get("userId")
        team = team_repo.get_by_id(team_id)
        user = user_repo.get_by_id(user_id)
        if not team or not user:
            raise NotFoundError("Team or user not found")
        team.members.append(user)
        db.commit()
        return {"data": {"teamId": team.id, "memberCount": len(team.members)}}
    except ApplicationError as e:
        raise e


# Teams endpoints
@app.post("/api/v1/teams")
async def create_team(
    payload: dict = Body(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        name = payload.get("name")
        description = payload.get("description")
        if not name:
            raise ValidationError("Team name is required")

        team_repo = TeamRepository(db)
        user_repo = UserRepository(db)
        team = team_repo.create_team(name, description)

        # Add creator as a member if user exists
        creator = user_repo.get_by_id(current_user)
        if creator:
            team.members.append(creator)
            db.commit()

        return {
            "data": {
                "teamId": team.id,
                "name": team.name,
                "description": team.description,
                "memberCount": len(team.members),
            }
        }
    except ApplicationError as e:
        raise e


@app.get("/api/v1/teams")
async def list_teams(
    current_user: str = Depends(get_current_user), db: Session = Depends(get_db)
):
    try:
        team_repo = TeamRepository(db)
        teams = team_repo.get_user_teams(current_user)

        return {
            "data": {
                "teams": [
                    {
                        "teamId": t.id,
                        "name": t.name,
                        "description": t.description,
                        "memberCount": len(t.members),
                        "members": [
                            {"userId": m.id, "email": m.email, "fullName": m.full_name}
                            for m in t.members
                        ],
                    }
                    for t in teams
                ]
            }
        }
    except ApplicationError as e:
        raise e


# Task endpoints
@app.post("/api/v1/tasks")
async def create_task(
    task_data: TaskCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new task."""
    try:
        task_service = TaskService(db)
        task = task_service.create_task(current_user, task_data)
        return {
            "data": {
                "taskId": task.task_id,
                "task_id": task.task_id,
                "id": task.task_id,
                "ownerId": task.owner.user_id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "owner": {
                    "userId": task.owner.user_id,
                    "user_id": task.owner.user_id,
                    "id": task.owner.user_id,
                    "email": task.owner.email,
                    "fullName": task.owner.full_name,
                },
                "assignee": (
                    {
                        "userId": task.assignee.user_id,
                        "user_id": task.assignee.user_id,
                        "id": task.assignee.user_id,
                        "email": task.assignee.email,
                        "fullName": task.assignee.full_name,
                    }
                    if task.assignee
                    else None
                ),
                "dueDate": task.due_date,
                "createdAt": task.created_at,
            }
        }
    except ApplicationError as e:
        raise e


@app.get("/api/v1/tasks")
async def list_tasks(
    search: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assignee: Optional[str] = None,
    owner: Optional[str] = None,
    archived: Optional[bool] = False,
    sort: str = "recently_updated",
    order: str = "desc",
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List tasks with filtering and pagination."""
    try:
        task_service = TaskService(db)
        skip = (page - 1) * limit
        tasks, total = task_service.list_tasks(
            user_id=current_user,
            skip=skip,
            limit=limit,
            search=search,
            status=status,
            priority=priority,
            assignee_id=assignee,
            owner_id=owner,
            archived=archived,
            sort_by=sort,
            order=order,
        )

        return {
            "data": {
                "tasks": [
                    {
                        "taskId": t.task_id,
                        "task_id": t.task_id,
                        "id": t.task_id,
                        "title": t.title,
                        "description": t.description,
                        "status": t.status,
                        "priority": t.priority,
                        "ownerId": t.owner.user_id,
                        "owner": {
                            "userId": t.owner.user_id,
                            "user_id": t.owner.user_id,
                            "id": t.owner.user_id,
                            "email": t.owner.email,
                            "fullName": t.owner.full_name,
                        },
                        "assignee": (
                            {
                                "userId": t.assignee.user_id,
                                "user_id": t.assignee.user_id,
                                "id": t.assignee.user_id,
                                "email": t.assignee.email,
                            }
                            if t.assignee
                            else None
                        ),
                        "dueDate": t.due_date,
                        "createdAt": t.created_at,
                        "updatedAt": t.updated_at,
                        "archivedAt": t.archived_at,
                    }
                    for t in tasks
                ]
            },
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": (total + limit - 1) // limit,
            },
        }
    except ApplicationError as e:
        raise e


@app.get("/api/v1/tasks/{task_id}")
async def get_task(
    task_id: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get task details."""
    try:
        task_service = TaskService(db)
        task = task_service.get_task(task_id, current_user)
        # Fetch comments for the task (non-blocking on errors)
        collab_service = CollaborationService(db)
        try:
            comments, _ = collab_service.get_task_comments(
                task_id, current_user, 0, 100
            )
        except ApplicationError:
            comments = []

        return {
            "data": {
                "taskId": task.task_id,
                "task_id": task.task_id,
                "id": task.task_id,
                "ownerId": task.owner.user_id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "owner": {
                    "userId": task.owner.user_id,
                    "user_id": task.owner.user_id,
                    "id": task.owner.user_id,
                    "email": task.owner.email,
                    "fullName": task.owner.full_name,
                },
                "assignee": (
                    {
                        "userId": task.assignee.user_id,
                        "user_id": task.assignee.user_id,
                        "id": task.assignee.user_id,
                        "email": task.assignee.email,
                        "fullName": task.assignee.full_name,
                    }
                    if task.assignee
                    else None
                ),
                "dueDate": task.due_date,
                "createdAt": task.created_at,
                "updatedAt": task.updated_at,
                "archivedAt": task.archived_at,
                "comments": [
                    {
                        "commentId": c.comment_id,
                        "comment_id": c.comment_id,
                        "id": c.comment_id,
                        "author": {
                            "userId": c.author.user_id,
                            "user_id": c.author.user_id,
                            "id": c.author.user_id,
                            "email": c.author.email,
                            "fullName": c.author.full_name,
                        },
                        "content": c.content,
                        "createdAt": c.created_at,
                        "updatedAt": c.updated_at,
                    }
                    for c in comments
                ],
                "history": [
                    {
                        "action": "created",
                        "timestamp": task.created_at,
                        "details": "Task created",
                    }
                ],
            }
        }
    except ApplicationError as e:
        raise e


@app.patch("/api/v1/tasks/{task_id}")
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a task."""
    try:
        task_service = TaskService(db)
        task = task_service.update_task(task_id, current_user, task_data)
        return {
            "data": {
                "taskId": task.task_id,
                "task_id": task.task_id,
                "id": task.task_id,
                "ownerId": task.owner.user_id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "owner": {
                    "userId": task.owner.user_id,
                    "user_id": task.owner.user_id,
                    "id": task.owner.user_id,
                    "email": task.owner.email,
                    "fullName": task.owner.full_name,
                },
                "assignee": (
                    {
                        "userId": task.assignee.user_id,
                        "user_id": task.assignee.user_id,
                        "id": task.assignee.user_id,
                        "email": task.assignee.email,
                        "fullName": task.assignee.full_name,
                    }
                    if task.assignee
                    else None
                ),
                "dueDate": task.due_date,
                "createdAt": task.created_at,
                "updatedAt": task.updated_at,
                "archivedAt": task.archived_at,
            }
        }
    except ApplicationError as e:
        raise e


@app.delete("/api/v1/tasks/{task_id}")
async def delete_task(
    task_id: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a task (admin only)."""
    try:
        task_service = TaskService(db)
        task_service.delete_task(task_id, current_user)
        return None
    except ApplicationError as e:
        raise e


@app.post("/api/v1/tasks/{task_id}/archive")
async def archive_task(
    task_id: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Archive a task."""
    try:
        task_service = TaskService(db)
        task = task_service.archive_task(task_id, current_user)
        return {"data": {"task_id": task.task_id, "archived_at": task.archived_at}}
    except ApplicationError as e:
        raise e


@app.post("/api/v1/tasks/{task_id}/restore")
async def restore_task(
    task_id: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Restore an archived task."""
    try:
        task_service = TaskService(db)
        task = task_service.restore_task(task_id, current_user)
        return {"data": {"task_id": task.task_id, "archived_at": task.archived_at}}
    except ApplicationError as e:
        raise e


@app.post("/api/v1/tasks/{task_id}/duplicate")
async def duplicate_task(
    task_id: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Duplicate a task."""
    try:
        task_service = TaskService(db)
        task = task_service.duplicate_task(task_id, current_user)
        return {
            "data": {
                "task_id": task.task_id,
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
                "created_at": task.created_at,
            }
        }
    except ApplicationError as e:
        raise e


# Comment endpoints
@app.post("/api/v1/tasks/{task_id}/comments")
async def add_comment(
    task_id: str,
    comment_data: CommentCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a comment to a task."""
    try:
        collab_service = CollaborationService(db)
        comment = collab_service.add_comment(
            task_id, current_user, comment_data.content
        )
        return {
            "data": {
                "commentId": comment.comment_id,
                "comment_id": comment.comment_id,
                "id": comment.comment_id,
                "author": {
                    "userId": comment.author.user_id,
                    "user_id": comment.author.user_id,
                    "id": comment.author.user_id,
                    "email": comment.author.email,
                },
                "content": comment.content,
                "createdAt": comment.created_at,
            }
        }
    except ApplicationError as e:
        raise e


@app.get("/api/v1/tasks/{task_id}/comments")
async def get_task_comments(
    task_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get comments for a task."""
    try:
        collab_service = CollaborationService(db)
        skip = (page - 1) * limit
        comments, total = collab_service.get_task_comments(
            task_id, current_user, skip, limit
        )
        return {
            "data": {
                "comments": [
                    {
                        "commentId": c.comment_id,
                        "author": {
                            "userId": c.author.user_id,
                            "email": c.author.email,
                            "fullName": c.author.full_name,
                        },
                        "content": c.content,
                        "createdAt": c.created_at,
                        "updatedAt": c.updated_at,
                    }
                    for c in comments
                ]
            },
            "pagination": {"page": page, "limit": limit, "total": total},
        }
    except ApplicationError as e:
        raise e


@app.patch("/api/v1/tasks/{task_id}/comments/{comment_id}")
async def update_comment(
    task_id: str,
    comment_id: str,
    comment_data: CommentCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a comment."""
    try:
        collab_service = CollaborationService(db)
        comment = collab_service.update_comment(
            task_id, comment_id, current_user, comment_data.content
        )
        return {
            "data": {
                "commentId": comment.comment_id,
                "content": comment.content,
                "updatedAt": comment.updated_at,
            }
        }
    except ApplicationError as e:
        raise e


@app.delete("/api/v1/tasks/{task_id}/comments/{comment_id}")
async def delete_comment(
    task_id: str,
    comment_id: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a comment."""
    try:
        collab_service = CollaborationService(db)
        collab_service.delete_comment(task_id, comment_id, current_user)
        return None
    except ApplicationError as e:
        raise e


# Dashboard endpoints
@app.get("/api/v1/dashboard/metrics")
async def get_dashboard_metrics(
    current_user: str = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get dashboard metrics."""
    try:
        reporting_service = ReportingService(db)
        metrics = reporting_service.get_dashboard_metrics(current_user)
        return {"data": metrics}
    except ApplicationError as e:
        raise e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
