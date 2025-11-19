from pydantic import BaseModel, EmailStr,Field
from typing import Optional, Annotated
from datetime import datetime
from app.database.models.accounts import AccountType

class AccountBase(BaseModel):
    balance: Annotated[float, Field(description="Balance of the account")]
    user_id: Annotated[int, Field(description="ID of the user owning the account")]
    type: Annotated[AccountType, Field(description="Type of the account (savings, credit)")]
    is_active: Optional[int] = 1
    
    
class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    name: Optional[Annotated[str, Field(max_length=100, description="Name of the account")]] = None
    balance: Optional[Annotated[float, Field(description="Balance of the account")]] = None
    type: Optional[Annotated[AccountType, Field(description="Type of the account (savings, credit)")]] = None
    is_active: Optional[int] = None
    
    
class AccountResponse(AccountBase):
    id: int
    balance: float
    type: AccountType
    created_at: datetime
    updated_at: datetime
    

    class Config:
        from_attributes = True