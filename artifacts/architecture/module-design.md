# Module Design

## Purpose
Define module responsibilities, boundaries, public interfaces, and dependencies.

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-04
- Status: Draft
- Artifact ID: MOD-DESIGN-001

---

## Modules Overview

The system is organized into 8 major modules within the Business Layer and supporting infrastructure modules:

| Module | Responsibility | Dependencies | Input | Output |
|--------|-----------------|--------------|-------|--------|
| AuthModule | User authentication and session management | UserRepository, AuditService | Credentials, Recovery Request | Session Token, User Context |
| TaskModule | Task CRUD and lifecycle management | TaskRepository, TeamRepository, AuditService, ValidationService | Task Data, Actions | Task Record, Status Confirmation |
| TeamModule | Team and membership management | TeamRepository, UserRepository, AuditService | Team/User Data, Actions | Team Record, Member List |
| CollaborationModule | Comments, attachments, activity tracking | CommentRepository, TaskRepository, NotificationService, AuditService | Comment/Attachment Data | Activity Record, Notification Event |
| NotificationModule | User preferences and notification dispatch | NotificationRepository, UserRepository | Preference Updates, Events | Preference Confirmation, Delivery Log |
| ReportingModule | Dashboard and summary metrics | TaskRepository, TeamRepository, UserRepository | Query Request | Metric Summary |
| ValidationModule | Business rule enforcement | Constants, Business Rules | Entity Data | Validation Result |
| AuditModule | Immutable event recording | AuditRepository | Action, Context | Audit Entry |

---

## Module Definitions

### AuthModule

**Purpose:** Secure authentication and session lifecycle management.

**Public Interfaces:**
```
interface IAuthService {
  register(email: string, password: string, fullName: string): Promise<UserDTO>
  signIn(email: string, password: string): Promise<SessionToken>
  signOut(sessionToken: string): Promise<void>
  validateSession(sessionToken: string): Promise<UserContext>
  initiatePasswordRecovery(email: string): Promise<void>
  resetPassword(recoveryToken: string, newPassword: string): Promise<void>
}
```

**Responsibilities:**
- Credential validation against hashed passwords
- Session token generation and validation
- Password recovery link generation and expiration
- Account status verification (active, disabled)
- Audit logging of authentication events

**Security Constraints:**
- Passwords minimum 8 characters, hashed using bcrypt
- Session tokens expire after 24 hours (configurable)
- Password recovery tokens expire after 15 minutes
- Failed login attempts rate-limited
- Account locked after 5 failed attempts for 15 minutes

**Error Conditions:**
- Invalid credentials → 401 Unauthorized
- Duplicate email on register → 400 Bad Request
- Expired recovery token → 410 Gone
- Account disabled → 403 Forbidden
- Rate limit exceeded → 429 Too Many Requests

**Dependencies:**
- UserRepository (account lookup and update)
- AuditService (login attempt recording)

---

### TaskModule

**Purpose:** Task creation, update, deletion, archiving, restoration, and state progression.

**Public Interfaces:**
```
interface ITaskService {
  createTask(taskInput: TaskInput, userId: string): Promise<TaskDTO>
  getTaskById(taskId: string, userId: string): Promise<TaskDTO>
  updateTask(taskId: string, updates: TaskUpdate, userId: string): Promise<TaskDTO>
  deleteTask(taskId: string, userId: string): Promise<void>
  archiveTask(taskId: string, userId: string): Promise<void>
  restoreTask(taskId: string, userId: string): Promise<void>
  duplicateTask(taskId: string, userId: string): Promise<TaskDTO>
  listTasks(filter: TaskFilter, userId: string): Promise<TaskDTO[]>
  updateTaskStatus(taskId: string, newStatus: TaskStatus, userId: string): Promise<TaskDTO>
  bulkUpdateTasks(taskIds: string[], updates: TaskUpdate, userId: string): Promise<void>
}
```

**Responsibilities:**
- Task CRUD operations with authorization checks
- Status progression enforcement (allowed transitions only)
- Archive and restore with visibility rules (BR-003)
- Task duplication with new ID and timestamps
- Completed task protection (BR-004, admin override)
- Due date validation (BR-006)
- Audit trail generation for all changes
- Permission enforcement (owner, assignee, admin)

**Business Rules Enforced:**
- BR-001: Single ownership, optional assignee
- BR-003: Archived tasks read-only for non-admins
- BR-004: Completed tasks locked unless admin
- BR-005: Immutable history recorded
- BR-006: Due dates must not be in past
- BR-007: Status must be from allowed set
- BR-008: Priority must be from allowed set

**Error Conditions:**
- Invalid title → 400 Bad Request
- Past due date → 400 Bad Request
- Invalid status transition → 409 Conflict
- Unauthorized edit → 403 Forbidden
- Task not found → 404 Not Found
- Concurrent edit conflict → 409 Conflict

**Dependencies:**
- TaskRepository (CRUD and search)
- TeamRepository (team access check)
- ValidationService (business rule enforcement)
- AuditService (state change recording)
- NotificationService (event emission)

---

### TeamModule

