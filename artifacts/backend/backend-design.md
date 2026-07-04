# Backend Design

## Purpose
Document the technical design and implementation details of the Task Management System backend.

## Metadata
- Version: 1.0
- Author: Backend Developer
- Date: 2026-07-04
- Status: Complete
- Technology: Python, FastAPI, SQLAlchemy, SQLite/PostgreSQL
- Artifact ID: BACKEND-DESIGN-001

---

## Architecture Overview

The backend implements a Clean Architecture with clear separation of concerns:

```
┌──────────────────────────────────────┐
│   FastAPI Routes (main.py)           │
│   - Request handling & response      │
│   - Dependency injection             │
│   - Error handling middleware        │
└──────────────────┬───────────────────┘
                   │
┌──────────────────▼───────────────────┐
│   Services (Business Logic)          │
│   - AuthService                      │
│   - TaskService                      │
│   - CollaborationService             │
│   - ReportingService                 │
└──────────────────┬───────────────────┘
                   │
┌──────────────────▼───────────────────┐
│   Repositories (Data Access)         │
│   - UserRepository                   │
│   - TaskRepository                   │
│   - CommentRepository                │
│   - AuditRepository                  │
│   - TeamRepository                   │
│   - NotificationRepository           │
└──────────────────┬───────────────────┘
                   │
┌──────────────────▼───────────────────┐
│   SQLAlchemy ORM & Models            │
│   - User, Task, Team, Comment        │
│   - Notification, AuditEntry         │
│   - Database schema & relationships  │
└──────────────────┬───────────────────┘
                   │
┌──────────────────▼───────────────────┐
│   Database (SQLite/PostgreSQL)       │
│   - Tables and relationships         │
│   - Indexes for performance          │
│   - Audit trail (immutable)          │
└──────────────────────────────────────┘
```

---

## Layered Design

### API Layer (main.py)
- **FastAPI application** with async request handling
- **Route handlers** for all REST endpoints
- **Dependency injection** for services and database
- **Error handling middleware** for structured responses
- **Authentication** via JWT Bearer tokens

### Service Layer
**AuthService**:
- User registration and password hashing
- Login and token generation
- Credential validation with bcrypt
- Audit logging for auth events

**TaskService**:
- Task CRUD operations with authorization checks
- Business rule validation (BR-001 through BR-008)
- Task status and priority management
- Archive/restore functionality
- Task duplication
- List filtering, searching, and pagination

**CollaborationService**:
- Comment creation and management
- Comment editing (author/admin only)
- Comment deletion with authorization
- Comment retrieval with pagination

**ReportingService**:
- Dashboard metrics calculation
- Task statistics and summaries
- Overdue task detection
- Completion rate calculation

### Repository Layer
Base repository pattern for consistent CRUD operations:
- Generic `BaseRepository<T>` for common operations
- Specialized repositories with domain-specific queries
- Transaction management and session handling
- Query filtering and pagination

**UserRepository**:
- User lookup by ID and email
- Active user retrieval
- User creation with role assignment

**TaskRepository**:
- Complex task filtering with multiple criteria
- Full-text search on title and description
- Status and priority filtering
- Due date range filtering
- Visibility checks (authorization)
- Archive/restore operations
- Pagination support

**CommentRepository**, **TeamRepository**, **AuditRepository**, **NotificationRepository**:
- Specialized repositories for their domains
- Domain-specific queries
- Relationship management

### Model Layer
**SQLAlchemy ORM Models**:
- User: Account with email, password_hash, role, timestamps
- Task: Work item with ownership, assignment, status, priority, due date
- Team: Group of users
- Comment: Task discussion with author and timestamps
- Notification: Event notification to users
- NotificationPreference: User notification settings
- AuditEntry: Immutable log of all actions

**Enums**:
- TaskStatus: todo, in_progress, review, completed, blocked
- TaskPriority: low, medium, high, critical
- UserRole: ADMIN, TEAM_LEAD, TEAM_MEMBER

### Database Layer
**SQLAlchemy Configuration**:
- SQLite for development (file-based)
- PostgreSQL support for production
- Connection pooling
- Automatic schema creation on startup

**Indexes**:
- task.owner_id for task ownership queries
- task.assignee_id for assignment queries
- task.status for status filtering
- task.team_id for team filtering
- user.email for login lookups
- comment.task_id for comment retrieval
- notification.user_id for notification queries
- audit_entry.task_id and audit_entry.created_at for audit logs

---

## Key Design Decisions

### 1. Clean Architecture
Separation of concerns enables:
- Easy testing with mock repositories
- Business logic independent of frameworks
- Database abstraction
- Simple service injection

### 2. Repository Pattern
Benefits:
- Consistent data access interface
- Easy to swap database implementations
- Centralized query logic
- Transaction management

### 3. Service Locator Pattern
- Services receive repositories via constructor
- Explicit dependencies
- Easy to test and mock

### 4. DTOs (Data Transfer Objects)
Pydantic schemas provide:
- Request/response validation
- Type checking at API boundaries
- Automatic documentation
- JSON serialization/deserialization

### 5. Error Handling
Custom exceptions hierarchy:
- ApplicationError (base)
- ValidationError (INVALID_INPUT, 400)
- UnauthorizedError (UNAUTHORIZED, 401)
- ForbiddenError (FORBIDDEN, 403)
- NotFoundError (NOT_FOUND, 404)
- ConflictError (CONFLICT, 409)
- DuplicateResourceError (DUPLICATE_RESOURCE, 400)
- UnprocessableError (UNPROCESSABLE, 422)
- DependencyUnavailableError (DEPENDENCY_UNAVAILABLE, 503)

