from fastapi import HTTPException, Depends, APIRouter
from app.database.connection.db_connection import get_db
from app.api.v1.schemas.User import UserCreate, UserResponse
from app.api.v1.schemas.Accounts import AccountResponse
from app.database.crud import create_user, get_user_by_id, update_user, get_accounts_by_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user_controller(data: UserCreate, db=Depends(get_db)) -> UserResponse:
    """Create a new user."""
    user = await create_user(db, data)
    if not user:
        raise HTTPException(status_code=400, detail="User creation failed")
    return user

@router.get("/{user_id}", response_model=UserResponse, status_code=200)
async def get_user_controller(user_id: int, db=Depends(get_db)) -> UserResponse:
    """Retrieve user details by user ID."""
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.put("/{user_id}", response_model=UserResponse, status_code=200)
async def update_user_controller(user_id: int, data: UserCreate, db=Depends(get_db)) -> UserResponse:
    """Update an existing user."""
    user = await update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=400, detail="User update failed")
    return user


@router.get("/{user_id}/accounts", response_model=list[AccountResponse], status_code=200)
async def get_user_accounts_controller(user_id: int, db=Depends(get_db)) -> list[AccountResponse]:
    """Retrieve all accounts for a given user."""
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    accounts = await get_accounts_by_user(db, user_id)
    return accounts