**Purpose:** Team creation, membership management, and role assignment.

**Public Interfaces:**
```
interface ITeamService {
  createTeam(teamInput: TeamInput, userId: string): Promise<TeamDTO>
  getTeamById(teamId: string, userId: string): Promise<TeamDTO>
  updateTeam(teamId: string, updates: TeamUpdate, userId: string): Promise<TeamDTO>
  addMember(teamId: string, userId: string, role: TeamRole, actorId: string): Promise<void>
  removeMember(teamId: string, userId: string, actorId: string): Promise<void>
  listTeamMembers(teamId: string, userId: string): Promise<UserDTO[]>
  listUserTeams(userId: string): Promise<TeamDTO[]>
}
```

**Responsibilities:**
- Team CRUD with permission enforcement
- Add/remove team members
- Role assignment (Team Lead, Team Member)
- Team-scoped task visibility
- Audit logging of membership changes
- Permission checks (team owner, admin)

**Error Conditions:**
- Unauthorized action → 403 Forbidden
- Team not found → 404 Not Found
- Duplicate membership → 400 Bad Request
- Invalid role assignment → 400 Bad Request

**Dependencies:**
- TeamRepository (team data)
- UserRepository (member lookup)
- AuditService (membership changes)

---

### CollaborationModule

**Purpose:** Comments, attachments, and activity tracking on tasks.

**Public Interfaces:**
```
interface ICollaborationService {
  addComment(taskId: string, content: string, userId: string): Promise<CommentDTO>
  editComment(commentId: string, content: string, userId: string): Promise<CommentDTO>
  deleteComment(commentId: string, userId: string): Promise<void>
  addAttachment(taskId: string, attachmentData: AttachmentInput, userId: string): Promise<AttachmentDTO>
  getTaskActivity(taskId: string, userId: string): Promise<ActivityDTO[]>
  getTaskComments(taskId: string, userId: string): Promise<CommentDTO[]>
}
```

**Responsibilities:**
- Comment creation, editing, deletion
- Attachment metadata storage (file references)
- Activity history aggregation
- Permission validation (task participants only)
- Audit logging of collaboration events
- Trigger notifications on comments

**Error Conditions:**
- Empty comment → 400 Bad Request
- Unauthorized access → 403 Forbidden
- Task not found → 404 Not Found
- Comment not found → 404 Not Found

**Dependencies:**
- CommentRepository (comment storage)
- TaskRepository (task access)
- NotificationService (notify participants)
- AuditService (collaboration events)

---

### NotificationModule

**Purpose:** User notification preferences and delivery management.

**Public Interfaces:**
```
interface INotificationService {
  updatePreferences(userId: string, preferences: NotificationPreferences): Promise<void>
  getPreferences(userId: string): Promise<NotificationPreferences>
  emitEvent(event: TaskEvent, taskId: string): Promise<void>
  dispatchNotifications(event: TaskEvent): Promise<void>
  markAsRead(notificationId: string, userId: string): Promise<void>
  getUserNotifications(userId: string, limit: number): Promise<NotificationDTO[]>
}
```

**Responsibilities:**
- Notification preference storage and retrieval
- Event-driven notification dispatch
- Delivery channel selection (in-app, email)
- Read/unread status tracking
- Preference-aware filtering

**Business Rules:**
- In-app notifications required
- Email delivery optional per user preference
- Notifications only for authorized task participants

**Error Conditions:**
- Invalid preference value → 400 Bad Request
- User not found → 404 Not Found

**Dependencies:**
- NotificationRepository (preference storage)
- UserRepository (user lookup)
- Email service (email delivery - external)

---

### ReportingModule

**Purpose:** Dashboard metrics and workload summary reports.

**Public Interfaces:**
```
interface IReportingService {
  getDashboardMetrics(userId: string): Promise<DashboardMetrics>
  getWorkloadSummary(teamId: string, userId: string): Promise<WorkloadSummary>
  getOverdueTasksSummary(userId: string): Promise<TaskSummary>
  getProductivityReport(userId: string, dateRange: DateRange): Promise<ProductivityReport>
}
```

**Responsibilities:**
- Aggregate task metrics by status
- Calculate workload per team member
- Detect and summarize overdue tasks
- Provide role-scoped visibility (admin sees all, member sees personal/team)
- Cache metrics with TTL for performance
- Query optimization for complex aggregations

**Performance Constraints:**
- Dashboard metrics load within 2 seconds (p95)
- Caching layer with 5-minute TTL
- Background refresh job for cache invalidation

**Error Conditions:**
- No tasks found → empty result with zero metrics
- User not authorized for report → 403 Forbidden

**Dependencies:**
- TaskRepository (complex queries)
- TeamRepository (team scope)
- UserRepository (user access)
- Cache service (metrics caching)

---

### ValidationModule

**Purpose:** Centralized business rule validation.

**Public Interfaces:**
```
interface IValidationService {
  validateTaskInput(input: TaskInput): ValidationResult
  validateStatusTransition(currentStatus: TaskStatus, newStatus: TaskStatus): ValidationResult
  validateDueDate(dueDate: Date): ValidationResult
  validateEmail(email: string): ValidationResult
  validatePassword(password: string): ValidationResult
  validateTaskAccess(userId: string, taskId: string, action: TaskAction): ValidationResult
}
```

