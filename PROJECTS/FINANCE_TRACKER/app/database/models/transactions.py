from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from app.database.base import Base

class TransactionType(str, enum.Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    
    
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)  
    account = relationship('Account', back_populates='transactions')
    payments = relationship('Payment', back_populates='transaction')
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    