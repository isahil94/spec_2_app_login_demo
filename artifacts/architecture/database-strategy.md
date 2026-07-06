# Database Strategy

## Purpose
Define the conceptual data persistence strategy for the Task Management System without DDL.

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-04
- Status: Draft
- Artifact ID: DB-STRAT-001

---

## Database Technology Selection

### Development: SQLite
- **Rationale:** Zero-config local development, file-based persistence, no server setup
- **Deployment:** `apps/data/task_management.db` file in project directory
- **Connection:** Direct file connection

### Production: PostgreSQL
- **Rationale:** ACID compliance, proven reliability, scalability, replication support
- **Version:** 13+ LTS
- **High Availability:** Primary + Read Replica with failover
- **Connection:** Connection pooling (max 20 connections per app instance)

---

## Conceptual Data Model

### Entities

#### User Entity
**Business Meaning:** Represents an authenticated account holder with access permissions.
**Relationships:**
- User owns many Tasks (1:N)
- User is assigned to many Tasks (1:N via task.assignee)
- User belongs to many Teams (M:N)
- User is author of many Comments (1:N)
- User receives many Notifications (1:N)

**Key Attributes:**
- email (unique, indexed)
- role (ADMIN, TEAM_LEAD, TEAM_MEMBER)
- account_status (active, disabled, deleted)
- profile: fullName, contactInformation
- preferences: theme, language, timezone
- password_hash (bcrypt)
- audit fields: created_at, updated_at, created_by, updated_by

**Lifecycle:**
- Created → Active → Disabled (soft-delete) → Deleted (admin purge)
- Soft-delete preserves audit trail

**Audit Considerations:**
- All profile changes recorded
- Role changes audited
- Login attempts tracked
- Password resets logged

---

#### Team Entity
**Business Meaning:** Represents a collaborative group of users.
**Relationships:**
- Team has many Users (M:N via team_membership)
- Team has many Tasks (1:N, optional)
- Team has many Reports (1:N)

**Key Attributes:**
- name (unique within scope)
- description
- owner (FK to User)
- created_at, updated_at

**Lifecycle:**
- Created → Active → Archived

---

#### Task Entity
**Business Meaning:** Represents a discrete unit of work with status and ownership.
**Relationships:**
- Task belongs to User (owner, 1:N)
- Task may be assigned to User (optional, 1:N)
- Task belongs to Team (optional, 1:N)
- Task has many Comments (1:N)
- Task has Audit entries (1:N)
- Task has Attachment metadata (1:N)

**Key Attributes:**
- title (max 100 chars, indexed for search)
- description (max 2000 chars)
- status (todo, in_progress, review, completed, blocked)
- priority (low, medium, high, critical)
- owner_id (FK to User, indexed)
- assignee_id (FK to User, optional, indexed)
- team_id (FK to Team, optional, indexed)
- due_date (indexed, optional)
- labels (array or separate table)
- archived_at (soft-delete marker, nullable)
- version (optimistic lock for concurrent edits)
- audit fields: created_at, updated_at, created_by, updated_by

**Indexes:**
- owner_id, assignee_id, team_id, status, priority, due_date, created_date, archived_at
- Full-text index on title + description for search

**Constraints:**
- title NOT NULL
- status must be from allowed set
- priority must be from allowed set
- due_date >= CURRENT_DATE OR NULL
- archived_at = NULL (active) or datetime (archived)

**Lifecycle:**
- Created (Todo) → Active (In Progress, Review, Blocked) → Completed
- Can be archived at any point
- Can be restored from archive

**Audit Trail:**
- Every state change recorded (status, priority, assignee, etc.)
- Change history stored in audit table (not in task table itself)

---

#### Comment Entity
**Business Meaning:** Represents a user-contributed note or discussion on a task.
**Relationships:**
- Comment belongs to Task (1:N)
- Comment belongs to User author (1:N)
- Comment may reference Users (mentions, M:N)

**Key Attributes:**
- task_id (FK, indexed)
- author_id (FK to User, indexed)
- content (text, not nullable)
- created_at (indexed)
- updated_at (nullable, only if edited)
- edit_history (JSON array of previous versions, optional)

**Lifecycle:**
- Created → Optional edits → Deleted (soft or hard)

**Audit Trail:**
- Comment creation and deletion logged
- Edit history tracked in json field

---

#### Notification Entity
**Business Meaning:** Represents a user-facing event or activity.
**Relationships:**
- Notification belongs to User recipient (1:N)
- Notification may reference Task (optional, 1:N)
- Notification may reference another User (actor, 1:N)

