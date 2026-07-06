"""Clear test data from the project's database.

Behavior:
- Reads DATABASE_URL from environment or from apps.backend.src.config.settings.Settings
- If SQLite file-based DB, creates a timestamped backup copy and removes the DB file and related journal/shm/wal files.
- If in-memory SQLite: reports nothing to do.
- If non-SQLite: prints a warning and exits (to avoid accidental data loss).

Run from repository root:
    .\.venv\Scripts\python.exe scripts\clear_test_data.py
"""

import os
import shutil
import time
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]


def get_database_url():
    env_db = os.environ.get("DATABASE_URL")
    if env_db:
        return env_db
    # try import settings
    try:
        import sys

        sys.path.insert(0, str(WORKSPACE_ROOT / "apps" / "backend" / "src"))
        from config.settings import settings

        return settings.DATABASE_URL
    except Exception:
        return None


def resolve_sqlite_path(db_url: str) -> Path:
    # db_url like sqlite:///apps/data/task_management.db
    assert db_url.startswith("sqlite"), "Not an sqlite url"
    # in-memory sqlite URLs contain ':memory:'; caller handles that case
    if db_url.endswith(":memory:"):
        return None
    sqlite_path = db_url.replace("sqlite:///", "")
    p = Path(sqlite_path)
    if not p.is_absolute():
        p = WORKSPACE_ROOT / sqlite_path
    return p.resolve()


def backup_and_remove(path: Path):
    ts = time.strftime("%Y%m%d%H%M%S")
    backup = path.parent / f"{path.name}.bak.{ts}"
    print(f"Backing up {path} -> {backup}")
    shutil.copy2(path, backup)
    # also copy WAL/SHM if present
    for ext in ["-wal", "-shm", "-journal"]:
        other = Path(str(path) + ext)
        if other.exists():
            shutil.copy2(other, Path(str(other) + f".bak.{ts}"))
    # remove files
    print(f"Removing {path} and related journal files")
    for p in [
        path,
        Path(str(path) + "-wal"),
        Path(str(path) + "-shm"),
        Path(str(path) + "-journal"),
    ]:
        try:
            if p.exists():
                p.unlink()
        except Exception as e:
            print(f"Warning: could not remove {p}: {e}")


if __name__ == "__main__":
    db_url = get_database_url()
    if not db_url:
        print("DATABASE_URL not found in environment or settings; aborting.")
        raise SystemExit(1)
    print(f"Resolved DATABASE_URL={db_url}")
    if db_url.startswith("sqlite"):
        if ":memory:" in db_url:
            print("Database is in-memory SQLite; nothing to remove.")
            raise SystemExit(0)
        db_path = resolve_sqlite_path(db_url)
        if not db_path or not db_path.exists():
            print(f"SQLite DB file not found at {db_path}; nothing to remove.")
            raise SystemExit(0)
        # backup and remove
        backup_and_remove(db_path)
        # verify
        if not db_path.exists():
            print("Database file removed.")
            # list files in apps/data
            data_dir = db_path.parent
            print("Remaining files in data dir:")
            for f in sorted(data_dir.iterdir()):
                print(" -", f.name)
            raise SystemExit(0)
        else:
            print("Failed to remove database file.")
            raise SystemExit(2)
    else:
        print(
            "Non-SQLite DATABASE_URL detected. To avoid accidental data loss, this script only handles SQLite file databases."
        )
        raise SystemExit(1)
