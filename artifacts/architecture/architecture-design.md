# Architecture Design

## Purpose
Define the comprehensive system architecture, design decisions, and layer responsibilities for the Task Management System.

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-04
- Status: Draft
- Workflow ID: WF-20260704-001
- Artifact ID: ARCH-DESIGN-001
- Related Artifacts: requirements_spec.md, user_stories.md, business_rules.md, api-specifications.md, lld.md, database-strategy.md, security-architecture.md

## Executive Summary

The Task Management System is a **three-tier web application** designed to support collaborative task execution across individuals and teams. The architecture separates concerns into:

1. **Presentation Layer** – Web UI providing authenticated access to business functions
2. **Business Layer** – Services implementing domain logic, validation, and orchestration
3. **Data Layer** – Repositories managing entity persistence and queries

All layers include comprehensive error handling, audit logging, and dependency-unavailable state management to ensure reliability and observability per non-functional requirements.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  (Web UI: Login, Register, Dashboard, Task List/Details,    │
│   Profile, Settings)                                        │
│  Responsibilities:                                          │
│  - Route navigation and screen rendering                    │
│  - Form validation and user feedback                        │
│  - Session management                                       │
│  - Dependency-unavailable state handling                    │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP/REST API
┌──────────────────▼──────────────────────────────────────────┐
│                   BUSINESS LAYER                            │
│  ┌────────────────────────────────────────────────────────┐│
│  │ Services:                                              ││
│  │ - AuthService: Sign-in, sign-up, password recovery    ││
│  │ - TaskService: CRUD, status transitions, archiving    ││
│  │ - TeamService: Team and user management               ││
│  │ - CollaborationService: Comments, attachments         ││
│  │ - NotificationService: Preference and dispatch        ││
│  │ - ReportingService: Dashboard and summary metrics     ││
│  │ - ValidationService: Business rule enforcement        ││
│  │ - AuditService: Immutable event recording             ││
│  └────────────────────────────────────────────────────────┘│
│  Responsibilities:                                         │
│  - Domain logic and business rule enforcement              │
│  - Data validation and transformation                      │
│  - Cross-service orchestration                             │
│  - Error handling and recovery                             │
│  - Audit event generation                                  │
└──────────────────┬──────────────────────────────────────────┘
                   │ Repository Pattern
┌──────────────────▼──────────────────────────────────────────┐
│                    DATA LAYER                               │
│  Repositories:                                              │
│  - UserRepository: Account and profile management          │
│  - TaskRepository: Task CRUD and search                    │
│  - TeamRepository: Team and membership queries             │
│  - CommentRepository: Comment storage and retrieval        │
│  - NotificationRepository: Notification persistence        │
│  - AuditRepository: Immutable audit log queries            │
│  Database: Relational (SQLite/PostgreSQL)                  │
└──────────────────┬──────────────────────────────────────────┘
                   │ SQL Queries
┌──────────────────▼──────────────────────────────────────────┐
│                    PERSISTENCE                              │
│  SQLite (local) or PostgreSQL (production)                 │
│  - User Accounts & Profiles                                │
│  - Tasks & Status History                                  │
│  - Teams & Memberships                                     │
│  - Comments & Attachments (metadata)                       │
│  - Notifications & Delivery Log                            │
│  - Audit Entries (immutable)                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer Responsibilities

### Presentation Layer

**Purpose:** Render screens, manage user interactions, route navigation, and handle authentication state.

**Responsibilities:**
- Screen rendering (Login, Register, Dashboard, Task List, Task Details, Create/Edit Task, Profile, Settings)
- User input validation and feedback
- Session and authentication state management
- Route protection (authenticated vs. unauthenticated)
- Dependency-unavailable UI state management (graceful degradation)
- Accessibility and responsive design
- Error display and user guidance