**Key Attributes:**
- recipient_id (FK to User, indexed)
- type (task_assigned, task_status_changed, comment_added, mentioned, etc.)
- title (short, < 100 chars)
- message (< 500 chars)
- task_id (FK optional)
- actor_id (FK optional)
- delivery_channel (in_app, email, sms)
- read_at (nullable timestamp, marks as read)
- dismissed_at (nullable timestamp, marks as dismissed)
- created_at (indexed)

**Lifecycle:**
- Created → Delivered (in-app immediate) → Optional email send → Read/Dismissed
- Auto-expire after 30 days

**Audit Trail:**
- Notification dispatch logged
- Read status tracked

---

#### Audit Entity (Immutable, Append-Only)
**Business Meaning:** Immutable record of all significant system actions.
**Relationships:**
- References User (actor)
- References Entity (task, user, team, comment, etc.)

**Key Attributes:**
- audit_id (PK)
- entity_type (user, task, team, comment, notification, settings)
- entity_id (FK to related entity, indexed)
- action (created, updated, deleted, archived, restored, status_changed, role_changed, etc.)
- actor_id (FK to User who performed action, indexed)
- timestamp (created_at, indexed)
- details (JSON: before/after values, field changes)
- ip_address (optional, for security)

**Constraints:**
- Immutable (no UPDATE, no DELETE allowed)
- Append-only table
- Indexed for query: entity_type, entity_id, action, timestamp, actor_id

**Retention:** Indefinite (with optional archive to cold storage after 1 year)

---

#### Team Membership Junction Entity
**Business Meaning:** Represents a user's membership in a team with a role.
**Relationships:**
- Links User to Team
- Many-to-many relationship

**Key Attributes:**
- team_id (FK, part of PK)
- user_id (FK, part of PK)
- role (TEAM_LEAD, TEAM_MEMBER)
- joined_at
- updated_at

**Constraints:**
- Composite PK on (team_id, user_id)
- Unique constraint: user cannot be in team twice

---

#### Attachment Metadata Entity (Conceptual)
**Business Meaning:** Metadata reference for files attached to tasks.
**Relationships:**
- Attachment belongs to Task (1:N)
- Attachment belongs to User uploader (1:N)

**Key Attributes:**
- attachment_id (PK)
- task_id (FK, indexed)
- uploader_id (FK to User)
- file_name
- file_url (reference to storage system)
- file_size
- mime_type
- created_at

**Storage:** Actual files stored in object storage (S3, GCS, etc.) with URL reference

---

## Data Flow

```
┌──────────────────────────────┐
│     API Request              │
└──────────────┬───────────────┘
               │
        ┌──────▼──────────┐
        │ Business Layer  │
        │ (Validation)    │
        └──────┬──────────┘
               │
        ┌──────▼──────────────────┐
        │ Repository Pattern      │
        │ (Service → Repo calls)  │
        └──────┬──────────────────┘
               │
     ┌─────────┴─────────┐
     │                   │
┌────▼──────────┐  ┌────▼──────────┐
│  SELECT/      │  │  INSERT/      │
│  QUERY        │  │  UPDATE/      │
│               │  │  DELETE       │
└────┬──────────┘  └────┬──────────┘
     │                  │
┌────▼──────────────────▼───────────┐
│      PostgreSQL / SQLite          │
│  (Transaction, Constraints)       │
└────┬─────────────────────────────┘
     │
     ├─── Task Table (with audit fields)
     ├─── User Table
     ├─── Team Table
     ├─── Comment Table
     ├─── Notification Table
     ├─── Audit Table (append-only)
     └─── Indexes (performance)
```

---

## Transaction Strategy

### Isolation Level
- **Default:** READ_COMMITTED (PostgreSQL default)
- **Critical Operations:** SERIALIZABLE (e.g., concurrent task edits)

### Transaction Boundaries
- **Task Creation:** Single transaction (insert task + insert audit entry)
- **Task Update:** Single transaction (update task + insert audit entry)
- **Status Change:** Single transaction with version check (optimistic locking)
- **Bulk Operations:** Wrapped in transaction for consistency

### Deadlock Prevention
- Consistent lock ordering (always lock in same order across transactions)
- Short transaction duration
- Retry logic for transaction failures

---

## Indexing Strategy

### Clustered Index (Primary Key)
- All tables: id or composite key

