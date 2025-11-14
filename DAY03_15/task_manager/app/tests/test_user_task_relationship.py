"""Test cases for User-Task relationship functionality."""

import pytest
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from httpx import AsyncClient

from app.core.database import AsyncSessionLocal
from app.core.models import User, Task, Base
from app.api.v1.schemas.tasks import Priority, Status
from app.main import app
from app.core.config import settings


# Test database setup
TEST_DATABASE_URL = "mysql+aiomysql://vivek:vivek2002@localhost/taskmanager_test_db"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

TestAsyncSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture
async def test_db():
    """Create test database tables."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(test_db):
    """Get test database session."""
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def sample_user(db_session: AsyncSession):
    """Create a sample user for testing."""
    user = User(
        name="Test User",
        email="test@example.com"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def sample_users(db_session: AsyncSession):
    """Create multiple sample users for testing."""
    users = [
        User(name="John Doe", email="john@example.com"),
        User(name="Jane Smith", email="jane@example.com"),
        User(name="Bob Johnson", email="bob@example.com")
    ]
    
    for user in users:
        db_session.add(user)
    
    await db_session.commit()
    
    for user in users:
        await db_session.refresh(user)
    
    return users


@pytest.fixture
async def sample_task(db_session: AsyncSession, sample_user: User):
    """Create a sample task for testing."""
    task = Task(
        title="Test Task",
        description="This is a test task",
        priority=Priority.medium,
        status=Status.pending,
        due_date=datetime.now() + timedelta(days=7),
        user_id=sample_user.id
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    return task


class TestUserModel:
    """Test User model functionality."""
    
    async def test_create_user(self, db_session: AsyncSession):
        """Test creating a user."""
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        assert user.id is not None
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.created_at is not None
    
    async def test_user_tasks_relationship(self, db_session: AsyncSession, sample_user: User):
        """Test user-tasks relationship."""
        # Create tasks for the user
        tasks = [
            Task(
                title=f"Task {i}",
                description=f"Description {i}",
                priority=Priority.medium,
                status=Status.pending,
                user_id=sample_user.id
            )
            for i in range(3)
        ]
        
        for task in tasks:
            db_session.add(task)
        
        await db_session.commit()
        
        # Refresh user to load relationships
        await db_session.refresh(sample_user)
        
        # Test relationship
        result = await db_session.execute(
            select(User).where(User.id == sample_user.id)
        )
        user_with_tasks = result.scalar_one()
        
        assert len(user_with_tasks.tasks) == 3
        for task in user_with_tasks.tasks:
            assert task.user_id == sample_user.id
            assert task.user == user_with_tasks


class TestTaskModel:
    """Test Task model functionality."""
    
    async def test_create_task(self, db_session: AsyncSession, sample_user: User):
        """Test creating a task."""
        task = Task(
            title="Test Task",
            description="This is a test task",
            priority=Priority.high,
            status=Status.in_progress,
            due_date=datetime.now() + timedelta(days=5),
            user_id=sample_user.id
        )
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)
        
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "This is a test task"
        assert task.priority == Priority.high
        assert task.status == Status.in_progress
        assert task.user_id == sample_user.id
        assert task.created_at is not None
    
    async def test_task_user_relationship(self, db_session: AsyncSession, sample_task: Task, sample_user: User):
        """Test task-user relationship."""
        # Refresh task to load relationships
        await db_session.refresh(sample_task)
        
        assert sample_task.user is not None
        assert sample_task.user.id == sample_user.id
        assert sample_task.user.name == sample_user.name
        assert sample_task.user.email == sample_user.email
    
    async def test_cascade_delete(self, db_session: AsyncSession, sample_users: list[User]):
        """Test cascade delete when user is deleted."""
        user = sample_users[0]
        
        # Create tasks for the user
        tasks = [
            Task(
                title=f"Task {i}",
                description=f"Description {i}",
                priority=Priority.medium,
                status=Status.pending,
                user_id=user.id
            )
            for i in range(2)
        ]
        
        for task in tasks:
            db_session.add(task)
        
        await db_session.commit()
        
        # Verify tasks exist
        result = await db_session.execute(
            select(Task).where(Task.user_id == user.id)
        )
        user_tasks = result.scalars().all()
        assert len(user_tasks) == 2
        
        # Delete user
        await db_session.delete(user)
        await db_session.commit()
        
        # Verify tasks are deleted (cascade)
        result = await db_session.execute(
            select(Task).where(Task.user_id == user.id)
        )
        remaining_tasks = result.scalars().all()
        assert len(remaining_tasks) == 0


class TestUserTaskQueries:
    """Test complex queries involving users and tasks."""
    
    async def test_get_users_with_task_counts(self, db_session: AsyncSession, sample_users: list[User]):
        """Test getting users with their task counts."""
        # Create different numbers of tasks for each user
        task_counts = [3, 1, 2]
        
        for i, user in enumerate(sample_users):
            for j in range(task_counts[i]):
                task = Task(
                    title=f"Task {j} for {user.name}",
                    description=f"Description {j}",
                    priority=Priority.medium,
                    status=Status.pending,
                    user_id=user.id
                )
                db_session.add(task)
        
        await db_session.commit()
        
        # Query users with task counts
        from sqlalchemy import func
        result = await db_session.execute(
            select(
                User.id,
                User.name,
                func.count(Task.id).label('task_count')
            )
            .outerjoin(Task)
            .group_by(User.id, User.name)
            .order_by(User.name)
        )
        
        users_with_counts = result.all()
        
        assert len(users_with_counts) == 3
        # Check task counts match what we created
        expected_counts = dict(zip([u.name for u in sample_users], task_counts))
        for user_id, user_name, count in users_with_counts:
            assert count == expected_counts[user_name]
    
    async def test_get_tasks_by_status_and_user(self, db_session: AsyncSession, sample_users: list[User]):
        """Test getting tasks filtered by status and user."""
        user1, user2 = sample_users[0], sample_users[1]
        
        # Create tasks with different statuses
        tasks = [
            Task(title="Task 1", description="Desc 1", status=Status.pending, user_id=user1.id),
            Task(title="Task 2", description="Desc 2", status=Status.in_progress, user_id=user1.id),
            Task(title="Task 3", description="Desc 3", status=Status.pending, user_id=user2.id),
            Task(title="Task 4", description="Desc 4", status=Status.completed, user_id=user2.id),
        ]
        
        for task in tasks:
            db_session.add(task)
        
        await db_session.commit()
        
        # Query pending tasks for user1
        result = await db_session.execute(
            select(Task)
            .where(Task.user_id == user1.id)
            .where(Task.status == Status.pending)
        )
        pending_tasks_user1 = result.scalars().all()
        
        assert len(pending_tasks_user1) == 1
        assert pending_tasks_user1[0].title == "Task 1"
        
        # Query all tasks for user2
        result = await db_session.execute(
            select(Task)
            .where(Task.user_id == user2.id)
        )
        all_tasks_user2 = result.scalars().all()
        
        assert len(all_tasks_user2) == 2
    
    async def test_get_overdue_tasks_by_user(self, db_session: AsyncSession, sample_users: list[User]):
        """Test getting overdue tasks grouped by user."""
        user = sample_users[0]
        
        # Create overdue and future tasks
        overdue_date = datetime.now() - timedelta(days=2)
        future_date = datetime.now() + timedelta(days=2)
        
        tasks = [
            Task(title="Overdue Task 1", description="Desc 1", due_date=overdue_date, user_id=user.id),
            Task(title="Overdue Task 2", description="Desc 2", due_date=overdue_date, user_id=user.id),
            Task(title="Future Task", description="Desc 3", due_date=future_date, user_id=user.id),
        ]
        
        for task in tasks:
            db_session.add(task)
        
        await db_session.commit()
        
        # Query overdue tasks
        result = await db_session.execute(
            select(Task)
            .where(Task.user_id == user.id)
            .where(Task.due_date < datetime.now())
            .where(Task.status != Status.completed)
        )
        overdue_tasks = result.scalars().all()
        
        assert len(overdue_tasks) == 2
        for task in overdue_tasks:
            assert "Overdue" in task.title


class TestUserTaskIntegration:
    """Integration tests for user-task functionality."""
    
    async def test_user_task_crud_operations(self, db_session: AsyncSession):
        """Test complete CRUD operations for users and tasks."""
        # Create user
        user = User(name="CRUD User", email="crud@example.com")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        # Create task
        task = Task(
            title="CRUD Task",
            description="CRUD Description",
            priority=Priority.high,
            status=Status.pending,
            due_date=datetime.now() + timedelta(days=3),
            user_id=user.id
        )
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)
        
        # Read operations
        result = await db_session.execute(
            select(User).where(User.id == user.id)
        )
        retrieved_user = result.scalar_one()
        assert retrieved_user.name == "CRUD User"
        
        result = await db_session.execute(
            select(Task).where(Task.id == task.id)
        )
        retrieved_task = result.scalar_one()
        assert retrieved_task.title == "CRUD Task"
        assert retrieved_task.user_id == user.id
        
        # Update operations
        retrieved_task.title = "Updated CRUD Task"
        retrieved_task.status = Status.in_progress
        await db_session.commit()
        
        result = await db_session.execute(
            select(Task).where(Task.id == task.id)
        )
        updated_task = result.scalar_one()
        assert updated_task.title == "Updated CRUD Task"
        assert updated_task.status == Status.in_progress
        
        # Delete operations
        await db_session.delete(updated_task)
        await db_session.commit()
        
        result = await db_session.execute(
            select(Task).where(Task.id == task.id)
        )
        deleted_task = result.scalar_one_or_none()
        assert deleted_task is None
        
        # User should still exist
        result = await db_session.execute(
            select(User).where(User.id == user.id)
        )
        remaining_user = result.scalar_one_or_none()
        assert remaining_user is not None