**Key Constraints:**
- All protected routes require active session
- Public routes: Login, Register
- Protected routes: Dashboard, Task List, Task Details, Profile, Settings
- All API calls respect authorization headers and error responses

**Cross-Layer Dependencies:**
- Depends on Business Layer APIs for all business operations
- Communicates dependency failures to users through consistent UI patterns

---

### Business Layer

**Purpose:** Implement domain logic, validate business rules, orchestrate services, and ensure data consistency.

**Responsibilities:**
- **AuthService**: Secure credential validation, session creation, password recovery, account status checks
- **TaskService**: Task CRUD, status transition enforcement (adhering to BR-007), priority management, archiving/restore logic, duplication
- **TeamService**: Team CRUD, user assignment, role-based access control
- **CollaborationService**: Comment add/edit/delete, attachment metadata, activity history
- **NotificationService**: Preference management, notification dispatch, delivery channel selection
- **ReportingService**: Dashboard metrics aggregation, team workload summaries, overdue task detection
- **ValidationService**: Business rule evaluation (e.g., BR-001 ownership, BR-006 due date policy, BR-003 archive visibility)
- **AuditService**: Immutable event recording for all privileged and state-change actions

**Key Constraints:**
- Every state change generates an audit entry
- Completed tasks (BR-004) cannot be edited by standard users
- Archived tasks (BR-003) remain visible but read-only
- All delete operations require admin permission (BR-002)
- Due dates must not be in the past (BR-006)
- Status transitions must follow allowed state machine
- Password recovery links expire after configurable period
- Services enforce role-based authorization before allowing operations

**Error Handling:**
- Validation errors return meaningful feedback to UI
- Dependency failures propagate with clear error codes
- Transactional consistency maintained for multi-step operations

---

### Data Layer

**Purpose:** Provide persistence and query operations through repositories implementing the Repository pattern.

**Repositories:**
1. **UserRepository**
   - Create account, retrieve by email, update profile
   - Find by role, find by team membership
   - Query disabled/active accounts
   - Soft-delete support (archive account)

2. **TaskRepository**
   - Full-text search by title, description, labels
   - Filtered queries by status, priority, assignee, owner, due date, created date, team
   - Sorted results by due date, priority, status, recency
   - Retrieve task history/audit trail
   - Support for pagination and bulk operations

3. **TeamRepository**
   - Create, retrieve, update team
   - Add/remove team members
   - Query team-assigned tasks

4. **CommentRepository**
   - Add comment to task
   - Retrieve comments for task in order
   - Support comment author and timestamp

5. **NotificationRepository**
   - Create notification event
   - Retrieve unread notifications for user
   - Mark as read/dismissed
   - Query by delivery channel preference

6. **AuditRepository**
   - Append immutable audit entries
   - Query by entity type, action, date range, actor
   - Support for compliance audits

**Key Constraints:**
- All repositories support soft-delete where applicable
- Audit log is immutable (append-only)
- Queries respect user access scope (no cross-team leakage)
- Transaction boundaries ensure consistency

---

## Folder Structure

