from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.src.db.database import SessionLocal
from apps.backend.src.dto.auth import (
    LoginRequest,
    ProfileResponse,
    RegisterRequest,
    TokenResponse,
)
from apps.backend.src.middleware.auth import get_current_user
from apps.backend.src.services.auth_service import (
    authenticate_user,
    create_session_token,
    register_user,
    update_password,
)
from apps.backend.src.validation.validators import validate_password_strength

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(request: RegisterRequest):
    validate_password_strength(request.password)
    db = SessionLocal()
    try:
        user = register_user(db, request.email, request.password, request.full_name)
        token = create_session_token(user)
        return TokenResponse(access_token=token, token_type="bearer")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    finally:
        db.close()


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    db = SessionLocal()
    try:
        user = authenticate_user(db, request.email, request.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token = create_session_token(user)
        return TokenResponse(access_token=token, token_type="bearer")
    finally:
        db.close()


@router.get("/me", response_model=ProfileResponse)
def profile(user=Depends(get_current_user)):
    return ProfileResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
    )


@router.patch("/me", response_model=ProfileResponse)
def update_profile(data: RegisterRequest, user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        user.full_name = data.full_name
        if data.password:
            validate_password_strength(data.password)
            user.hashed_password = update_password(user, data.password).hashed_password
        db.add(user)
        db.commit()
        db.refresh(user)
        return ProfileResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
        )
    finally:
        db.close()
