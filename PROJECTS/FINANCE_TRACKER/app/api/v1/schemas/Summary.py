from pydantic import BaseModel, Field
from typing import Annotated, List
from datetime import datetime
from app.database.models.accounts import AccountType
from .Transactions import TransactionResponse
from .Payments import PaymentResponse

class SummaryResponse(BaseModel):
    id: int
    user_id: int
    balance: float
    type: AccountType
    is_active: int
    created_at: datetime
    updated_at: datetime
    payments_made: List[PaymentResponse]
    payments_received: List[PaymentResponse]
    
    class Config:
        from_attributes = True 
        
    