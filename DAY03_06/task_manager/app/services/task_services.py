from typing import Optional
from app.api.v1.schemas.tasks import TaskListResponse, TaskCreate, TaskResponse, TaskUpdate
from app.core.tasks import generate_id
from fastapi import HTTPException
from datetime import date
from app.unit_of_work import IUnitOfWork

class TaskService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def list_tasks(self, status: Optional[str], due_date: Optional[date], search: Optional[str]) -> TaskListResponse:
        """List all tasks according to filters provided"""
        async with self.uow:
            tasks = await self.uow.tasks.get_all()
            
            if status:
                tasks = [task for task in tasks if task.get("status") == status.strip()]
            if due_date:
                tasks = [task for task in tasks if task.get("due_date") == str(due_date)]
            if search:
                tasks = [task for task in tasks if search.strip().lower() in task["title"].lower()]
            
            # Return empty list if no tasks found (don't raise 404 for list endpoints)
            return TaskListResponse(tasks=[TaskResponse.model_validate(task) for task in tasks])

    async def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """Create a new task"""
        async with self.uow:
            new_task_dict = task_data.model_dump()
            new_task_dict["id"] = await generate_id()
            await self.uow.tasks.add(new_task_dict)
            await self.uow.commit()
            return TaskResponse.model_validate(new_task_dict)

    async def update_task(self, task_id: str, task_data: TaskUpdate) -> TaskResponse:
        """Update an existing task by its ID"""
        async with self.uow:
            existing_task = await self.uow.tasks.get_by_id(task_id)
            if not existing_task:
                raise HTTPException(status_code=404, detail="Task not found")

            update_data = task_data.model_dump(exclude_unset=True)
            updated_task_dict = {**existing_task, **update_data}
            
            await self.uow.tasks.update(task_id, updated_task_dict)
            await self.uow.commit()
            return TaskResponse.model_validate(updated_task_dict)

    async def delete_task(self, task_id: str) -> None:
        """Delete a task by its ID"""
        async with self.uow:
            task_to_delete = await self.uow.tasks.get_by_id(task_id)
            if not task_to_delete:
                raise HTTPException(status_code=404, detail="Task not found")
            await self.uow.tasks.delete(task_id)
            await self.uow.commit()

    async def get_task_by_id(self, task_id: str) -> TaskResponse:
        """Get a single task by its ID"""
        async with self.uow:
            task = await self.uow.tasks.get_by_id(task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            return TaskResponse.model_validate(task)
