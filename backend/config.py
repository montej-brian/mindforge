"""
MINDFORGE — Application Settings
Loaded from environment variables / .env file via pydantic-settings.
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ─── App ──────────────────────────────────────────────────────────────────
    app_env: str = "development"
    app_secret_key: str = "change-me-please"
    debug: bool = True

    # ─── Server ───────────────────────────────────────────────────────────────
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # ─── Google Gemini ────────────────────────────────────────────────────────
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-pro-latest"

    # ─── LangChain ────────────────────────────────────────────────────────────
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""
    langchain_project: str = "MINDFORGE"

    # ─── Selenium ─────────────────────────────────────────────────────────────
    browser_headless: bool = False
    browser_timeout: int = 30
    selenium_remote_url: str = ""

    # ─── Voice ────────────────────────────────────────────────────────────────
    voice_engine: str = "google"        # google | whisper
    whisper_model_size: str = "base"
    audio_sample_rate: int = 16000
    audio_chunk_size: int = 1024

    # ─── Database ─────────────────────────────────────────────────────────────
    database_url: str = "sqlite+aiosqlite:///./mindforge.db"

    # ─── Redis ────────────────────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"

    # ─── Logging ──────────────────────────────────────────────────────────────
    log_level: str = "INFO"
    log_file: str = "logs/mindforge.log"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
