from fastapi import APIRouter, Depends
from typing import List, Optional
from datetime import date

from app.api.v1.schemas.tasks import TaskCreate, TaskUpdate, TaskListResponse, TaskResponse
from app.services.task_services import TaskService
from app.dependencies import get_task_service

router = APIRouter()

@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    status: Optional[str] = None,
    due_date: Optional[date] = None,
    search: Optional[str] = None,
    service: TaskService = Depends(get_task_service)
):
    return await service.list_tasks(status, due_date, search)

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service)
):
    return await service.create_task(task_data)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    return await service.update_task(task_id, task_data)

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    await service.delete_task(task_id)
    return

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    return await service.get_task_by_id(task_id)
