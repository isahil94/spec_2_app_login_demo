"""User repository for data access."""

from typing import Optional

from sqlalchemy.orm import Session

from src.models.models import User
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model."""

    def __init__(self, session: Session):
        """Initialize user repository."""
        super().__init__(session, User)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.session.query(User).filter(User.email == email).first()

    def create_user(
        self, email: str, password_hash: str, full_name: str, role="TEAM_MEMBER"
    ) -> User:
        """Create a new user."""
        user = User(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            role=role,
            is_active=True,
            theme="system",
            language="en",
            timezone="UTC",
            notifications_in_app=True,
            notifications_email=False,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_active_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get active users."""
        return (
            self.session.query(User)
            .filter(User.is_active.is_(True))
            .offset(skip)
            .limit(limit)
            .all()
        )
