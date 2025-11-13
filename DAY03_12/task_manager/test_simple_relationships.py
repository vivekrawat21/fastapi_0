"""Simple pytest test for user-task relationships."""

import pytest
import asyncio
from datetime import datetime, timedelta

from app.repositories.sqlalchemy_repository import SQLAlchemyTaskRepository
from app.core.database import AsyncSessionLocal
from app.core.models import User, Task
from app.api.v1.schemas.tasks import Priority, Status


@pytest.mark.asyncio
async def test_repository_includes_user_data():
    """Test that repository methods include user data."""
    async with AsyncSessionLocal() as session:
        repo = SQLAlchemyTaskRepository(session)
        
        # Get all tasks
        tasks = await repo.get_all()
        assert len(tasks) > 0, "Should have seeded tasks"
        
        # Check first task has user data
        task = tasks[0]
        assert "user" in task, "Task should include user data"
        assert "user_id" in task, "Task should include user_id"
        assert task["user"] is not None, "User data should not be None"
        assert "name" in task["user"], "User should have name"
        assert "email" in task["user"], "User should have email"
        assert task["user"]["id"] == task["user_id"], "User ID should match user_id field"


@pytest.mark.asyncio
async def test_get_single_task_with_user():
    """Test getting single task includes user data."""
    async with AsyncSessionLocal() as session:
        repo = SQLAlchemyTaskRepository(session)
        
        # Get all tasks first
        all_tasks = await repo.get_all()
        assert len(all_tasks) > 0, "Should have tasks"
        
        # Get specific task
        task_id = all_tasks[0]["id"]
        task = await repo.get_by_id(task_id)
        
        assert task is not None, "Task should exist"
        assert "user" in task, "Task should include user data"
        assert task["user"]["name"] is not None, "User name should exist"


@pytest.mark.asyncio
async def test_user_task_relationship_consistency():
    """Test that user-task relationships are consistent."""
    async with AsyncSessionLocal() as session:
        repo = SQLAlchemyTaskRepository(session)
        
        # Get all tasks
        tasks = await repo.get_all()
        
        # Group tasks by user
        users_tasks = {}
        for task in tasks:
            user_id = task["user_id"]
            user_name = task["user"]["name"]
            
            if user_id not in users_tasks:
                users_tasks[user_id] = {"name": user_name, "tasks": []}
            users_tasks[user_id]["tasks"].append(task)
        
        # Verify each user has consistent data across tasks
        for user_id, user_data in users_tasks.items():
            user_name = user_data["name"]
            user_tasks = user_data["tasks"]
            
            # All tasks for this user should have same user name
            for task in user_tasks:
                assert task["user"]["name"] == user_name, f"Inconsistent user name for user {user_id}"
                assert task["user_id"] == user_id, f"Inconsistent user_id for user {user_id}"


if __name__ == "__main__":
    # Run tests directly
    asyncio.run(test_repository_includes_user_data())
    asyncio.run(test_get_single_task_with_user())
    asyncio.run(test_user_task_relationship_consistency())
    print("✅ All tests passed!")