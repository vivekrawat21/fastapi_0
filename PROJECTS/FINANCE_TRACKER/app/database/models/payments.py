from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum,Float
from sqlalchemy.orm import relationship
import enum
from app.database.base import Base

class PaymentMethod(str, enum.Enum):
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"
    UPI = "upi"
    
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    from_account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    to_account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    method = Column(Enum(PaymentMethod), nullable=False) 
    from_account = relationship('Account', foreign_keys=[from_account_id], back_populates='payments_made')
    to_account = relationship('Account', foreign_keys=[to_account_id], back_populates='payments_received')
    transaction = relationship('Transaction', back_populates='payments')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
