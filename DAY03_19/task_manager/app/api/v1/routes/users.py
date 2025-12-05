from fastapi import APIRouter, HTTPException, Depends, Query
from app.api.v1.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_services import UserService
from app.dependencies import get_user_service, get_current_user, get_admin_user, get_admin_or_supervisor
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=dict)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserResponse = Depends(get_admin_or_supervisor),
    user_service: UserService = Depends(get_user_service)
):
    """List all users (Admin & Supervisor only)"""
    return await user_service.get_all_users(skip, limit)


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_create: UserCreate,
    current_user: UserResponse = Depends(get_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user (Admin only)"""
    return await user_service.create_user(user_create)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: UserResponse = Depends(get_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """Get user by ID (Admin only)"""
    return await user_service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: UserResponse = Depends(get_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """Update user (Admin only)"""
    return await user_service.update_user(user_id, user_update)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    current_user: UserResponse = Depends(get_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """Delete user (Admin only)"""
    await user_service.delete_user(user_id)