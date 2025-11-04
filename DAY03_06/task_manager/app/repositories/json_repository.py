from typing import List, Optional, Dict, Any
from app.repositories.interfaces.task_repository_interface import ITaskRepository
from app.utils.files_io import read_tasks, write_tasks

class JsonTaskRepository(ITaskRepository):
    def __init__(self):
        self.tasks: List[Dict[str, Any]] = []
        self.loaded = False

    async def _load_data(self):
        if not self.loaded:
            self.tasks = await read_tasks()
            self.loaded = True

    async def get_all(self) -> List[Dict[str, Any]]:
        await self._load_data()
        return self.tasks

    async def get_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        await self._load_data()
        return next((task for task in self.tasks if task["id"] == task_id), None)

    async def add(self, task_data: Dict[str, Any]):
        await self._load_data()
        self.tasks.append(task_data)

    async def update(self, task_id: str, task_data: Dict[str, Any]):
        await self._load_data()
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks[i] = task_data
                break

    async def delete(self, task_id: str):
        await self._load_data()
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
