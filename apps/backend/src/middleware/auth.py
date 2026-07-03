from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from apps.backend.src.auth.jwt import decode_access_token
from apps.backend.src.core.models import User
from apps.backend.src.db.database import SessionLocal

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db),
) -> User:
    token = credentials.credentials
    try:
        subject = decode_access_token(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")

    user = db.query(User).filter(User.email == subject, User.is_active).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return user


async def request_correlation_middleware(request: Request, call_next):
    request.state.correlation_id = request.headers.get("X-Correlation-ID", "unknown")
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = request.state.correlation_id
    return response
