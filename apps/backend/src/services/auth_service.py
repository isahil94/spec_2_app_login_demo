"""Authentication service."""

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session
from src.models.models import User, UserRole
from src.repositories.other_repositories import AuditRepository
from src.repositories.user_repository import UserRepository
from src.schemas.schemas import UserDTO
from src.utils.exceptions import (
    DuplicateResourceError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)
from src.utils.jwt import create_access_token
from src.utils.password import hash_password, verify_password


class AuthService:
    """Service for authentication and user account management."""

    def __init__(self, session: Session):
        """Initialize auth service."""
        self.session = session
        self.user_repo = UserRepository(session)
        self.audit_repo = AuditRepository(session)

    def register(self, email: str, password: str, full_name: str) -> UserDTO:
        """Register a new user."""
        # Validate input
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        if "@" not in email or "." not in email:
            raise ValidationError("Invalid email format")

        # Check if user already exists
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            raise DuplicateResourceError(f"Email {email} is already registered")

        # Create user
        password_hash = hash_password(password)
        user = self.user_repo.create_user(
            email, password_hash, full_name, UserRole.TEAM_MEMBER
        )

        # Log audit
        self.audit_repo.log_action(user.id, "user_registered", "user", user.id)

        return self._user_to_dto(user)

    def login(self, email: str, password: str) -> tuple[str, int, UserDTO]:
        """Authenticate user and return token."""
        # Get user by email
        user = self.user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError("Invalid credentials")

        # Verify password
        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid credentials")

        # Check if user is active
        if not user.is_active:
            raise UnauthorizedError("Account is disabled")

        # Generate token
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
        }
        token = create_access_token(token_data)

        # Log audit
        self.audit_repo.log_action(user.id, "user_login", "user", user.id)

        expires_in = 86400  # 24 hours in seconds

        return token, expires_in, self._user_to_dto(user)

    def get_user_by_id(self, user_id: str) -> Optional[UserDTO]:
        """Get user by ID."""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        return self._user_to_dto(user)

    def logout(self, user_id: str) -> bool:
        """Log user logout."""
        self.audit_repo.log_action(user_id, "user_logout", "user", user_id)
        return True

    def _user_to_dto(self, user: User) -> UserDTO:
        """Convert user to DTO."""
        return UserDTO(
            user_id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            created_at=user.created_at,
        )
