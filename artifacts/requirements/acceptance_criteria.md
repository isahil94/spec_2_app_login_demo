# Acceptance Criteria

## Metadata
- Version: 1.0.0
- Author: Business Analyst
- Date: 2026-07-01
- Status: Draft
- Artifact ID: AC-001
- Traceability: US-001 to US-008, REQ-001 to REQ-012

## Acceptance Criteria by User Story

### US-001
- AC-001: A user can create an account using a valid email address and password that meets the minimum length requirement.
- AC-002: A user receives a clear validation error when the email format is invalid or the password is too short.
- AC-003: A user can sign in with valid credentials and is redirected to the appropriate workspace area.
- AC-004: A user can recover access through a password reset flow and receive guidance if the recovery link is invalid or expired.
- AC-005: An authenticated user can sign out and is no longer able to access protected areas without re-authentication.

### US-002
- AC-006: An authorized user can create a task with a required title and valid values for status, priority, and due date.
- AC-007: An authorized user can edit a task they own or are allowed to modify and see the changes reflected immediately.
- AC-008: A non-administrator user cannot edit a completed task and receives a clear restriction message.
- AC-009: An authorized user can archive a task and the task remains visible in search results but is marked as read-only.
- AC-010: An authorized administrator can restore an archived task and make it active again.
- AC-011: An authorized administrator can permanently delete a task, while regular users cannot.

### US-003
- AC-012: A user can change a task status only to an allowed next state based on the business workflow.
- AC-013: A task moved to Review can be returned to In Progress, and a Blocked task can be moved to In Progress.
- AC-014: A task marked Completed cannot be edited by a non-administrator user.
- AC-015: Every task status change is reflected in task history and audit information.

### US-004
- AC-016: A user can search tasks by title, description, or label and see matching results.
- AC-017: A user can filter tasks by status, priority, assignee, due date, created date, and team.
- AC-018: A user can sort tasks by due date, priority, status, and recently updated.
- AC-019: When no results match the current criteria, the user sees an empty state with guidance.

### US-005
- AC-020: A user can add a comment to a visible task and the comment appears in task context.
- AC-021: A user receives a notification when assigned to a task, when a task is updated, or when mentioned in a comment.
- AC-022: A notification is shown only to the relevant recipient and is not exposed to unauthorized users.
- AC-023: A task activity history records comments and status changes in an immutable audit trail.

### US-006
- AC-024: An administrator or team lead can invite a user to a team and assign a valid role.
- AC-025: An administrator or team lead can remove or change team membership and the change is reflected immediately.
- AC-026: A user without management privileges cannot perform team or user administration actions.
- AC-027: Membership and role changes are captured in audit history.

### US-007
- AC-028: An authorized user can open the dashboard and see totals for tasks, completed work, pending work, overdue work, and due today.
- AC-029: A team lead or administrator can view workload and completion summaries for the relevant team or organization.
- AC-030: When there is no relevant activity data, the dashboard or report view shows an informative empty state.
- AC-031: Dashboard and report values reflect the user’s visible task and activity data.

### US-008
- AC-032: A user can update profile details, avatar, and personal settings and save the changes successfully.
- AC-033: A user can change a password only when the password meets validation requirements.
- AC-034: A user receives clear feedback for invalid profile or password input values.
- AC-035: An administrator can configure organization-level preferences that apply to the relevant scope.

## Coverage Expectations
- Each story includes acceptance criteria for success, validation, authorization, and error behavior where applicable.
- Each criterion is measurable, business-visible, and testable.