### 6. Authentication
- JWT tokens with 24-hour expiry
- Bcrypt password hashing (recommended cost factor)
- Bearer token in Authorization header
- Stateless authentication

### 7. Authorization
- Role-based access control (RBAC)
- Service-level authorization checks
- Task ownership and assignment checks
- Admin override capabilities

### 8. Audit Logging
- Immutable audit trail
- JSON-serialized change tracking
- Automatic action logging
- Timestamp recording

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role ENUM('ADMIN', 'TEAM_LEAD', 'TEAM_MEMBER'),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status ENUM('todo', 'in_progress', 'review', 'completed', 'blocked'),
    priority ENUM('low', 'medium', 'high', 'critical'),
    owner_id VARCHAR(36) FOREIGN KEY REFERENCES users(id),
    assignee_id VARCHAR(36) FOREIGN KEY REFERENCES users(id),
    team_id VARCHAR(36) FOREIGN KEY REFERENCES teams(id),
    due_date DATETIME,
    archived_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Comments Table
```sql
CREATE TABLE comments (
    id VARCHAR(36) PRIMARY KEY,
    task_id VARCHAR(36) FOREIGN KEY REFERENCES tasks(id),
    author_id VARCHAR(36) FOREIGN KEY REFERENCES users(id),
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

### Audit Entries Table
```sql
CREATE TABLE audit_entries (
    id VARCHAR(36) PRIMARY KEY,
    task_id VARCHAR(36) FOREIGN KEY REFERENCES tasks(id),
    user_id VARCHAR(36) FOREIGN KEY REFERENCES users(id),
    action VARCHAR(100),
    entity_type VARCHAR(50),
    entity_id VARCHAR(36),
    details TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## API Implementation Details

### Request/Response Format
All responses wrapped in consistent format:
```json
{
  "data": {...},
  "pagination": {...} // Optional, for list endpoints
}
```

### Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": [{...}],
    "timestamp": "ISO-8601 timestamp",
    "requestId": "UUID"
  }
}
```

### Authentication
JWT token in header: `Authorization: Bearer <token>`
Token claims:
- user_id
- email
- role
- iat (issued at)
- exp (expiration)

---

## Performance Considerations

### Database Indexes
- User email lookup (login): < 10ms
- Task queries by owner/assignee: < 50ms with pagination
- Comment retrieval: < 100ms with pagination
- Full-text search: < 1 second for typical workloads

### Query Optimization
- Pagination limiting to 100 items max
- Lazy loading of relationships where needed
- Index usage for common filters
- No N+1 queries in service methods

### Caching Strategy
- Dashboard metrics: 5-minute TTL (future implementation)
- User profile: Per-request cache
- Task relationships: Loaded with task

---

## Security Implementation

### Password Security
- Bcrypt hashing with configurable cost
- Minimum 8 characters enforced
- No password reuse check (future)

### Token Security
- HS256 symmetric algorithm
- 24-hour expiry
- Tokens invalidated by logout (future)
- Secure secret key in production

### Input Validation
- Pydantic schema validation
- Email format validation
- String length limits
- Enum validation for status/priority

### Authorization Enforcement
- Service-level checks before data access
- Task ownership verification
- Role-based admin checks
- Team membership validation (future)

### Data Protection
- SQL injection prevention via SQLAlchemy ORM
- CORS enabled for frontend origins
- Audit trail for accountability
- No sensitive data in logs

---

## Testing Strategy

### Unit Tests
- Service layer business logic
- Repository data access operations
- Utility functions (JWT, password hashing)
- Validation rules

### Integration Tests
- API endpoint contract testing
- Database transaction handling
- End-to-end workflows
- Error handling paths

### Test Coverage
Target: 80%+ code coverage
- Critical services: 90%+ coverage
- Utility functions: 100% coverage
- Repositories: 85%+ coverage
- API routes: 75%+ coverage

---

## Deployment Strategy

### Development
- SQLite database file-based
- uvicorn development server
- Auto-reload on code changes

### Production
- PostgreSQL database with connection pooling
- Gunicorn WSGI server with multiple workers
- Docker containerization
- Environment-based configuration
- Secrets management via environment variables

---

## Future Enhancements

### Short-term (Next Sprint)
- Password reset email tokens
- Notification delivery (email/in-app)
- Full-text search optimization
- Rate limiting per endpoint
- Request ID correlation for debugging

### Medium-term
- WebSocket support for real-time updates
- Bulk operations optimization
- Advanced analytics and reporting
- File attachment storage
- Email notifications with templates

### Long-term
- Event-driven architecture with message queue
- Caching layer (Redis)
- Elasticsearch for full-text search
- GraphQL API alongside REST
- API versioning strategy

---

## Maintenance Notes

### Database Migrations
- Alembic configured (to be implemented)
- Version control for schema changes
- Migration scripts in `migrations/` directory

### Logging
- Structured logging via FastAPI/Uvicorn
- Audit trail in database
- Future: Centralized logging service

### Monitoring
- Health check endpoint `/health`
- Future: Prometheus metrics
- Future: Sentry error tracking

---

## Success Criteria

✓ All 35+ API endpoints implemented
✓ Business rules BR-001 through BR-015 enforced
✓ Authentication and authorization working
✓ Audit trail recording all privileged actions
✓ /health endpoint responding successfully
✓ Error codes matching specification
✓ Database schema created automatically
✓ No unhandled exceptions
✓ Response formats matching API spec
✓ Test suite executing successfully
