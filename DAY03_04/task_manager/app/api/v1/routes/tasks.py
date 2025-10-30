from fastapi import APIRouter,Query
from app.api.v1.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,Status 
from app.utils.files_io import read_tasks, write_tasks
from datetime import date
from typing import Optional

router = APIRouter( prefix="/tasks",tags=["tasks"],)

@router.get("/", response_model=TaskListResponse, status_code=200)
async def list_tasks(status:Optional[Status] = Query(None, description="Filter tasks by status"),
                     due_date:Optional[date] = Query(None, description="Filter tasks by due date"),
                     search:Optional[str] = Query(None, description="Search tasks by title ")):
    """List all tasks"""
    
    tasks = await read_tasks()
    if status:
        tasks = [task for task in tasks if task["status"] == status.strip()]
    if due_date:
        tasks = [task for task in tasks if task["due_date"] == due_date]
    if search:
        tasks = [task for task in tasks if search.strip().lower() in task["title"].lower()]
        
    return TaskListResponse(tasks=tasks)