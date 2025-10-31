from fastapi import APIRouter,Query,Path, HTTPException
from app.api.v1.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,Status ,Task
from app.utils.files_io import read_tasks, write_tasks
from app.core import generate_id
from datetime import date
from typing import Optional

router = APIRouter( prefix="/tasks",tags=["tasks"],)

@router.get("", response_model=TaskListResponse, status_code=200)
async def list_tasks(status:Optional[Status] = Query(None, description="Filter tasks by status"),
                     due_date:Optional[date] = Query(None, description="Filter tasks by due date"),
                     search:Optional[str] = Query(None, description="Search tasks by title ")):
    """List all tasks Accordin to filters provided"""
    
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


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task_create: TaskCreate):
    """Create a new task"""
    tasks = await read_tasks()

    new_task = task_create.dict()
    new_task["id"] = await generate_id()
    
    tasks.append(new_task)
    await write_tasks(tasks=tasks)
    
    return TaskResponse(**new_task)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str = Path(..., description="The ID of the task to delete")):
    """Delete a task by its ID"""
    tasks = await read_tasks()
    if task_id not in [task["id"] for task in tasks]:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks_after_deletion = [task for task in tasks if task["id"] != task_id]
    await write_tasks(tasks=tasks_after_deletion)
    return 


@router.put("/{task_id}", response_model=TaskResponse, status_code=200)
async def update_task(task_id: str = Path(..., description="The ID of the task to update"), task_update: TaskUpdate = ...):
    """Update a task by its ID"""
    existing_tasks = await read_tasks()
    is_id_found = False
    updated_task = {}
    for task in existing_tasks:
        if task["id"] == task_id:
            is_id_found = True
            updated_data = task_update.model_dump(exclude_unset=True)
            for key,value in updated_data.items():
                task[key] = value
            updated_task = task

    if not is_id_found:
        raise HTTPException(status_code=404, detail="Task not found")

    await write_tasks(tasks=existing_tasks)
    return TaskResponse(**updated_task)



@router.get("/{task_id}", response_model=TaskResponse, status_code=200)
async def get_task(task_id: str = Path(..., description="The ID of the task to retrieve")):
    """Get a task by its ID"""
    tasks = await read_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return TaskResponse(**task)
    
    raise HTTPException(status_code=404, detail="Task not found")
