from pydantic import BaseModel, EmailStr,Field
from typing import Optional,Annotated
from datetime import datetime

class UserBase(BaseModel):
    name: Annotated[str, Field(max_length=100,description="name of the user")]
    email: Annotated[EmailStr, Field(max_length=100,description="email of the user")]
    is_active: Optional[int] = 1

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[Annotated[str, Field(max_length=100,description="name of the user")]] = None
    email: Optional[Annotated[EmailStr, Field(max_length=100,description="email of the user")]] = None
    is_active: Optional[int] = None
    
class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True