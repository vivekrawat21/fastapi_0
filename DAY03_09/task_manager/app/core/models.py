from sqlalchemy import Column, Integer, String,  Text,Boolean, DateTime, func, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from app.api.v1.schemas.tasks import Priority, Status

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(SQLEnum(Priority, name='task_priority'), default=Priority.medium)
    status = Column(SQLEnum(Status, name='task_status'), default=Status.pending)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())