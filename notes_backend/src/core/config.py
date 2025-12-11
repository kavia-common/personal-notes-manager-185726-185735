import os
from functools import lru_cache
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""
    # Database file path for SQLite, default to ./data/notes.db within container root execution dir
    notes_db_path: str = os.getenv("NOTES_DB_PATH", "./data/notes.db")
    app_title: str = os.getenv("APP_TITLE", "Personal Notes Manager API")
    app_description: str = os.getenv(
        "APP_DESCRIPTION",
        "A FastAPI backend that manages personal notes with full CRUD over SQLite storage."
    )
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    api_prefix: str = "/api/v1"


# PUBLIC_INTERFACE
@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
