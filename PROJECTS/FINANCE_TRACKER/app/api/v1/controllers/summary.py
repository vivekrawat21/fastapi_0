from fastapi import APIRouter, Depends, HTTPException, status
from app.database.connection.db_connection import get_db
from app.api.v1.schemas.Summary import SummaryResponse
from app.database.crud import get_account_by_id

router = APIRouter(prefix="/summary", tags=["summary"])
@router.get("/account/{account_id}", response_model=SummaryResponse, status_code=status.HTTP_200_OK)
async def get_account_summary(account_id: int, db=Depends(get_db)) :
    """Retrieve summary details for a given account."""
    account = await get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    print(account)
    
    # Assuming SummaryResponse has fields: id, name, balance, created_at

    return account