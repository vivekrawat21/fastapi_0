from app.core.config import get_settings
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

settings = get_settings()
DATABASE_URL = settings.database_url
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=settings.debug)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    """Yield a database session."""
    async with AsyncSessionLocal() as session:
        yield session