```
apps/
  task-management-system/
    src/
      presentation/          # Screen routing and UI concerns
        screens/
          Login.tsx
          Register.tsx
          Dashboard.tsx
          TaskList.tsx
          TaskDetails.tsx
          CreateTask.tsx
          EditTask.tsx
          Profile.tsx
          Settings.tsx
        components/          # Shared UI components
          AuthForm.tsx
          TaskCard.tsx
          TaskForm.tsx
          Metrics.tsx
          Filter.tsx
        routing/
          Router.tsx
          ProtectedRoute.tsx
          routes.config.ts
        state/
          authStore.ts
          sessionStore.ts
      business/              # Service layer
        services/
          AuthService.ts
          TaskService.ts
          TeamService.ts
          CollaborationService.ts
          NotificationService.ts
          ReportingService.ts
          ValidationService.ts
          AuditService.ts
        dto/                 # Data Transfer Objects
          UserDTO.ts
          TaskDTO.ts
          CommentDTO.ts
        models/              # Domain models
          User.ts
          Task.ts
          Team.ts
          Comment.ts
          Notification.ts
        validators/          # Business rule validators
          TaskValidator.ts
          UserValidator.ts
        errors/              # Custom exceptions
          ValidationError.ts
          NotFoundError.ts
          UnauthorizedError.ts
      data/                  # Repository layer
        repositories/
          UserRepository.ts
          TaskRepository.ts
          TeamRepository.ts
          CommentRepository.ts
          NotificationRepository.ts
          AuditRepository.ts
        database/
          connection.ts
          migrations/
            001_init.sql
            002_audit.sql
        queries/             # SQL statement definitions
          userQueries.ts
          taskQueries.ts
      shared/                # Cross-cutting concerns
        logging/
          Logger.ts
          LogEntry.ts
        config/
          config.ts
          environment.ts
        error-handling/
          ErrorHandler.ts
          DependencyUnavailable.ts
        auth/
          JWTProvider.ts
          SessionManager.ts
        constants/
          statusValues.ts
          priorityValues.ts
          roles.ts
        utils/
          dateUtils.ts
          stringUtils.ts
      tests/
        unit/
        integration/
        e2e/
      main.ts               # Application entry point
      app.ts                # App initialization
  config/
    package.json
    tsconfig.json
    webpack.config.js
  docs/
    API.md
    SETUP.md
```

---

## Design Decisions

### 1. Three-Tier Architecture
**Decision:** Separate Presentation, Business, and Data layers.
**Rationale:** Enables independent scaling, testing, and modification of each layer per business requirements for scalability (500+ concurrent users).
**Trade-off:** Requires clear layer boundary contracts and increased initial complexity.

### 2. Repository Pattern
**Decision:** Data access through repositories, not direct SQL or ORM usage in services.
**Rationale:** Enables query complexity isolation, consistent error handling, and future database switching. Supports complex search/filter/sort per REQ-004.
**Trade-off:** Requires repository interface definitions and implementation.

### 3. Service Layer for Business Logic
**Decision:** Dedicated services for each domain concern (Auth, Task, Team, Collaboration, Notification, Reporting, Validation, Audit).
**Rationale:** Ensures business rules are centralized and consistently enforced (BR-001 through BR-015), enabling clear validation and audit trails.
**Trade-off:** Requires orchestration of multiple services for complex flows.

### 4. Immutable Audit Log (Append-Only)
**Decision:** Separate immutable audit table with no update/delete capability (BR-005).
**Rationale:** Ensures compliance, accountability, and non-repudiation of task and administrative changes.
**Trade-off:** Audit table growth over time; requires archival strategy.

### 5. Soft-Delete Pattern
**Decision:** Tasks and accounts are archived, not permanently deleted, except by admin purge (BR-002, BR-003).
**Rationale:** Preserves audit history and enables undelete workflows while maintaining visibility in searches.
**Trade-off:** Queries must filter archived records by default; admin views must have option to include archived.

### 6. Dependency-Unavailable State Management
**Decision:** All screens and services implement explicit handling for unavailable dependencies (authentication, task store, notification service, reporting).
**Rationale:** Per non-functional requirement for clear recovery experience (REQ-008 acceptance criteria AC-004, AC-008, AC-012, AC-016, AC-020, AC-024, AC-028).
**Trade-off:** Requires state machine for each screen and service capability.

### 7. Role-Based Access Control (RBAC)
**Decision:** Three roles (Administrator, Team Lead, Team Member) with role-specific permissions enforced at service level.
**Rationale:** Aligns with personas and business rules for task visibility, admin actions, and reporting scope.
**Trade-off:** Requires permission checks in every service method.

### 8. Stateless Session Management
**Decision:** JWT or token-based sessions (stateless on backend, session state in client store).
**Rationale:** Supports scalability and enables horizontal deployment without session affinity.
**Trade-off:** Requires token refresh strategy and logout revocation mechanism.

