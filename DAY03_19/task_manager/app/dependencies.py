from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.unit_of_work import SQLAlchemyUnitOfWork, JsonUnitOfWork, IUnitOfWork
from app.services.task_services import TaskService
from app.services.user_services import UserService
from app.repositories.user_repository import UserRepository
from app.core.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency function that yields database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_uow() -> IUnitOfWork:
    return SQLAlchemyUnitOfWork()


def get_task_service(uow: IUnitOfWork = Depends(get_uow)) -> TaskService:
    return TaskService(uow)


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)
