# Task Manager (FastAPI)

A small, file-backed task management API built with FastAPI. This repository contains a minimal example app that stores tasks in a JSON file and exposes endpoints to list tasks with filtering.

---

## Quick highlights
- FastAPI app with simple file-based persistence (`tasks.json`).
- Async file I/O using `aiofiles`.
- Structured with clear packages: `app.api`, `app.schemas`, `app.utils`.
- Task filtering by status, due_date, and search.

---

## Folder structure

```
DAY03_04/task_manager/
├─ app/
│  ├─ __init__.py
│  ├─ main.py                # FastAPI app
│  ├─ api/
│  │  ├─ __init__.py
│  │  ├─ v1/
│  │     ├─ __init__.py
│  │     ├─ routes/
│  │     │  ├─ __init__.py
│  │     │  ├─ health.py     # health check route
│  │     │  └─ tasks.py     # routes for /tasks
│  │     └─ schemas/
│  │        ├─ __init__.py
│  │        └─ tasks.py     # Pydantic models
│  └─ utils/
│     ├─ __init__.py
│     └─ files_io.py        # read/write tasks.json using aiofiles
├─ tasks.json                # data file (created/updated at runtime)
├─ requirements.txt
└─ .myenv/                   # (optional) local virtualenv — ignore in git
```

---

## Prerequisites
- Python 3.10+ (project uses 3.12 on your environment).
- The repository includes a virtual environment at `.myenv/` (do not commit this folder). If you prefer to create a fresh venv:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If you'd rather use the included `.myenv`:

```bash
source .myenv/bin/activate
```

---

## Running the app (development)

From the project root (`DAY03_04/task_manager`):

```bash
# activate venv (example using provided .myenv)
source .myenv/bin/activate

# run the FastAPI app with hot reload
.myenv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs for the interactive OpenAPI docs.

---

## API Endpoints

- GET `/health` — simple health check (returns `{ "status": "ok" }`).
- GET `/tasks/` — list all tasks with optional filtering by `status`, `due_date`, and `search` (title search).

Example: list tasks with status filter

```bash
curl "http://127.0.0.1:8000/tasks/?status=pending"
```

Example: search tasks by title

```bash
curl "http://127.0.0.1:8000/tasks/?search=grocery"
```

---

## Data persistence
- Tasks are stored in `tasks.json` in the project root. `app/utils/files_io.py` uses an absolute path — run the server from the project root to ensure the file is found.

---

## Contribution
- Fork and open a PR. Keep changes small and focused.
---
Happy coding!</content>
<parameter name="filePath">/home/vivek-rawat/Desktop/RSVR/fastapi_0/DAY03_04/task_manager/README.md