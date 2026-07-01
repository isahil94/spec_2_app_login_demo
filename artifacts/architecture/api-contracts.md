# API Contracts

## Purpose
Define the task management API contracts, request/response models, authentication requirements, and error handling for the Task Management System.

## Metadata
- Version: 1.0.0
- Author: Solution Architect
- Date: 2026-07-01
- Status: Draft
- API ID: API-001
- Service: Task Management API
- Workflow ID: WF-20260701-001
- Correlation ID: CORR-20260701-001
- Traceability: requirements_spec.md, user_stories.md, acceptance_criteria.md

## API Overview
The API exposes RESTful endpoints for authentication, task lifecycle management, teams, comments, notifications, dashboards, and user preferences. All endpoints use JSON over HTTPS.

## Contract Coverage
- Authentication: US-001
- Tasks: US-002, US-003, US-004
- Comments & Notifications: US-005
- Teams & Roles: US-006
- Dashboard & Reports: US-007
- Profile & Settings: US-008

## Error Model
- `error_code`: machine-readable string
- `message`: human-readable summary
- `details`: optional array of field-specific validation details
- `request_id`: correlation identifier

Example
```
{
  "error_code": "AUTH_INVALID_CREDENTIALS",
  "message": "Invalid email or password.",
  "details": [],
  "request_id": "abc-123"
}
```

## Authentication and Authorization
- All protected endpoints require an authentication token or session cookie.
- Role checks: Administrator, TeamLead, User.
- Authorization is enforced per endpoint and per entity ownership.

## Endpoints

### Authentication
- `POST /auth/register`
  - Purpose: create a new user account.
  - Request: `email`, `password`, `display_name`, `remember_me`.
  - Response: `user_id`, `email`, `display_name`, `token`, `expires_in`.

- `POST /auth/login`
  - Purpose: authenticate a user.
  - Request: `email`, `password`, `remember_me`.
  - Response: `user_id`, `token`, `expires_in`, `roles`.

- `POST /auth/recover`
  - Purpose: initiate password recovery.
  - Request: `email`.
  - Response: `status`, `message`.

- `POST /auth/reset`
  - Purpose: complete password reset.
  - Request: `token`, `new_password`.
  - Response: `status`, `message`.

### Profile and Preferences
- `GET /users/me`
  - Purpose: retrieve current user profile.
  - Response: `user_id`, `email`, `display_name`, `roles`, `teams`, `preferences`.

- `PUT /users/me`
  - Purpose: update profile details.
  - Request: `display_name`, `avatar_url`, `time_zone`, `language`.
  - Response: updated profile.

- `GET /users/settings`
  - Purpose: retrieve notification and UI preferences.
  - Response: `notification_preferences`, `theme`, `time_zone`, `language`.

- `PUT /users/settings`
  - Purpose: update personal settings.
  - Request: `notification_preferences`, `theme`, `time_zone`, `language`.
  - Response: updated settings.

### Task Management
- `GET /tasks`
  - Purpose: retrieve task list with filtering, sorting, and paging.
  - Query: `search`, `status`, `priority`, `assignee_id`, `team_id`, `due_date_from`, `due_date_to`, `created_date_from`, `created_date_to`, `archived`.
  - Response: array of task summaries, `total_count`, `page`, `page_size`.

- `POST /tasks`
  - Purpose: create a new task.
  - Request: `title`, `description`, `status`, `priority`, `assignee_id`, `due_date`, `labels`, `team_id`, `attachments`.
  - Response: created task metadata.

- `GET /tasks/{task_id}`
  - Purpose: retrieve task details.
  - Response: full task payload, history summary, comments count.

- `PUT /tasks/{task_id}`
  - Purpose: update a task.
  - Request: any editable task fields.
  - Response: updated task.

- `POST /tasks/{task_id}/archive`
  - Purpose: archive a task.
  - Response: archived task status.

- `POST /tasks/{task_id}/restore`
  - Purpose: restore an archived task.
  - Response: restored task status.

- `POST /tasks/{task_id}/duplicate`
  - Purpose: duplicate an existing task.
  - Response: new task metadata.

- `POST /tasks/{task_id}/status`
  - Purpose: update task status according to allowed transitions.
  - Request: `status`, `comment`.
  - Response: updated status and history entry.

### Comments
- `GET /tasks/{task_id}/comments`
  - Purpose: list comments for a task.
  - Response: comment array.

