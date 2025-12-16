import os
from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    # App
    app_name: str = "Wishlist API Test"
    environment: str = "test"
    backend_cors_origins: str = Field("http://localhost,http://localhost:3000,http://127.0.0.1,http://127.0.0.1:3000", env="BACKEND_CORS_ORIGINS")

    # Security
    jwt_secret_key: str = "test-jwt-secret-key-for-development-purposes-only"
    jwt_refresh_secret_key: str = "test-jwt-refresh-secret-key-for-development-purposes-only"
    session_secret_key: str = "test-session-secret-key-for-development-purposes-only"
    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 60 * 24
    refresh_token_expires_days: int = 7

    # Database - используем SQLite для тестирования
    database_url: str = Field(
        "sqlite:///./test_wishlist.db",  # используем SQLite вместо PostgreSQL
        env="DATABASE_URL",
    )

    # Rate limiting
    rate_limit_per_minute: int = Field(100, env="RATE_LIMIT_PER_MINUTE")

    @field_validator("backend_cors_origins")
    def normalize_cors(cls, v: str) -> str:
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_test_settings() -> TestSettings:
    return TestSettings()