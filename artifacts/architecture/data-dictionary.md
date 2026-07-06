# Data Dictionary

## Purpose
Define canonical data definitions, ownership, and usage for all business entities and data elements.

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-04
- Status: Draft
- Artifact ID: DATA-DICT-001

---

## Data Dictionary

### User Entity

| Field | Type | Required | Unique | Indexed | PII | Description |
|-------|------|----------|--------|---------|-----|-------------|
| user_id | UUID | Yes | Yes | Yes | No | Primary identifier |
| email | String(254) | Yes | Yes | Yes | Yes | Email address, used for login |
| password_hash | String(60) | Yes | No | No | Yes | bcrypt hashed password |
| full_name | String(100) | Yes | No | No | Yes | User's display name |
| contact_information | String(200) | No | No | No | Yes | Phone, secondary email, etc. |
| avatar_url | String(500) | No | No | No | No | URL to avatar image |
| role | Enum | Yes | No | Yes | No | ADMIN, TEAM_LEAD, TEAM_MEMBER |
| account_status | Enum | Yes | No | Yes | No | active, disabled, deleted |
| theme | String(10) | No | No | No | No | light, dark, system |
| language | String(5) | No | No | No | No | en, es, fr, etc. |
| timezone | String(50) | No | No | No | No | UTC, America/New_York, etc. |
| notify_in_app | Boolean | No | No | No | No | Default: true |
| notify_email | Boolean | No | No | No | No | Default: false |
| created_at | DateTime | Yes | No | Yes | No | Account creation timestamp |
| updated_at | DateTime | Yes | No | Yes | No | Last profile update |
| created_by | UUID | Yes | No | No | No | Admin or system |
| updated_by | UUID | No | No | No | No | Last modifier |
| last_login_at | DateTime | No | No | No | No | Last sign-in timestamp |
| account_locked_until | DateTime | No | No | No | No | Lockout expiration |

**Owner:** User (self), Admins (full access)  
**Access:** Private data; visible to self and admins  
**Retention:** Active while account active; 90 days after soft-delete  

---

### Team Entity

| Field | Type | Required | Unique | Indexed | Description |
|-------|------|----------|--------|---------|-------------|
| team_id | UUID | Yes | Yes | Yes | Primary identifier |
| name | String(100) | Yes | No | Yes | Team display name |
| description | String(500) | No | No | No | Team purpose and scope |
| owner_id | UUID | Yes | No | Yes | Team creator/owner |
| created_at | DateTime | Yes | No | Yes | Team creation timestamp |
| updated_at | DateTime | Yes | No | No | Last update |
| created_by | UUID | Yes | No | No | Creator user ID |
| updated_by | UUID | No | No | No | Last modifier |
| archived_at | DateTime | No | No | Yes | Soft-delete marker |

**Owner:** Team owner, Admins  
**Access:** Team members can view; owner/admin can modify  
**Retention:** Indefinite while active; auditable after archive  

---

### Task Entity

| Field | Type | Required | Unique | Indexed | Description |
|-------|------|----------|--------|---------|-------------|
| task_id | UUID | Yes | Yes | Yes | Primary identifier |
| title | String(100) | Yes | No | Yes | Task name (searchable) |
| description | String(2000) | No | No | Yes | Task details (searchable) |
| status | Enum | Yes | No | Yes | todo, in_progress, review, completed, blocked (BR-007) |
| priority | Enum | Yes | No | Yes | low, medium, high, critical (BR-008) |
| owner_id | UUID | Yes | No | Yes | Task creator/owner (BR-001) |
| assignee_id | UUID | No | No | Yes | Assigned team member (optional, BR-001) |
| team_id | UUID | No | No | Yes | Owning team (optional) |
| due_date | Date | No | No | Yes | Deadline (must not be in past, BR-006) |
| labels | Array(String) | No | No | No | Task tags |
| version | Integer | Yes | No | No | Optimistic lock counter |
| created_at | DateTime | Yes | No | Yes | Creation timestamp |
| updated_at | DateTime | Yes | No | Yes | Last update timestamp |
| created_by | UUID | Yes | No | No | Creator user ID |
| updated_by | UUID | No | No | No | Last modifier |
| archived_at | DateTime | No | No | Yes | Soft-delete marker (BR-003) |

