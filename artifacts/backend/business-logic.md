# Business Logic

## Service Modules
- auth_service.py: registration, authentication, token issuance integration.
- project_service.py: project creation and retrieval.
- task_service.py: task lifecycle operations (create/update/archive/restore/duplicate/status).
- team_service.py: team management and membership updates.
- comment_service.py: task comment listing and creation.
- notification_service.py: read/list notification behavior.
- user_service.py: profile and settings retrieval/update.

## Behavioral Rules
- Route handlers validate input and delegate business decisions to services.
- Services enforce domain checks and return normalized data structures.
- Error paths are surfaced through HTTPException mapping with consistent error payload structure.

## Data Flow
- Route -> DTO parse -> Service call -> ORM persistence/query -> DTO response serialization.
