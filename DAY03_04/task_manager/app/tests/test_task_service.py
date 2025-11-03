import pytest
from unittest.mock import AsyncMock, patch
from app.services.task_services import TaskService
from app.api.v1.schemas import TaskCreate, TaskUpdate, TaskListResponse, TaskResponse
from fastapi import HTTPException
from datetime import date

@pytest.fixture
def task_service():
    return TaskService()

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

@pytest.mark.anyio
@patch('app.services.task_services.read_tasks')
async def test_list_tasks_no_filters(mock_read_tasks, task_service, sample_tasks):
    mock_read_tasks.return_value = sample_tasks
    result = await task_service.list_tasks(None, None, None)
    assert isinstance(result, TaskListResponse)
    assert len(result.tasks) == 2


@pytest.mark.anyio
@patch('app.services.task_services.read_tasks')
async def test_list_tasks_with_status_filter(mock_read_tasks, task_service, sample_tasks):
    mock_read_tasks.return_value = sample_tasks
    result = await task_service.list_tasks("pending", None, None)
    assert len(result.tasks) == 1
    assert result.tasks[0].status == "pending"


@pytest.mark.anyio
@patch('app.services.task_services.read_tasks')
async def test_list_tasks_with_search_no_match(mock_read_tasks, task_service, sample_tasks):
    mock_read_tasks.return_value = sample_tasks
    with pytest.raises(HTTPException) as exc_info:
        await task_service.list_tasks(None, None, "nonexistent")
    assert exc_info.value.status_code == 404


@pytest.mark.anyio
@patch('app.services.task_services.read_tasks')
@patch('app.services.task_services.write_tasks')
@patch('app.services.task_services.generate_id', return_value="new-id")
async def test_create_task(mock_generate_id, mock_write_tasks, mock_read_tasks, task_service, sample_tasks):
    mock_read_tasks.return_value = sample_tasks
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
    mock_write_tasks.assert_called_once()



@pytest.mark.anyio
@patch('app.services.task_services.read_tasks')
@patch('app.services.task_services.write_tasks')
async def test_update_task(mock_write_tasks, mock_read_tasks, task_service, sample_tasks):
    mock_read_tasks.return_value = sample_tasks
    task_update = TaskUpdate(title="Updated Title")
    result = await task_service.update_task("1", task_update)
    assert result.title == "Updated Title"
    mock_write_tasks.assert_called_once()

@pytest.mark.anyio
@patch('app.services.task_services.read_tasks')
@patch('app.services.task_services.write_tasks')
async def test_delete_task(mock_write_tasks, mock_read_tasks, task_service, sample_tasks):
    mock_read_tasks.return_value = sample_tasks
    await task_service.delete_task("1")
    mock_write_tasks.assert_called_once()


@pytest.mark.anyio
@patch('app.services.task_services.read_tasks')
async def test_update_task_not_found(mock_read_tasks, task_service):
    mock_read_tasks.return_value = []
    with pytest.raises(HTTPException) as exc_info:
        await task_service.update_task("nonexistent", TaskUpdate())
    assert exc_info.value.status_code == 404
