import os
from functools import lru_cache
from pydantic import BaseSettings


class Config(BaseSettings):
    debug: bool = bool(int(os.getenv("DEBUG", False)))


@lru_cache()
def get_settings() -> Config:
    return Config()
