# Contact Manager (FastAPI)

A small, file-backed contact management API built with FastAPI. This repository contains a minimal example app that stores contacts in a JSON file and exposes endpoints to list, create, and update contacts.

---

## Quick highlights
- FastAPI app with simple file-based persistence (`contacts.json`).
- Async file I/O using `aiofiles`.
- Structured with clear packages: `app.api`, `app.schemas`, `app.services`, `app.utils`.

---

## Folder structure

```
DAY01_02/contact_manager/
├─ app/
│  ├─ __init__.py
│  ├─ main.py                # FastAPI app
│  ├─ api/
│  │  ├─ __init__.py
│  │  ├─ core/
│  │  │  ├─ __init__.py
│  │  │  └─ contact.py       # id generation, core helpers
│  │  └─ routers/
│  │     ├─ __init__.py
│  │     └─ contact.py       # routes for /contacts
│  ├─ schemas/
│  │  ├─ __init__.py
│  │  └─ contact_schema.py   # Pydantic models
│  ├─ services/
│  │  └─ contact_services.py # (optional) business logic
│  └─ utils/
│     ├─ __init__.py
│     └─ file_utils.py       # read/write contacts.json using aiofiles
├─ contacts.json              # data file (created/updated at runtime)
├─ requirements.txt
└─ myenv/                     # (optional) local virtualenv — ignore in git
```

---

## Prerequisites
- Python 3.10+ (project uses 3.12 on your environment).
- The repository includes a virtual environment at `myenv/` (do not commit this folder). If you prefer to create a fresh venv:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If you'd rather use the included `myenv`:

```bash
source myenv/bin/activate
```

---

## Running the app (development)

From the project root (`DAY01_02/contact_manager`):

```bash
# activate venv (example using provided myenv)
source myenv/bin/activate

# run the FastAPI app with hot reload
myenv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs for the interactive OpenAPI docs.

---

## API Endpoints

- GET `/health` — simple health check (returns `{ "status": "ok" }`).
- GET `/contacts/` — list all contacts defaulty sorted according to name.
- GET `/search` - Partial searching according to name help of query parameters
- POST `/contacts/` — create a contact.
 Expects a JSON body with `name`, `email`, and `phone`.
- PUT `/contacts/{contact_id}` — update an existing contact (current implementation performs a partial merge of provided fields).

Example: create a contact with curl

```bash
curl -X POST http://127.0.0.1:8000/contacts/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com","phone":"+11111111"}'
```

---

## Data persistence
- Contacts are stored in `contacts.json` in the project root. `app/utils/file_utils.py` currently uses a relative path `'contacts.json'` — run the server from the project root to ensure the file is found. Consider changing `CONTACTS_FILE_PATH` to an absolute or configurable path for more robust deployments.

---

## Design notes & tips
- Keep `__init__.py` files lightweight. Avoid heavy imports in package initializers to prevent import errors during testing or tooling.
- `app/api/routers/contact.py` uses `ContactCreate` and `ContactUpdate` Pydantic models. For partial updates, `.model_dump(exclude_unset=True)` is used so only provided fields are merged.
- `generate_unique_id` lives in `app/api/core/contact.py` and is async; remember to `await` it when used.

---

## Contribution
- Fork and open a PR. Keep changes small and focused.
- Add tests (pytest) for new behavior and include sample data when useful.

---
Happy coding!
