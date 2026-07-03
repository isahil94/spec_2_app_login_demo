from typing import Optional

from passlib.context import CryptContext

from apps.backend.src.auth.jwt import create_access_token
from apps.backend.src.core.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def register_user(db, email: str, password: str, full_name: Optional[str]) -> User:
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password, full_name=full_name, role="user")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email, User.is_active).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_session_token(user: User) -> str:
    return create_access_token(subject=user.email)


def update_password(user: User, new_password: str) -> User:
    user.hashed_password = get_password_hash(new_password)
    return user
