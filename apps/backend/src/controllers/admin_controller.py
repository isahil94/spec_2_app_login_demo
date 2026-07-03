from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.src.core.models import Team, User
from apps.backend.src.db.database import SessionLocal
from apps.backend.src.dto.admin import (
    TeamCreateRequest,
    TeamResponse,
    UserCreateRequest,
    UserUpdateRequest,
)
from apps.backend.src.middleware.auth import require_admin

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/users", response_model=list[UserCreateRequest])
def list_users(admin=Depends(require_admin)):
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return [UserCreateRequest(email=user.email, full_name=user.full_name, role=user.role) for user in users]
    finally:
        db.close()


@router.post("/users", response_model=UserCreateRequest, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreateRequest, admin=Depends(require_admin)):
    db = SessionLocal()
    try:
        user = User(email=payload.email, full_name=payload.full_name, role=payload.role, hashed_password="")
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserCreateRequest(email=user.email, full_name=user.full_name, role=user.role)
    finally:
        db.close()


@router.patch("/users/{user_id}", response_model=UserCreateRequest)
def update_user(user_id: int, payload: UserUpdateRequest, admin=Depends(require_admin)):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if payload.full_name is not None:
            user.full_name = payload.full_name
        if payload.role is not None:
            user.role = payload.role
        if payload.is_active is not None:
            user.is_active = payload.is_active
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserCreateRequest(email=user.email, full_name=user.full_name, role=user.role)
    finally:
        db.close()


@router.get("/teams", response_model=list[TeamResponse])
def list_teams(admin=Depends(require_admin)):
    db = SessionLocal()
    try:
        teams = db.query(Team).all()
        return [TeamResponse(id=team.id, name=team.name) for team in teams]
    finally:
        db.close()


@router.post("/teams", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(payload: TeamCreateRequest, admin=Depends(require_admin)):
    db = SessionLocal()
    try:
        team = Team(name=payload.name)
        db.add(team)
        db.commit()
        db.refresh(team)
        return TeamResponse(id=team.id, name=team.name)
    finally:
        db.close()
