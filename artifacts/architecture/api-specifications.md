# API Specifications

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-05
- Status: Draft
- Architecture ID: ARCH-003
- Workflow ID: WF-20260705-001

## API Catalog

### Authentication API
- Purpose: Register, authenticate, log out, and recover passwords
- Consumer: Frontend web application
- Provider: Authentication service
- Methods: POST /auth/register, POST /auth/login, POST /auth/logout, POST /auth/password-reset, POST /auth/oauth/login
- AuthN: Session-based or token-based authentication
- AuthZ: Public for registration/login, protected for logout and password reset
- Validation Rules: Email format, password policy, request body validation
- Error Model: 400 validation error, 401 unauthorized, 409 conflict, 503 dependency unavailable
- Audit Expectations: Login, logout, password-reset, and registration events

### Task API
- Purpose: Create, update, list, retrieve, archive, restore, duplicate, and delete tasks
- Consumer: Frontend web application
- Provider: Task service
- Methods: GET /tasks, POST /tasks, GET /tasks/{id}, PUT /tasks/{id}, PATCH /tasks/{id}/status, POST /tasks/{id}/archive, POST /tasks/{id}/restore, POST /tasks/{id}/duplicate, DELETE /tasks/{id}
- AuthN: Required
- AuthZ: Role and ownership checks
- Validation Rules: Required title, valid due date, allowed status transitions, permission checks
- Error Model: 400 validation error, 403 forbidden, 404 not found, 409 conflict, 503 dependency unavailable
- Audit Expectations: Task lifecycle and status-change events

### Collaboration API
- Purpose: Manage comments, attachments, and task history
- Consumer: Frontend web application
- Provider: Collaboration service
- Methods: GET /tasks/{id}/comments, POST /tasks/{id}/comments, POST /tasks/{id}/attachments, GET /tasks/{id}/history
- AuthN: Required
- AuthZ: Task visibility and write permission checks
- Validation Rules: Comment content and attachment metadata validation
- Error Model: 400 validation error, 403 forbidden, 404 not found, 503 dependency unavailable
- Audit Expectations: Comment and attachment create events

### Notification API
- Purpose: Retrieve and manage user notifications
- Consumer: Frontend web application
- Provider: Notification service
- Methods: GET /notifications, PATCH /notifications/{id}/read, POST /notifications/refresh
- AuthN: Required
- AuthZ: Recipient-scoped access
- Validation Rules: Notification read-state updates and recipient checks
- Error Model: 403 forbidden, 404 not found, 503 dependency unavailable
- Audit Expectations: Notification delivery and read events

### Reporting API
- Purpose: Retrieve report summaries and analytics data
- Consumer: Frontend web application
- Provider: Reporting service
- Methods: GET /reports, GET /reports/{type}
- AuthN: Required
- AuthZ: Role-based report visibility
- Validation Rules: Filter and scope validation
- Error Model: 400 validation error, 403 forbidden, 404 not found, 503 dependency unavailable
- Audit Expectations: Report access events

### Profile and Settings API
- Purpose: View and update profile, password, avatar, and preferences
- Consumer: Frontend web application
- Provider: Profile service
- Methods: GET /profile, PUT /profile, PUT /profile/password, PUT /profile/preferences
- AuthN: Required
- AuthZ: Self-service for profile and settings, admin controls for broader account management
- Validation Rules: Email, password, preference schema validation
- Error Model: 400 validation error, 401 unauthorized, 403 forbidden, 503 dependency unavailable
- Audit Expectations: Profile update and password-change events

## Shared Contract Principles
- All API responses must preserve correlation identifiers for logs and tracing.
- Dependency failures must return explicit unavailable-state responses rather than false success.
- Validation and permission failures must remain explicit and user-actionable.
