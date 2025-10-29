import aiofiles
import json
from typing import List, Dict, Any


async def read_contacts() -> List[Dict[str, Any]]:  
    try:
        async with aiofiles.open("contacts.json", mode='r') as f:
            content = await f.read()
            return  json.loads(content)

    except FileNotFoundError:
        return []

async def write_contacts(contacts: List[Dict[str, Any]]) -> None:
    try:
        async with aiofiles.open("contacts.json", mode='w') as f:
            await f.write(json.dumps(contacts, indent=4))
    except Exception as e:
        print(f"Error writing to file: {e}")    