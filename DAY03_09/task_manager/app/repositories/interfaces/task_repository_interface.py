from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.api.v1.schemas.tasks import TaskResponse

class ITaskRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    async def get_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        ...

    @abstractmethod
    async def add(self, task_data: Dict[str, Any]):
        ...

    @abstractmethod
    async def update(self, task_id: str, task_data: Dict[str, Any]):
        ...

    @abstractmethod
    async def delete(self, task_id: str):
        ...
