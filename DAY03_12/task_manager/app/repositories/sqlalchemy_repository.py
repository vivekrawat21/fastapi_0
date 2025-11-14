from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload
from app.core.models import Task, User
from app.repositories.interfaces.task_repository_interface import ITaskRepository


class SQLAlchemyTaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        result = {
            "id": task.id, 
            "user_id": task.user_id, 
            "title": task.title,
            "description": task.description,
            "priority": task.priority.value if task.priority else None,
            "status": task.status.value if task.status else None,
            "due_date": task.due_date.date() if task.due_date else None,
        }
        
        if task.user:
            result["user"] = {
                "id": task.user.id,
                "name": task.user.name,
                "email": task.user.email,
                "is_active": task.user.is_active,
                "created_at": task.user.created_at,
                "updated_at": task.user.updated_at
            }
        else:
            result["user"] = None
            
        return result

    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        status_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        
        query = select(Task).options(selectinload(Task.user))
        
        if status_filter:
            query = query.where(Task.status == status_filter)
        
        if hasattr(Task, sort_by):
            if sort_order.lower() == "desc":
                query = query.order_by(getattr(Task, sort_by).desc())
            else:
                query = query.order_by(getattr(Task, sort_by).asc())
        
        paginated_query = query.offset(skip).limit(limit)
        
        count_query = select(func.count(Task.id))
        if status_filter:
            count_query = count_query.where(Task.status == status_filter)
        
        result = await self.session.execute(paginated_query)
        count_result = await self.session.execute(count_query)
        
        tasks = result.scalars().all()
        total = count_result.scalar()
        
        return {
            "items": [self._task_to_dict(task) for task in tasks],
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_next": skip + limit < total,
            "has_previous": skip > 0
        }

    async def get_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        result = await self.session.execute(
            select(Task).options(selectinload(Task.user)).where(Task.id == int(task_id))
        )
        task = result.scalar_one_or_none()
        return self._task_to_dict(task) if task else None

    async def add(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        task = Task(
            title=task_data["title"],
            description=task_data.get("description"),
            priority=task_data.get("priority"),
            status=task_data.get("status"),
            due_date=task_data.get("due_date"),
            user_id=task_data.get("user_id"),
        )
        self.session.add(task)
        
        await self.session.flush()
        await self.session.refresh(task, ["user"])
        return self._task_to_dict(task)

    async def update(self, task_id: str, task_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        update_data = {k: v for k, v in task_data.items() if k != 'id'}
        
        if update_data:  
            await self.session.execute(
                update(Task)
                .where(Task.id == int(task_id))
                .values(**update_data)
            )
            await self.session.flush()
        
        return await self.get_by_id(task_id)

    async def delete(self, task_id: str):
        await self.session.execute(
            delete(Task).where(Task.id == int(task_id))
        )