# Endpoint Implementation

## Implemented Endpoint Groups
- Health: GET /health
- Auth: POST /auth/register, POST /auth/login, POST /auth/recover, POST /auth/reset
- Users: GET /users/me, PUT /users/me, GET /users/settings, PUT /users/settings
- Projects: POST /projects, GET /projects/{project_id}
- Tasks: GET /tasks, POST /tasks, GET /tasks/{task_id}, PUT /tasks/{task_id}, POST /tasks/{task_id}/archive, POST /tasks/{task_id}/restore, POST /tasks/{task_id}/duplicate, POST /tasks/{task_id}/status
- Comments: GET /tasks/{task_id}/comments, POST /tasks/{task_id}/comments
- Teams: GET /teams, POST /teams, GET /teams/{team_id}, POST /teams/{team_id}/members

## Contract Alignment
- Request/response DTOs are implemented under apps/backend/src/dto/.
- HTTP error handling is centralized in apps/backend/main.py handlers.
- Protected endpoint authorization uses apps/backend/src/auth/security.py dependencies.

## Notes
- Project endpoints are included to satisfy existing backend baseline tests.
