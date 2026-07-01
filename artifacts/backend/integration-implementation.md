# Integration Implementation

## Internal Integrations
- SQLAlchemy session integration via apps/backend/db.py and dependency injection in routes.
- JWT integration via apps/backend/src/auth/jwt.py and security dependency wrappers.
- Logging integration via apps/backend/src/logging/logger.py and app bootstrap in main.py.

## External/Deferred Integrations
- Password recovery delivery is implemented as API behavior placeholder pending provider wiring.
- Notification delivery provider integration remains deferred; persistence and API contracts are in place.

## Integration Boundaries
- Backend stage owns API/service integration points and contracts.
- Database schema evolution and deployment integrations remain downstream responsibilities.
