# Data Requirements

## Purpose
Capture business data expectations for the Task Management System without defining database schema.

## Metadata
- Version: 1.0
- Author: Business Analyst
- Date: 2026-07-04
- Status: Draft
- Workflow ID: WF-20260704-001

## Business Entities

### Entity: User
- Business Meaning: Represents an account holder with access to the platform and permissions based on role.
- Owner: Business/Administrator
- Required Attributes: Email address, password, role, account status, profile details
- Optional Attributes: Avatar, contact information, preferences, timezone, language
- Relationships: User belongs to one or more teams; user may own or be assigned tasks; user may receive notifications.
- Lifecycle: Account created, active, disabled, deleted, restored
- Retention: Account and activity data retained according to business and compliance expectations
- PII Classification: Sensitive

### Entity: Team
- Business Meaning: Represents a group of users who collaborate on work.
- Owner: Administrator or Team Lead
- Required Attributes: Team name, owner, membership
- Optional Attributes: Description, reporting scope, visibility settings
- Relationships: Team contains users; team owns or shares tasks and reports.
- Lifecycle: Team created, active, archived, removed
- Retention: Team data retained while active and auditable for historical work
- PII Classification: Internal

### Entity: Task
- Business Meaning: Represents a discrete unit of work with status, ownership, and deadlines.
- Owner: Task owner or accountable team lead
- Required Attributes: Title, status, priority, owner, created date
- Optional Attributes: Description, assignee, due date, labels, attachments, comments, archived flag
- Relationships: Task belongs to a team or owner; task may be assigned to a user; task may have comments and history.
- Lifecycle: Created, active, archived, completed, blocked, restored
- Retention: Task data retained for historical visibility and audit purposes
- PII Classification: Internal

### Entity: Comment
- Business Meaning: Represents discussion or context added to a task.
- Owner: Task participant
- Required Attributes: Task reference, author, content, created date
- Optional Attributes: Mentioned users, attachments, editing history
- Relationships: Comment belongs to one task and one user
- Lifecycle: Added, edited, removed where policy permits
- Retention: Retained as part of task collaboration history
- PII Classification: Internal

### Entity: Notification
- Business Meaning: Represents a user-visible event about tasks or account activity.
- Owner: User
- Required Attributes: Recipient, event type, timestamp
- Optional Attributes: Delivery channel, read status, task reference
- Relationships: Notification relates to a task, user, or account event
- Lifecycle: Created, delivered, read, dismissed
- Retention: Retained according to notification preference and policy
- PII Classification: Internal

## Notes
- The data requirements above are business-focused and implementation-agnostic.
- No schema, table, or column design is included.
