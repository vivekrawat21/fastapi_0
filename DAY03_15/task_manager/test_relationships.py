"""Simple test script to verify user-task relationships."""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.models import User, Task
from app.repositories.sqlalchemy_repository import SQLAlchemyTaskRepository


async def test_user_task_relationships():
    """Test the user-task relationships in the database."""
    print("Testing User-Task Relationships...")
    
    async with AsyncSessionLocal() as session:
        try:
            # Test 1: Get users with their tasks
            print("\n1. Testing users with tasks:")
            result = await session.execute(
                select(User).limit(3)
            )
            users = result.scalars().all()
            
            for user in users:
                print(f"   User: {user.name} ({user.email})")
                print(f"   Tasks: {len(user.tasks)} tasks")
                for task in user.tasks[:2]:  # Show first 2 tasks
                    print(f"     - {task.title} ({task.status})")
            
            # Test 2: Get tasks with user information
            print("\n2. Testing tasks with user info:")
            result = await session.execute(
                select(Task).limit(5)
            )
            tasks = result.scalars().all()
            
            for task in tasks:
                print(f"   Task: {task.title}")
                print(f"   Assigned to: {task.user.name if task.user else 'No user'}")
                print(f"   Priority: {task.priority}, Status: {task.status}")
            
            # Test 3: Repository methods with user data
            print("\n3. Testing repository with user relationships:")
            repository = SQLAlchemyTaskRepository(session)
            
            # Get all tasks with user info
            all_tasks = await repository.get_all()
            print(f"   Total tasks from repository: {len(all_tasks)}")
            
            for task_dict in all_tasks[:3]:  # Show first 3
                print(f"   Task: {task_dict['title']}")
                if 'user' in task_dict and task_dict['user']:
                    print(f"   User: {task_dict['user']['name']} ({task_dict['user']['email']})")
                else:
                    print("   User: No user data")
            
            # Test 4: Get specific task with user
            if all_tasks:
                task_id = all_tasks[0]['id']
                specific_task = await repository.get_by_id(task_id)
                print(f"\n4. Testing specific task retrieval:")
                print(f"   Task: {specific_task['title']}")
                if 'user' in specific_task and specific_task['user']:
                    print(f"   User: {specific_task['user']['name']}")
                    print(f"   User Active: {specific_task['user']['is_active']}")
                
            print("\n✅ All relationship tests passed!")
            
        except Exception as e:
            print(f"\n❌ Error testing relationships: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(test_user_task_relationships())