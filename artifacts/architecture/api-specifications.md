# API Specifications

## Purpose
Define complete HTTP API contracts for the Task Management System.

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-04
- Status: Draft
- Artifact ID: API-SPEC-001
- Base URL: http://localhost:5000/api/v1 (dev), https://api.example.com/api/v1 (prod)

---

## API Overview

The API is organized into 7 resource groups:

| Resource | Operations | Purpose |
|----------|-----------|---------|
| `/auth` | POST register, POST login, POST logout, POST recover-password, POST reset-password | Authentication |
| `/tasks` | GET list, POST create, GET /:id, PATCH /:id, DELETE /:id, POST /:id/archive, POST /:id/restore, POST /:id/duplicate | Task Management |
| `/tasks/:id/comments` | GET, POST, PATCH /:commentId, DELETE /:commentId | Collaboration |
| `/tasks/:id/attachments` | GET, POST, DELETE /:attachmentId | Attachments |
| `/dashboard` | GET metrics | Reporting |
| `/users` | GET /:id, PATCH /:id, GET /:id/profile, PATCH /:id/profile, GET /:id/settings, PATCH /:id/settings | User Management |
| `/teams` | GET, POST, GET /:id, PATCH /:id, POST /:id/members, DELETE /:id/members/:userId | Team Management |
| `/notifications` | GET, GET /preferences, PATCH /preferences, PATCH /:id/read | Notifications |

---

## Error Model

All error responses follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "User-friendly error message",
    "details": {
      "field": "fieldName",
      "issue": "Specific validation or business rule violation"
    },
    "timestamp": "2026-07-04T12:00:00Z",
    "requestId": "req-uuid-here"
  }
}
```

### Error Codes

| Code | HTTP Status | Meaning |
|------|------------|---------|
| INVALID_INPUT | 400 | Validation error |
| DUPLICATE_RESOURCE | 400 | Resource already exists (e.g., email) |
| UNAUTHORIZED | 401 | Invalid credentials |
| FORBIDDEN | 403 | Access denied (authorization) |
| NOT_FOUND | 404 | Resource not found |
| CONFLICT | 409 | Concurrent edit or invalid state transition |
| UNPROCESSABLE | 422 | Business rule violation |
| RATE_LIMIT | 429 | Too many requests |
| DEPENDENCY_UNAVAILABLE | 503 | Required service/database unavailable |
| INTERNAL_ERROR | 500 | Server error |

---

## Authentication & Authorization

### Session Management
- **Method:** JWT bearer token
- **Header:** `Authorization: Bearer <token>`
- **Token Format:** `Header.Payload.Signature`
- **Payload Contains:** `{ userId, email, role, iat, exp }`
- **Expiry:** 24 hours
- **Refresh:** POST `/auth/refresh` with valid token

### Authorization Model
- **Mechanism:** Role-based access control (RBAC)
- **Roles:** ADMIN, TEAM_LEAD, TEAM_MEMBER
- **Check:** Enforced in service layer before data access

### Public Endpoints (No Auth Required)
- POST `/auth/register`
- POST `/auth/login`
- POST `/auth/recover-password`
- POST `/auth/reset-password`

### Protected Endpoints (Auth Required)
- All other endpoints require valid JWT

---

## API Endpoints

### Authentication

#### POST /auth/register
**Purpose:** Create a new user account.
**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "fullName": "John Doe"
}
```
**Response (201 Created):**
```json
{
  "data": {
    "userId": "uuid-here",
    "email": "user@example.com",
    "fullName": "John Doe",
    "role": "TEAM_MEMBER",
    "createdAt": "2026-07-04T12:00:00Z"
  }
}
```
**Validation:**
- Email must be valid format and unique
- Password minimum 8 characters
- Full name required
**Errors:** DUPLICATE_RESOURCE (400), INVALID_INPUT (400), DEPENDENCY_UNAVAILABLE (503)
**Audit:** User registration recorded
**Related AC:** AC-001