**Business Rules:** BR-001, BR-003, BR-004, BR-006, BR-007, BR-008  
**Owner:** Task owner, Admins  
**Access:** Owner, assignee, team members, admins (role-scoped)  
**Audit:** All changes recorded to audit table  
**Retention:** Indefinite; soft-delete preserves audit trail  

---

### Comment Entity

| Field | Type | Required | Unique | Indexed | Description |
|-------|------|----------|--------|---------|-------------|
| comment_id | UUID | Yes | Yes | Yes | Primary identifier |
| task_id | UUID | Yes | No | Yes | Parent task |
| author_id | UUID | Yes | No | Yes | Comment creator |
| content | String(5000) | Yes | No | No | Comment text |
| created_at | DateTime | Yes | No | Yes | Creation timestamp |
| updated_at | DateTime | No | No | No | Last edit timestamp |
| edited_by | UUID | No | No | No | Editor user ID |
| created_by | String(36) | Yes | No | No | Audit creator |
| updated_by | String(36) | No | No | No | Audit updater |

**Owner:** Comment author, Admins  
**Access:** Task participants, admins  
**Audit:** Creation, edit, deletion logged  
**Retention:** Retained as part of task history  

---

### Notification Entity

| Field | Type | Required | Unique | Indexed | Description |
|-------|------|----------|--------|---------|-------------|
| notification_id | UUID | Yes | Yes | Yes | Primary identifier |
| recipient_id | UUID | Yes | No | Yes | Target user |
| event_type | String(50) | Yes | No | Yes | task_assigned, status_changed, comment_added, etc. |
| title | String(100) | Yes | No | No | Notification headline |
| message | String(500) | Yes | No | No | Notification body |
| task_id | UUID | No | No | Yes | Related task (optional) |
| actor_id | UUID | No | No | No | User who triggered event |
| delivery_channel | Enum | Yes | No | No | in_app, email, both |
| read_at | DateTime | No | No | No | Null until read |
| dismissed_at | DateTime | No | No | No | Null until dismissed |
| created_at | DateTime | Yes | No | Yes | Notification generation time |
| expires_at | DateTime | No | No | No | Auto-expire after 30 days |

**Owner:** Recipient user  
**Access:** Recipient only (admins can view logs)  
**Retention:** 30 days; auto-expire  
**Audit:** Delivery and read status logged  

---

### Audit Entity (Immutable, Append-Only)

| Field | Type | Required | Unique | Indexed | Description |
|-------|------|----------|--------|---------|-------------|
| audit_id | UUID | Yes | Yes | Yes | Primary identifier |
| entity_type | String(50) | Yes | No | Yes | user, task, team, comment, notification, settings |
| entity_id | UUID | Yes | No | Yes | Related entity ID |
| action | String(50) | Yes | No | Yes | created, updated, deleted, status_changed, etc. |
| actor_id | UUID | Yes | No | Yes | User who performed action |
| timestamp | DateTime | Yes | No | Yes | Action timestamp (immutable) |
| details | JSON | No | No | No | Field changes: {from, to} |
| ip_address | String(45) | No | No | No | Source IP (optional) |
| user_agent | String(500) | No | No | No | Browser info (optional) |
| success | Boolean | Yes | No | No | Action succeeded |
| error_message | String(500) | No | No | No | Error details if failed |

**Properties:** Immutable, append-only, never updated or deleted  
**Owner:** System  
**Access:** Admins only  
**Retention:** Indefinite (compliance requirement)  
**Audit:** N/A (audit table itself cannot be audited)  

---

### Team Membership Junction Entity

| Field | Type | Required | Unique | Indexed | Description |
|-------|------|----------|--------|---------|-------------|
| team_id | UUID | Yes | Yes (with user_id) | Yes | Team reference |
| user_id | UUID | Yes | Yes (with team_id) | Yes | User reference |
| role | Enum | Yes | No | No | TEAM_LEAD, TEAM_MEMBER |
| joined_at | DateTime | Yes | No | No | Membership creation |
| updated_at | DateTime | Yes | No | No | Role change timestamp |

**Constraints:** Composite PK (team_id, user_id); no duplicates  
**Owner:** Team owner, Admins  
**Access:** Visible to team members  

---

## Enumerated Values

### Task Status (BR-007)
```
todo           - Initial state, not yet started
in_progress    - Actively being worked
review         - Pending review before completion
completed      - Finished work
blocked        - Temporarily blocked, waiting for something
```

### Task Priority (BR-008)
```
low            - Non-urgent, backlog item
medium         - Normal priority (default)
high           - Important, prioritize over medium
critical       - Urgent, highest priority
```

