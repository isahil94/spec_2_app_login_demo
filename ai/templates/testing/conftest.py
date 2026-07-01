"""Reusable pytest conftest template for backend agents.

Usage:
- Copy this file into `tests/conftest.py` when generating backend code.
- Ensures `DATABASE_URL` is set before importing app and provides fixtures:
  - `test_client` (FastAPI TestClient)
  - `db_session` (transactional SQLAlchemy session rolled back per test)

Adjust `SQLALCHEMY_TEST_DATABASE_URL` or set `TEST_DATABASE_URL` env var in CI to use PostgreSQL.
"""
import os
import sys
from pathlib import Path

# Ensure repo root is importable
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Tests must set the DATABASE_URL *before* importing application code
os.environ.setdefault("DATABASE_URL", os.environ.get("TEST_DATABASE_URL", "sqlite:///./test_db.sqlite3"))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test DB url
SQLALCHEMY_TEST_DATABASE_URL = os.environ["DATABASE_URL"]

# Create engine (file-based SQLite by default; allow Postgres via TEST_DATABASE_URL)
connect_args = {"check_same_thread": False} if SQLALCHEMY_TEST_DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args=connect_args)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import AFTER environment variables and engine creation
from src.database import Base, get_db  # noqa: E402
from src.main import app  # noqa: E402

# Ensure tables exist for tests
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def _cleanup_test_db_session():
    """Cleanup test database file after the whole test session finishes.

    For SQLite file-based DBs we remove the file to avoid accumulating artifacts.
    """
    yield
    try:
        # Drop all tables and remove file if using SQLite file
        Base.metadata.drop_all(bind=engine)
        if SQLALCHEMY_TEST_DATABASE_URL.startswith("sqlite"):
            sqlite_path = SQLALCHEMY_TEST_DATABASE_URL.replace("sqlite:///", "")
            if os.path.exists(sqlite_path):
                os.remove(sqlite_path)
    except Exception:
        pass


def override_get_db():
    """Dependency override that yields a transactional session for tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database state between tests by dropping/creating all tables.

    This is simple and robust for most small test suites. For faster isolation,
    replace with connection + nested transaction pattern.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def test_client():
    return client


@pytest.fixture
def db_session():
    """Provide a DB session bound to the test engine. Rollback is handled by reset_db fixture."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
