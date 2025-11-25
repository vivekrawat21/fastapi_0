from fastapi import APIRouter, HTTPException, Depends
from app.api.v1.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_services import UserService
from app.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user"""
    return await user_service.create_user(user_create)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Get user by ID"""
    return await user_service.get_user_by_id(user_id)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    """Update user"""
    return await user_service.update_user(user_id, user_update)

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Delete user"""
    await user_service.delete_user(user_id)