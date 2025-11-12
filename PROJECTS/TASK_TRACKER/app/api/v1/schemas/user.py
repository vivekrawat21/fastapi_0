from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union
from app.api.v1.schemas.tasks import TaskResponse

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, json_schema_extra={'example': "John Doe"})
    email: EmailStr = Field(..., json_schema_extra={'example': "john.doe@example.com"})
    is_active: Optional[bool] = Field(default=True, json_schema_extra={'example': True})
    
    
class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50, json_schema_extra={'example': "John Doe"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={'example': "john.doe@example.com"})
    is_active: Optional[bool] = Field(None, json_schema_extra={'example': True})
    
    
class UserResponse(BaseModel):
    id: Union[int, str]
    name: str
    email: EmailStr
    tasks: list[TaskResponse] = []
    is_active: bool