---

## Security Design

**Authentication:** Credentials validated against stored hashed passwords. Session tokens issued on successful sign-in.
**Authorization:** Role-based access control enforced before every service operation.
**Input Validation:** All user inputs validated against business rules and sanitized before storage.
**Data Protection:** Sensitive fields (passwords, recovery tokens) stored securely; PII (email, profile) protected per privacy expectations.
**Audit Logging:** All privileged and state-change actions recorded immutably.
**Error Handling:** Generic error messages returned to client; detailed errors logged server-side.

See [security-architecture.md](security-architecture.md) for complete security details.

---

## Performance & Scalability

**Dashboard Performance:** Metrics aggregation cached with 5-minute TTL; background service refreshes cache.
**Search Performance:** Full-text indexes on Task title, description, labels; lazy pagination (20 items per page default).
**Database Indexes:** 
  - User: unique on email, btree on role, team_id
  - Task: unique on id, btree on owner, assignee, status, due_date, created_date, team_id, archived_at
  - Comment: btree on task_id, created_at
  - Audit: btree on entity_type, entity_id, action, created_at

**Concurrency:** Optimistic locking on task edits using version fields; conflict detection in update path.
**Load Distribution:** Stateless services enable horizontal scaling behind load balancer.

See [deployment-architecture.md](deployment-architecture.md) for production deployment strategy.

---

## Logging & Observability

**Structured Logging:** All events logged in JSON format with:
  - timestamp
  - workflow_id
  - correlation_id
  - component
  - level (INFO, WARN, ERROR)
  - message
  - context (user_id, entity_id, action)

**Audit Logging:** Every significant action recorded:
  - User sign-in/sign-out
  - Task creation, update, status change, archive, restore, delete
  - Comment add, edit, delete
  - User role change, team assignment
  - Notification dispatch, preference update
  - Settings change

**Error Tracking:** All errors include error code and context; dependency failures explicitly logged.

**Observability Metrics:**
  - API response time (p50, p95, p99)
  - Authentication success/failure rate
  - Task operation latency
  - Search query performance
  - Notification delivery rate
  - Database query performance
  - Cache hit rate

---

## Integration Points

### External Integrations (Out of Scope for Phase 1)
- Email service for password recovery and email notifications
- Object storage for attachment files
- Analytics service for usage tracking
- Business intelligence for executive reporting

### Internal Integration Contracts
- **Auth → Task:** AuthService validates session before TaskService operations
- **Task → Audit:** TaskService calls AuditService for state changes
- **Task → Notification:** TaskService emits events consumed by NotificationService
- **Reporting → Task:** ReportingService queries TaskRepository with filtered scope
- **Collaboration → Task:** CollaborationService links comments to tasks

---

## Error Handling Strategy

**Validation Errors:**
- Return 400 Bad Request with field-specific error details
- Examples: invalid email format, past due date, duplicate email

**Authorization Errors:**
- Return 403 Forbidden with generic "access denied" message
- Log unauthorized attempt with user context

**Resource Not Found:**
- Return 404 Not Found
- Applies to non-existent tasks, users, teams

**Dependency Unavailable:**
- Return 503 Service Unavailable or present UI state indicating unavailable component
- Examples: authentication service down, task database unavailable, notification service down
- Screens show explicit state indicating what is unavailable and what actions are blocked

**Server Errors:**
- Return 500 Internal Server Error with request ID for support
- Log full error stack and context server-side

**Transactional Failures:**
- Rollback all changes, return error to client
- Examples: concurrent task edit conflict, team assignment rollback

---

## Deployment Considerations

**Environment Strategy:**
- **Development:** SQLite local database, file-based logging
- **Test:** PostgreSQL, in-memory cache, full audit logging
- **Production:** PostgreSQL with replication, centralized logging, cache cluster

