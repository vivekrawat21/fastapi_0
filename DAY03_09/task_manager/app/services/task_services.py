from typing import Optional
from app.api.v1.schemas.tasks import TaskListResponse, TaskCreate, TaskResponse, TaskUpdate
from app.core.tasks import generate_int_id
# compatibility alias for tests that patch 'generate_id'
generate_id = generate_int_id
from fastapi import HTTPException
from datetime import date
from app.unit_of_work import IUnitOfWork

class TaskService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def list_tasks(self, status: Optional[str], due_date: Optional[date], search: Optional[str]) -> TaskListResponse:
        """List all tasks according to filters provided"""
        try:
            async with self.uow:
                tasks = await self.uow.tasks.get_all()

                if status:
                    tasks = [task for task in tasks if task.get("status") == status]
                    if not tasks:
                        raise HTTPException(status_code=404, detail="No tasks found")
                if due_date:
                    tasks = [task for task in tasks if task.get("due_date") == due_date.isoformat()]
                    if not tasks:
                        raise HTTPException(status_code=404, detail="No tasks found")
                if search:
                    tasks = [task for task in tasks if search.lower() in task.get("title", "").lower()]
                    if not tasks:
                        raise HTTPException(status_code=404, detail="No tasks found")

                return TaskListResponse(tasks=[TaskResponse.model_validate(task) for task in tasks])
        except HTTPException:
            # Re-raise HTTPExceptions created by service logic (404 etc.)
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        

    async def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """Create a new task"""
        try:
            async with self.uow:
                new_task_dict = task_data.model_dump()
                new_task_dict["id"] = await generate_id()  # Generate integer ID
                await self.uow.tasks.add(new_task_dict)
                await self.uow.commit()
                return TaskResponse.model_validate(new_task_dict)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_task(self, task_id: int, task_data: TaskUpdate) -> TaskResponse:
        """Update an existing task by its ID"""
        try:
            async with self.uow:
                existing_task = await self.uow.tasks.get_by_id(str(task_id))
                if not existing_task:
                    raise HTTPException(status_code=404, detail="Task not found")

                updated_data = task_data.model_dump(exclude_unset=True)
                existing_task.update(updated_data)

                await self.uow.tasks.update(str(task_id), existing_task)
                await self.uow.commit()

                return TaskResponse.model_validate(existing_task)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        
    async def delete_task(self, task_id: int) -> None:
        """Delete a task by its ID"""
        try:
            async with self.uow:
                existing_task = await self.uow.tasks.get_by_id(str(task_id))
                if not existing_task:
                    raise HTTPException(status_code=404, detail="Task not found")

                await self.uow.tasks.delete(str(task_id))
                await self.uow.commit()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_task_by_id(self, task_id: int) -> TaskResponse:
        """Get a single task by its ID"""
        try:
            async with self.uow:
                task = await self.uow.tasks.get_by_id(str(task_id))
                if not task:
                    raise HTTPException(status_code=404, detail="Task not found")

                return TaskResponse.model_validate(task)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
