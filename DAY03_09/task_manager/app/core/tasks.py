import uuid
import random

async def generate_id():
    return str(uuid.uuid4())

async def generate_int_id():
    """Generate a random integer ID for tasks"""
    return random.randint(1000, 999999)