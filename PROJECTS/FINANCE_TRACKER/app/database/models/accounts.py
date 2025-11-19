from datetime import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
import enum
from app.database.base import Base

class AccountType(str, enum.Enum):
    SAVINGS = "savings"
    CREDIT = "credit"


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    balance = Column(Float, default=0.0)
    type = Column(Enum(AccountType), nullable=False)
    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account')
    payments_made = relationship('Payment', foreign_keys='Payment.from_account_id', back_populates='from_account')
    payments_received = relationship('Payment', foreign_keys='Payment.to_account_id', back_populates='to_account')
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)