### User Role
```
ADMIN          - Full system access
TEAM_LEAD      - Team manager, limited admin
TEAM_MEMBER    - Regular contributor
```

### Account Status
```
active         - Normal, can sign in
disabled       - Locked out, cannot sign in (soft-delete)
deleted        - Marked for deletion (soft-delete)
```

### Notification Event Type
```
task_assigned              - User assigned to task
task_status_changed        - Task status updated
task_archived              - Task archived
comment_added              - Comment added to task
mentioned_in_comment       - User mentioned in comment
task_due_today             - Reminder: task due today
task_overdue               - Alert: task overdue
```

### Notification Delivery Channel
```
in_app         - Display in UI (required)
email          - Send email (optional, preference-based)
both           - In-app and email
```

---

## Calculated/Derived Fields

### Dashboard Metrics

| Metric | Calculation | Owner | Usage |
|--------|-----------|-------|-------|
| Total Tasks | COUNT(tasks WHERE archived_at IS NULL AND scope matches user) | System | Dashboard summary |
| Completed Tasks | COUNT(tasks WHERE status='completed' AND archived_at IS NULL) | System | Dashboard summary |
| Pending Tasks | COUNT(tasks WHERE status != 'completed' AND archived_at IS NULL) | System | Dashboard summary |
| Overdue Tasks | COUNT(tasks WHERE due_date < TODAY AND status != 'completed' AND archived_at IS NULL) | System | Dashboard alert |
| Due Today Tasks | COUNT(tasks WHERE due_date = TODAY AND status != 'completed') | System | Dashboard focus |

---

## Data Constraints & Validation

### Email
- **Format:** RFC 5321 (alphanumeric + special chars @domain)
- **Length:** 1-254 characters
- **Uniqueness:** Globally unique across all users
- **Validation:** Server-side email format check; optional DNS MX lookup

### Password
- **Length:** 8-100 characters
- **Format:** Printable ASCII
- **Complexity:** No requirements (encourages passphrases)
- **History:** Cannot reuse last 3 passwords
- **Storage:** Never logged, only bcrypt hash stored

### Task Title
- **Length:** 1-100 characters
- **Format:** Any text characters allowed
- **Uniqueness:** NOT required (can duplicate titles)

### Due Date
- **Format:** ISO 8601 date (YYYY-MM-DD)
- **Constraint:** Must not be earlier than current date (BR-006)
- **Timezone:** Stored as UTC, converted for display

### Description
- **Max Length:** 2000 characters
- **Format:** Plain text + newlines
- **No HTML:** Tags stripped on save

---

## Data Ownership & Access Matrix

| Data | Owner | Read | Write | Delete | Audit |
|------|-------|------|-------|--------|-------|
| User Account | Self, Admins | Self, Admins | Self, Admins | Admins (soft) | All changes |
| Task | Owner, Admins | Owner, Assignee, Team, Admins | Owner, Assignee (status), Admins | Admins (soft) | All changes |
| Comment | Author, Admins | Task participants, Admins | Author, Admins | Author, Admins | All changes |
| Team | Owner, Admins | Members, Admins | Owner, Admins | Admins (soft) | All changes |
| Notification | Recipient, Admins | Recipient, Admins | System, Admins | Recipient, Admins | Delivery events |
| Settings | Self, Admins | Self, Admins | Self, Admins | N/A | All changes |
| Audit Log | System, Admins | Admins only | System only | System only (never) | Immutable |

---

## Data Quality Rules

### Completeness
- **Required fields:** Must be non-null per schema
- **Task title:** Required before save
- **User email:** Required and unique
- **Status:** Must be selected (default: todo)

### Consistency
- **Status transitions:** Must follow allowed state machine (BR-007)
- **Role assignments:** User role must be valid enum value
- **Team membership:** User and team must exist

### Accuracy
- **Due dates:** Enforced not in past (BR-006)
- **Priority values:** Must be from allowed set (BR-008)
- **Owner assignment:** User must exist and be active

### Timeliness
- **Timestamps:** Automatically set to server time (UTC)
- **Activity logs:** Recorded immediately on action
- **Audit trail:** Immutable, never overwritten

---

## Document Control

- **Document ID:** DATA-DICT-001
- **Version:** 1.0
- **Author:** Solution Architect
- **Status:** Ready for Database Developer Handoff
