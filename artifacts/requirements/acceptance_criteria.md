# Acceptance Criteria

## Purpose
Define objective, verifiable conditions required for each story to be accepted.

## Metadata
- Version: 1.0
- Author: Business Analyst
- Date: 2026-07-04
- Status: Draft
- Artifact ID: AC-001
- Traceability: US-001 to US-007, REQ-001 to REQ-010

## Acceptance Criteria by User Story

### US-001
- AC-001: A user can create an account using a valid email address and a password of at least 8 characters, and the system accepts the registration request.
- AC-002: A user can sign in with valid credentials and is taken to the Dashboard after successful authentication.
- AC-003: An invalid credential attempt shows a clear error message and does not grant access.
- AC-004: When a backend or data dependency for authentication cannot be reached, the user is shown the Login screen with an explicit service-unavailable message and no access is granted.

### US-002
- AC-005: An authenticated user can create a task with a title, description, status, priority, and due date and the task appears in the task list.
- AC-006: An authenticated user can edit an owned or assigned task and the updated values are reflected in the task details and task list.
- AC-007: A completed task cannot be edited by a standard user and the system shows a permission-related message; an administrator may override that restriction.
- AC-008: When the task service or data dependency is unavailable, the user remains on the task form or task list and sees an explicit dependency-unavailable state rather than a silent failure.

### US-003
- AC-009: A user can search by title, description, or labels and see only matching tasks.
- AC-010: A user can filter by status, priority, assignee, due date, created date, or team and the task list updates accordingly.
- AC-011: A user can sort by due date, priority, status, or recently updated and the list order changes accordingly.
- AC-012: When the search or filter dependency cannot be reached, the user sees the Task List with a dependency-unavailable state and no misleading empty results.

### US-004
- AC-013: A user with task access can add a comment or attachment to a task and the new item appears in the task activity history.
- AC-014: A user can configure notification preferences and the system respects those preferences for subsequent task events.
- AC-015: A user without task access cannot add collaboration content and is shown a permission message.
- AC-016: When notifications or collaboration data cannot be retrieved, the user sees an explicit dependency-unavailable state in the task details or settings experience.

### US-005
- AC-017: A user with report access can open the Dashboard and view total tasks, completed tasks, pending tasks, overdue tasks, and due-today tasks.
- AC-018: A team lead can view workload and productivity summaries for assigned teams and the displayed values match the visible task data.
- AC-019: A user without report access cannot view restricted report content and is shown a permission message.
- AC-020: When reporting data cannot be reached, the Dashboard or Reports screen shows a dependency-unavailable state and a clear explanation.

### US-006
- AC-021: An administrator can invite, disable, enable, or delete users and the account state changes accordingly.
- AC-022: An administrator can assign roles and team membership and the new access level is reflected in subsequent actions.
- AC-023: A non-administrator cannot perform privileged administration actions and is shown a permission message.
- AC-024: When the user-management or team-management dependency is unavailable, the administration screen shows a dependency-unavailable state and retains the current user or team state.

### US-007
- AC-025: A user can view and edit profile details, upload an avatar, and change a password.
- AC-026: A user can update notification, language, theme, timezone, email, and privacy settings and the changes persist for future sessions.
- AC-027: A user can only update their own profile and settings unless an administrator performs an account-level change.
- AC-028: When profile or settings data cannot be reached, the Profile or Settings screen shows a dependency-unavailable state and preserves the user’s last known values.

## Coverage Expectations
- Each story includes acceptance criteria for happy path, alternate path, validation, error, authorization, and dependency-unavailable behavior.
- Each criterion is measurable, testable, and aligned to the business requirement set.
- Dependency-Unavailable Criteria are included for every story as required.

## Rules
- This file is the single source of truth for acceptance criteria.
- Each AC maps to a story and related requirement through the traceability package.
- No implementation technology or design details are included.

## Approval
- Prepared By: Business Analyst
- Reviewed By: Pending
- Approved By: Pending
