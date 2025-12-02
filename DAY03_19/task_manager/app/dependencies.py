from typing import AsyncGenerator

from app.api.v1.schemas.user import UserResponse
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.unit_of_work import SQLAlchemyUnitOfWork, JsonUnitOfWork, IUnitOfWork
from app.services.task_services import TaskService
from app.services.user_services import UserService
from app.repositories.user_repository import UserRepository
from app.core.database import AsyncSessionLocal
from app.core.security import decode_token

# HTTPBearer - extracts token from "Authorization: Bearer <token>" header
security = HTTPBearer()

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


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials  # Extract the actual token
    payload = decode_token(token)
    if not payload:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = await user_service.get_user_by_email(email)
    if not user:
        raise credentials_exception
    
    return UserResponse.model_validate(user)