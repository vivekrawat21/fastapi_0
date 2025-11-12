# Task Manager (FastAPI)

A clean and simple Task Manager API built with FastAPI, following Clean Architecture principles. This project uses file-based JSON storage with async I/O for persistence, includes full CRUD operations, filtering capabilities, error handling, and comprehensive testing.

## Features

- **FastAPI** with automatic API documentation (Swagger/ReDoc)
- **File-based persistence** using JSON storage (`app/tasks.json`)
- **Clean Architecture** with clear separation of concerns
- **Async I/O** operations for all file handling
- **Full CRUD operations** for task management
- **Filtering support** by status, due date, and title search
- **Pydantic validation** for request/response models
- **Unit testing** with pytest and async mocks
- **Exception middleware** for centralized error handling
- **CORS support** for frontend integration

## Project Structure

```
TASK_MANAGER/
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app factory and configuration
│   ├── dependencies.py             # Dependency injection setup
│   ├── tasks.json                  # JSON data store
│   ├── unit_of_work.py             # Unit of Work pattern implementation
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── routers/
│   │       │   └── tasks.py        # Task CRUD endpoints
│   │       ├── routes/
│   │       │   ├── __init__.py
│   │       │   └── health.py       # Health check endpoint
│   │       └── schemas/
│   │           ├── __init__.py
│   │           ├── tasks.py        # Pydantic models and enums
│   │           └── health.py       # Health response models
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Application settings
│   │   └── tasks.py                # ID generation utilities
│   ├── middleware/
│   │   └── exception_middleware.py # Global exception handling
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── json_repository.py      # JSON file repository implementation
│   │   └── interfaces/
│   │       └── task_repository_interface.py  # Repository interface
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_services.py        # Business logic layer
│   │   └── interfaces/
│   │       └── task_service_interfaces.py    # Service interfaces
│   ├── utils/
│   │   ├── __init__.py
│   │   └── files_io.py             # Async file I/O utilities
│   └── tests/
│       ├── __init__.py
│       ├── test_health.py
│       ├── test_middleware.py
│       └── test_task_service.py    # Service layer tests
```

## Installation

1. **Clone the repository and navigate to the project folder:**

```bash
cd TASK_MANAGER
```

2. **Create and activate a virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## Running the Application

**Start the development server:**

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Access the API:**
- **API Documentation (Swagger):** http://127.0.0.1:8000/docs
- **Alternative Documentation (ReDoc):** http://127.0.0.1:8000/redoc
- **Health Check:** http://127.0.0.1:8000/ or http://127.0.0.1:8000/api/v1/health

## API Endpoints

### Health Check
- `GET /` - Root health check
- `GET /api/v1/health` - Versioned health check

### Tasks
- `GET /api/v1/tasks/` - List all tasks (supports filtering)
- `GET /api/v1/tasks/{id}` - Get a specific task by ID
- `POST /api/v1/tasks/` - Create a new task
- `PUT /api/v1/tasks/{id}` - Update an existing task
- `DELETE /api/v1/tasks/{id}` - Delete a task

### Query Parameters for Task Listing
- `status` - Filter by task status (`pending`, `in_progress`, `completed`)
- `due_date` - Filter by due date (YYYY-MM-DD format)
- `search` - Search tasks by title (case-insensitive)

## API Examples

**Create a task:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, Bread, Eggs",
    "priority": "medium",
    "status": "pending",
    "due_date": "2025-11-15"
  }'
```

**List pending tasks:**
```bash
curl "http://127.0.0.1:8000/api/v1/tasks/?status=pending"
```

**Search tasks by title:**
```bash
curl "http://127.0.0.1:8000/api/v1/tasks/?search=groceries"
```

## Data Storage

Tasks are stored in `app/tasks.json` as a JSON array. The file is automatically created when the first task is added. All file operations are handled asynchronously using `aiofiles` for optimal performance.

## Testing

**Run all tests:**
```bash
pytest
```

**Run tests with verbose output:**
```bash
pytest -v
```

**Run specific test file:**
```bash
pytest app/tests/test_task_service.py -v
```

**Run tests with coverage:**
```bash
pytest --cov=app
```

The test suite includes:
- Service layer unit tests with async mocks using `pytest-asyncio`
- Health endpoint tests
- Middleware exception handling tests

All tests use the asyncio backend for consistent async testing.

## Architecture Overview

This project follows **Clean Architecture** principles:

- **API Layer** (`app/api/`): FastAPI routes and Pydantic schemas
- **Service Layer** (`app/services/`): Business logic and domain rules
- **Repository Layer** (`app/repositories/`): Data access abstraction
- **Core Layer** (`app/core/`): Configuration and shared utilities
- **Infrastructure** (`app/utils/`, `app/middleware/`): Cross-cutting concerns

The **Unit of Work pattern** ensures data consistency and provides a clean interface for managing transactions (in this case, atomic JSON file writes).

## Development

The project uses:
- **Dependency Injection** via FastAPI's `Depends()`
- **Interface Segregation** with abstract base classes
- **Single Responsibility** with focused, testable components
- **Async/Await** throughout for non-blocking operations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is open source and available under the MIT License.</content>
<parameter name="filePath">/home/vivek-rawat/Desktop/RSVR/fastapi_0/DAY03_04/task_manager/README.md