"""User schemas for API requests and responses."""

from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields."""
    name: str = Field(..., min_length=2, max_length=100, json_schema_extra={'example': "John Doe"})
    email: str = Field(..., min_length=5, max_length=254, json_schema_extra={'example': "john.doe@example.com"})


class UserCreate(UserBase):
    """Schema for creating a new user."""
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
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserListResponse(BaseModel):
    """Schema for user list response."""
    users: list[UserResponse]