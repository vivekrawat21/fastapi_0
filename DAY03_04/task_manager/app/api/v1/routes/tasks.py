from fastapi import APIRouter,Query
from app.api.v1.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,Status ,Task
from app.utils.files_io import read_tasks, write_tasks
from app.core import generate_id
from datetime import date
from typing import Optional

router = APIRouter( prefix="/tasks",tags=["tasks"],)

@router.get("/", response_model=TaskListResponse, status_code=200)
async def list_tasks(status:Optional[Status] = Query(None, description="Filter tasks by status"),
                     due_date:Optional[date] = Query(None, description="Filter tasks by due date"),
                     search:Optional[str] = Query(None, description="Search tasks by title ")):
    """List all tasks Accordin to filters provided"""
    
    tasks = await read_tasks()
    
    if status:
        tasks = [task for task in tasks if task["status"] == status.strip()]
    if due_date:
        tasks = [task for task in tasks if task["due_date"] == due_date]
    if search:
        tasks = [task for task in tasks if search.strip().lower() in task["title"].lower()]
        
    return TaskListResponse(tasks=tasks)

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task_create: TaskCreate):
    """Create a new task"""
    tasks = await read_tasks()

    new_task = task_create.dict()
    new_task["id"] = await generate_id()
    
    tasks.append(new_task)
    await write_tasks(tasks=tasks)
    
    return TaskResponse(**new_task)
    
    
