from pydantic import BaseModel, Field
from typing import Optional, Union
from enum import Enum
from datetime import date
from app.api.v1.schemas.user import UserBase


class Priority(str,Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Status(str,Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    

class Task(BaseModel):
    id: Union[int, str]
    title: str
    description: Optional[str]
    priority: Priority
    status: Status
    due_date: date
    
    
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100, json_schema_extra={'example': "Buy groceries"})
    description: Optional[str] = Field(None, max_length=300, json_schema_extra={'example': "Milk, Bread, Eggs"})
    priority: Optional[Priority] = Field(default="medium", json_schema_extra={'example': "medium"})
    status: Optional[Status] = Field(default="pending", json_schema_extra={'example': "pending"})
    due_date: Optional[date] = Field(default=date.today(), json_schema_extra={'example': "2025-12-31"})
    
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=100, json_schema_extra={'example': "Buy groceries"})
    description: Optional[str] = Field(None, max_length=300, json_schema_extra={'example': "Milk, Bread, Eggs"})
    priority: Optional[Priority] = Field(None, json_schema_extra={'example': "medium"})
    status: Optional[Status] = Field(None, json_schema_extra={'example': "pending"})
    due_date: Optional[date] = Field(None, json_schema_extra={'example': "2023-12-31"})
    
    
class TaskResponse(BaseModel):
    id: Union[int, str]
    user_id: Optional[Union[int, str]]
    user: list[UserBase] = []
    title: str
    description: Optional[str]
    priority: Priority
    status: Status
    due_date: Optional[date]


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]