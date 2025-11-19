from fastapi import APIRouter, Depends, HTTPException
from app.database.connection.db_connection import get_db
from  app.api.v1.schemas.Accounts import AccountCreate, AccountResponse,AccountUpdate
from app.database.crud import create_account,get_account_by_id,update_account,get_all_accounts


router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/", response_model=AccountResponse, status_code=201)
async def create(data: AccountCreate, db=Depends(get_db)) -> AccountResponse:
    """Create a new account for a user."""
    account = await create_account(db, data)
    if not account:
        raise HTTPException(status_code=400, detail="Account creation failed")
    return account

@router.get("/{account_id}", response_model=AccountResponse, status_code=200)
async def get_account(account_id: int, db=Depends(get_db)) -> AccountResponse:
    """Retrieve account details by account ID."""
    account = await get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/{account_id}", response_model=AccountResponse, status_code=200)
async def update(account_id: int, data: AccountUpdate, db=Depends(get_db)) -> AccountResponse:
    """Update an existing account."""
    account = await update_account(db, account_id, data)
    if not account:
        raise HTTPException(status_code=400, detail="Account update failed")
    return account



@router.get("/", response_model=list[AccountResponse], status_code=200)
async def get_accounts(db=Depends(get_db)) -> list[AccountResponse]:
    """Retrieve all accounts."""
    accounts = await get_all_accounts(db)
    return accounts