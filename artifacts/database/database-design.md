# Database Design

## Workflow Context
- Workflow ID: WF-1783270392315
- Correlation ID: WF-1783270392315
- Agent: database-developer
- Stage: Database

## Objective
Design a relational database schema for the Task Management System that supports user authentication, task management, collaboration, and reporting needs reflected in the backend and frontend handoff contracts.

## Core Entities

### users
Stores user account and profile information.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | Surrogate key |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Login identifier |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password |
| full_name | VARCHAR(255) | NOT NULL | Display name |
| role | VARCHAR(50) | NOT NULL | admin, manager, member |
| status | VARCHAR(50) | NOT NULL | active, disabled |
| avatar_url | TEXT | NULL | Optional profile image |
| preferences | JSON | NULL | Theme, notifications, language |
| created_at | TIMESTAMP | NOT NULL | Audit field |
| updated_at | TIMESTAMP | NOT NULL | Audit field |

### teams
Represents collaborative groups that own tasks and members.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | Surrogate key |
| name | VARCHAR(255) | NOT NULL | Team name |
| description | TEXT | NULL | Optional context |
| created_at | TIMESTAMP | NOT NULL | Audit field |
| updated_at | TIMESTAMP | NOT NULL | Audit field |

### team_members
Associates users with teams.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| team_id | UUID | FK -> teams.id | 
| user_id | UUID | FK -> users.id | 
| role | VARCHAR(50) | NOT NULL | member, lead |
| created_at | TIMESTAMP | NOT NULL | Audit field |
| PRIMARY KEY | (team_id, user_id) | | Composite key |

### tasks
Stores task records and workflow state.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | Surrogate key |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | NULL | Detailed content |
| status | VARCHAR(50) | NOT NULL | todo, in_progress, review, completed, blocked |
| priority | VARCHAR(50) | NOT NULL | low, medium, high, critical |
| assignee_id | UUID | FK -> users.id | Nullable |
| reporter_id | UUID | FK -> users.id | Nullable |
| team_id | UUID | FK -> teams.id | Nullable |
| due_date | DATE | NULL | Deadline |
| labels | JSON | NULL | Tags or categories |
| archived | BOOLEAN | NOT NULL DEFAULT false | Soft delete flag |
| created_at | TIMESTAMP | NOT NULL | Audit field |
| updated_at | TIMESTAMP | NOT NULL | Audit field |

### comments
Stores user comments on tasks.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | Surrogate key |
| task_id | UUID | FK -> tasks.id | 
| author_id | UUID | FK -> users.id | 
| body | TEXT | NOT NULL | Comment content |
| created_at | TIMESTAMP | NOT NULL | Audit field |

### attachments
Stores file uploads associated with tasks.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | Surrogate key |
| task_id | UUID | FK -> tasks.id | 
| file_name | VARCHAR(255) | NOT NULL | Original filename |
| storage_path | TEXT | NOT NULL | Stored file path |
| uploaded_by | UUID | FK -> users.id | 
| created_at | TIMESTAMP | NOT NULL | Audit field |

### activity_logs
Tracks audit activity for task and user operations.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | Surrogate key |
| entity_type | VARCHAR(50) | NOT NULL | task, user, team |
| entity_id | UUID | NOT NULL | Target entity |
| action | VARCHAR(100) | NOT NULL | created, updated, deleted, archived |
| actor_id | UUID | FK -> users.id | Nullable |
| created_at | TIMESTAMP | NOT NULL | Audit field |

## Relationships
- One user may belong to many teams through team_members.
- One team may own many tasks.
- One task has many comments.
- One task has many attachments.
- One task may generate many activity log entries.

## Constraints and Rules
- Email must be unique.
- Task status must be one of the supported workflow states.
- Priority must be one of low, medium, high, critical.
- Archived tasks are read-only in business logic.
- Completed tasks may only be edited by administrators.

## Index Recommendations
- users.email
- tasks.assignee_id
- tasks.reporter_id
- tasks.team_id
- tasks.due_date
- tasks.status
- comments.task_id
- attachments.task_id
- activity_logs.entity_type, entity_id

## Migration Notes
- Use UUID primary keys for portability across services.
- Enforce foreign keys where supported by the target database engine.
- Add timestamp fields for auditability.
- Prefer JSON for flexible user preferences and labels unless a normalized structure is required later.
