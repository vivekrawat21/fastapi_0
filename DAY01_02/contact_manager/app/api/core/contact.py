import uuid
from typing import List, Dict, Any
async def generate_unique_id(existing_contacts_data: List[Dict[str, Any]]) -> str:
    """Generate a unique time-based UUID not present in existing contacts.""" 
    existing_ids = {contact.get('id') for contact in existing_contacts_data if contact.get('id')}
    while True:
        new_id = str(uuid.uuid1())
        if new_id not in existing_ids:
              return new_id
            
        # This collision case is extremely rare, even more so with time-based IDs.
        print(f"Time-based ID Collision detected: {new_id}. Regenerating...")
