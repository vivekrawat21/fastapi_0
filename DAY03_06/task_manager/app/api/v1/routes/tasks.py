from fastapi import APIRouter, Query, Path, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.schemas.tasks import TaskCreate, TaskUpdate, TaskResponse, Task
from app.services.task_services import TaskService
from app.core.models import Task as TaskModel
from datetime import date
from typing import Optional, List
from app.dependencies import get_task_service, get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskResponse], status_code=200)
async def list_tasks(
    status: Optional[str] = Query(None, description="Filter tasks by status"),
    due_date: Optional[date] = Query(None, description="Filter tasks by due date"),
    search: Optional[str] = Query(None, description="Search tasks by title"),
    task_service: TaskService = Depends(get_task_service),
    db: AsyncSession = Depends(get_db)
):
    """List all tasks according to filters provided"""
    result = await task_service.list_tasks(
        status=status,
        due_date=due_date,
        search=search
    )
    return result.tasks

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task_create: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
    db: AsyncSession = Depends(get_db)
):
    """Create a new task"""
    return await task_service.create_task(task_create)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int = Path(..., description="The ID of the task to delete"),
    task_service: TaskService = Depends(get_task_service),
    db: AsyncSession = Depends(get_db)
):
    """Delete a task by its ID"""
    await task_service.delete_task(task_id)


@router.put("/{task_id}", response_model=TaskResponse, status_code=200)
async def update_task(
    task_id: int = Path(..., description="The ID of the task to update"),
    task_update: TaskUpdate = ...,
    task_service: TaskService = Depends(get_task_service),
    db: AsyncSession = Depends(get_db)
):
    """Update a task by its ID"""
    return await task_service.update_task(task_id, task_update)


@router.get("/{task_id}", response_model=TaskResponse, status_code=200)
async def get_task(
    task_id: int = Path(..., description="The ID of the task to retrieve"),
    task_service: TaskService = Depends(get_task_service),
    db: AsyncSession = Depends(get_db)
):
    """Get a task by its ID"""
    return await task_service.get_task_by_id(task_id)
