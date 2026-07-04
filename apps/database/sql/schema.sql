-- Schema for Task Management System
-- Compatible with SQLite development and PostgreSQL production

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    contact_information TEXT,
    avatar_url TEXT,
    role TEXT NOT NULL,
    account_status TEXT NOT NULL,
    theme TEXT NOT NULL DEFAULT 'system',
    language TEXT NOT NULL DEFAULT 'en',
    timezone TEXT NOT NULL DEFAULT 'UTC',
    notify_in_app BOOLEAN NOT NULL DEFAULT 1,
    notify_email BOOLEAN NOT NULL DEFAULT 0,
    privacy_preferences JSON,
    last_login_at DATETIME,
    account_locked_until DATETIME,
    created_by TEXT NOT NULL,
    updated_by TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);
CREATE INDEX IF NOT EXISTS ix_users_role ON users(role);
CREATE INDEX IF NOT EXISTS ix_users_account_status ON users(account_status);

CREATE TABLE IF NOT EXISTS teams (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    owner_id TEXT NOT NULL,
    archived_at DATETIME,
    created_by TEXT NOT NULL,
    updated_by TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_teams_owner_id ON teams(owner_id);
CREATE UNIQUE INDEX IF NOT EXISTS ux_teams_name_owner ON teams(owner_id, name);

CREATE TABLE IF NOT EXISTS team_membership (
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,
    joined_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(team_id, user_id)
);

CREATE INDEX IF NOT EXISTS ix_team_membership_user_id ON team_membership(user_id);

CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    priority TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    assignee_id TEXT,
    team_id TEXT,
    due_date DATE,
    version INTEGER NOT NULL DEFAULT 1,
    archived_at DATETIME,
    created_by TEXT NOT NULL,
    updated_by TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_tasks_owner_id ON tasks(owner_id);
CREATE INDEX IF NOT EXISTS ix_tasks_assignee_id ON tasks(assignee_id);
CREATE INDEX IF NOT EXISTS ix_tasks_team_id ON tasks(team_id);
CREATE INDEX IF NOT EXISTS ix_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS ix_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS ix_tasks_due_date ON tasks(due_date);
CREATE INDEX IF NOT EXISTS ix_tasks_archived_at ON tasks(archived_at);

CREATE TABLE IF NOT EXISTS task_labels (
    task_id TEXT NOT NULL,
    label TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(task_id, label)
);

CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    author_id TEXT NOT NULL,
    content TEXT NOT NULL,
    edit_history JSON,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    edited_by TEXT
);

CREATE INDEX IF NOT EXISTS ix_comments_task_id ON comments(task_id);
CREATE INDEX IF NOT EXISTS ix_comments_author_id ON comments(author_id);

CREATE TABLE IF NOT EXISTS attachments (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    uploader_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_url TEXT NOT NULL,
    mime_type TEXT,
    file_size INTEGER,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_attachments_task_id ON attachments(task_id);
CREATE INDEX IF NOT EXISTS ix_attachments_uploader_id ON attachments(uploader_id);

CREATE TABLE IF NOT EXISTS notifications (
    id TEXT PRIMARY KEY,
    recipient_id TEXT NOT NULL,
    task_id TEXT,
    actor_id TEXT,
    event_type TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    delivery_channel TEXT NOT NULL DEFAULT 'in_app',
    read_at DATETIME,
    dismissed_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME
);

CREATE INDEX IF NOT EXISTS ix_notifications_recipient_id ON notifications(recipient_id);
CREATE INDEX IF NOT EXISTS ix_notifications_task_id ON notifications(task_id);
CREATE INDEX IF NOT EXISTS ix_notifications_event_type ON notifications(event_type);

CREATE TABLE IF NOT EXISTS notification_preferences (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    in_app_notifications BOOLEAN NOT NULL DEFAULT 1,
    email_notifications BOOLEAN NOT NULL DEFAULT 0,
    task_assigned BOOLEAN NOT NULL DEFAULT 1,
    task_status_changed BOOLEAN NOT NULL DEFAULT 1,
    comment_added BOOLEAN NOT NULL DEFAULT 1,
    mentioned_in_comment BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_notification_preferences_user_id ON notification_preferences(user_id);

CREATE TABLE IF NOT EXISTS audit_entries (
    id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    task_id TEXT,
    action TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    details JSON,
    ip_address TEXT,
    user_agent TEXT,
    success BOOLEAN NOT NULL DEFAULT 1,
    error_message TEXT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_audit_entries_entity_type ON audit_entries(entity_type);
CREATE INDEX IF NOT EXISTS ix_audit_entries_entity_id ON audit_entries(entity_id);
CREATE INDEX IF NOT EXISTS ix_audit_entries_task_id ON audit_entries(task_id);
CREATE INDEX IF NOT EXISTS ix_audit_entries_actor_id ON audit_entries(actor_id);
CREATE INDEX IF NOT EXISTS ix_audit_entries_timestamp ON audit_entries(timestamp);

-- Foreign key constraints are added through the application layer for SQLite and enforced in PostgreSQL.
