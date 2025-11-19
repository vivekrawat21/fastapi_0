from fastapi import APIRouter, Depends, HTTPException, status
from app.database.connection.db_connection import get_db
from app.api.v1.schemas.Transactions import TransactionCreate, TransactionResponse
from app.database.crud import create_payment,get_payment_by_id,update_payment
from app.database.crud import  get_transaction_by_id,get_account_transactions,get_all_transactions


router = APIRouter(prefix="/transactions", tags=["transactions"])
@router.get("/all", response_model=list[TransactionResponse], status_code=status.HTTP_200_OK)
async def all_transactions(db=Depends(get_db)) -> list[TransactionResponse]:
     """Retrieve all transactions."""
     transactions = await get_all_transactions(db)
     return transactions

@router.get("/account/{account_id}", response_model=list[TransactionResponse], status_code=status.HTTP_200_OK)
async def get_transactions_for_account(account_id: int, db=Depends(get_db)) -> list[TransactionResponse]:
    """Retrieve all transactions for a given account."""
    transactions = await get_account_transactions(db, account_id)
    return transactions

@router.get("/{transaction_id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
async def get_transaction(transaction_id: int, db=Depends(get_db)) -> TransactionResponse:
    """Retrieve transaction details by transaction ID."""
    transaction = await get_transaction_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction