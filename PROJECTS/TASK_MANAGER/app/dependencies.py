from fastapi import Depends

from app.unit_of_work import JsonUnitOfWork, IUnitOfWork
from app.services.task_services import TaskService


def get_uow() -> IUnitOfWork:
    return JsonUnitOfWork()


def get_task_service(uow: IUnitOfWork = Depends(get_uow)) -> TaskService:
    return TaskService(uow)
