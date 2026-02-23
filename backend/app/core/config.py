from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    CORS_ORIGINS: List[str] = ["http://localhost:3002", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cors_origins_env = os.getenv("CORS_ORIGINS")
        if cors_origins_env:
            self.CORS_ORIGINS = [origin.strip() for origin in cors_origins_env.split(",")]


settings = Settings()
