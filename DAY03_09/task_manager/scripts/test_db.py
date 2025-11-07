import asyncio
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

async def test_database():
    async with AsyncSessionLocal() as session:
        try:
            # Test the connection
            result = await session.execute(text('SELECT 1'))
            print("Database connection successful!")
            
            # List all tasks
            result = await session.execute(text('SELECT * FROM tasks'))
            tasks = result.fetchall()
            print("\nCurrent tasks in database:")
            for task in tasks:
                print(task)
                
        except Exception as e:
            print(f"Error connecting to database: {e}")

if __name__ == "__main__":
    asyncio.run(test_database())