#### POST /auth/login
**Purpose:** Authenticate user and create session.
**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "rememberMe": false
}
```
**Response (200 OK):**
```json
{
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 86400,
    "user": {
      "userId": "uuid-here",
      "email": "user@example.com",
      "role": "TEAM_MEMBER"
    }
  }
}
```
**Validation:**
- Email and password required
- Email format validation
**Errors:** UNAUTHORIZED (401), INVALID_INPUT (400), RATE_LIMIT (429), DEPENDENCY_UNAVAILABLE (503)
**Audit:** Login attempt recorded (success and failure)
**Security:** Rate limit: 5 attempts per 15 minutes
**Related AC:** AC-002, AC-003

#### POST /auth/logout
**Purpose:** Invalidate current session.
**Request:** No body (token in header)
**Response (200 OK):**
```json
{
  "data": {
    "message": "Logged out successfully"
  }
}
```
**Errors:** UNAUTHORIZED (401)
**Audit:** Logout event recorded

#### POST /auth/recover-password
**Purpose:** Initiate password recovery process.
**Request:**
```json
{
  "email": "user@example.com"
}
```
**Response (200 OK):**
```json
{
  "data": {
    "message": "Recovery email sent"
  }
}
```
**Validation:** Email must exist and account must be active
**Errors:** NOT_FOUND (404), INVALID_INPUT (400)
**Note:** Does not leak whether email exists; email sent if account active
**Audit:** Password recovery initiated

#### POST /auth/reset-password
**Purpose:** Complete password recovery with reset token.
**Request:**
```json
{
  "token": "recovery-token-from-email",
  "newPassword": "NewPassword123!"
}
```
**Response (200 OK):**
```json
{
  "data": {
    "message": "Password reset successfully"
  }
}
```
**Validation:**
- Token must be valid and not expired (15-minute expiry)
- New password minimum 8 characters
- Cannot reuse previous password
**Errors:** UNAUTHORIZED (401), INVALID_INPUT (400), DEPENDENCY_UNAVAILABLE (503)
**Audit:** Password reset recorded

---

### Tasks

#### GET /tasks
**Purpose:** List tasks with filtering, sorting, and search.
**Query Parameters:**
```
?search=text             # Search title, description, labels
&status=todo             # Filter by status: todo, in_progress, review, completed, blocked
&priority=high           # Filter by priority: low, medium, high, critical
&assignee=uuid           # Filter by assignee user ID
&owner=uuid              # Filter by owner user ID
&dueDate=2026-08-04     # Filter by due date (exact match)
&dueDateFrom=2026-08-01 # Filter by due date range (from)
&dueDateTo=2026-08-31   # Filter by due date range (to)
&createdDate=2026-07-01 # Filter by created date
&team=team-uuid          # Filter by team
&archived=false          # Include archived: false (default), true, all
&sort=due_date           # Sort by: recently_updated (default), due_date, priority, status, created_date
&order=asc               # Order: asc, desc
&page=1                  # Page number (default 1)
&limit=20                # Items per page (default 20, max 100)
```
**Response (200 OK):**
```json
{
  "data": {
    "tasks": [
      {
        "taskId": "uuid-here",
        "title": "Task title",
        "description": "Task description",
        "status": "todo",
        "priority": "high",
        "owner": { "userId": "uuid", "email": "owner@example.com", "fullName": "Owner Name" },
        "assignee": { "userId": "uuid", "email": "assignee@example.com" },
        "dueDate": "2026-08-04",
        "createdAt": "2026-07-04T12:00:00Z",
        "updatedAt": "2026-07-04T12:30:00Z",
        "archivedAt": null
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "totalPages": 3
    }
  }
}
```
**Validation:**
- User can only see tasks they have access to (owner, assignee, team member, admin)
- Sort and filter values must be valid
**Errors:** INVALID_INPUT (400), FORBIDDEN (403), DEPENDENCY_UNAVAILABLE (503)
**Audit:** Search action logged
**Performance:** p95 < 1 second
**Related AC:** AC-009, AC-010, AC-011

#### POST /tasks
**Purpose:** Create new task.
**Request:**
```json
{
  "title": "New Task",
  "description": "Task description (optional)",
  "status": "todo",
  "priority": "medium",
  "assignee": "uuid-or-null",
  "dueDate": "2026-08-04",
  "team": "team-uuid-or-null"
}
```
**Response (201 Created):**
```json
{
  "data": {
    "taskId": "uuid-here",
    "title": "New Task",
    "status": "todo",
    "priority": "medium",
    "owner": { "userId": "current-user-uuid", "email": "user@example.com" },
    "assignee": null,
    "createdAt": "2026-07-04T12:00:00Z"
  }
}
```
**Validation:**
- Title required (max 100 chars)
- Status must be valid (default: todo)
- Priority must be valid (default: medium)
- Due date must not be in past (BR-006)
- Assignee must be valid user if provided
**Errors:** INVALID_INPUT (400), FORBIDDEN (403), DEPENDENCY_UNAVAILABLE (503)
**Business Rules:** BR-001 (ownership), BR-007 (status), BR-008 (priority), BR-006 (due date)
**Audit:** Task creation recorded
**Related AC:** AC-005

#### GET /tasks/:taskId
**Purpose:** Get task details.
**Response (200 OK):**
```json
{
  "data": {
    "taskId": "uuid-here",
    "title": "Task title",
    "description": "Task description",
    "status": "in_progress",
    "priority": "high",
    "owner": { "userId": "uuid", "email": "owner@example.com", "fullName": "Owner Name" },
    "assignee": { "userId": "uuid", "email": "assignee@example.com", "fullName": "Assignee Name" },
    "dueDate": "2026-08-04",
    "labels": ["bug", "urgent"],
    "createdAt": "2026-07-04T12:00:00Z",
    "updatedAt": "2026-07-04T12:30:00Z",
    "history": [
      {
        "action": "created",
        "actor": { "userId": "uuid", "email": "owner@example.com" },
        "timestamp": "2026-07-04T12:00:00Z",
        "details": { "field": null }
      },
      {
        "action": "status_changed",
        "actor": { "userId": "uuid", "email": "owner@example.com" },
        "timestamp": "2026-07-04T12:30:00Z",
        "details": { "from": "todo", "to": "in_progress" }
      }
    ],
    "comments": [
      {
        "commentId": "uuid",
        "author": { "userId": "uuid", "email": "user@example.com" },
        "content": "Comment text",
        "createdAt": "2026-07-04T13:00:00Z",
        "updatedAt": null
      }
    ]
  }
}
```
**Errors:** NOT_FOUND (404), FORBIDDEN (403)
**Authorization:** User must have task access
**Related AC:** AC-007

#### PATCH /tasks/:taskId
**Purpose:** Update task.
**Request:**
```json
{
  "title": "Updated title",
  "status": "in_progress",
  "priority": "critical",
  "assignee": "uuid-or-null",
  "dueDate": "2026-08-10"
}
```
**Response (200 OK):**
```json
{
  "data": {
    "taskId": "uuid-here",
    "title": "Updated title",
    "status": "in_progress",
    "updatedAt": "2026-07-04T13:00:00Z"
  }
}
```
**Validation:**
- Task must exist
- User must have update permission (owner, assignee, admin)
- Completed tasks cannot be edited by non-admins (BR-004)
- Archived tasks cannot be edited by non-admins (BR-003)
- Due date must not be in past (BR-006)
- Status transition must be valid (BR-007)
**Errors:** NOT_FOUND (404), FORBIDDEN (403), CONFLICT (409), UNPROCESSABLE (422)
**Business Rules:** BR-003, BR-004, BR-006, BR-007, BR-008
**Audit:** Task update recorded with field changes
**Related AC:** AC-006, AC-007

#### DELETE /tasks/:taskId
**Purpose:** Delete task (admin only).
**Response (204 No Content):**
```
```
**Validation:** User must be admin (BR-002)
**Errors:** FORBIDDEN (403), NOT_FOUND (404)
**Business Rules:** BR-002 (admin only)
**Audit:** Task deletion recorded
**Related AC:** AC-007

#### POST /tasks/:taskId/archive
**Purpose:** Archive task (mark as archived, remains searchable).
**Response (200 OK):**
```json
{
  "data": {
    "taskId": "uuid-here",
    "archivedAt": "2026-07-04T13:00:00Z"
  }
}
```
**Validation:** User must have update permission
**Business Rules:** BR-003 (visibility rules)
**Audit:** Archive action recorded

#### POST /tasks/:taskId/restore
**Purpose:** Restore archived task.
**Response (200 OK):**
```json
{
  "data": {
    "taskId": "uuid-here",
    "archivedAt": null
  }
}
```
**Validation:** User must have update permission
**Audit:** Restore action recorded

#### POST /tasks/:taskId/duplicate
**Purpose:** Create copy of task with new ID.
**Request:**
```json
{
  "title": "Copy of Original Task"
}
```
**Response (201 Created):**
```json
{
  "data": {
    "taskId": "new-uuid-here",
    "title": "Copy of Original Task",
    "status": "todo",
    "priority": "medium",
    "createdAt": "2026-07-04T13:00:00Z"
  }
}
```
**Validation:** Original task must exist and user must have read access
**Audit:** Duplication recorded

---

### Tasks Comments

#### GET /tasks/:taskId/comments
**Purpose:** Get task comments.
**Query Parameters:** ?page=1&limit=20
**Response (200 OK):**
```json
{
  "data": {
    "comments": [
      {
        "commentId": "uuid",
        "author": { "userId": "uuid", "email": "user@example.com", "fullName": "User Name" },
        "content": "Comment text",
        "createdAt": "2026-07-04T13:00:00Z",
        "updatedAt": null
      }
    ],
    "pagination": { "page": 1, "limit": 20, "total": 5 }
  }
}
```
**Errors:** NOT_FOUND (404), FORBIDDEN (403)
**Related AC:** AC-013

#### POST /tasks/:taskId/comments
**Purpose:** Add comment to task.
**Request:**
```json
{
  "content": "This is a comment"
}
```
**Response (201 Created):**
```json
{
  "data": {
    "commentId": "uuid",
    "author": { "userId": "current-user-uuid", "email": "current@example.com" },
    "content": "This is a comment",
    "createdAt": "2026-07-04T13:00:00Z"
  }
}
```
**Validation:**
- Content required (non-empty)
- User must have task access
**Errors:** INVALID_INPUT (400), NOT_FOUND (404), FORBIDDEN (403)
**Audit:** Comment created
**Trigger:** Notification sent to task participants
**Related AC:** AC-013

#### PATCH /tasks/:taskId/comments/:commentId
**Purpose:** Edit comment.
**Request:**
```json
{
  "content": "Updated comment text"
}
```
**Response (200 OK):**
```json
{
  "data": {
    "commentId": "uuid",
    "content": "Updated comment text",
    "updatedAt": "2026-07-04T13:15:00Z"
  }
}
```
**Validation:**
- Comment must exist
- User must be comment author or admin
- Content required (non-empty)
**Errors:** INVALID_INPUT (400), NOT_FOUND (404), FORBIDDEN (403)
**Audit:** Comment edited

#### DELETE /tasks/:taskId/comments/:commentId
**Purpose:** Delete comment.
**Response (204 No Content):**
```
```
**Validation:** User must be comment author or admin
**Errors:** NOT_FOUND (404), FORBIDDEN (403)
**Audit:** Comment deleted

---

### Dashboard & Reporting

#### GET /dashboard/metrics
**Purpose:** Get dashboard summary metrics.
**Response (200 OK):**
```json
{
  "data": {
    "totalTasks": 45,
    "completedTasks": 20,
    "pendingTasks": 25,
    "overdueTasks": 3,
    "dueTodayTasks": 2,
    "recentActivity": [
      {
        "type": "task_created",
        "title": "New Task",
        "actor": "User Name",
        "timestamp": "2026-07-04T13:00:00Z"
      }
    ]
  }
}
```
**Validation:** User must be authenticated
**Errors:** DEPENDENCY_UNAVAILABLE (503), FORBIDDEN (403)
**Performance:** p95 < 2 seconds (cached, 5-minute TTL)
**Authorization:** Role-scoped (admin sees all, member sees personal/team)
**Related AC:** AC-017, AC-020

---

### Users & Profiles

#### GET /users/:userId/profile
**Purpose:** Get user profile.
**Response (200 OK):**
```json
{
  "data": {
    "userId": "uuid",
    "email": "user@example.com",
    "fullName": "John Doe",
    "avatar": "https://example.com/avatar.jpg",
    "contactInformation": "john@example.com",
    "role": "TEAM_MEMBER",
    "createdAt": "2026-07-04T12:00:00Z"
  }
}
```
**Authorization:** User can view own profile; admins can view all
**Errors:** NOT_FOUND (404), FORBIDDEN (403)
**Related AC:** AC-025

#### PATCH /users/:userId/profile
**Purpose:** Update user profile.
**Request:**
```json
{
  "fullName": "Jane Doe",
  "contactInformation": "jane@example.com",
  "avatar": "https://example.com/new-avatar.jpg"
}
```
**Response (200 OK):**
```json
{
  "data": {
    "userId": "uuid",
    "fullName": "Jane Doe",
    "updatedAt": "2026-07-04T13:00:00Z"
  }
}
```
**Validation:**
- User can update own profile; admins can update any
- Email format if updated
**Errors:** INVALID_INPUT (400), NOT_FOUND (404), FORBIDDEN (403)
**Audit:** Profile update recorded
**Related AC:** AC-025

#### GET /users/:userId/settings
**Purpose:** Get user settings and preferences.
**Response (200 OK):**
```json
{
  "data": {
    "userId": "uuid",
    "theme": "system",
    "language": "en",
    "timezone": "UTC",
    "notificationPreferences": {
      "inApp": true,
      "email": true,
      "emailOnComment": true,
      "emailOnStatusChange": true,
      "emailOnAssignment": true
    },
    "privacyPreferences": {
      "profileVisible": true,
      "taskVisibilityDefault": "team"
    }
  }
}
```
**Authorization:** User can view own settings; admins can view all
**Errors:** NOT_FOUND (404), FORBIDDEN (403)
**Related AC:** AC-026

#### PATCH /users/:userId/settings
**Purpose:** Update user settings.
**Request:**
```json
{
  "theme": "dark",
  "language": "es",
  "timezone": "America/New_York",
  "notificationPreferences": {
    "emailOnComment": false
  }
}
```
**Response (200 OK):**
```json
{
  "data": {
    "userId": "uuid",
    "theme": "dark",
    "updatedAt": "2026-07-04T13:00:00Z"
  }
}
```
**Validation:**
- Theme: light, dark, system
- Language: supported languages
- Timezone: valid timezone
- Preference values must be valid
**Errors:** INVALID_INPUT (400), NOT_FOUND (404), FORBIDDEN (403)
**Audit:** Settings change recorded
**Related AC:** AC-026

---

### Notifications

#### GET /notifications
**Purpose:** Get user notifications.
**Query Parameters:** ?unreadOnly=false&page=1&limit=20
**Response (200 OK):**
```json
{
  "data": {
    "notifications": [
      {
        "notificationId": "uuid",
        "type": "task_status_changed",
        "title": "Task Updated",
        "message": "Your task 'Build Feature' was updated",
        "taskId": "uuid",
        "readAt": null,
        "createdAt": "2026-07-04T13:00:00Z"
      }
    ],
    "pagination": { "page": 1, "limit": 20, "total": 12 }
  }
}
```
**Authorization:** User sees only own notifications
**Errors:** FORBIDDEN (403)

#### GET /notifications/preferences
**Purpose:** Get user notification preferences.
**Response (200 OK):**
```json
{
  "data": {
    "userId": "uuid",
    "inAppNotifications": true,
    "emailNotifications": true,
    "eventPreferences": {
      "taskAssigned": true,
      "taskStatusChanged": true,
      "commentAdded": true,
      "mentionedInComment": true
    }
  }
}
```
**Authorization:** User sees own preferences; admins can view all
**Errors:** FORBIDDEN (403)
**Related AC:** AC-014

#### PATCH /notifications/preferences
**Purpose:** Update notification preferences.
**Request:**
```json
{
  "inAppNotifications": true,
  "emailNotifications": false,
  "eventPreferences": {
    "taskAssigned": true,
    "emailOnComment": false
  }
}
```
**Response (200 OK):**
```json
{
  "data": {
    "userId": "uuid",
    "emailNotifications": false,
    "updatedAt": "2026-07-04T13:00:00Z"
  }
}
```
**Audit:** Preference change recorded
**Related AC:** AC-014

#### PATCH /notifications/:notificationId/read
**Purpose:** Mark notification as read.
**Response (200 OK):**
```json
{
  "data": {
    "notificationId": "uuid",
    "readAt": "2026-07-04T13:00:00Z"
  }
}
```

---

### Teams

#### GET /teams
**Purpose:** List teams user is member of.
**Response (200 OK):**
```json
{
  "data": {
    "teams": [
      {
        "teamId": "uuid",
        "name": "Engineering",
        "description": "Engineering team",
        "owner": { "userId": "uuid", "fullName": "Team Lead Name" },
        "memberCount": 5,
        "createdAt": "2026-07-04T12:00:00Z"
      }
    ]
  }
}
```
**Authorization:** User sees only teams they're member of (admin sees all)

#### POST /teams
**Purpose:** Create team (admin only).
**Request:**
```json
{
  "name": "New Team",
  "description": "Team description"
}
```
**Response (201 Created):**
```json
{
  "data": {
    "teamId": "uuid",
    "name": "New Team",
    "owner": { "userId": "current-user-uuid" },
    "createdAt": "2026-07-04T12:00:00Z"
  }
}
```
**Validation:** Name required, unique within context
**Errors:** INVALID_INPUT (400), FORBIDDEN (403)
**Audit:** Team creation recorded

#### GET /teams/:teamId
**Purpose:** Get team details.
**Response (200 OK):**
```json
{
  "data": {
    "teamId": "uuid",
    "name": "Engineering",
    "description": "Team description",
    "owner": { "userId": "uuid", "fullName": "Owner Name" },
    "members": [
      { "userId": "uuid", "email": "user@example.com", "fullName": "User Name", "role": "TEAM_LEAD" }
    ]
  }
}
```
**Authorization:** User must be team member or admin
**Errors:** NOT_FOUND (404), FORBIDDEN (403)

#### POST /teams/:teamId/members
**Purpose:** Add member to team.
**Request:**
```json
{
  "userId": "uuid",
  "role": "TEAM_MEMBER"
}
```
**Response (201 Created):**
```json
{
  "data": {
    "userId": "uuid",
    "role": "TEAM_MEMBER",
    "addedAt": "2026-07-04T13:00:00Z"
  }
}
```
**Validation:** User must not already be member, valid role
**Errors:** INVALID_INPUT (400), FORBIDDEN (403), CONFLICT (409)
**Audit:** Member added

#### DELETE /teams/:teamId/members/:userId
**Purpose:** Remove member from team.
**Response (204 No Content):**
```
```
**Validation:** User must be team member or admin
**Errors:** NOT_FOUND (404), FORBIDDEN (403)
**Audit:** Member removed

---

## Pagination

All list endpoints support pagination:
- **Default:** page=1, limit=20
- **Max limit:** 100
- **Response includes:** page, limit, total, totalPages

---

## Versioning

- **API Version:** v1
- **Header:** Accept: application/json
- **Future Versions:** /api/v2 endpoint with backward compatibility

---

## Rate Limiting

- **Global:** 1000 requests per hour per user
- **Login:** 5 attempts per 15 minutes per email
- **Search:** 100 searches per minute per user
- **Header Response:** `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## Response Headers

```
Content-Type: application/json
X-Request-ID: unique-request-id-for-tracking
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1625356000
X-Response-Time: 125ms
```

---

## Document Control

- **Document ID:** API-SPEC-001
- **Version:** 1.0
- **Author:** Solution Architect
- **Status:** Ready for Handoff
