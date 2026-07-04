"""Database configuration and session management."""

import os
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config.settings import settings

# Resolve relative SQLite URL paths to the backend package directory

database_url = settings.DATABASE_URL
if database_url.startswith("sqlite:///"):
    sqlite_path = database_url.removeprefix("sqlite:///")
    if sqlite_path and not os.path.isabs(sqlite_path):
        backend_dir = Path(__file__).resolve().parents[2]
        backend_db_path = backend_dir / sqlite_path
        workspace_root = backend_dir.parents[1]
        root_db_path = workspace_root / sqlite_path

        if root_db_path.exists():
            resolved_path = root_db_path
        elif backend_db_path.exists():
            resolved_path = backend_db_path
        else:
            # Default to backend-local database path when none exists yet.
            resolved_path = backend_db_path

        database_url = f"sqlite:///{resolved_path}"

# Create engine
engine = create_engine(
    database_url,
    connect_args=(
        {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    ),
    echo=settings.SQLALCHEMY_ECHO,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
    if database_url.startswith("sqlite"):
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(users)"))
            columns = {row[1] for row in result.fetchall()}
            if "contact_information" not in columns:
                conn.execute(
                    text("ALTER TABLE users ADD COLUMN contact_information TEXT")
                )
            if "theme" not in columns:
                conn.execute(text("ALTER TABLE users ADD COLUMN theme TEXT"))
            if "language" not in columns:
                conn.execute(text("ALTER TABLE users ADD COLUMN language TEXT"))
            if "timezone" not in columns:
                conn.execute(text("ALTER TABLE users ADD COLUMN timezone TEXT"))
            if "privacy" not in columns:
                conn.execute(text("ALTER TABLE users ADD COLUMN privacy TEXT"))
            if "notifications_in_app" not in columns:
                conn.execute(
                    text("ALTER TABLE users ADD COLUMN notifications_in_app BOOLEAN")
                )
            if "notifications_email" not in columns:
                conn.execute(
                    text("ALTER TABLE users ADD COLUMN notifications_email BOOLEAN")
                )
