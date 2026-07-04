import sqlite3
from pathlib import Path

DB_PATH = Path("apps/data/task_management.db")
SCHEMA_FILE = Path("apps/database/sql/schema.sql")
SEED_FILE = Path("apps/database/sql/seed/sample_seed.sql")

if not DB_PATH.exists():
    raise SystemExit(f"Database not found: {DB_PATH}")

conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()

# Get existing columns
cur.execute("PRAGMA table_info(users);")
existing = [r[1] for r in cur.fetchall()]
print("Existing user columns:", existing)

# Expected columns from schema
expected = {
    "contact_information": "TEXT",
    "avatar_url": "TEXT",
    "role": "TEXT",
    "account_status": "TEXT",
    "theme": "TEXT DEFAULT 'system'",
    "language": "TEXT DEFAULT 'en'",
    "timezone": "TEXT DEFAULT 'UTC'",
    "notify_in_app": "BOOLEAN DEFAULT 1",
    "notify_email": "BOOLEAN DEFAULT 0",
    "privacy_preferences": "JSON",
    "last_login_at": "DATETIME",
    "account_locked_until": "DATETIME",
    "created_by": "TEXT",
    "updated_by": "TEXT",
}

for col, coltype in expected.items():
    if col not in existing:
        sql = f"ALTER TABLE users ADD COLUMN {col} {coltype};"
        try:
            cur.execute(sql)
            print("Added column", col)
        except Exception as e:
            print("Error adding column", col, e)

conn.commit()

# Ensure notifications table has expected columns
cur.execute("PRAGMA table_info(notifications);")
notif_existing = [r[1] for r in cur.fetchall()]
print("Existing notifications columns:", notif_existing)
notif_expected = {
    "recipient_id": "TEXT",
    "actor_id": "TEXT",
    "event_type": "TEXT",
    "delivery_channel": "TEXT DEFAULT 'in_app'",
    "read_at": "DATETIME",
    "dismissed_at": "DATETIME",
    "expires_at": "DATETIME",
}
for col, coltype in notif_expected.items():
    if col not in notif_existing:
        try:
            cur.execute(f"ALTER TABLE notifications ADD COLUMN {col} {coltype};")
            print("Added notifications column", col)
        except Exception as e:
            print("Error adding notifications column", col, e)
conn.commit()

# Ensure audit_entries table has expected columns
cur.execute("PRAGMA table_info(audit_entries);")
audit_existing = [r[1] for r in cur.fetchall()]
print("Existing audit_entries columns:", audit_existing)
audit_expected = {
    "actor_id": "TEXT",
    "ip_address": "TEXT",
    "user_agent": "TEXT",
    "success": "BOOLEAN DEFAULT 1",
    "error_message": "TEXT",
}
for col, coltype in audit_expected.items():
    if col not in audit_existing:
        try:
            cur.execute(f"ALTER TABLE audit_entries ADD COLUMN {col} {coltype};")
            print("Added audit_entries column", col)
        except Exception as e:
            print("Error adding audit_entries column", col, e)
# After ensuring expected audit columns, add timestamp column if missing
if "timestamp" not in audit_existing:
    try:
        cur.execute("ALTER TABLE audit_entries ADD COLUMN timestamp DATETIME;")
        print("Added audit_entries column timestamp (no default)")
        try:
            cur.execute(
                "UPDATE audit_entries SET timestamp = created_at WHERE timestamp IS NULL;"
            )
            print("Backfilled audit_entries.timestamp from created_at")
        except Exception as e:
            print("Error backfilling timestamp:", e)
    except Exception as e:
        print("Error adding audit_entries column timestamp", e)
    conn.commit()

conn.commit()

