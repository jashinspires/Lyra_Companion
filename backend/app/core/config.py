"""Application configuration settings."""

from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables with defaults."""

    project_name: str = "Lyra Backend"
    project_description: str = (
        "API services for Lyra, the empathetic mental health companion."
    )
    version: str = "0.1.0"

    gemini_api_key: str | None = None
    openai_api_key: str | None = None
    pinecone_api_key: str | None = None
    pinecone_environment: str | None = None
    pinecone_index: str | None = None

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "lyra"

    allow_origins: List[str] = ["*"]

    environment: str = "local"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""

    return Settings()  # type: ignore[call-arg]


settings = get_settings()
