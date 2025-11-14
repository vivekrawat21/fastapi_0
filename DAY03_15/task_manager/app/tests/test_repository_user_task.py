"""Test cases for repository layer user-task relationships."""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from unittest.mock import AsyncMock, patch

from app.repositories.sqlalchemy_repository import SQLAlchemyTaskRepository
from app.core.models import User, Task
from app.api.v1.schemas.tasks import Priority, Status


class TestSQLAlchemyTaskRepositoryUserRelations:
    """Test SQLAlchemy repository with user-task relationships."""
    
    @pytest.fixture
    async def repository(self, test_session: AsyncSession):
        """Create repository instance with test session."""
        return SQLAlchemyTaskRepository(test_session)
    
    async def test_get_all_tasks_includes_user_info(self, repository: SQLAlchemyTaskRepository, sample_tasks, sample_users):
        """Test get_all returns tasks with user information."""
        tasks = await repository.get_all()
        
        assert len(tasks) == 6  # 2 tasks per user * 3 users
        
        for task_dict in tasks:
            assert "user" in task_dict
            assert "user_id" in task_dict
            assert task_dict["user"]["id"] == task_dict["user_id"]
            assert "name" in task_dict["user"]
            assert "email" in task_dict["user"]
    
    async def test_get_by_id_includes_user_info(self, repository: SQLAlchemyTaskRepository, sample_task, sample_user):
        """Test get_by_id returns task with user information."""
        task_dict = await repository.get_by_id(sample_task.id)
        
        assert task_dict is not None
        assert task_dict["id"] == sample_task.id
        assert "user" in task_dict
        assert task_dict["user"]["id"] == sample_user.id
        assert task_dict["user"]["name"] == sample_user.name
        assert task_dict["user"]["email"] == sample_user.email
        assert task_dict["user_id"] == sample_user.id
    
    async def test_create_task_with_user_relationship(self, repository: SQLAlchemyTaskRepository, sample_user):
        """Test creating task establishes user relationship."""
        task_data = {
            "title": "New Task with User",
            "description": "Test description",
            "priority": Priority.high,
            "status": Status.pending,
            "due_date": datetime.now() + timedelta(days=5),
            "user_id": sample_user.id
        }
        
        created_task = await repository.create(task_data)
        
        assert created_task["title"] == "New Task with User"
        assert created_task["user_id"] == sample_user.id
        assert "user" in created_task
        assert created_task["user"]["name"] == sample_user.name
        
        # Verify in database
        retrieved_task = await repository.get_by_id(created_task["id"])
        assert retrieved_task["user"]["email"] == sample_user.email
    
    async def test_update_task_preserves_user_relationship(self, repository: SQLAlchemyTaskRepository, sample_task, sample_user):
        """Test updating task preserves user relationship."""
        update_data = {
            "title": "Updated Task Title",
            "status": Status.in_progress
        }
        
        updated_task = await repository.update(sample_task.id, update_data)
        
        assert updated_task["title"] == "Updated Task Title"
        assert updated_task["status"] == Status.in_progress
        assert updated_task["user_id"] == sample_user.id
        assert "user" in updated_task
        assert updated_task["user"]["name"] == sample_user.name
    
    async def test_update_task_change_user_assignment(self, repository: SQLAlchemyTaskRepository, sample_task, sample_users):
        """Test updating task to assign to different user."""
        new_user = sample_users[1]  # Different user
        
        update_data = {
            "user_id": new_user.id
        }
        
        updated_task = await repository.update(sample_task.id, update_data)
        
        assert updated_task["user_id"] == new_user.id
        assert updated_task["user"]["name"] == new_user.name
        assert updated_task["user"]["email"] == new_user.email
    
    async def test_delete_task_maintains_user(self, repository: SQLAlchemyTaskRepository, sample_task, sample_user, test_session: AsyncSession):
        """Test deleting task doesn't affect user."""
        task_id = sample_task.id
        user_id = sample_user.id
        
        # Delete task
        result = await repository.delete(task_id)
        assert result is True
        
        # Verify task is deleted
        deleted_task = await repository.get_by_id(task_id)
        assert deleted_task is None
        
        # Verify user still exists
        user_result = await test_session.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()
        assert user is not None
        assert user.name == sample_user.name
    
    async def test_get_tasks_by_user_filter(self, repository: SQLAlchemyTaskRepository, sample_tasks, sample_users):
        """Test filtering tasks by specific user."""
        # This would require extending the repository to support user filtering
        # For now, we'll test by manually filtering results
        all_tasks = await repository.get_all()
        
        # Filter tasks for first user
        user_1_tasks = [task for task in all_tasks if task["user_id"] == sample_users[0].id]
        
        assert len(user_1_tasks) == 2  # 2 tasks per user from fixture
        for task in user_1_tasks:
            assert task["user"]["name"] == sample_users[0].name
            assert task["user_id"] == sample_users[0].id
    
    async def test_task_to_dict_includes_user_data(self, repository: SQLAlchemyTaskRepository, sample_task, sample_user, test_session: AsyncSession):
        """Test _task_to_dict method includes user data."""
        # Get the task with user relationship loaded
        task_result = await test_session.execute(
            select(Task).where(Task.id == sample_task.id)
        )
        task = task_result.scalar_one()
        
        # Convert to dict
        task_dict = repository._task_to_dict(task)
        
        assert "user" in task_dict
        assert task_dict["user"]["id"] == sample_user.id
        assert task_dict["user"]["name"] == sample_user.name
        assert task_dict["user"]["email"] == sample_user.email
        assert task_dict["user"]["is_active"] == sample_user.is_active
        assert task_dict["user_id"] == sample_user.id
    
    async def test_create_task_with_invalid_user_id(self, repository: SQLAlchemyTaskRepository):
        """Test creating task with non-existent user ID fails."""
        task_data = {
            "title": "Task with Invalid User",
            "description": "Test description",
            "priority": Priority.medium,
            "status": Status.pending,
            "due_date": datetime.now() + timedelta(days=3),
            "user_id": 999  # Non-existent user
        }
        
        with pytest.raises(Exception):  # Should raise foreign key constraint error
            await repository.create(task_data)
    
    async def test_multiple_tasks_same_user(self, repository: SQLAlchemyTaskRepository, sample_user):
        """Test creating multiple tasks for same user."""
        task_data_list = [
            {
                "title": f"Task {i}",
                "description": f"Description {i}",
                "priority": Priority.medium,
                "status": Status.pending,
                "user_id": sample_user.id
            }
            for i in range(3)
        ]
        
        created_tasks = []
        for task_data in task_data_list:
            created_task = await repository.create(task_data)
            created_tasks.append(created_task)
        
        assert len(created_tasks) == 3
        
        for task in created_tasks:
            assert task["user_id"] == sample_user.id
            assert task["user"]["name"] == sample_user.name
    
    async def test_user_data_consistency_across_operations(self, repository: SQLAlchemyTaskRepository, sample_task, sample_user):
        """Test user data remains consistent across different operations."""
        task_id = sample_task.id
        
        # Get task
        task_get = await repository.get_by_id(task_id)
        user_data_get = task_get["user"]
        
        # Update task
        updated_task = await repository.update(task_id, {"title": "Updated Title"})
        user_data_update = updated_task["user"]
        
        # Get all tasks and find our task
        all_tasks = await repository.get_all()
        our_task = next(task for task in all_tasks if task["id"] == task_id)
        user_data_all = our_task["user"]
        
        # All user data should be identical
        assert user_data_get == user_data_update == user_data_all
        assert all(user_data["name"] == sample_user.name for user_data in [user_data_get, user_data_update, user_data_all])
        assert all(user_data["email"] == sample_user.email for user_data in [user_data_get, user_data_update, user_data_all])


