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
    database_url: str = "mysql+aiomysql://vivek:vivek2002@localhost:3306/taskmanager_db"
    # For PostgreSQL, use: "postgresql+asyncpg://user:password@localhost/dbname"
    # For MySQL, use: "mysql+aiomysql://user:password@localhost/dbname"
    # For SQLite, use: "sqlite+aiosqlite:///./task_manager.db"

    # PostgreSQL specific settings
    postgres_host: Optional[str] = "localhost"
    postgres_port: Optional[int] = 5432
    postgres_user: Optional[str] = "postgres"
    postgres_password: Optional[str] = "password"
    postgres_db: Optional[str] = "task_manager"
    
    # MySQL specific settings
    mysql_host: Optional[str] = "localhost"
    mysql_port: Optional[int] = 3306
    mysql_user: Optional[str] = "vivek"
    mysql_password: Optional[str] = "vivek2002"
    mysql_db: Optional[str] = "taskmanager_db"
    
    frontend_cors_origins: list = ["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"]

    # SQLite specific settings
    sqlite_file: str = "./task_manager.db"

    class Config:
        env_file = ".env"

    @property
    def postgres_url(self) -> str:
        """Construct PostgreSQL URL from individual components."""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def mysql_url(self) -> str:
        """Construct MySQL URL from individual components."""
        return f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"

    @property
    def sqlite_url(self) -> str:
        """Construct SQLite URL."""
        return f"sqlite+aiosqlite:///{self.sqlite_file}"
    class Config:
        env_file = ".env"
        case_sensitive = False


# Initialize settings instance
settings = Settings()
