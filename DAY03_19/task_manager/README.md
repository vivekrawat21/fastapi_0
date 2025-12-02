# Task Manager API (FastAPI)

A production-ready task management API built with FastAPI, featuring JWT authentication with role-based access control, MySQL database with SQLAlchemy ORM, and Clean Architecture principles.

---

## Quick Highlights

- **FastAPI** with async SQLAlchemy and MySQL database
- **JWT Authentication** with role-based access (Admin, Collector, Supervisor)
- **Clean Architecture**: Separated into routers, schemas, services, repositories, and models
- **SOLID Principles**: Dependency injection, interface segregation, single responsibility
- **Full CRUD**: Create, read, update, delete tasks with validation
- **User Management**: Registration, login, role assignment
- **Filtering**: By status, due_date, priority, and title search
- **Auto-docs**: Swagger UI at `/docs`, ReDoc at `/redoc`
- **Alembic Migrations**: Database version control
- **Error Handling**: Global middleware for exceptions

---

## Features

### ✅ Authentication & Authorization
- JWT token-based authentication
- Password hashing with Argon2
- Role-based access control:
  - **ADMIN**: Full access to all resources
  - **COLLECTOR**: Standard user access
  - **SUPERVISOR**: Elevated permissions
- Token includes user role in claims

### ✅ Task Management
- Create, read, update, delete tasks
- Task fields: title, description, status, priority, due_date
- Automatic user association via JWT
- Filter tasks by status, priority, due date

### ✅ User Management
- User registration with role selection
- Secure login with JWT tokens
- User profile with role information

---

## Architecture Overview

```
app/
├── main.py                 # FastAPI app with middleware
├── dependencies.py         # Dependency injection
├── unit_of_work.py         # Unit of Work pattern
├── api/
│   └── v1/
│       ├── routes/
│       │   ├── auth.py     # Authentication endpoints
│       │   ├── tasks.py    # Task CRUD endpoints
│       │   └── health.py   # Health check
│       └── schemas/
│           ├── tasks.py    # Task Pydantic models
│           └── user.py     # User models with UserRole enum
├── core/
│   ├── config.py           # Pydantic settings
│   ├── database.py         # SQLAlchemy async setup
│   ├── models.py           # SQLAlchemy ORM models
│   └── security.py         # JWT & password utilities
├── services/
│   ├── task_services.py    # Task business logic
│   └── user_services.py    # User business logic
├── repositories/
│   └── sqlalchemy_repository.py  # Generic repository pattern
└── middleware/
    └── exception_handler.py  # Global error handling
```

---

## Tech Stack

- **Framework**: FastAPI
- **Database**: MySQL with async SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Argon2 (passlib)
- **Validation**: Pydantic v2
- **ASGI Server**: Uvicorn

---

## Prerequisites

- Python 3.10+ (tested on 3.12)
- MySQL 8.0+
- Virtual environment recommended

---

## Installation

```bash
# Navigate to project
cd DAY03_19/task_manager

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your MySQL credentials
```

### Environment Variables

```env
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/taskmanager
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Database Setup

```bash
# Run migrations
alembic upgrade head
```

---

## Running the App

```bash
# Development
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **Health Check**: GET http://127.0.0.1:8000/api/v1/health

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login and get JWT | No |

### Tasks

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/tasks/` | List all tasks | Yes |
| GET | `/api/v1/tasks/{id}` | Get single task | Yes |
| POST | `/api/v1/tasks/` | Create new task | Yes |
| PUT | `/api/v1/tasks/{id}` | Update task | Yes |
| DELETE | `/api/v1/tasks/{id}` | Delete task | Yes |

### Health

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/health` | Health check | No |

---

## API Examples

### Register User

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "role": "COLLECTOR"
  }'
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "COLLECTOR"
}
```

### Login

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Create Task

```bash
curl -X POST http://127.0.0.1:8000/api/v1/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{
    "title": "New Task",
    "description": "Task description",
    "priority": "high",
    "status": "pending",
    "due_date": "2025-12-01"
  }'
```

### List Tasks with Filters

```bash
# Filter by status
curl "http://127.0.0.1:8000/api/v1/tasks/?status=pending" \
  -H "Authorization: Bearer <your-token>"

# Filter by priority
curl "http://127.0.0.1:8000/api/v1/tasks/?priority=high" \
  -H "Authorization: Bearer <your-token>"
```

---

## User Roles

The system supports three user roles defined in the `UserRole` enum:

| Role | Value | Description |
|------|-------|-------------|
| ADMIN | `"ADMIN"` | Full administrative access |
| COLLECTOR | `"COLLECTOR"` | Standard user (default) |
| SUPERVISOR | `"SUPERVISOR"` | Elevated permissions |

Roles are stored in MySQL as an ENUM type and included in JWT token claims.

---

## Database Models

### User Model

```python
class User(Base):
    id: int (primary key)
    email: str (unique)
    password: str (hashed)
    role: UserRole (default: COLLECTOR)
    tasks: relationship -> Task[]
```

### Task Model

```python
class Task(Base):
    id: int (primary key)
    title: str
    description: str (optional)
    status: str (pending/in_progress/completed)
    priority: str (low/medium/high)
    due_date: date
    user_id: int (foreign key -> User.id)
    user: relationship -> User
```

---

## Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1

# View current version
alembic current
```

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest app/tests/test_auth.py -v
```

---

## Recent Updates

### v2.0.0
- ✅ JWT Authentication with role claims
- ✅ Role-based access control (Admin, Collector, Supervisor)
- ✅ User registration with role selection
- ✅ Fixed task creation to get user_id from JWT
- ✅ Fixed task update logic in service layer
- ✅ MySQL enum case sensitivity fix
- ✅ Alembic migrations for role column
- ✅ Argon2 password hashing

---

## Contribution

- Follow Clean Architecture; add tests for new features
- Commit with conventional style (e.g., `feat: add task creation`)

---

## License

MIT

---

Happy coding!