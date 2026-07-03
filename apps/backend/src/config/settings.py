from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Task Management Backend"
    auth_secret_key: str = "change-this-secret-for-production"
    auth_algorithm: str = "HS256"
    auth_access_token_expires_minutes: int = 60
    database_url: str = "sqlite+pysqlite:///:memory:"
    environment: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