### Non-Clustered Indexes (Performance)
- **User:** email (unique), role, account_status
- **Task:** owner_id, assignee_id, team_id, status, priority, due_date, created_at, archived_at
  - Full-text index: title + description
- **Comment:** task_id, author_id, created_at
- **Notification:** recipient_id, created_at, read_at
- **Audit:** entity_type, entity_id, action, actor_id, timestamp

### Index Maintenance
- Monitor slow queries (>1000ms)
- Rebuild indexes monthly
- Analyze query plans quarterly

---

## Soft Delete & Archive Strategy

### Soft Delete Implementation
- **Approach:** archived_at or deleted_at nullable timestamp column
- **Query Impact:** Default query: WHERE deleted_at IS NULL
- **Admin Access:** Include archived records with separate flag
- **Benefit:** Preserves audit history, enables restore

### Example: Task Archive
- User archives task: UPDATE task SET archived_at = NOW() WHERE id = ?
- Task List queries: SELECT * FROM task WHERE archived_at IS NULL
- Restore: UPDATE task SET archived_at = NULL WHERE id = ?

### Backup & Purge
- Soft-deleted records retained for compliance audit window (typically 90 days minimum)
- Hard delete only by admin after retention period
- Audit entries never deleted

---

## Backup & Recovery

### Backup Strategy
- **Frequency:** Hourly snapshots (production)
- **Retention:** 30 days rolling backup window
- **Location:** Separate storage from primary database
- **Test Recovery:** Weekly restore verification

### Recovery Procedure
- Point-in-time recovery (PITR) for < 30 days back
- Full backup restore for older states
- Transaction logs replayed to target timestamp

---

## Data Ownership & Access

| Entity | Owner | Can Read | Can Write |
|--------|-------|----------|-----------|
| User Account | User | User, Admins | User, Admins |
| Task | Owner | Owner, Assignee, Team, Admins | Owner, Assignee (status), Admins |
| Comment | Author | Task participants, Admins | Author, Admins |
| Team | Team Owner | Members, Admins | Owner, Admins |
| Notification | Recipient | Recipient, Admins | System, Admins |
| Audit | System | Admins | System only |
| Settings | User | User, Admins | User, Admins |

---

## Performance Considerations

### Query Optimization
- **N+1 Prevention:** Eager loading relationships in repositories
- **Pagination:** Always limit result sets (default 20, max 100)
- **Lazy Loading:** Avoid loading full comment list on task details; paginate comments

### Caching
- **Dashboard Metrics:** Cache with 5-minute TTL
- **User Preferences:** Cache with 1-hour TTL
- **Invalidation:** Clear cache on write to related entity

### Partitioning (Future)
- **Task Table:** Partition by created_year for very large datasets
- **Audit Table:** Archive older partitions to cold storage

---

## Security & Compliance

### Data Protection
- **Passwords:** Hashed with bcrypt, never stored plain-text
- **Sensitive Fields:** Email addresses indexed (searchable)
- **Encryption:** TLS in transit; at-rest encryption optional (PostgreSQL pgcrypto)
- **PII:** Retain only as needed per business requirements

### Access Control
- **Row-Level Security:** PostgreSQL RLS for multi-tenant isolation (future)
- **Audit Logging:** All privileged and sensitive operations recorded
- **Compliance:** GDPR right-to-be-forgotten supported via soft-delete + audit cleanup

### Data Retention Policies
- Active user data: Retained indefinitely while account active
- Deleted user data: Retained 90 days for audit, then purged
- Audit records: Retained indefinitely (compliance requirement)
- Notification records: Retained 30 days, then archived

---

## Database Initialization

### Schema Creation
- Version-controlled SQL migration files
- Migrations run on deployment before application start
- Numbered sequentially: 001_init.sql, 002_audit.sql, etc.

### Seed Data
- Reference data: Status values, priority values, roles
- Test fixtures: Sample users, tasks for development

### Environment Setup
- **Dev:** Local SQLite, auto-migrate on start
- **Test:** Ephemeral PostgreSQL in Docker, seed test data
- **Prod:** PostgreSQL with HA, manual migration approval

---

## Related Documents

- [lld.md](lld.md) – Detailed package and repository design
- [api-specifications.md](api-specifications.md) – API contracts referencing entities
- [architecture-design.md](architecture-design.md) – Higher-level architecture
- [security-architecture.md](security-architecture.md) – Data protection strategy

---

## Document Control

- **Document ID:** DB-STRAT-001
- **Version:** 1.0
- **Author:** Solution Architect
- **Status:** Ready for Database Developer Handoff
