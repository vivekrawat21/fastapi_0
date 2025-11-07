"""Application configuration using Pydantic settings.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

        # Database configuration
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/taskmanager"
    # For PostgreSQL, use: "postgresql+asyncpg://user:password@localhost/dbname"
    # For MySQL, use: "mysql+asyncmy://user:password@localhost/dbname"
    # For SQLite, use: "sqlite+aiosqlite:///./task_manager.db"

    # PostgreSQL specific settings
    postgres_host: Optional[str] = "localhost"
    postgres_port: Optional[int] = 5432
    postgres_user: Optional[str] = "postgres"
    postgres_password: Optional[str] = "password"
    postgres_db: Optional[str] = "task_manager"
    frontend_cors_origins: list = ["http://localhost:3000", "http://localhost:3001"]

    # SQLite specific settings
    sqlite_file: str = "./task_manager.db"

    class Config:
        env_file = ".env"

    @property
    def postgres_url(self) -> str:
        """Construct PostgreSQL URL from individual components."""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def sqlite_url(self) -> str:
        """Construct SQLite URL."""
        return f"sqlite+aiosqlite:///{self.sqlite_file}"
    class Config:
        env_file = ".env"
        case_sensitive = False


# Initialize settings instance
settings = Settings()
