from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.core.models import Task
from app.repositories.interfaces.task_repository_interface import ITaskRepository


class SQLAlchemyTaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """Convert SQLAlchemy Task model to dictionary."""
        return {
            "id": task.id,  # Keep as integer
            "title": task.title,
            "description": task.description,
            "priority": task.priority.value if task.priority else None,
            "status": task.status.value if task.status else None,
            "due_date": task.due_date.date() if task.due_date else None,
        }

    async def get_all(self) -> List[Dict[str, Any]]:
        result = await self.session.execute(select(Task))
        tasks = result.scalars().all()
        return [self._task_to_dict(task) for task in tasks]

    async def get_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        result = await self.session.execute(select(Task).where(Task.id == int(task_id)))
        task = result.scalar_one_or_none()
        return self._task_to_dict(task) if task else None

    async def add(self, task_data: Dict[str, Any]):
        task = Task(
            title=task_data["title"],
            description=task_data.get("description"),
            priority=task_data.get("priority"),
            status=task_data.get("status"),
            due_date=task_data.get("due_date"),
        )
        self.session.add(task)
        
        
        await self.session.flush()
        await self.session.refresh(task)
        return self._task_to_dict(task)

    async def update(self, task_id: str, task_data: Dict[str, Any]):
        # Remove 'id' from task_data to prevent updating the primary key
        update_data = {k: v for k, v in task_data.items() if k != 'id'}
        
        if update_data:  
            await self.session.execute(
                update(Task)
                .where(Task.id == int(task_id))
                .values(**update_data)
            )
            await self.session.flush()

    async def delete(self, task_id: str):
        await self.session.execute(
            delete(Task).where(Task.id == int(task_id))
        )