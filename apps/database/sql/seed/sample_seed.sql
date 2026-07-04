PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

INSERT OR IGNORE INTO users (id, email, password_hash, full_name, role, account_status, theme, language, timezone, notify_in_app, notify_email, created_by, created_at, updated_at)
VALUES
('user-1-uuid', 'admin@example.com', 'hashed-password', 'Admin User', 'ADMIN', 'active', 'system', 'en', 'UTC', 1, 0, 'user-1-uuid', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user-2-uuid', 'lead@example.com', 'hashed-password', 'Team Lead', 'TEAM_LEAD', 'active', 'system', 'en', 'UTC', 1, 0, 'user-1-uuid', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user-3-uuid', 'member@example.com', 'hashed-password', 'Team Member', 'TEAM_MEMBER', 'active', 'system', 'en', 'UTC', 1, 0, 'user-1-uuid', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT OR IGNORE INTO teams (id, name, description, owner_id, created_by, created_at, updated_at)
VALUES
('team-1-uuid', 'Engineering', 'Engineering team', 'user-2-uuid', 'user-2-uuid', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT OR IGNORE INTO team_membership (team_id, user_id, role, joined_at, updated_at)
VALUES
('team-1-uuid', 'user-2-uuid', 'TEAM_LEAD', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('team-1-uuid', 'user-3-uuid', 'TEAM_MEMBER', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT OR IGNORE INTO tasks (id, title, description, status, priority, owner_id, assignee_id, team_id, due_date, version, created_by, updated_by, created_at, updated_at)
VALUES
('task-1-uuid', 'Set up project onboarding', 'Create the initial onboarding workflow for the new task system.', 'todo', 'high', 'user-2-uuid', 'user-3-uuid', 'team-1-uuid', DATE('now', '+7 days'), 1, 'user-2-uuid', 'user-2-uuid', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT OR IGNORE INTO task_labels (task_id, label, created_at)
VALUES
('task-1-uuid', 'onboarding', CURRENT_TIMESTAMP),
('task-1-uuid', 'urgent', CURRENT_TIMESTAMP);

INSERT OR IGNORE INTO comments (id, task_id, author_id, content, created_at)
VALUES
('comment-1-uuid', 'task-1-uuid', 'user-3-uuid', 'Please include the team checklist in the task details.', CURRENT_TIMESTAMP);

INSERT OR IGNORE INTO notifications (id, recipient_id, task_id, actor_id, event_type, title, message, delivery_channel, created_at)
VALUES
('notification-1-uuid', 'user-3-uuid', 'task-1-uuid', 'user-2-uuid', 'task_assigned', 'Task assigned', 'You have been assigned a task.', 'in_app', CURRENT_TIMESTAMP);

INSERT OR IGNORE INTO notification_preferences (id, user_id, in_app_notifications, email_notifications, task_assigned, task_status_changed, comment_added, mentioned_in_comment, created_at, updated_at)
VALUES
('pref-1-uuid', 'user-1-uuid', 1, 0, 1, 1, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('pref-2-uuid', 'user-2-uuid', 1, 0, 1, 1, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('pref-3-uuid', 'user-3-uuid', 1, 0, 1, 1, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT OR IGNORE INTO audit_entries (id, entity_type, entity_id, task_id, action, actor_id, details, success, timestamp)
VALUES
('audit-1-uuid', 'task', 'task-1-uuid', 'task-1-uuid', 'created', 'user-2-uuid', '{"status":"todo","priority":"high"}', 1, CURRENT_TIMESTAMP);

COMMIT;
PRAGMA foreign_keys = ON;
