# Acceptance Criteria

## Metadata
- Version: 1.0
- Author: Business Analyst
- Date: 2026-07-05
- Status: Draft
- Artifact ID: AC-001
- Traceability: US-001 to US-007, REQ-001 to REQ-010

## Acceptance Criteria by User Story

### US-001
- AC-001: A new user can register with a valid email, password, and required profile details.
- AC-002: A registered user can sign in with valid credentials and reach the dashboard.
- AC-003: Invalid credentials show an error state and do not grant access.
- AC-004: A user can use password recovery and receive a reset path without exposing account details.
- AC-005: When authentication services are unavailable, the system shows the Login screen with a dependency-unavailable state and no false success message.

### US-002
- AC-006: A user with permission can create a task with title, status, priority, due date, and assignment details.
- AC-007: An authorized user can update an existing task and see the revised values in the task list and details view.
- AC-008: A task cannot be saved if required fields are missing or due date violates the business rule.
- AC-009: A completed task cannot be edited by a non-administrator and shows a permission-denied state.
- AC-010: When the task service is unavailable, the task form remains on the same screen and shows a dependency-unavailable state.

### US-003
- AC-011: A user can search by title, description, and labels and see matching results.
- AC-012: A user can filter by status, priority, assignee, due date, created date, and team.
- AC-013: A user can sort results by due date, priority, status, or recent update.
- AC-014: A search with no matching results shows an empty state and no misleading success message.
- AC-015: When the search index or data dependency is unavailable, the task list shows a dependency-unavailable state and preserves the current filter context.

### US-004
- AC-016: A user with task access can add a comment and attachment to an existing task.
- AC-017: New comment or attachment activity is visible in the task history and task details view.
- AC-018: A user without access cannot add comments or attachments and is shown a permission state.
- AC-019: A failed upload or comment save shows a clear error state without losing the current task context.
- AC-020: When the collaboration service is unavailable, the task details screen shows a dependency-unavailable state and preserves the entered content.

### US-005
- AC-021: An administrator or team lead can invite users, assign roles, and manage team membership.
- AC-022: A user can be disabled or removed only by an authorized role.
- AC-023: A role assignment that violates permission rules is rejected and shown as a validation error.
- AC-024: A non-authorized user attempting team or user management sees an access-denied state.
- AC-025: When team or user management services are unavailable, the management screen remains open and shows a dependency-unavailable state.

### US-006
- AC-026: A user receives notifications for task assignments, updates, comments, due-date reminders, and overdue tasks where applicable.
- AC-027: A user can open the notifications or reports view and review the available items.
- AC-028: A user without reporting access cannot view reports and is shown an access-denied state.
- AC-029: A report with no data shows an empty state rather than an error.
- AC-030: When notification or reporting data cannot be retrieved, the relevant screen shows a dependency-unavailable state and preserves the last successful view.

### US-007
- AC-031: A user can view and edit profile information and settings.
- AC-032: Password changes require valid current credentials and meet minimum policy requirements.
- AC-033: Invalid profile or settings values are rejected with clear validation feedback.
- AC-034: A user can upload an avatar and see the updated profile image.
- AC-035: When profile or settings services are unavailable, the settings screen shows a dependency-unavailable state and preserves the unsaved changes.

## Coverage Expectations
- Each story includes happy path, validation, authorization, and dependency-unavailable criteria.
- All criteria are measurable and aligned to the business requirements and user stories.
