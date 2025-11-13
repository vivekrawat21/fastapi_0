"""Pytest configuration and fixtures for testing."""

import pytest
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient

from app.core.models import Base, User, Task
from app.api.v1.schemas.tasks import Priority, Status
from app.main import app


# Test database configuration
TEST_DATABASE_URL = "mysql+aiomysql://vivek:vivek2002@localhost/taskmanager_test_db"


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    """Create event loop for session scope."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
async def test_session():
    """Create test database session."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
    )
    
    TestSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with TestSessionLocal() as session:
        # Clean up tables before each test
        await session.execute("DELETE FROM tasks")
        await session.execute("DELETE FROM users")
        await session.commit()
        
        yield session
    
    await engine.dispose()


@pytest.fixture
async def sample_user(test_session: AsyncSession):
    """Create a sample user for testing."""
    user = User(
        name="Test User",
        email="test@example.com"
    )
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user


@pytest.fixture
async def sample_users(test_session: AsyncSession):
    """Create multiple sample users for testing."""
    users = [
        User(name="Alice Johnson", email="alice@example.com"),
        User(name="Bob Smith", email="bob@example.com"),
        User(name="Charlie Brown", email="charlie@example.com")
    ]
    
    for user in users:
        test_session.add(user)
    
    await test_session.commit()
    
    for user in users:
        await test_session.refresh(user)
    
    return users


@pytest.fixture
async def sample_task(test_session: AsyncSession, sample_user: User):
    """Create a sample task for testing."""
    task = Task(
        title="Test Task",
        description="This is a test task",
        priority=Priority.medium,
        status=Status.pending,
        due_date=datetime.now() + timedelta(days=7),
        user_id=sample_user.id
    )
    test_session.add(task)
    await test_session.commit()
    await test_session.refresh(task)
    return task


@pytest.fixture
async def sample_tasks(test_session: AsyncSession, sample_users):
    """Create multiple sample tasks for testing."""
    tasks = []
    
    # Create 2 tasks for each user
    for i, user in enumerate(sample_users):
        for j in range(2):
            task = Task(
                title=f"Task {i+1}-{j+1}",
                description=f"Description for task {i+1}-{j+1}",
                priority=Priority.medium,
                status=Status.pending if j == 0 else Status.in_progress,
                due_date=datetime.now() + timedelta(days=j+1),
                user_id=user.id
            )
            test_session.add(task)
            tasks.append(task)
    
    await test_session.commit()
    
    for task in tasks:
        await test_session.refresh(task)
    
    return tasks


@pytest.fixture
def sample_task_data():
    """Sample task data for API testing."""
    return {
        "title": "Sample Task",
        "description": "Sample task description",
        "priority": "high",
        "status": "pending",
        "due_date": "2025-11-20T10:00:00",
        "user_id": 1
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "is_active": True,
        "created_at": datetime(2025, 11, 13, 12, 0, 0),
        "updated_at": None
    }