class TestRepositoryUserTaskConstraints:
    """Test database constraints and data integrity in repository."""
    
    @pytest.fixture
    async def repository(self, test_session: AsyncSession):
        """Create repository instance."""
        return SQLAlchemyTaskRepository(test_session)
    
    async def test_foreign_key_constraint(self, repository: SQLAlchemyTaskRepository, test_session: AsyncSession):
        """Test foreign key constraint prevents orphaned tasks."""
        # Create user and task
        user = User(name="Temp User", email="temp@example.com")
        test_session.add(user)
        await test_session.commit()
        await test_session.refresh(user)
        
        task_data = {
            "title": "Constraint Test Task",
            "description": "Test description",
            "priority": Priority.low,
            "status": Status.pending,
            "user_id": user.id
        }
        
        created_task = await repository.create(task_data)
        assert created_task["user_id"] == user.id
        
        # Try to delete user (should fail due to foreign key constraint)
        with pytest.raises(Exception):
            await test_session.delete(user)
            await test_session.commit()
    
    async def test_cascade_delete_behavior(self, repository: SQLAlchemyTaskRepository, test_session: AsyncSession):
        """Test cascade delete when user is removed."""
        # Create user
        user = User(name="Cascade User", email="cascade@example.com")
        test_session.add(user)
        await test_session.commit()
        await test_session.refresh(user)
        
        # Create tasks
        task_ids = []
        for i in range(2):
            task_data = {
                "title": f"Cascade Task {i}",
                "description": f"Description {i}",
                "priority": Priority.medium,
                "status": Status.pending,
                "user_id": user.id
            }
            task = await repository.create(task_data)
            task_ids.append(task["id"])
        
        # Verify tasks exist
        for task_id in task_ids:
            task = await repository.get_by_id(task_id)
            assert task is not None
        
        # Delete user (should cascade to tasks due to model configuration)
        await test_session.delete(user)
        await test_session.commit()
        
        # Verify tasks are deleted
        for task_id in task_ids:
            task = await repository.get_by_id(task_id)
            assert task is None