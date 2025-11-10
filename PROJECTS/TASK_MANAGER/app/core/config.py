"""Application configuration using Pydantic settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI Task Manager"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    frontend_cors_origins: list = ["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        case_sensitive = False


# Initialize settings instance
settings = Settings()
