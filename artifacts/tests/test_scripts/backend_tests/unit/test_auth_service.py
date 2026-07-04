"""Unit tests for auth service."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import Base
from src.services.auth_service import AuthService
from src.utils.exceptions import (
    DuplicateResourceError,
    UnauthorizedError,
    ValidationError,
)


# Setup test database
@pytest.fixture
def test_db():
    """Create test database."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    yield SessionLocal()


def test_register_user(test_db):
    """Test user registration."""
    auth_service = AuthService(test_db)
    user = auth_service.register("test@example.com", "password123", "Test User")

    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.user_id is not None


def test_register_duplicate_email(test_db):
    """Test duplicate email registration."""
    auth_service = AuthService(test_db)
    auth_service.register("test@example.com", "password123", "Test User")

    with pytest.raises(DuplicateResourceError):
        auth_service.register("test@example.com", "password123", "Another User")


def test_login_user(test_db):
    """Test user login."""
    auth_service = AuthService(test_db)
    auth_service.register("test@example.com", "password123", "Test User")

    token, expires_in, user = auth_service.login("test@example.com", "password123")

    assert token is not None
    assert expires_in == 86400
    assert user.email == "test@example.com"


def test_login_invalid_credentials(test_db):
    """Test login with invalid credentials."""
    auth_service = AuthService(test_db)
    auth_service.register("test@example.com", "password123", "Test User")

    with pytest.raises(UnauthorizedError):
        auth_service.login("test@example.com", "wrongpassword")


def test_register_short_password(test_db):
    """Test registration with short password."""
    auth_service = AuthService(test_db)

    with pytest.raises(ValidationError):
        auth_service.register("test@example.com", "short", "Test User")