**Configuration Management:** Environment-based config (dev, test, prod) with secrets management.
**Database Migrations:** Version-controlled migration scripts run on deployment.
**Health Checks:** Liveness and readiness probes for orchestration.
**Rolling Deployment:** Blue-green deployment strategy to maintain availability.

See [deployment-architecture.md](deployment-architecture.md) for full details.

---

## Data Ownership

| Entity | Owner | Read Access | Write Access |
|--------|-------|-------------|--------------|
| User Account | User (self) | User, Admins | User (self), Admins |
| Task | Task Owner | Owner, Assignee, Team, Admins | Owner, Assignee (status only), Admins |
| Comment | Comment Author | Task participants, Admins | Author, Admins |
| Team | Team Owner | Members, Admins | Owner, Admins |
| Notification | Recipient User | User, Admins | User (preference), Admins |
| Audit | System | Admins | System only (immutable) |
| Settings | User | User | User |

---

## Cross-Cutting Concerns

**Logging:** Structured JSON logs with correlation IDs for tracing requests through system.
**Configuration:** Environment-based config with secrets management (API keys, DB passwords).
**Dependency Injection:** Services receive dependencies via constructor injection.
**Exception Handling:** Centralized error handler converts exceptions to HTTP responses.
**Observability:** Metrics collection and structured logging for incident diagnosis.
**Performance Monitoring:** Track slow queries, API response times, cache efficiency.

---

## Known Constraints & Assumptions

1. **Figma Design:** The supplied Figma design at https://www.figma.com/make/YnxUzBz6USzrnokLtV4Jd0/Task-Management-System-Screens is the authoritative visual specification.
2. **Notification Delivery:** In-app notifications required at launch; email delivery configurable by user preference (resolved from OQ-001).
3. **Reporting Scope:** Role-based reporting access; full details in database-strategy.md (resolved from OQ-002).
4. **Single Owner Model:** Every task has one owner; assignee is optional per BR-001.
5. **Status State Machine:** Only allowed transitions are Todo → In Progress → Review → Completed or any → Blocked (per BR-007).
6. **Audit Retention:** Audit records retained indefinitely; separate archive table may be created after 1 year.
7. **Concurrent User Limit:** Architecture supports 500+ concurrent users; load testing required for validation.

---

## Architecture Decision Records

See [architecture-decision-records.md](architecture-decision-records.md) for detailed ADRs.

---

## Related Documents

- [module-design.md](module-design.md) – Module responsibilities and boundaries
- [api-specifications.md](api-specifications.md) – API contract details
- [lld.md](lld.md) – Low-level design and internal architecture
- [database-strategy.md](database-strategy.md) – Data persistence strategy
- [security-architecture.md](security-architecture.md) – Security design
- [deployment-architecture.md](deployment-architecture.md) – Infrastructure and deployment
- [technology-stack.md](technology-stack.md) – Technology selections
- [user-flow-specification.md](user-flow-specification.md) – Navigation and workflow
- [data-dictionary.md](data-dictionary.md) – Data definitions

---

## Pre-Handoff Checklist

- [x] All BA artifacts consumed
- [x] Architecture aligned with epics and features
- [x] Layer responsibilities clearly defined
- [x] API and integration contracts defined
- [x] Security, validation, error handling specified
- [x] Navigation and workflow covered
- [x] Database conceptual design included
- [x] Performance and scalability addressed
- [x] Logging and audit strategy defined
- [x] Deployment considerations documented
- [x] No implementation code included
- [x] No SQL or DDL included
- [x] Traceability to requirements included

---

## Document Control

- **Document ID:** ARCH-DESIGN-001
- **Version:** 1.0
- **Author:** Solution Architect
- **Date:** 2026-07-04
- **Status:** Ready for Handoff
- **Next Stage:** UI/UX Developer & Backend Developer (parallel)
- **Approval:** Pending
