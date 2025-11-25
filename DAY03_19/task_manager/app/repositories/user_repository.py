from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.models import User
from typing import Optional

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self.db.get(User, user_id)

    async def get_by_name(self, name: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.name == name))
        return result.scalar_one_or_none()

    async def update(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User):
        await self.db.delete(user)
        await self.db.commit()