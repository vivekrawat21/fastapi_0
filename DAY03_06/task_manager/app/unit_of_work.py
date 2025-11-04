from abc import ABC, abstractmethod
from app.repositories.json_repository import JsonTaskRepository
from app.utils.files_io import write_tasks

class IUnitOfWork(ABC):
    tasks: JsonTaskRepository

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
