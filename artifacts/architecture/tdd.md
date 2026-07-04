# Test-Driven Design (TDD)

## Purpose
Provide a test-oriented implementation blueprint that translates architecture and contracts into a validation-first delivery plan.

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-04
- Status: Draft
- Workflow ID: WF-20260704-001
- Traceability: requirements_spec.md, api-specifications.md, lld.md, database-strategy.md

---

## Design Summary
- The Task Management System is built as a three-tier architecture with a React frontend, Node.js/Express backend, and PostgreSQL persistence.
- Tests must validate business rules, API contracts, security boundaries, data integrity, and user workflows.
- Implementation uses dependency injection, repository abstraction, and service-layer validation; tests should be written against interfaces and mocks where practical.

---

## Functional Overview
- Authentication and authorization journeys
- Task lifecycle management (create, update, progress, archive, restore, duplicate)
- Search, filter, and sorting operations
- Collaboration with comments and notifications
- Team administration and user profile management
- Dashboard metrics and reporting

---

## Frontend Design
### Screen Responsibilities
- Login/Register/Forgot Password/Reset Password screens: authenticate and direct user into protected workspace.
- Dashboard screen: display role-based metrics and recent activity.
- Task List screen: list tasks with filters, search, sorting, pagination.
- Task Details screen: show task metadata, comments, activity, and action buttons.
- Create/Edit Task screen: collect task data, enforce client-side validation, and send API requests.
- Profile/Settings screens: allow user profile editing and preference updates.
- Teams screen: allow team leads/admins to manage team membership and roles.

### Client-Side State and Routing Expectations
- Protected routes require valid JWT and redirect unauthenticated users to `/login`.
- Role-based UI elements should hide or disable restricted actions for non-admin users.
- Form validation should mirror backend validation rules (task title, due date, status, priority).
- Loading and error states should render clearly and enable retry behaviors.

### Reference Architecture Artifacts
- `user-flow-specification.md`
- `api-specifications.md`
- `screen_elements.md`
- `ui_observations.md`

---

## Backend Design
### Service Responsibilities
- AuthService: register, login, logout, password recovery, reset.
- TaskService: create, read, update, delete, archive, restore, duplicate, bulk operations, status transitions.
- TeamService: manage teams, membership, role-based access.
- CollaborationService: comment lifecycle and notification triggers.
- NotificationService: user notification preferences, retrieval, mark-read.
- ReportingService: dashboard metrics and team-based summaries.

### Validation and Error-Handling Responsibilities
- Schema validation with Joi/Zod for request payloads.
- Business rule validation in service methods with explicit error codes.
- Authorization checks on each protected endpoint.
- Error middleware to map domain errors to API response codes and structured JSON.
- Dependency-unavailable responses for DB/cache outages.

### Reference Architecture Artifacts
- `module-design.md`
- `api-specifications.md`
- `security-architecture.md`
- `lld.md`

---

## Database Design
### Business Entities and Ownership
- User: owns tasks, teams, notifications, and personal settings.
- Task: owned by a user, optionally assigned, optionally part of a team.
- Team: owns membership and team-scoped task access.
- Comment: authored by a user on a task.
- Notification: recipient-based event record.
- Audit: append-only record of all privileged actions.

### Persistence Concerns and Lifecycle Expectations
- Transactions around task create/update and bulk operations.
- Soft-delete semantics for task archive and account disable.
- Optimistic locking for concurrent task edits.
- Audit records written for all state changes, with no delete/update operations.
- Index-backed search and filtering performance.

### Reference Architecture Artifacts
- `database-strategy.md`
- `data-dictionary.md`
- `deployment-architecture.md`

---

## Component Responsibilities
| Component | Responsibility | Dependencies |
|-----------|----------------|--------------|
| AuthService | Authentication, token issuance, password management | UserRepository, PasswordHasher, TokenProvider |
| TaskService | Task lifecycle, business validation, status workflows | TaskRepository, AuditService, NotificationService, TeamService |
| TeamService | Team creation, membership, role-based scope | TeamRepository, UserRepository |
| CollaborationService | Comments lifecycle, comment permissions | CommentRepository, TaskRepository, NotificationService |
| NotificationService | Notification preferences, retrieval, mark-read | NotificationRepository, EventPublisher |
| ReportingService | Aggregated metrics, team reports | TaskRepository, UserRepository, CommentRepository |
| ValidationService | Business rule validation and domain constraints | Domain models, utility validators |
| ErrorMiddleware | Map errors to API responses | Custom error types, logger |

---

## API Inventory Summary
| API ID | Capability | Consumer | Notes |
|--------|------------|----------|-------|
| AUTH-001 | User registration | Frontend auth forms | POST /auth/register |
| AUTH-002 | User login | Frontend auth forms | POST /auth/login |
| AUTH-003 | Password recovery | Frontend auth forms | POST /auth/recover-password |
| TASK-001 | Create task | Task form | POST /tasks |
| TASK-002 | List tasks | Task list | GET /tasks |
| TASK-003 | View task | Task details | GET /tasks/:id |
| TASK-004 | Update task | Task edit | PATCH /tasks/:id |
| TASK-005 | Archive/restore | Task detail actions | PATCH /tasks/:id/archive, /tasks/:id/restore |
| TASK-006 | Duplicate task | Task detail actions | POST /tasks/:id/duplicate |
| TEAM-001 | Create team | Team management | POST /teams |
| TEAM-002 | Manage members | Team management | PATCH /teams/:id/members |
| NOTIF-001 | List notifications | Notification tray | GET /notifications |
| DASH-001 | Dashboard metrics | Dashboard view | GET /dashboard/metrics |

---

## Validation Checklist
- [x] Requirements coverage complete
- [x] Architecture references are current
- [x] API and data responsibilities are explicit
- [x] Security and reliability constraints are reflected
- [x] Frontend workflows mapped to tests
- [x] Backend service contracts mapped to tests
- [x] Data integrity and transaction expectations documented
- [x] Open questions captured in `openlog.md`

---

## Test Planning Notes
- Unit tests should verify each service method and validator using mocks for repositories and external dependencies.
- Integration tests should validate API endpoints against a running test database and mocked authentication.
- E2E tests should cover critical user journeys: login, create task, update status, comment, filter/search, team management.
- Security tests should verify unauthorized access is denied and role restrictions are enforced.
- Performance tests should validate dashboard response time and task search response time against target thresholds.
