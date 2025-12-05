from fastapi import APIRouter, HTTPException, Depends, Response, Cookie
from pydantic import BaseModel
from app.api.v1.schemas.user import UserResponse
from app.services.user_services import UserService
from app.dependencies import get_user_service, get_current_user
from app.core.security import verify_password
from app.core.security import create_access_token, create_referesh_token, decode_token

from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str  

class RegisterRequest(BaseModel):
    email: str
    name: str
    password: str
    role: str = "COLLECTOR"

class LoginResponse(BaseModel):
    type: Optional[str] = "Bearer"
    access_token: str

class SubscriptionRequest(BaseModel):
    plan: str 

class SubscriptionResponse(BaseModel):
    message: str
    user: UserResponse
    new_role: str

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(
    login_request: LoginRequest,
    response: Response,
    user_service: UserService = Depends(get_user_service)
):
    """Login with username, create if not exists"""
    user = await user_service.get_user_by_email(login_request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(login_request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email, "role": user.role.value})
    refresh_token = create_referesh_token(data={"sub": user.email, "role": user.role.value})
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,     
        secure=False,    
        samesite="lax", 
        max_age=7 * 24 * 60 * 60  
    )
    
    return LoginResponse(access_token=access_token)

@router.post("/register", response_model=UserResponse)
async def register(
    register_request: RegisterRequest,
    user_service: UserService = Depends(get_user_service)
):
    """Register a new user"""
    user = await user_service.create_user_auth(register_request.name, register_request.email, register_request.password, register_request.role)
    return user


@router.post("/refresh", response_model=LoginResponse)
async def refresh(
    refresh_token: str = Cookie(None),
    user_service: UserService = Depends(get_user_service)
):
    """Refresh access token using refresh token from cookies"""
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
    payload = decode_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    email = payload.get("sub")
    role = payload.get("role")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    access_token = create_access_token(data={"sub": email, "role": role})
    
    return LoginResponse(access_token=access_token)


@router.post("/subscribe", response_model=SubscriptionResponse)
async def subscribe_to_plan(
    subscription: SubscriptionRequest,
    current_user: UserResponse = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Subscribe to Pro plan and upgrade to SUPERVISOR role"""
    if subscription.plan.lower() not in ["pro", "enterprise"]:
        raise HTTPException(status_code=400, detail="Invalid plan. Choose 'pro' or 'enterprise'")
    
    role_str = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    
    if role_str == "ADMIN":
        raise HTTPException(status_code=400, detail="Admin users cannot change their role")
    
    if role_str == "SUPERVISOR":
        return SubscriptionResponse(
            message="You already have an active Pro subscription!",
            user=current_user,
            new_role="SUPERVISOR"
        )
    updated_user = await user_service.upgrade_to_supervisor(current_user.id)
    
    return SubscriptionResponse(
        message=f"Successfully subscribed to {subscription.plan} plan!",
        user=updated_user,
        new_role="SUPERVISOR"
    )
    