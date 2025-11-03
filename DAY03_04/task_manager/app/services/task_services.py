from .interfaces.task_service_interfaces import TaskServiceInterface
from typing import Optional
from app.api.v1.schemas import TaskListResponse, TaskCreate, TaskResponse, TaskUpdate
from app.utils.files_io import read_tasks, write_tasks
from app.core.tasks import generate_id
from fastapi import HTTPException
from datetime import date

class TaskService(TaskServiceInterface):
    async def list_tasks(self, status: Optional[str], due_date: Optional[str], search: Optional[str]) -> TaskListResponse:
        """List all tasks according to filters provided"""
        tasks = await read_tasks()
        
        if status:
            tasks = [task for task in tasks if task["status"] == status.strip()]
            if not tasks:
                return TaskListResponse(tasks=[])
        if due_date:
            tasks = [task for task in tasks if task["due_date"] == due_date]
            if not tasks:
                return TaskListResponse(tasks=[])
            
        if search:
            tasks = [task for task in tasks if search.strip().lower() in task["title"].lower()]
            if not tasks:
                raise HTTPException(status_code=404, detail="No tasks found by the given search criteria")
            
        return TaskListResponse(tasks=tasks)
    
    async def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """Create a new task"""
        tasks = await read_tasks()

        new_task = task_data.model_dump()
        new_task["id"] = await generate_id()
        
        tasks.append(new_task)
        await write_tasks(tasks=tasks)
        
        return TaskResponse(**new_task)
    
    async def update_task(self, task_id: str, task_data: TaskUpdate) -> TaskResponse:
        """Update an existing task by its ID"""
        tasks = await read_tasks()
        for index, task in enumerate(tasks):
            if task["id"] == task_id:
                updated_task = task.copy()
                update_data = task_data.model_dump(exclude_unset=True)
                updated_task.update(update_data)
                tasks[index] = updated_task
                await write_tasks(tasks=tasks)
                return TaskResponse(**updated_task)
            
        raise HTTPException(status_code=404, detail="Task not found")
    
    async def delete_task(self, task_id: str) -> None:
        """Delete a task by its ID"""
        tasks = await read_tasks()
        if task_id not in [task["id"] for task in tasks]:
            raise HTTPException(status_code=404, detail="Task not found")
        
        tasks_after_deletion = [task for task in tasks if task["id"] != task_id]
        await write_tasks(tasks=tasks_after_deletion)
        return 
    