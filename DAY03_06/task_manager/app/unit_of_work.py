from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.json_repository import JsonTaskRepository
from app.repositories.sqlalchemy_repository import SQLAlchemyTaskRepository
from app.repositories.interfaces.task_repository_interface import ITaskRepository
from app.utils.files_io import write_tasks
from app.core.database import AsyncSessionLocal

class IUnitOfWork(ABC):
    tasks: ITaskRepository  # Changed to use interface instead of concrete type

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...

class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session: AsyncSession = None

    async def __aenter__(self):
        self.session = AsyncSessionLocal()
        self.tasks = SQLAlchemyTaskRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

class JsonUnitOfWork(IUnitOfWork):
    def __init__(self):
        self.tasks = JsonTaskRepository()

    async def __aenter__(self):
        await self.tasks._load_data()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    async def commit(self):
        await write_tasks(self.tasks.tasks)

    async def rollback(self):
        pass
