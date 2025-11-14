from fastapi import APIRouter, Query, Path, HTTPException, Depends
from app.api.v1.schemas.tasks import TaskCreate, TaskUpdate, TaskResponse, PaginatedTaskResponse
from app.services.task_services import TaskService
from datetime import date
from typing import Optional, List
from app.dependencies import get_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=PaginatedTaskResponse, status_code=200)
async def list_tasks(
    status: Optional[str] = Query(None, description="Filter tasks by status"),
    due_date: Optional[date] = Query(None, description="Filter tasks by due date"),
    search: Optional[str] = Query(None, description="Search tasks by title"),
    skip: int = Query(0, ge=0, description="Number of tasks to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Number of tasks to return (max 1000)"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order: asc or desc"),
    task_service: TaskService = Depends(get_task_service)
):
    """List all tasks with pagination, filtering, and sorting"""
    result = await task_service.list_tasks(
        status=status,
        due_date=due_date,
        search=search,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    task_responses = [TaskResponse.model_validate(task) for task in result["tasks"]]
    
    return PaginatedTaskResponse(
        items=task_responses,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
        has_next=result["has_next"],
        has_previous=result["has_previous"]
    )


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task_create: TaskCreate,
    task_service: TaskService = Depends(get_task_service)
):
    """Create a new task"""
    return await task_service.create_task(task_create)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int = Path(..., description="The ID of the task to delete"),
    task_service: TaskService = Depends(get_task_service)
):
    """Delete a task by its ID"""
    await task_service.delete_task(task_id)


@router.put("/{task_id}", response_model=TaskResponse, status_code=200)
async def update_task(
    task_id: int = Path(..., description="The ID of the task to update"),
    task_update: TaskUpdate = ...,
    task_service: TaskService = Depends(get_task_service)
):
    """Update a task by its ID"""
    return await task_service.update_task(task_id, task_update)


@router.get("/{task_id}", response_model=TaskResponse, status_code=200)
async def get_task(
    task_id: int = Path(..., description="The ID of the task to retrieve"),
    task_service: TaskService = Depends(get_task_service)
):
    """Get a task by its ID"""
    return await task_service.get_task_by_id(task_id)
