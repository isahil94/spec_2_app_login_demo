# Validation Rules

## Request Validation
- FastAPI + DTO schemas validate required fields and field types.
- Optional fields use explicit nullable/default handling in DTOs.

## Domain Validation
- Route-level checks enforce existence for user/task/team/project entities before updates.
- Status transition requests are validated through task service logic.

## Error Contract
- Validation errors map to 422 with structured payload in main.py exception handler.
- Business validation errors map to 400/401/404 as appropriate.

## Security Validation
- Auth dependencies validate token presence/decoding for protected routes.
- Role checks are enforced through security dependency helpers where required.
