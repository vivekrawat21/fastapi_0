from pydantic import BaseModel,Field,EmailStr
from typing import Optional


    
    
class ContactCreate(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(...,example="john.doe@example.com")
    phone: str = Field(..., example="+1234567890")
    

class ContactUpdate(BaseModel):
    name: Optional[str] = Field(None, example="John Doe")
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    phone: Optional[str] = Field(None, example="+1234567890")  


  
    
