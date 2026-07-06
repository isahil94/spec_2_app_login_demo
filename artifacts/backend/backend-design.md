# Backend Design

## Workflow Context
- Workflow ID: WF-20260705-001
- Correlation ID: CORR-20260705-001
- Agent: backend-developer
- Stage: Backend

## Summary
The backend for the Task Management System will provide a secure REST API for authentication, user management, task operations, comments, attachments, and reporting. The design is intended to support the web application described in the specification and to integrate with the approved frontend and database contracts.

## Technology Choices
- Framework: FastAPI
- Server: Uvicorn
- Validation: Pydantic
- ORM: SQLAlchemy
- Authentication: JWT with password hashing
- Storage: Relational database with support for users, tasks, comments, and attachments
- Logging: Structured application logs

## API Surface
### Authentication
- POST /auth/register
- POST /auth/login
- POST /auth/logout
- POST /auth/forgot-password
- POST /auth/reset-password

### Users and Profiles
- GET /users/me
- PUT /users/me
- GET /users/{id}
- PUT /users/{id} (admin)
- DELETE /users/{id} (admin)

### Tasks
- GET /tasks
- GET /tasks/{id}
- POST /tasks
- PUT /tasks/{id}
- DELETE /tasks/{id}
- POST /tasks/{id}/restore
- POST /tasks/bulk-update (admin)
- DELETE /tasks/bulk-delete (admin)

### Comments and Attachments
- GET /tasks/{id}/comments
- POST /tasks/{id}/comments
- POST /tasks/{id}/attachments

### Dashboard and Reporting
- GET /dashboard/summary
- GET /dashboard/recent-activity
- GET /dashboard/workload

## Core Data Model
- User
  - id, email, password_hash, name, role, status, avatar_url, preferences
- Task
  - id, title, description, status, priority, assignee_id, reporter_id, due_date, labels, archived, created_at, updated_at
- Comment
  - id, task_id, author_id, body, created_at
- Attachment
  - id, task_id, file_name, storage_path, uploaded_by, created_at
- ActivityLog
  - id, entity_type, entity_id, action, actor_id, created_at

## Business Rules
- Task statuses: Todo, In Progress, Review, Completed, Blocked
- Valid transitions: Todo -> In Progress, In Progress -> Review, Review -> Completed, Review -> In Progress, Blocked -> In Progress
- Completed tasks are read-only except for administrators
- Archived tasks are read-only
- Only administrators may perform bulk delete and role changes

## Validation and Error Handling
- Request validation via Pydantic schemas
- Business-rule validation at service layer
- Standardized error responses for 400, 401, 403, 404, 409, 422, and 500
- Structured logs for failed requests and permission violations

## Security Considerations
- Password hashing with a strong one-way hash
- JWT-based authentication and authorization
- Role-based access control for admin and non-admin operations
- Input sanitization and output encoding for user-generated content

## Testing Strategy
- Unit tests for services and validators
- Integration tests for API endpoints and auth flow
- Workflow tests for task lifecycle and permission scenarios
