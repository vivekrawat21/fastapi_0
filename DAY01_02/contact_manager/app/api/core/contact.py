import uuid
from typing import List, Dict, Any
async def generate_unique_id(existing_contacts_data: List[Dict[str, Any]]) -> str:
    
    existing_ids = {contact.get('id') for contact in existing_contacts_data if contact.get('id')}
    while True:
        new_id = str(uuid.uuid1())
        if new_id not in existing_ids:
              return new_id
            
        print(f"Time-based ID Collision detected: {new_id}. Regenerating...")
