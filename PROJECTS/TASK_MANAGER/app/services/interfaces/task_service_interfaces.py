from abc import ABC,abstractmethod
from typing import List, Optional
from app.api.v1.schemas.tasks import Task
from app.api.v1.schemas import TaskListResponse,TaskCreate,TaskResponse,TaskUpdate
class TaskServiceInterface(ABC):
    @abstractmethod
    async def list_tasks(self,status: Optional[str],due_date: Optional[str],search: Optional[str]) -> TaskListResponse:
        pass

    @abstractmethod
    async def create_task(self, task_data:TaskCreate) -> TaskResponse:
        pass
    
    @abstractmethod
    async def update_task(self, task_id:str, task_data:TaskUpdate) -> TaskResponse:
        pass

    @abstractmethod
    async def delete_task(self, task_id:str) -> None:
        pass