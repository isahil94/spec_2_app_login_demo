# Backend Design

## Scope
Business layer implementation for authentication, users, projects, tasks, teams, comments, notifications, and reporting endpoints.

## Structure
- API entrypoint: apps/backend/main.py
- Route composition: apps/backend/src/routes/routes.py
- Services: apps/backend/src/services/
- Domain models: apps/backend/src/domain/models.py
- DTOs: apps/backend/src/dto/
- Auth/security: apps/backend/src/auth/

## Layering
- Routes handle transport concerns and dependency wiring.
- Services encapsulate business rules and persistence operations.
- DTOs define request/response contracts.
- Domain models map persistent entities.

## Design Constraints
- Follow architecture contracts from artifacts/architecture/api-contracts.md.
- Keep implementation within backend boundary; no DB migration ownership in this stage.
- Keep error model and auth behavior consistent across routes.
