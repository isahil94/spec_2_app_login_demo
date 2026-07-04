"""Application configuration settings."""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # API
    API_TITLE: str = "Task Management System API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = (
        "Collaborative task management system with role-based access control"
    )
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8001

    # Database
    DATABASE_URL: str = "sqlite:///apps/data/task_management.db"
    SQLALCHEMY_ECHO: bool = False

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Password
    PASSWORD_MIN_LENGTH: int = 8

    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:4173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
