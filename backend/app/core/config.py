import os
from functools import lru_cache
from pydantic import BaseSettings


class Config(BaseSettings):
    DEBUG: bool = bool(os.getenv("DEBUG", False))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///app.db")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 8
    )
    SUPERUSER_EMAIL: str = os.getenv("SUPERUSER_EMAIL", "admin@mail.com")
    SUPERUSER_PASSWORD: str = os.getenv("SUPERUSER_PASSWORD", "ultra_strong_password")
    SUPERUSER_NAME: str = os.getenv("SUPERUSER_NAME", "admin")


@lru_cache()
def get_settings() -> Config:
    return Config()