**Responsibilities:**
- Enforce all business rules (BR-001 through BR-015)
- Validate user inputs
- Check permission constraints
- Provide detailed error messages for failures

**Validated Rules:**
- Single ownership (BR-001)
- Permanent deletion requires admin (BR-002)
- Archive visibility (BR-003)
- Completed task protection (BR-004)
- Immutable history (BR-005)
- Due date policy (BR-006)
- Allowed statuses (BR-007)
- Allowed priorities (BR-008)

**Dependencies:**
- Constants (allowed values)
- None (no repository calls)

---

### AuditModule

**Purpose:** Immutable event recording for compliance and accountability.

**Public Interfaces:**
```
interface IAuditService {
  recordEvent(event: AuditEvent): Promise<void>
  queryEvents(filter: AuditFilter): Promise<AuditEntry[]>
  getEntityHistory(entityType: string, entityId: string): Promise<AuditEntry[]>
}
```

**Responsibilities:**
- Append-only audit entry creation
- No update or delete capability on audit table
- Query audit history by entity or user
- Timestamp and actor tracking
- Compliance reporting support

**Audited Events:**
- User sign-in, sign-out, password reset
- Task create, update, status change, archive, restore, delete
- Comment add, edit, delete
- User role change, team assignment
- Notification preference change
- Settings changes
- Administrative actions

**Constraints:**
- Audit entries immutable (append-only)
- Audit retention indefinite (with archive strategy)
- Every privileged action recorded
- Complete audit trail for compliance

**Dependencies:**
- AuditRepository (append entries)

---

## Module Interaction Flows

### Task Creation Flow
```
Presentation Layer
  ↓
TaskService.createTask()
  ├→ ValidationService.validateTaskInput()
  ├→ TaskRepository.create()
  ├→ AuditService.recordEvent("TASK_CREATED")
  └→ NotificationService.emitEvent("TASK_CREATED")
```

### Task Status Update Flow
```
TaskService.updateTaskStatus()
  ├→ ValidationService.validateStatusTransition()
  ├→ ValidationService.validateTaskAccess()
  ├→ TaskRepository.update()
  ├→ AuditService.recordEvent("TASK_STATUS_CHANGED")
  ├→ NotificationService.emitEvent("TASK_STATUS_CHANGED")
  └→ CollaborationService.recordActivity()
```

### User Authentication Flow
```
AuthService.signIn()
  ├→ UserRepository.findByEmail()
  ├→ Validate password hash
  ├→ Create session token
  ├→ AuditService.recordEvent("USER_SIGNED_IN")
  └→ Return SessionToken
```

### Dashboard Load Flow
```
ReportingService.getDashboardMetrics()
  ├→ Check cache for user metrics
  ├→ If cache miss:
  │   ├→ TaskRepository.countByStatus()
  │   ├→ TaskRepository.countOverdue()
  │   ├→ TaskRepository.getRecentActivity()
  │   └→ Cache results (TTL: 5 minutes)
  └→ Return DashboardMetrics
```

---

## Module Dependencies

```
┌─────────────────────────────────────────────┐
│         Presentation Layer                  │
│       (screens, routing, forms)             │
└────────────────────┬────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    ┌────▼────┐  ┌──▼────┐  ┌──▼────┐
    │  Auth   │  │ Task  │  │ Team  │
    │ Module  │  │Module │  │Module │
    └────┬────┘  └──┬────┘  └──┬────┘
         │          │           │
    ┌────▼──────────▼───────────▼────┐
    │   Collaboration Module          │
    │   (depends on Task, User info)  │
    └────┬─────────────────────────┬──┘
         │                         │
    ┌────▼──────────┐  ┌──────────▼──┐
    │ Notification  │  │ Reporting   │
    │   Module      │  │ Module      │
    └──────────────┬┘  └──────┬──────┘
                   │          │
    ┌──────────────▼──────────▼────┐
    │  Validation & Audit Modules  │
    │  (used by all services)      │
    └──────────────┬───────────────┘
                   │
    ┌──────────────▼───────────────┐
    │    Repository Layer          │
    │  (UserRepo, TaskRepo, etc.)  │
    └──────────────┬───────────────┘
                   │
    ┌──────────────▼───────────────┐
    │      Database Layer          │
    └──────────────────────────────┘
```

---

## Interface Contracts

All module interfaces are technology-neutral and define:
- Input parameters (DTOs)
- Output return types
- Exception/error conditions
- Authorization requirements
- Side effects (audit, notification, cache)

See [api-specifications.md](api-specifications.md) for HTTP API contracts.

---

## Module Testing Strategy

Each module includes:
- **Unit tests:** Pure business logic testing (validation, status transitions)
- **Integration tests:** Repository and service collaboration
- **Contract tests:** Module interface compliance

---

## Document Control

- **Document ID:** MOD-DESIGN-001
- **Version:** 1.0
- **Author:** Solution Architect
- **Status:** Ready for Handoff
