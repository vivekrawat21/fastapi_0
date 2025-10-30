import aiofiles
import json
from typing import List, Dict, Any
from datetime import date

TASKS = "/home/vivek-rawat/Desktop/RSVR/fastapi_0/DAY03_04/task_manager/app/tasks.json"

def date_converter(o):
    if isinstance(o, date):
        return o.isoformat()
    return str(o)

async def read_tasks() -> List[Dict[str, Any]]:  
    try:
        async with aiofiles.open(TASKS, mode='r') as f:
            content = await f.read()
            return  json.loads(content)

    except FileNotFoundError:
        return []

async def write_tasks(tasks: List[Dict[str, Any]]) -> None:
    try:
        async with aiofiles.open(TASKS, mode='w') as f:
            await f.write(json.dumps(tasks, indent=4, default=date_converter))
    except Exception as e:
        print(f"Error writing to file: {e}")    