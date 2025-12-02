from app.api.v1.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.models import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def create_user(self, user_create: UserCreate) -> UserResponse:
        # Check if email already exists
        existing_user = await self.user_repository.get_by_email(user_create.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = hash_password(user_create.password)
        user = User(name=user_create.name, email=user_create.email, password=hashed_password, role=user_create.role) 
        
        try:
            created_user = await self.user_repository.create(user)
            return UserResponse.model_validate(created_user)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Email already registered")

    async def create_user_from_name(self, name: str) -> UserResponse:
        user = User(name=name, email=f"{name}@example.com")  
        try:
            created_user = await self.user_repository.create(user)
            return UserResponse.model_validate(created_user)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Email already registered")
            
    async def create_user_auth(self, name: str, email: str, password: str, role: str = "Collector") -> UserResponse:
        db_user = await self.user_repository.get_by_email(email)
        
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = hash_password(password)
        user = User(name=name, email=email, password=hashed_password, role=role)
        
        try:
            created_user = await self.user_repository.create(user)
            return UserResponse.model_validate(created_user)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Returns raw User model (includes password for auth verification)"""
        user = await self.user_repository.get_by_email(email)
        return user
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user)

    async def get_user_by_name(self, name: str) -> Optional[UserResponse]:
        user = await self.user_repository.get_by_name(name)
        if user:
            return UserResponse.model_validate(user)
        return None

    async def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        updated_user = await self.user_repository.update(user)
        return UserResponse.model_validate(updated_user)

    async def delete_user(self, user_id: int):
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await self.user_repository.delete(user)