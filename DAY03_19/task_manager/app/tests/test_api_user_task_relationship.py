"""API integration tests for User-Task relationship functionality."""

import pytest
import asyncio
from datetime import datetime, timedelta
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch

from app.main import app
from app.core.models import User, Task
from app.api.v1.schemas.tasks import Priority, Status
from app.core.database import AsyncSessionLocal


class TestTaskAPIWithUsers:
    """Test Task API endpoints with user relationships."""
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock database session."""
        return AsyncMock(spec=AsyncSession)
    
    @pytest.fixture
    def sample_user_dict(self):
        """Sample user dictionary for testing."""
        return {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": None
        }
    
    @pytest.fixture
    def sample_task_dict(self, sample_user_dict):
        """Sample task dictionary with user for testing."""
        return {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "status": "pending",
            "due_date": datetime.now() + timedelta(days=7),
            "created_at": datetime.now(),
            "updated_at": None,
            "user_id": 1,
            "user": sample_user_dict
        }
    
    @pytest.fixture
    def multiple_tasks_with_users(self, sample_user_dict):
        """Multiple tasks with different users for testing."""
        users = [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "is_active": True, "created_at": datetime.now(), "updated_at": None},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "is_active": True, "created_at": datetime.now(), "updated_at": None},
            {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "is_active": True, "created_at": datetime.now(), "updated_at": None}
        ]
        
        return [
            {
                "id": 1,
                "title": "Documentation Task",
                "description": "Write API documentation",
                "priority": "high",
                "status": "in_progress",
                "due_date": datetime.now() + timedelta(days=5),
                "created_at": datetime.now(),
                "updated_at": None,
                "user_id": 1,
                "user": users[0]
            },
            {
                "id": 2,
                "title": "Code Review",
                "description": "Review pull requests",
                "priority": "medium",
                "status": "pending",
                "due_date": datetime.now() + timedelta(days=3),
                "created_at": datetime.now(),
                "updated_at": None,
                "user_id": 2,
                "user": users[1]
            },
            {
                "id": 3,
                "title": "Database Migration",
                "description": "Update database schema",
                "priority": "high",
                "status": "completed",
                "due_date": datetime.now() - timedelta(days=1),
                "created_at": datetime.now(),
                "updated_at": None,
                "user_id": 3,
                "user": users[2]
            }
        ]
    
    @patch('app.services.task_services.TaskService.list_tasks')
    async def test_get_all_tasks_with_users(self, mock_list_tasks, multiple_tasks_with_users):
        """Test GET /tasks returns tasks with user information."""
        # Mock service response
        mock_list_tasks.return_value = {
            "tasks": multiple_tasks_with_users,
            "total": 3,
            "page": 1,
            "per_page": 10,
            "total_pages": 1
        }
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/api/v1/tasks")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "tasks" in data
        assert len(data["tasks"]) == 3
        
        # Verify user information is included
        for task in data["tasks"]:
            assert "user" in task
            assert "id" in task["user"]
            assert "name" in task["user"]
            assert "email" in task["user"]
            assert "is_active" in task["user"]
            
            # Verify user_id matches user.id
            assert task["user_id"] == task["user"]["id"]
    
    @pytest.mark.asyncio
    @patch('app.services.task_services.TaskService.get_task')
    async def test_get_single_task_with_user(self, mock_get_task, sample_task_dict):
        """Test GET /tasks/{id} returns task with user information."""
        mock_get_task.return_value = sample_task_dict
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/api/v1/tasks/1")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == 1
        assert data["title"] == "Test Task"
        assert "user" in data
        assert data["user"]["id"] == 1
        assert data["user"]["name"] == "John Doe"
        assert data["user"]["email"] == "john@example.com"
        assert data["user_id"] == data["user"]["id"]
    
    @pytest.mark.asyncio
    @patch('app.services.task_services.TaskService.create_task')
    async def test_create_task_with_user_id(self, mock_create_task, sample_task_dict):
        """Test POST /tasks creates task and includes user information."""
        mock_create_task.return_value = sample_task_dict
        
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "status": "pending",
            "due_date": "2025-11-20T10:00:00",
            "user_id": 1
        }
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/v1/tasks", json=task_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["title"] == "Test Task"
        assert data["user_id"] == 1
        assert "user" in data
        assert data["user"]["name"] == "John Doe"
        
        # Verify the service was called with correct data
        mock_create_task.assert_called_once()
        call_args = mock_create_task.call_args[0][0]
        assert call_args["title"] == "Test Task"
        assert call_args["user_id"] == 1
    
    @patch('app.services.task_services.TaskService.update_task')
    async def test_update_task_preserves_user_relationship(self, mock_update_task, sample_task_dict):
        """Test PUT /tasks/{id} preserves user relationship."""
        updated_task = sample_task_dict.copy()
        updated_task["title"] = "Updated Task"
        updated_task["status"] = "in_progress"
        
        mock_update_task.return_value = updated_task
        
        update_data = {
            "title": "Updated Task",
            "description": "Test Description",
            "priority": "high",
            "status": "in_progress",
            "due_date": "2025-11-20T10:00:00",
            "user_id": 1
        }
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.put("/api/v1/tasks/1", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["title"] == "Updated Task"
        assert data["status"] == "in_progress"
        assert data["user_id"] == 1
        assert "user" in data
        assert data["user"]["name"] == "John Doe"
    
    @patch('app.services.task_services.TaskService.list_tasks')
    async def test_filter_tasks_by_user_status(self, mock_list_tasks, multiple_tasks_with_users):
        """Test filtering tasks by status shows correct user assignments."""
        # Filter for pending tasks only
        pending_tasks = [task for task in multiple_tasks_with_users if task["status"] == "pending"]
        
        mock_list_tasks.return_value = {
            "tasks": pending_tasks,
            "total": len(pending_tasks),
            "page": 1,
            "per_page": 10,
            "total_pages": 1
        }
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/api/v1/tasks?status=pending")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["tasks"]) == 1
        task = data["tasks"][0]
        assert task["status"] == "pending"
        assert task["user"]["name"] == "Jane Smith"
    
    @patch('app.services.task_services.TaskService.list_tasks')
    async def test_search_tasks_includes_user_info(self, mock_list_tasks, multiple_tasks_with_users):
        """Test searching tasks includes user information in results."""
        # Filter for tasks containing "Code"
        search_results = [task for task in multiple_tasks_with_users if "Code" in task["title"]]
        
        mock_list_tasks.return_value = {
            "tasks": search_results,
            "total": len(search_results),
            "page": 1,
            "per_page": 10,
            "total_pages": 1
        }
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/api/v1/tasks?search=Code")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["tasks"]) == 1
        task = data["tasks"][0]
        assert "Code" in task["title"]
        assert task["user"]["name"] == "Jane Smith"
        assert task["user"]["email"] == "jane@example.com"


class TestUserTaskRelationshipValidation:
    """Test validation of user-task relationships in API."""
    
    @patch('app.services.task_services.TaskService.create_task')
    async def test_create_task_with_invalid_user_id(self, mock_create_task):
        """Test creating task with non-existent user ID."""
        # Mock service to raise an exception for invalid user
        mock_create_task.side_effect = Exception("User not found")
        
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "status": "pending",
            "due_date": "2025-11-20T10:00:00",
            "user_id": 999  # Non-existent user
        }
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/v1/tasks", json=task_data)
        
        assert response.status_code == 500
    
    async def test_create_task_without_user_id(self):
        """Test creating task without user_id should fail validation."""
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "status": "pending",
            "due_date": "2025-11-20T10:00:00"
            # Missing user_id
        }
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/v1/tasks", json=task_data)
        
        assert response.status_code == 422  # Validation error
        
        data = response.json()
        assert "detail" in data
        # Check if validation error mentions user_id
        error_messages = str(data["detail"])
        assert "user_id" in error_messages.lower()
    
    async def test_task_response_schema_validation(self):
        """Test that task response includes required user fields."""
        # This test validates the schema structure
        from app.api.v1.schemas.tasks import TaskResponse, UserBase
        from pydantic import ValidationError
        
        # Valid task response data
        valid_data = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "status": "pending",
            "due_date": datetime.now() + timedelta(days=7),
            "created_at": datetime.now(),
            "updated_at": None,
            "user_id": 1,
            "user": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "is_active": True,
                "created_at": datetime.now()
            }
        }
        
        # Should validate successfully
        task_response = TaskResponse(**valid_data)
        assert task_response.user.name == "John Doe"
        assert task_response.user_id == 1
        
        # Invalid data - missing user
        invalid_data = valid_data.copy()
        del invalid_data["user"]
        
        with pytest.raises(ValidationError):
            TaskResponse(**invalid_data)
        
        # Invalid data - user_id mismatch
        mismatch_data = valid_data.copy()
        mismatch_data["user"]["id"] = 2  # Different from user_id
        
        # This should still validate as we don't enforce matching in schema
        # But we can test this logic in service layer
        task_response = TaskResponse(**mismatch_data)
        assert task_response.user_id == 1
        assert task_response.user.id == 2


class TestUserTaskAPIIntegration:
    """Integration tests combining multiple API operations."""
    
    @patch('app.services.task_services.TaskService')
    async def test_complete_user_task_workflow(self, mock_service):
        """Test complete workflow of creating, updating, and managing user tasks."""
        # Mock service instance
        mock_service_instance = AsyncMock()
        mock_service.return_value = mock_service_instance
        
        # Sample user data
        user_data = {
            "id": 1,
            "name": "Workflow User",
            "email": "workflow@example.com",
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": None
        }
        
        # Step 1: Create task
        task_data = {
            "title": "Workflow Task",
            "description": "Test workflow",
            "priority": "medium",
            "status": "pending",
            "due_date": "2025-11-20T10:00:00",
            "user_id": 1
        }
        
        created_task = {
            "id": 1,
            "title": "Workflow Task",
            "description": "Test workflow",
            "priority": "medium",
            "status": "pending",
            "due_date": datetime.now() + timedelta(days=7),
            "created_at": datetime.now(),
            "updated_at": None,
            "user_id": 1,
            "user": user_data
        }
        
        mock_service_instance.create_task.return_value = created_task
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # Create task
            response = await ac.post("/api/v1/tasks", json=task_data)
            assert response.status_code == 201
            
            created_data = response.json()
            assert created_data["user"]["name"] == "Workflow User"
            
            # Step 2: Update task status
            updated_task = created_task.copy()
            updated_task["status"] = "in_progress"
            mock_service_instance.update_task.return_value = updated_task
            
            update_data = task_data.copy()
            update_data["status"] = "in_progress"
            
            response = await ac.put("/api/v1/tasks/1", json=update_data)
            assert response.status_code == 200
            
            updated_data = response.json()
            assert updated_data["status"] == "in_progress"
            assert updated_data["user"]["name"] == "Workflow User"
            
            # Step 3: Get task
            mock_service_instance.get_task.return_value = updated_task
            
            response = await ac.get("/api/v1/tasks/1")
            assert response.status_code == 200
            
            get_data = response.json()
            assert get_data["id"] == 1
            assert get_data["status"] == "in_progress"
            assert get_data["user"]["name"] == "Workflow User"