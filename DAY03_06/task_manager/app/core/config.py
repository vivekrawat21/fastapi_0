"""Application configuration using Pydantic settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    """Return settings instance (constructs from environment / .env)."""
    return Settings()
