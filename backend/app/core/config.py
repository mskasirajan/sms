from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/sms_db"
    # Optional separate URL for running Alembic migrations (should use a
    # superuser or a role with DDL rights). Falls back to DATABASE_URL when
    # not set, which is fine for development.
    MIGRATION_DATABASE_URL: Optional[str] = None
    SECRET_KEY: str = "change-this-to-a-random-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    @property
    def migration_url(self) -> str:
        return self.MIGRATION_DATABASE_URL or self.DATABASE_URL

    class Config:
        env_file = ".env"


settings = Settings()