# Ensure notification_preferences table has expected columns
cur.execute("PRAGMA table_info(notification_preferences);")
pref_existing = [r[1] for r in cur.fetchall()]
print("Existing notification_preferences columns:", pref_existing)
pref_expected = {
    "in_app_notifications": "BOOLEAN DEFAULT 1",
    "email_notifications": "BOOLEAN DEFAULT 0",
    "task_assigned": "BOOLEAN DEFAULT 1",
    "task_status_changed": "BOOLEAN DEFAULT 1",
    "comment_added": "BOOLEAN DEFAULT 1",
    "mentioned_in_comment": "BOOLEAN DEFAULT 1",
}
for col, coltype in pref_expected.items():
    if col not in pref_existing:
        try:
            cur.execute(
                f"ALTER TABLE notification_preferences ADD COLUMN {col} {coltype};"
            )
            print("Added notification_preferences column", col)
        except Exception as e:
            print("Error adding notification_preferences column", col, e)
conn.commit()

# Ensure teams table has expected columns
cur.execute("PRAGMA table_info(teams);")
teams_existing = [r[1] for r in cur.fetchall()]
print("Existing teams columns:", teams_existing)
teams_expected = {
    "owner_id": "TEXT",
    "archived_at": "DATETIME",
    "created_by": "TEXT",
    "updated_by": "TEXT",
}
for col, coltype in teams_expected.items():
    if col not in teams_existing:
        try:
            cur.execute(f"ALTER TABLE teams ADD COLUMN {col} {coltype};")
            print("Added teams column", col)
        except Exception as e:
            print("Error adding teams column", col, e)
conn.commit()

# Ensure tasks table has expected columns
cur.execute("PRAGMA table_info(tasks);")
tasks_existing = [r[1] for r in cur.fetchall()]
print("Existing tasks columns:", tasks_existing)
tasks_expected = {
    "version": "INTEGER DEFAULT 1",
    "created_by": "TEXT",
    "updated_by": "TEXT",
}
for col, coltype in tasks_expected.items():
    if col not in tasks_existing:
        try:
            cur.execute(f"ALTER TABLE tasks ADD COLUMN {col} {coltype};")
            print("Added tasks column", col)
        except Exception as e:
            print("Error adding tasks column", col, e)
conn.commit()

# Create missing tables by extracting from schema.sql
schema_text = SCHEMA_FILE.read_text(encoding="utf-8") if SCHEMA_FILE.exists() else ""
# Simple extraction: find CREATE TABLE ... for attachments, task_labels, team_membership
for tbl in ["attachments", "task_labels", "team_membership"]:
    if (
        tbl
        in cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        ).fetchall()[0]
    ):
        pass

# Instead, attempt to execute CREATE statements directly (idempotent with IF NOT EXISTS)
create_attachments = """
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
"""
create_task_labels = """
CREATE TABLE IF NOT EXISTS task_labels (
    task_id TEXT NOT NULL,
    label TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(task_id, label)
);
"""
create_team_membership = """
CREATE TABLE IF NOT EXISTS team_membership (
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,
    joined_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(team_id, user_id)
);
CREATE INDEX IF NOT EXISTS ix_team_membership_user_id ON team_membership(user_id);
"""

for stmt in (create_attachments, create_task_labels, create_team_membership):
    try:
        cur.executescript(stmt)
        print("Executed create stmt for chunk")
    except Exception as e:
        print("Error executing create stmt", e)

conn.commit()

# Re-run seed
if SEED_FILE.exists():
    seed = SEED_FILE.read_text(encoding="utf-8")
    try:
        conn.executescript(seed)
        print("Seed applied")
    except Exception as e:
        print("Error applying seed:", e)
else:
    print("Seed file not found")

# Print final table list
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
_tables = [r[0] for r in cur.fetchall()]
print("Tables now:", _tables)

for t in [
    "users",
    "teams",
    "tasks",
    "comments",
    "attachments",
    "notifications",
    "notification_preferences",
    "audit_entries",
    "team_membership",
    "team_members",
    "task_history",
    "task_labels",
]:
    if t in _tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            cnt = cur.fetchone()[0]
        except Exception:
            cnt = "n/a"
        print(f" {t}: present, rows={cnt}")
    else:
        print(f" {t}: missing")

conn.close()
