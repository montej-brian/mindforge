"""
MINDFORGE — Configuration Loader
Strictly validates all environment variables on startup using Pydantic.
"""
import os
from functools import lru_cache
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings and environment validation.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ─── 7. Development / Production Flags ────────────────────────────────────
    app_env: str = Field(default="development", pattern="^(development|staging|production)$")
    debug: bool = True
    app_secret_key: str = Field(..., min_length=16)

    # ─── 1. Google Gemini API Configuration ──────────────────────────────────
    gemini_api_key: str = Field(...)
    gemini_model: str = "gemini-1.5-pro-latest"

    # ─── 2. Database Configuration ──────────────────────────────────────────
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "mindforge_user"
    db_password: str = "mindforge_password"
    db_name: str = "mindforge_db"
    database_url: str = Field(default="sqlite+aiosqlite:///./mindforge.db")

    @field_validator("database_url", mode="before")
    @classmethod
    def assemble_db_url(cls, v: str, info) -> str:
        """Constructs MariaDB URL if credentials are not defaults, otherwise uses provided v."""
        # Using Field info would be better but simple env check is more direct for pydantic-settings
        user = os.getenv("DB_USER")
        pw = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "3306")
        name = os.getenv("DB_NAME", "mindforge_db")
        
        if user and pw and user != "mindforge_user":
             return f"mysql+aiomysql://{user}:{pw}@{host}:{port}/{name}"
        return v

    # ─── 3. Voice / Speech API Keys ───────────────────────────────────────────
    voice_engine: str = "google"
    stt_api_key: Optional[str] = None
    tts_api_key: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None

    # ─── 4. Browser Automation Settings ───────────────────────────────────────
    browser_headless: bool = False
    browser_timeout: int = 30
    selenium_remote_url: Optional[str] = None

    # ─── 5. Security Keys & Secrets ───────────────────────────────────────────
    jwt_secret_key: str = Field(..., min_length=16)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # ─── 6. Logging Configuration ─────────────────────────────────────────────
    log_level: str = "INFO"
    log_file: str = "logs/mindforge.log"
    enable_file_logging: bool = True

    # ─── Other ────────────────────────────────────────────────────────────────
    langchain_tracing_v2: bool = False
    langchain_api_key: Optional[str] = None
    langchain_project: str = "MINDFORGE"


@lru_cache
def get_settings() -> Settings:
    """
    Loads and validates settings. 
    Provides clear instructions if required variables are missing.
    """
    try:
        return Settings()
    except Exception as e:
        import sys
        print("\n" + "="*60)
        print("❌ MINDFORGE CONFIGURATION ERROR")
        print("="*60)
        print(f"Details: {e}")
        print("\nACTION REQUIRED:")
        print("1. Create a '.env' file in the 'backend/' directory.")
        print("2. Copy contents from '.env.example' into '.env'.")
        print("3. Fill in required keys: GEMINI_API_KEY, APP_SECRET_KEY, JWT_SECRET_KEY.")
        print("="*60 + "\n")
        
        if os.getenv("APP_ENV") == "production":
            sys.exit(1)
            
        # Fallback for development: ensures attributes exist to avoid AttributeErrors
        # Use placeholders so the app can at least start.
        defaults = {
            "gemini_api_key": "MISSING_KEY",
            "app_secret_key": "placeholder_secret_key_16_chars",
            "jwt_secret_key": "placeholder_jwt_key_16_chars",
        }
        return Settings.model_construct(**{**defaults, **os.environ})


settings = get_settings()
