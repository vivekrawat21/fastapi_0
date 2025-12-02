"""User schemas for API requests and responses."""

from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "Admin"
    COLLECTOR = "Collector"
    SUPERVISOR = "Supervisor"


class UserBase(BaseModel):
    """Base user schema with common fields."""
    name: str = Field(..., min_length=2, max_length=100, json_schema_extra={'example': "John Doe"})
    email: str = Field(..., min_length=5, max_length=254, json_schema_extra={'example': "john.doe@example.com"})
    role: UserRole = Field(default=UserRole.COLLECTOR, json_schema_extra={'example': "Collector"})
    


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=128, json_schema_extra={'example': "strongpassword123"})
    pass


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    name: Optional[str] = Field(None, min_length=2, max_length=100, json_schema_extra={'example': "John Doe"})
    email: Optional[str] = Field(None, min_length=5, max_length=254, json_schema_extra={'example': "john.doe@example.com"})
    is_active: Optional[bool] = Field(None, json_schema_extra={'example': True})


class UserResponse(BaseModel):
    """Schema for user response."""
    id: Union[int, str]
    name: str
    email: str
    role: UserRole
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Schema for user list response."""
    users: list[UserResponse]