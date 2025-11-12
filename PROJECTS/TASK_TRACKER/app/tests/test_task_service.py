import pytest
from unittest.mock import AsyncMock, patch
from app.services.task_services import TaskService
from app.api.v1.schemas.tasks import TaskCreate, TaskUpdate, TaskListResponse, TaskResponse
from fastapi import HTTPException
from datetime import date
from app.unit_of_work import IUnitOfWork
from app.repositories.interfaces.task_repository_interface import ITaskRepository

@pytest.fixture
def mock_task_repo() -> AsyncMock:
    """Fixture for a mocked task repository."""
    return AsyncMock(spec=ITaskRepository)

@pytest.fixture
def mock_uow(mock_task_repo: AsyncMock) -> AsyncMock:
    """Fixture for a mocked Unit of Work that supports 'async with'."""
    uow = AsyncMock(spec=IUnitOfWork)
    uow.tasks = mock_task_repo
    # support async context manager used by TaskService
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)
    return uow

@pytest.fixture
def task_service(mock_uow: AsyncMock) -> TaskService:
    """Fixture for the TaskService, initialized with a mock UoW."""
    return TaskService(uow=mock_uow)

@pytest.fixture
def sample_tasks():
    return [
        {
            "id": "1",
            "title": "Task 1",
            "description": "Desc 1",
            "status": "pending",
            "priority": "high",
            "due_date": "2025-12-01"
        },
        {
            "id": "2",
            "title": "Task 2",
            "description": "Desc 2",
            "status": "completed",
            "priority": "low",
            "due_date": "2025-12-02"
        }
    ]

@pytest.mark.asyncio
async def test_list_tasks_no_filters(task_service: TaskService, mock_task_repo: AsyncMock, sample_tasks):
    mock_task_repo.get_all.return_value = sample_tasks
    
    result = await task_service.list_tasks(None, None, None)
    
    assert isinstance(result, TaskListResponse)
    assert len(result.tasks) == 2
    mock_task_repo.get_all.assert_called_once()

@pytest.mark.asyncio
async def test_list_tasks_with_status_filter(task_service: TaskService, mock_task_repo: AsyncMock, sample_tasks):
    mock_task_repo.get_all.return_value = sample_tasks
    
    result = await task_service.list_tasks("pending", None, None)
    
    assert len(result.tasks) == 1
    assert result.tasks[0].status == "pending"

@pytest.mark.asyncio
async def test_list_tasks_with_search_no_match(task_service: TaskService, mock_task_repo: AsyncMock, sample_tasks):
    mock_task_repo.get_all.return_value = sample_tasks
    
    with pytest.raises(HTTPException) as exc_info:
        await task_service.list_tasks(None, None, "nonexistent")
    
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
@patch('app.services.task_services.generate_id', new_callable=AsyncMock)
async def test_create_task(mock_generate_id, task_service: TaskService, mock_uow: AsyncMock):
    mock_generate_id.return_value = "new-id"
    task_data = TaskCreate(
        title="New Task",
        description="New Desc",
        priority="medium",
        status="pending",
        due_date=date.today()
    )
    
    result = await task_service.create_task(task_data)
    
    assert isinstance(result, TaskResponse)
    assert result.title == "New Task"
    assert result.id == "new-id"
    mock_uow.tasks.add.assert_called_once()
    mock_uow.commit.assert_called_once()

@pytest.mark.asyncio
async def test_update_task(task_service: TaskService, mock_uow: AsyncMock, sample_tasks):
    mock_uow.tasks.get_by_id.return_value = sample_tasks[0]
    task_update = TaskUpdate(title="Updated Title")
    
    result = await task_service.update_task(1, task_update)
    
    assert result.title == "Updated Title"
    mock_uow.tasks.get_by_id.assert_called_once_with("1")
    mock_uow.tasks.update.assert_called_once()
    mock_uow.commit.assert_called_once()

@pytest.mark.asyncio
async def test_delete_task(task_service: TaskService, mock_uow: AsyncMock, sample_tasks):
    mock_uow.tasks.get_by_id.return_value = sample_tasks[0]
    
    await task_service.delete_task(1)
    
    mock_uow.tasks.get_by_id.assert_called_once_with("1")
    mock_uow.tasks.delete.assert_called_once_with("1")
    mock_uow.commit.assert_called_once()

@pytest.mark.asyncio
async def test_update_task_not_found(task_service: TaskService, mock_uow: AsyncMock):
    mock_uow.tasks.get_by_id.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        await task_service.update_task(999, TaskUpdate())
    
    assert exc_info.value.status_code == 404
    mock_uow.commit.assert_not_called()