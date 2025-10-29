from fastapi import APIRouter,HTTPException,Query
from app.utils import read_contacts, write_contacts
from app.schemas.contact_schema import ContactCreate,ContactUpdate
from ..core import generate_unique_id
from typing import Optional


router = APIRouter(prefix="/contacts", tags=["contacts"])

#list contacts with optional sorting
@router.get("/list",status_code=200)
async def get_contacts(sort_by:Optional[str] = Query("name",description="Field to sort contacts by name or email")):
	contacts = await read_contacts()
	if sort_by.lower() in ["name","email"]:
		contacts = sorted(contacts, key=lambda x: x.get(sort_by)[0].lower())
	return contacts


@router.get("/search",status_code=200)
async def search_contacts(name: str = Query(..., description="Search query contact name ")):
    contacts = await read_contacts()
    filtered_contacts = [contact for contact in contacts if name.lower() in contact.get('name','no name found').lower()]
    if not filtered_contacts:
        raise HTTPException(status_code=404, detail=f"No contacts found matching the name: {name}")
    return filtered_contacts


@router.post("/", status_code=201)
async def add_contact(contact: ContactCreate):
    contacts = await read_contacts()
    for existing_contact in contacts:
        if (existing_contact.get('email')==contact.email and
			existing_contact.get('phone')==contact.phone):
            raise HTTPException(status_code=400, detail="Contact already exists.")
        
    id = await generate_unique_id(contacts)
    new_contact = contact.model_dump()
    new_contact['id'] = id
    contacts.append(new_contact)
    await write_contacts(contacts)
    return new_contact


@router.put("/{contact_id}",status_code=200)
async def update_contact(contact_id:str, contact:ContactUpdate):
        contacts = await read_contacts()
        updated_contact = contact.model_dump(exclude_unset=True)
        contact_found = False
        for existing_contact in contacts:
            if existing_contact.get('id') == contact_id:
                contact_found = True
                for key, value in updated_contact.items():
                    existing_contact[key] = value
                break
        if not contact_found:
            raise HTTPException(status_code=404, detail=f"Contact not found with provided ID: {contact_id}")
        
        await write_contacts(contacts)       
        for updated_contact in contacts:
            if updated_contact.get('id') == contact_id:
                updated_data = updated_contact
                break
            
        return updated_data
    
    
@router.delete("/{contact_id}",status_code=200)
async def delete_contact(contact_id:str):
    contacts = await read_contacts()
    contact_found = False
    for existing_contact in contacts:
        if existing_contact.get('id') == contact_id:
            contact_found = True
            contacts.remove(existing_contact)
            break
    if not contact_found:
        raise HTTPException(status_code=404, detail=f"Contact not found with provided ID: {contact_id}")

    await write_contacts(contacts)
    return {"detail": "Contact deleted successfully"}


@router.get("/{contact_id}",status_code=200)
async def get_contact(contact_id:str):
	contacts = await read_contacts()
	for existing_contact in contacts:
		if existing_contact.get('id') == contact_id:
			return existing_contact
	raise HTTPException(status_code=404, detail=f"Contact not found with provided ID: {contact_id}")
