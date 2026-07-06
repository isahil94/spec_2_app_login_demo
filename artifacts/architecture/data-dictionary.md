# Data Dictionary

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-06
- Status: Draft
- Architecture ID: ARCH-008
- Workflow ID: WF-20260705-001
- Correlation ID: WF-1783283413777
- Traceability: data_requirements.md, business_rules.md

## Canonical Data Objects
| Object | Purpose | Ownership | Key Fields |
|---|---|---|---|
| User | Authenticated account and profile | Identity service | id, email, role, status, displayName, preferences |
| Team | Collaborative grouping of users | Team administration service | id, name, ownerId, status |
| Task | Work item for assignment and tracking | Task service | id, title, description, status, priority, ownerId, assigneeId, dueDate, archivedFlag |
| Comment | Discussion entry on a task | Collaboration service | id, taskId, authorId, content, createdAt |
| Attachment | File reference attached to a task | Collaboration service | id, taskId, ownerId, metadata, createdAt |
| Notification | User-facing alert | Notification service | id, recipientId, eventType, relatedTaskId, readState, createdAt |
| ActivityLog | Audit history for changes | Audit service | id, actorId, entityType, entityId, eventType, timestamp, outcome |

## Data Ownership Notes
- User and account data are owned by the identity and profile domain.
- Team membership and role changes are owned by administration services.
- Task lifecycle and collaboration events are owned by task and collaboration services.
- Audit history is owned by the audit and observability domain.

## Validation and Integrity Expectations
- Required values, allowed status values, role scope, and due-date constraints are enforced in the business layer.
- Audit events must be emitted for material state changes and permission-sensitive actions.
