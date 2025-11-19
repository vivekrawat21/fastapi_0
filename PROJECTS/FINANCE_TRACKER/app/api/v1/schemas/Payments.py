from pydantic import BaseModel, EmailStr,Field
from typing import Optional, Annotated
from datetime import datetime
from app.database.models.payments import PaymentMethod

class PaymentBase(BaseModel):
    from_account_id: Annotated[int, Field(description="ID of the account from which payment is made")]
    to_account_id: Annotated[int, Field(description="ID of the account to which payment is made")]
    amount: Annotated[float, Field(description="Amount of the payment")]
    method: Annotated[PaymentMethod, Field(description="Method of payment (card, bank_transfer, cash, upi)")]

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    from_account_id: Optional[int] = None
    to_account_id: Optional[int] = None
    method: Optional[PaymentMethod] = None
    amount: Optional[float] = None
    
class PaymentResponse(PaymentBase):
    id: int
    amount: float
    method: PaymentMethod
    transaction_id: int
    to_account_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True