"""Seed data utilities for populating the database with initial data."""

import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.models import User, Task
from app.api.v1.schemas.tasks import Priority, Status


async def create_sample_users(session: AsyncSession) -> list[User]:
    """Create sample users in the database."""
    sample_users = [
        {
            "name": "John Doe",
            "email": "john.doe@example.com",
        },
        {
            "name": "Jane Smith", 
            "email": "jane.smith@example.com",
        },
        {
            "name": "Bob Johnson",
            "email": "bob.johnson@example.com",
        },
        {
            "name": "Alice Williams",
            "email": "alice.williams@example.com",
        },
        {
            "name": "Charlie Brown",
            "email": "charlie.brown@example.com",
        }
    ]
    
    created_users = []
    for user_data in sample_users:
        # Check if user already exists
        result = await session.execute(
            select(User).where(User.email == user_data["email"])
        )
        existing_user = result.scalar_one_or_none()
        
        if not existing_user:
            user = User(**user_data)
            session.add(user)
            await session.flush()  # Get the ID
            created_users.append(user)
            print(f"Created user: {user.name} ({user.email})")
        else:
            created_users.append(existing_user)
            print(f"User already exists: {existing_user.name} ({existing_user.email})")
    
    return created_users


async def create_sample_tasks(session: AsyncSession, users: list[User]) -> list[Task]:
    """Create sample tasks and assign them to users."""
    sample_tasks = [
        {
            "title": "Complete project documentation",
            "description": "Write comprehensive documentation for the FastAPI project including API endpoints and examples.",
            "priority": Priority.high,
            "status": Status.in_progress,
            "due_date": datetime.now() + timedelta(days=7)
        },
        {
            "title": "Review code changes",
            "description": "Review pull requests from team members and provide constructive feedback.",
            "priority": Priority.medium,
            "status": Status.pending,
            "due_date": datetime.now() + timedelta(days=3)
        },
        {
            "title": "Database optimization",
            "description": "Optimize database queries and add proper indexing to improve performance.",
            "priority": Priority.high,
            "status": Status.pending,
            "due_date": datetime.now() + timedelta(days=10)
        },
        {
            "title": "Setup CI/CD pipeline",
            "description": "Configure continuous integration and deployment pipeline for the project.",
            "priority": Priority.medium,
            "status": Status.completed,
            "due_date": datetime.now() - timedelta(days=2)  # Completed task
        },
        {
            "title": "Write unit tests",
            "description": "Increase test coverage by writing comprehensive unit tests for all services.",
            "priority": Priority.medium,
            "status": Status.in_progress,
            "due_date": datetime.now() + timedelta(days=5)
        },
        {
            "title": "API performance testing",
            "description": "Conduct load testing on API endpoints to identify bottlenecks.",
            "priority": Priority.low,
            "status": Status.pending,
            "due_date": datetime.now() + timedelta(days=14)
        },
        {
            "title": "Security audit",
            "description": "Perform security assessment of the application and fix vulnerabilities.",
            "priority": Priority.high,
            "status": Status.pending,
            "due_date": datetime.now() + timedelta(days=21)
        },
        {
            "title": "User interface improvements",
            "description": "Enhance user experience based on feedback and usability testing.",
            "priority": Priority.low,
            "status": Status.pending,
            "due_date": datetime.now() + timedelta(days=30)
        },
        {
            "title": "Backup strategy implementation",
            "description": "Implement automated backup solution for critical data.",
            "priority": Priority.medium,
            "status": Status.pending,
            "due_date": datetime.now() + timedelta(days=12)
        },
        {
            "title": "Training documentation",
            "description": "Create training materials for new team members.",
            "priority": Priority.low,
            "status": Status.completed,
            "due_date": datetime.now() - timedelta(days=5)  # Completed task
        }
    ]
    
    created_tasks = []
    for i, task_data in enumerate(sample_tasks):
        # Assign tasks to users in round-robin fashion
        assigned_user = users[i % len(users)]
        task_data["user_id"] = assigned_user.id
        
        task = Task(**task_data)
        session.add(task)
        await session.flush()  # Get the ID
        created_tasks.append(task)
        print(f"Created task: {task.title} (assigned to {assigned_user.name})")
    
    return created_tasks


async def seed_database():
    """Main function to seed the database with sample data."""
    print("Starting database seeding...")
    
    async with AsyncSessionLocal() as session:
        try:
            # Create sample users
            print("\n=== Creating Users ===")
            users = await create_sample_users(session)
            
            # Create sample tasks
            print("\n=== Creating Tasks ===")
            tasks = await create_sample_tasks(session, users)
            
            # Commit all changes
            await session.commit()
            
            print(f"\n✅ Database seeding completed successfully!")
            print(f"   - Created {len(users)} users")
            print(f"   - Created {len(tasks)} tasks")
            
        except Exception as e:
            await session.rollback()
            print(f"\n❌ Error during database seeding: {e}")
            raise


async def clear_database():
    """Clear all data from the database."""
    print("Clearing database...")
    
    async with AsyncSessionLocal() as session:
        try:
            # Delete all tasks first (due to foreign key constraint)
            await session.execute("DELETE FROM tasks")
            await session.execute("DELETE FROM users")
            await session.commit()
            print("✅ Database cleared successfully!")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error clearing database: {e}")
            raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database seeding utility")
    parser.add_argument(
        "--action",
        choices=["seed", "clear", "reseed"],
        default="seed",
        help="Action to perform: seed, clear, or reseed (clear + seed)"
    )
    
    args = parser.parse_args()
    
    if args.action == "seed":
        asyncio.run(seed_database())
    elif args.action == "clear":
        asyncio.run(clear_database())
    elif args.action == "reseed":
        asyncio.run(clear_database())
        asyncio.run(seed_database())