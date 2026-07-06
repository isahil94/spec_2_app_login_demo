# Data Requirements

## Metadata
- Version: 1.0
- Author: Business Analyst
- Date: 2026-07-05
- Status: Draft
- Workflow ID: WF-20260705-001

## Business Entities

### Entity: User
- Business Meaning: Authenticated person who accesses the system.
- Owner: Business Operations / System Administrator
- Required Attributes: Email, password hash, role, display name, account status.
- Optional Attributes: Avatar, phone, timezone, language, preferences.
- Relationships: Belongs to one or more teams; owns or is assigned tasks; receives notifications.
- Lifecycle: Active, Disabled, Deleted.
- Retention: Account records retained according to governance policy.
- PII Classification: Sensitive

### Entity: Team
- Business Meaning: A collaborative grouping of users.
- Owner: Team Lead / Administrator
- Required Attributes: Team name, owner, created date.
- Optional Attributes: Description, status, membership policy.
- Relationships: Contains users; owns tasks and reports.
- Lifecycle: Active, Archived.
- Retention: Retained while active and for audit history.
- PII Classification: Internal

### Entity: Task
- Business Meaning: A work item that must be planned, assigned, and completed.
- Owner: Task Owner / Assigned User
- Required Attributes: Title, description, status, priority, owner, assignee, created date, due date.
- Optional Attributes: Labels, attachments, comments, archived flag, reporter.
- Relationships: Belongs to a team or user; linked to comments, history, and notifications.
- Lifecycle: Todo, In Progress, Review, Completed, Blocked, Archived.
- Retention: Retained for reporting and audit history.
- PII Classification: Internal

### Entity: Comment
- Business Meaning: User discussion associated with a task.
- Owner: Task participant
- Required Attributes: Task reference, author, content, created date.
- Optional Attributes: Mentioned users, attachment reference.
- Relationships: Associated with one task and one user.
- Lifecycle: Active, Deleted.
- Retention: Retained with task context.
- PII Classification: Internal

### Entity: Notification
- Business Meaning: User-facing alert about task or system activity.
- Owner: System / User
- Required Attributes: Recipient, message, event type, created date.
- Optional Attributes: Read status, delivery channel, related task reference.
- Relationships: Related to a user and optionally a task.
- Lifecycle: New, Read, Dismissed.
- Retention: Short-term operational retention.
- PII Classification: Internal

### Entity: ActivityLog
- Business Meaning: Audit record of task and account changes.
- Owner: System
- Required Attributes: Event type, subject, actor, timestamp, outcome.
- Optional Attributes: Related task or user reference, comment reference.
- Relationships: Linked to users and tasks.
- Lifecycle: Recorded, Archived.
- Retention: Retained according to governance and audit requirements.
- PII Classification: Internal

## Notes
- Data requirements are implementation-agnostic and business-focused.
- No schema or storage design is included.
