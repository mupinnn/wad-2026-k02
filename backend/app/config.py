"""Settings dari .env di root repo. Uvicorn dijalankan dari backend/."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    secret_key: str = ""
    access_token_expire_minutes: int = 60
    admin_email: str = ""
    admin_password: str = ""
    user_email: str = ""
    user_password: str = ""

    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / ".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
