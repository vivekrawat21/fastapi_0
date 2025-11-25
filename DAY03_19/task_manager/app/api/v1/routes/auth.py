from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.api.v1.schemas.user import UserResponse
from app.services.user_services import UserService
from app.dependencies import get_user_service

class LoginRequest(BaseModel):
    username: str

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserResponse)
async def login(
    login_request: LoginRequest,
    user_service: UserService = Depends(get_user_service)
):
    """Login with username, create if not exists"""
    user = await user_service.get_user_by_name(login_request.username)
    if not user:
        user = await user_service.create_user_from_name(login_request.username)
    return user