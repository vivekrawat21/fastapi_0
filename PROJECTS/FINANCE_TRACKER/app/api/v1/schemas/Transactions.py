from pydantic import BaseModel, EmailStr,Field
from typing import Optional, Annotated
from datetime import datetime
from app.database.models.transactions import TransactionType

class TransactionBase(BaseModel):
    description: Optional[Annotated[str, Field(max_length=255, description="Description of the transaction")]] = None
    amount: Annotated[float, Field(description="Amount of the transaction")]
    account_id: Annotated[int, Field(description="ID of the account associated with the transaction")]
    transaction_type: Annotated[TransactionType, Field(description="Type of the transaction (credit, debit)")]
    
    
    
    
class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    description: Optional[Annotated[str, Field(max_length=255, description="Description of the transaction")]] = None
    amount: Optional[Annotated[float, Field(description="Amount of the transaction")]] = None
    transaction_type: Optional[Annotated[TransactionType, Field(description="Type of the transaction (credit, debit)")]] = None
    is_active: Optional[int] = None
    
    
class TransactionResponse(TransactionBase):
    id: int
    amount: float
    transaction_type: TransactionType
    account_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    