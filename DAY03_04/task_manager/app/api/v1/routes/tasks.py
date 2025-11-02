from fastapi import APIRouter,Query,Path, HTTPException, Depends
from app.api.v1.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,Status ,Task
from app.services.task_services import TaskService
from app.services.interfaces.task_service_interfaces import TaskServiceInterface
from datetime import date
from typing import Optional
from app.utils.files_io import read_tasks, write_tasks

router = APIRouter( prefix="/tasks",tags=["tasks"],)

def get_task_service() -> TaskServiceInterface:
    return TaskService()


@router.get("", response_model=TaskListResponse, status_code=200)
async def list_tasks(status:Optional[Status] = Query(None, description="Filter tasks by status"),
                     due_date:Optional[date] = Query(None, description="Filter tasks by due date"),
                     search:Optional[str] = Query(None, description="Search tasks by title "),
                     task_service: TaskServiceInterface = Depends(get_task_service)):
    """List all tasks Accordin to filters provided"""
    
    return await task_service.list_tasks(status=status.value if status else None,
                                         due_date=str(due_date) if due_date else None,
                                         search=search)

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task_create: TaskCreate,
                      task_service: TaskServiceInterface = Depends(get_task_service)):
    """Create a new task"""
    return await task_service.create_task(task_create)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str = Path(..., description="The ID of the task to delete"),
                      task_service: TaskServiceInterface = Depends(get_task_service)):
    """Delete a task by its ID"""
    await task_service.delete_task(task_id)
     


@router.put("/{task_id}", response_model=TaskResponse, status_code=200)
async def update_task(task_id: str = Path(..., description="The ID of the task to update"), task_update: TaskUpdate = ...):
    """Update a task by its ID"""
    task_service = get_task_service()
    return await task_service.update_task(task_id, task_update)



@router.get("/{task_id}", response_model=TaskResponse, status_code=200)
async def get_task(task_id: str = Path(..., description="The ID of the task to retrieve")):
    """Get a task by its ID"""
    tasks = await read_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return TaskResponse(**task)
    
    raise HTTPException(status_code=404, detail="Task not found")
