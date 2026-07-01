import uuid
from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from apps.backend.src.auth.jwt import create_token
from apps.backend.src.domain.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def register_user(db: Session, email: str, password: str, display_name: str) -> dict:
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise ValueError("Email already registered")

    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        email=email,
        password_hash=hash_password(password),
        display_name=display_name,
        roles="User",
        preferences="{}",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token_data = create_token(user_id, ["User"])
    return {
        "user_id": user_id,
        "email": user.email,
        "display_name": user.display_name,
        "token": token_data["token"],
        "expires_in": token_data["expires_in"],
        "roles": ["User"],
    }


def authenticate_user(db: Session, email: str, password: str) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    return {
        "user_id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "roles": user.roles.split(",") if user.roles else ["User"],
    }


def create_token_for_user(user_id: str, roles: list[str]) -> dict[str, object]:
    return create_token(user_id, roles)


create_token = create_token_for_user
