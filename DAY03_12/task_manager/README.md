# Task Manager (FastAPI)

A production-ready task management API built with FastAPI, following Clean Architecture and SOLID principles. Stores tasks in a JSON file with async I/O, includes CRUD operations, filtering, error handling, and testing. Features dependency injection and service interfaces for maintainability.

---

## Quick highlights
- FastAPI app with file-based persistence (`tasks.json`) and async operations.
- Clean Architecture: Separated into routers (endpoints), schemas (Pydantic models), services (business logic with interfaces), utils (file I/O), and core (config, helpers).
- SOLID principles: Dependency injection, interface segregation, single responsibility.
- Full CRUD: Create, read, update, delete tasks with validation.
- Filtering: By status, due_date, and title search.
- Auto-docs: Swagger UI at `/docs`, ReDoc at `/redoc`.
- Testing: Unit and integration tests with pytest + httpx.
- Error handling: Global middleware for exceptions.

---

## Architecture Overview
- **Routers** (`app/api/v1/routes/`): API endpoints with dependency injection.
- **Schemas** (`app/api/v1/schemas/`): Pydantic models for request/response validation.
- **Services** (`app/services/`): Business logic implementing interfaces (e.g., `TaskService` implements `TaskServiceInterface`).
- **Interfaces** (`app/services/interfaces/`): Abstract base classes defining contracts (e.g., `TaskServiceInterface` with abstract methods).
- **Utils** (`app/utils/`): File I/O helpers with custom JSON serialization.
- **Core** (`app/core/`): Config (Pydantic settings) and helpers (e.g., UUID generation).
- **Dependency Injection**: Routes inject services via `Depends()`, promoting testability and loose coupling.

---

## Folder structure

```
DAY03_04/task_manager/
├─ app/
│  ├─ __init__.py
│  ├─ main.py                # FastAPI app with middleware
│  ├─ api/
│  │  ├─ __init__.py
│  │  ├─ v1/
│  │     ├─ __init__.py
│  │     ├─ routes/
│  │     │  ├─ __init__.py
│  │     │  ├─ health.py     # health check
│  │     │  └─ tasks.py     # task CRUD routes with DI
│  │     └─ schemas/
│  │        ├─ __init__.py
│  │        └─ tasks.py     # Pydantic models (Task, TaskCreate, etc.)
│  ├─ services/
│  │  ├─ __init__.py
│  │  ├─ interfaces/
│  │  │  ├─ __init__.py
│  │  │  └─ task_service_interfaces.py  # ABC for TaskService
│  │  └─ task_services.py   # TaskService implementation
│  ├─ utils/
│  │  ├─ __init__.py
│  │  └─ files_io.py        # async read/write to tasks.json
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ config.py          # Pydantic settings
│  │  └─ tasks.py           # UUID generation
│  ├─ database/
│  │  └─ __init__.py        # placeholder for future DB layer
│  ├─ tests/
│  │  ├─ __init__.py
│  │  └─ test_health.py     # pytest tests
│  └─ tasks.json            # data file
├─ requirements.txt
├─ TaskManager-RSVR.postman_collection.json  # API tests
├─ .gitignore
└─ .myenv/                   # virtualenv (ignore in git)
```

---

## Prerequisites
- Python 3.10+ (tested on 3.12).
- Virtual environment: Use included `.myenv/` or create new:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Running the app (development)

From project root:

```bash
source .myenv/bin/activate
.myenv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- Docs: http://127.0.0.1:8000/docs (Swagger) or /redoc.
- Health: GET http://127.0.0.1:8000/health

---

## API Endpoints

- GET `/api/v1/health` — Health check.
- GET `/api/v1/tasks/` — List tasks with filtering.
- GET `/api/v1/tasks/{id}` — Fetch single task.
- POST `/api/v1/tasks/` — Create new task.
- PUT `/api/v1/tasks/{id}` — Update task.
- DELETE `/api/v1/tasks/{id}` — Delete task.

Examples:

```bash
# List pending tasks
curl "http://127.0.0.1:8000/api/v1/tasks/?status=pending"

# Create task
curl -X POST http://127.0.0.1:8000/api/v1/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title":"New Task","description":"Desc","priority":"high","status":"pending","due_date":"2025-12-01"}'
```

---

## Data persistence
- Tasks stored in `tasks.json` (absolute path in `files_io.py`).
- Async I/O with `aiofiles`; custom JSON encoder for dates.

---

## Testing
- Run tests: `pytest` (requires pytest, httpx in requirements).
- Covers unit tests for routes and services.

---

## Contribution
- Follow Clean Architecture; add tests for new features.
- Commit with conventional style (e.g., `feat: add task creation`).

---
Happy coding!</content>
<parameter name="filePath">/home/vivek-rawat/Desktop/RSVR/fastapi_0/DAY03_04/task_manager/README.md