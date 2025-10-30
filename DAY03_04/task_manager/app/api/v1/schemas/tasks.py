from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import date


class Priority(str,Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Status(str,Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str]
    priority: Priority
    status: Status
    due_date: date
    
    
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100, example="Buy groceries")
    description: Optional[str] = Field(None, max_length=300, example="Milk, Bread, Eggs")
    priority: Optional[Priority] = Field(default="medium", example="medium")
    status: Optional[Status] = Field(default="pending", example="pending")
    due_date: Optional[date] = Field(default=date.today(), example="2025-12-31")
    
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=100, example="Buy groceries")
    description: Optional[str] = Field(None, max_length=300, example="Milk, Bread, Eggs")
    priority: Optional[Priority] = Field(None, example="medium")
    status: Optional[Status] = Field(None, example="pending")
    due_date: Optional[date] = Field(None, example="2023-12-31")
    
    
class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    priority: Priority
    status: Status
    due_date: date


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]