import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DB = ROOT / "task_management.db"
# Centralize DB under apps/data
TARGET_DIR = ROOT / "apps" / "data"
TARGET_DB = TARGET_DIR / "task_management.db"
SCHEMA_FILE = ROOT / "apps" / "database" / "sql" / "schema.sql"
SEED_FILE = ROOT / "apps" / "database" / "sql" / "seed" / "sample_seed.sql"

print("Root:", ROOT)
print("Source DB exists:", SOURCE_DB.exists())
print("Target dir:", TARGET_DIR)
TARGET_DIR.mkdir(parents=True, exist_ok=True)

# Prefer existing repo root task_management.db as a source for migration; canonical runtime DB is apps/data/task_management.db
if not SOURCE_DB.exists():
    alt = ROOT / "apps" / "backend" / "task_management.db"
    if alt.exists():
        SOURCE_DB = alt
        print("Using alternative source:", SOURCE_DB)

if not SOURCE_DB.exists():
    print("No source task_management.db found. Creating new target DB file.")
    # create empty DB
    conn = sqlite3.connect(str(TARGET_DB))
    conn.close()
else:
    shutil.copy2(SOURCE_DB, TARGET_DB)
    print(f"Copied {SOURCE_DB} -> {TARGET_DB}")

# Apply schema.sql to ensure missing tables are created
if SCHEMA_FILE.exists():
    schema = SCHEMA_FILE.read_text(encoding="utf-8")
    conn = sqlite3.connect(str(TARGET_DB))
    cur = conn.cursor()
    try:
        cur.executescript(schema)
        conn.commit()
        print("Applied schema.sql to target DB")
    except Exception as e:
        print("Error applying schema:", e)
    finally:
        conn.close()
else:
    print("schema.sql not found at", SCHEMA_FILE)

# Apply seed if present
if SEED_FILE.exists():
    seed = SEED_FILE.read_text(encoding="utf-8")
    conn = sqlite3.connect(str(TARGET_DB))
    try:
        conn.executescript(seed)
        conn.commit()
        print("Inserted sample seed data")
    except Exception as e:
        print("Error inserting seed:", e)
    finally:
        conn.close()
else:
    print("No seed file found at", SEED_FILE)

# Print resulting tables and counts for key tables
conn = sqlite3.connect(str(TARGET_DB))
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = [r[0] for r in cur.fetchall()]
print("Resulting tables:", tables)
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
    if t in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            cnt = cur.fetchone()[0]
        except Exception:
            cnt = "n/a"
        print(f" {t}: present, rows={cnt}")
    else:
        print(f" {t}: missing")
conn.close()

print(
    "\nMigration complete. Please review files and confirm before removing old DB copies."
)
