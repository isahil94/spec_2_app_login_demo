from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    app_name: str = "Task Management API"
    debug: bool = False
    database_url: str = "sqlite:///./apps/backend/backend.db"
    jwt_secret: str = Field("change-me-in-env", env="JWT_SECRET")
    jwt_expiration_minutes: int = 60
    password_salt: str = Field("default-salt", env="PASSWORD_SALT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = AppSettings()
