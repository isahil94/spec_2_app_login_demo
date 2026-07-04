# Task Management System - Backend

FastAPI-based REST API backend for the collaborative task management system.

## Architecture

The backend follows a Clean Architecture pattern with layers:

- **Controllers/Routes**: HTTP request handling and response formatting
- **Services**: Business logic and orchestration
- **Repositories**: Data access and persistence
- **Models**: Domain entities and database schema
- **Schemas**: Request/response DTOs and validation

## Project Structure

apps/backend/
├── src/
│   ├── config/          # Configuration settings
│   ├── db/              # Database setup and initialization
│   ├── models/          # SQLAlchemy models
│   ├── repositories/    # Data access objects
│   ├── services/        # Business logic services
│   ├── schemas/         # Pydantic schemas (DTOs)
│   ├── middleware/      # FastAPI middleware
│   ├── utils/           # Utilities (JWT, password hashing, exceptions)
│   └── controllers/     # Route controllers
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── main.py              # FastAPI application entry point
├── conftest.py          # Pytest configuration
├── .env                 # Environment variables
└── README.md            # This file

## Getting Started

### Prerequisites

- Python 3.9+
- Virtual environment (venv)
- Dependencies from requirements.txt

### Installation

1. **Install dependencies**:

```bash
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

1. **Start the backend server**:

```bash
.\.venv\Scripts\python.exe -m uvicorn apps.backend.main:app --reload --port 8001
```

1. **Verify health endpoint**:

```bash
curl http://127.0.0.1:8001/health
```

Expected response:

```json
{"status": "healthy", "timestamp": "2026-07-04T..."}
```

## API Documentation

The API follows RESTful principles and is organized into resource groups:

### Authentication Endpoints

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Authenticate user
- `POST /api/v1/auth/logout` - Logout user

### Task Endpoints

- `GET /api/v1/tasks` - List tasks (with filtering and pagination)
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{taskId}` - Get task details
- `PATCH /api/v1/tasks/{taskId}` - Update task
- `DELETE /api/v1/tasks/{taskId}` - Delete task (admin only)
- `POST /api/v1/tasks/{taskId}/archive` - Archive task
- `POST /api/v1/tasks/{taskId}/restore` - Restore archived task
- `POST /api/v1/tasks/{taskId}/duplicate` - Duplicate task

### Comment Endpoints

- `GET /api/v1/tasks/{taskId}/comments` - Get task comments
- `POST /api/v1/tasks/{taskId}/comments` - Add comment
- `PATCH /api/v1/tasks/{taskId}/comments/{commentId}` - Update comment
- `DELETE /api/v1/tasks/{taskId}/comments/{commentId}` - Delete comment

### Dashboard Endpoints

- `GET /api/v1/dashboard/metrics` - Get dashboard metrics

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register** a new user at `POST /api/v1/auth/register`
2. **Login** to get a token at `POST /api/v1/auth/login`
3. **Include token** in subsequent requests: `Authorization: Bearer <token>`

Token expiry: 24 hours (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)

## Business Rules

Key business rules enforced:

- **BR-001**: Every task has one owner and at most one assignee
- **BR-002**: Only administrators can permanently delete tasks
- **BR-003**: Archived tasks remain searchable but read-only for standard users
- **BR-004**: Completed tasks cannot be edited by standard users
- **BR-005**: Task history is immutable with audit entries
- **BR-006**: Due dates cannot be earlier than today
- **BR-007**: Supported statuses: Todo, In Progress, Review, Completed, Blocked
- **BR-008**: Supported priorities: Low, Medium, High, Critical

## Database

**Development**: SQLite (file-based, no setup required)
**Production**: PostgreSQL (configurable via `DATABASE_URL` env var)

Tables automatically created on first run.

## Testing

Run unit tests:

```bash
.\.venv\Scripts\python.exe -m pytest tests/unit -v
```

Run all tests:

```bash
.\.venv\Scripts\python.exe -m pytest tests -v
```

Run with coverage:

```bash
.\.venv\Scripts\python.exe -m pytest tests --cov=apps.backend --cov-report=html
```

## Error Handling

The API returns structured error responses:

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Validation failed",
    "details": [...],
    "timestamp": "2026-07-04T...",
    "requestId": "..."
  }
}
```

Error codes:
- `INVALID_INPUT` (400): Validation error
- `UNAUTHORIZED` (401): Invalid credentials
- `FORBIDDEN` (403): Access denied
- `NOT_FOUND` (404): Resource not found
- `CONFLICT` (409): Concurrent edit or invalid state
- `UNPROCESSABLE` (422): Business rule violation
- `RATE_LIMIT` (429): Too many requests
- `DEPENDENCY_UNAVAILABLE` (503): Database or service unavailable

## Development

### Code Quality

Format code:
```bash
.\.venv\Scripts\python.exe -m black . --line-length=100
```

Lint code:
```bash
.\.venv\Scripts\python.exe -m flake8 . --max-line-length=100
```

### Environment Variables

Copy `.env.example` to `.env` and update for your environment:
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT signing key (change for production)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiry duration
- `DEBUG`: Enable/disable debug mode

## Performance

Target performance metrics:

- Dashboard queries: < 2 seconds (p95)
- Search queries: < 1 second (p95)
- Task list pagination: < 500ms (p95)

Database indexes created on:
- Task owner_id
- Task assignee_id
- Task status
- Task team_id

## Security

Implemented security measures:

- Password hashing: bcrypt with salting
- Authentication: JWT with configurable expiry
- Authorization: Role-based access control (RBAC)
- Input validation: Pydantic schema validation
- CORS: Configurable allowed origins
- SQL injection protection: SQLAlchemy parameterized queries
- Audit logging: Immutable audit trail for sensitive actions

## Deployment

### Docker

Build and run containerized backend:
```bash
docker build -f apps/backend/Dockerfile -t task-management-api .
docker run -p 8001:8001 task-management-api
```

### Production Checklist

- [ ] Update `SECRET_KEY` with secure random value
- [ ] Set `DEBUG=False`
- [ ] Use PostgreSQL for database
- [ ] Configure CORS origins appropriately
- [ ] Enable HTTPS (TLS)
- [ ] Set up monitoring and alerting
- [ ] Configure backup/recovery procedures
- [ ] Run security scan on dependencies
- [ ] Test rate limiting and load handling
- [ ] Set up centralized logging

## Troubleshooting

### Common Issues

**Port 8001 already in use**:

```bash
# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

**Database locked**:

- SQLite locks during concurrent writes
- Use PostgreSQL for concurrent access
- Restart the application if locked

**JWT token expired**:

- Login again to get a fresh token
- Increase `ACCESS_TOKEN_EXPIRE_MINUTES` if needed

## Contributing

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Run linting and formatting before commits

## License

Proprietary - See LICENSE file
