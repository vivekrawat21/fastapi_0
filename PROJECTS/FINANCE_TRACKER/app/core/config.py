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



# DATABSE CONFIGURATION
    database_name: str
    database_user: str
    database_password: str
    database_host: str
    database_port: int
    database_url: str = ""
    sync_database_url: str = ""
    def __init__(self, **values):
        super().__init__(**values)
        self.database_url = (
            f"postgresql+asyncpg://{self.database_user}:"
            f"{self.database_password}@{self.database_host}:"
            f"{self.database_port}/{self.database_name}"
        )
        self.sync_database_url = (
            f"postgresql+psycopg2://{self.database_user}:"
            f"{self.database_password}@{self.database_host}:"
            f"{self.database_port}/{self.database_name}"
        )
        
        
    
    


def get_settings() -> Settings:
    """Return settings instance (constructs from environment / .env)."""
    return Settings()