- `POST /tasks/{task_id}/comments`
  - Purpose: add a comment to a task.
  - Request: `content`, `mentions`, `attachments`.
  - Response: comment metadata.

### Teams and Membership
- `GET /teams`
  - Purpose: list teams visible to the authenticated user.
  - Response: team summaries.

- `POST /teams`
  - Purpose: create a new team.
  - Request: `name`, `description`, `lead_user_id`.
  - Response: created team metadata.

- `GET /teams/{team_id}`
  - Purpose: retrieve team details and members.
  - Response: team metadata, members.

- `POST /teams/{team_id}/members`
  - Purpose: invite or add a member.
  - Request: `user_id`, `role`.
  - Response: membership metadata.

- `PUT /teams/{team_id}/members/{user_id}`
  - Purpose: update a member role.
  - Request: `role`.
  - Response: updated membership.

- `DELETE /teams/{team_id}/members/{user_id}`
  - Purpose: remove a member from a team.
  - Response: membership removal acknowledgement.

### Notifications
- `GET /notifications`
  - Purpose: fetch notifications relevant to the current user.
  - Response: notification array, unread count.

- `POST /notifications/{notification_id}/read`
  - Purpose: mark a notification as read.
  - Response: updated notification state.

### Dashboard and Reporting
- `GET /dashboard`
  - Purpose: retrieve summary metrics for user or team.
  - Response: totals, overdue counts, upcoming due tasks, completion summaries.

- `GET /reports`
  - Purpose: retrieve report data for allowed scope.
  - Query: `team_id`, `from_date`, `to_date`, `type`.
  - Response: report dataset.

- `GET /reports/team/{team_id}`
  - Purpose: retrieve team-specific report details.
  - Response: team workload and completion metrics.

## Request Models
### TaskCreateRequest
- `title` (string, required, max 100)
- `description` (string, optional, max 2000)
- `status` (string, required, values: Todo, In Progress, Review, Completed, Blocked)
- `priority` (string, required, values: Low, Medium, High, Critical)
- `assignee_id` (string, optional)
- `due_date` (string, date, optional)
- `labels` (array of strings, optional)
- `team_id` (string, required)
- `attachments` (array of attachment references, optional)

### TaskStatusUpdateRequest
- `status` (string, required)
- `comment` (string, optional)

### CommentCreateRequest
- `content` (string, required, max 1000)
- `mentions` (array of user IDs, optional)
- `attachments` (array of attachment references, optional)

### TeamMembershipRequest
- `user_id` (string, required)
- `role` (string, required, values: Administrator, TeamLead, Member)

### ProfileUpdateRequest
- `display_name` (string, optional)
- `avatar_url` (string, optional)
- `time_zone` (string, optional)
- `language` (string, optional)

## Response Models
### TaskSummary
- `task_id`, `title`, `status`, `priority`, `assignee_id`, `team_id`, `due_date`, `archived`, `updated_at`

### TaskDetail
- all TaskSummary fields plus `description`, `labels`, `creator_id`, `created_at`, `history_summary`, `comments_count`, `attachments`

### NotificationSummary
- `notification_id`, `type`, `title`, `message`, `created_at`, `read`, `related_task_id`

## Pagination, Filtering, Sorting
- Pagination: `page`, `page_size`, `total_count`.
- Filtering: supported for task fields and report scope.
- Sorting: supported for due date, priority, status, and updated_at.

## Idempotency
- `POST /auth/recover` and `POST /tasks/{task_id}/status` are idempotent in effect when repeated with the same data.
- Task creation and updates should be safe when the client retries after network interruptions.

## Versioning and Compatibility
- Version APIs through URL or header when backward incompatible changes are required.
- Default contract version is v1.

## Audit Requirements
- Log every authentication, task lifecycle, team membership, comment, notification, and profile update event.
- Include `request_id`, `user_id`, `timestamp`, and `entity_id` where applicable.

## Integration Contracts
- I-001: Notification service provider must accept delivery requests in JSON and return status success/failure.
- I-002: Attachment storage provider must return secure upload/download URLs and preserve access control.

## Architecture Constraints
- All endpoints must reject unauthorized access before business logic executes.
- Task state transitions must validate allowed next states.
- Dashboard and report endpoints must scope data to user visibility.

## Open Questions
See `openlog.md` for assumptions and unresolved architecture questions.

## Approval
- Prepared By: Solution Architect
- Reviewed By: Pending
- Approved By: Pending
