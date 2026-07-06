"""Remove seeded test rows inserted by the project's seed scripts.

Usage:
  .\.venv\Scripts\python.exe scripts\clear_seed_rows.py --dry-run
  .\.venv\Scripts\python.exe scripts\clear_seed_rows.py --confirm

Behavior:
- Connects to the project's database via the backend SessionLocal.
- Identifies seeded records based on known seed values (emails, team names, task titles).
- In --dry-run mode, prints counts per table that would be deleted.
- In --confirm mode, deletes rows in safe order and prints summary.

Notes:
- This targets only the canonical seed values used in `apps/backend/seed_data.py` and
  `artifacts/tests/test_scripts/seed_data.py` (emails, team names, task titles).
- If your tests generate other test data, adjust the filters accordingly.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import List

# Ensure backend src is importable
WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
# Ensure the backend package root is on sys.path so `import src...` works
sys.path.insert(0, str(WORKSPACE_ROOT / "apps" / "backend"))

from sqlalchemy import delete, func, select, text
from sqlalchemy.orm import Session
from src.db.database import SessionLocal, engine
from src.models.models import (
    AuditEntry,
    Comment,
    Notification,
    NotificationPreference,
    Task,
    Team,
    User,
    task_history,
    team_members,
)

# Known seed markers
SEED_USER_EMAILS = [
    "alice@example.com",
    "bob@example.com",
    "charlie@example.com",
    "diana@example.com",
]
SEED_TEAM_NAMES = ["Engineering", "Design"]
SEED_TASK_TITLES = [
    "Fix authentication bug",
    "Design new dashboard layout",
    "Write API documentation",
    "Implement comment feature",
    "Setup CI/CD pipeline",
]


def show_counts(session: Session) -> dict:
    """Return a dict of counts for matching rows."""
    counts = {}
    # Users
    counts["users"] = (
        session.query(User).filter(User.email.in_(SEED_USER_EMAILS)).count()
    )
    # Teams
    counts["teams"] = session.query(Team).filter(Team.name.in_(SEED_TEAM_NAMES)).count()
    # Tasks
    counts["tasks"] = (
        session.query(Task).filter(Task.title.in_(SEED_TASK_TITLES)).count()
    )
    # Comments authored by seeded users or on seeded tasks
    seeded_user_ids = [
        u.id for u in session.query(User).filter(User.email.in_(SEED_USER_EMAILS)).all()
    ]
    seeded_task_ids = [
        t.id for t in session.query(Task).filter(Task.title.in_(SEED_TASK_TITLES)).all()
    ]
    comments_by_user = 0
    comments_by_task = 0
    if seeded_user_ids:
        comments_by_user = (
            session.query(Comment)
            .filter(Comment.author_id.in_(seeded_user_ids))
            .count()
        )
    if seeded_task_ids:
        comments_by_task = (
            session.query(Comment).filter(Comment.task_id.in_(seeded_task_ids)).count()
        )
    counts["comments_by_user"] = comments_by_user
    counts["comments_by_task"] = comments_by_task
    # Notifications
    notifications_by_user = 0
    if seeded_user_ids:
        notifications_by_user = (
            session.query(Notification)
            .filter(Notification.user_id.in_(seeded_user_ids))
            .count()
        )
    counts["notifications_by_user"] = notifications_by_user
    # Notification preferences
    notification_prefs = 0
    if seeded_user_ids:
        notification_prefs = (
            session.query(NotificationPreference)
            .filter(NotificationPreference.user_id.in_(seeded_user_ids))
            .count()
        )
    counts["notification_preferences"] = notification_prefs
    # Audit entries
    audit_by_user = 0
    audit_by_task = 0
    if seeded_user_ids:
        audit_by_user = (
            session.query(AuditEntry)
            .filter(AuditEntry.user_id.in_(seeded_user_ids))
            .count()
        )
    if seeded_task_ids:
        audit_by_task = (
            session.query(AuditEntry)
            .filter(AuditEntry.task_id.in_(seeded_task_ids))
            .count()
        )
    counts["audit_by_user"] = audit_by_user
    counts["audit_by_task"] = audit_by_task
    # Task history (task_history table)
    history_by_task = 0
    history_by_actor = 0
    if seeded_task_ids:
        stmt = (
            select(func.count())
            .select_from(task_history)
            .where(task_history.c.task_id.in_(seeded_task_ids))
        )
        history_by_task = session.execute(stmt).scalar_one()
    if seeded_user_ids:
        stmt2 = (
            select(func.count())
            .select_from(task_history)
            .where(task_history.c.actor_id.in_(seeded_user_ids))
        )
        history_by_actor = session.execute(stmt2).scalar_one()
    counts["history_by_task"] = int(history_by_task or 0)
    counts["history_by_actor"] = int(history_by_actor or 0)

    return counts


def perform_deletes(session: Session) -> dict:
    """Delete matching seeded rows in correct order. Returns summary dict."""
    summary = {}
    # Resolve seeded users and tasks
    seeded_users = session.query(User).filter(User.email.in_(SEED_USER_EMAILS)).all()
    seeded_user_ids = [u.id for u in seeded_users]
    seeded_tasks = session.query(Task).filter(Task.title.in_(SEED_TASK_TITLES)).all()
    seeded_task_ids = [t.id for t in seeded_tasks]

    # Delete notifications referencing seeded users or seeded tasks
    notif_q = session.query(Notification).filter(
        (Notification.user_id.in_(seeded_user_ids))
        | (Notification.task_id.in_(seeded_task_ids))
    )
    summary["notifications_deleted"] = notif_q.count()
    if summary["notifications_deleted"]:
        notif_q.delete(synchronize_session=False)

    # Delete notification preferences for seeded users
    prefs_q = session.query(NotificationPreference).filter(
        NotificationPreference.user_id.in_(seeded_user_ids)
    )
    summary["notification_prefs_deleted"] = prefs_q.count()
    if summary["notification_prefs_deleted"]:
        prefs_q.delete(synchronize_session=False)

    # Delete audit entries referencing seeded users or seeded tasks
    audit_q = session.query(AuditEntry).filter(
        (AuditEntry.user_id.in_(seeded_user_ids))
        | (AuditEntry.task_id.in_(seeded_task_ids))
    )
    summary["audit_deleted"] = audit_q.count()
    if summary["audit_deleted"]:
        audit_q.delete(synchronize_session=False)

    # Delete task_history entries
    if seeded_task_ids or seeded_user_ids:
        # Delete by task_id then by actor_id using SQLAlchemy delete()
        if seeded_task_ids:
            session.execute(
                delete(task_history).where(task_history.c.task_id.in_(seeded_task_ids))
            )
        if seeded_user_ids:
            session.execute(
                delete(task_history).where(task_history.c.actor_id.in_(seeded_user_ids))
            )
        # We don't have reliable row counts easily here; rely on counts shown earlier
        summary["task_history_deleted"] = "see counts"

    # Delete comments by seeded users or on seeded tasks
    comments_q = session.query(Comment).filter(
        (Comment.author_id.in_(seeded_user_ids))
        | (Comment.task_id.in_(seeded_task_ids))
    )
    summary["comments_deleted"] = comments_q.count()
    if summary["comments_deleted"]:
        comments_q.delete(synchronize_session=False)

    # Delete tasks (will cascade comments & audit_entries if configured)
    tasks_q = session.query(Task).filter(Task.title.in_(SEED_TASK_TITLES))
    summary["tasks_deleted"] = tasks_q.count()
    if summary["tasks_deleted"]:
        tasks_q.delete(synchronize_session=False)

    # Remove entries in association table team_members for seeded users or seeded teams
    if seeded_user_ids or seeded_task_ids:
        # Delete team_members for seeded users
        if seeded_user_ids:
            session.execute(
                delete(team_members).where(team_members.c.user_id.in_(seeded_user_ids))
            )
        # Delete team_members for seeded teams (by team name lookup)
        if seeded_user_ids:
            pass

    # Delete teams
    teams_q = session.query(Team).filter(Team.name.in_(SEED_TEAM_NAMES))
    summary["teams_deleted"] = teams_q.count()
    if summary["teams_deleted"]:
        teams_q.delete(synchronize_session=False)

    # Delete users
    users_q = session.query(User).filter(User.email.in_(SEED_USER_EMAILS))
    summary["users_deleted"] = users_q.count()
    if summary["users_deleted"]:
        users_q.delete(synchronize_session=False)

    session.commit()
    return summary


def main(dry_run: bool = True):
    session = SessionLocal()
    try:
        counts = show_counts(session)
        print("Counts for seeded items:")
        for k, v in counts.items():
            print(f" - {k}: {v}")

        if dry_run:
            print(
                "\nDry-run mode: no deletions performed. Run with --confirm to delete these rows."
            )
            return 0

        # Confirm
        print("\nDeleting seeded rows...")
        summary = perform_deletes(session)
        print("Deletion summary:")
        for k, v in summary.items():
            print(f" - {k}: {v}")
        return 0
    finally:
        session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clear seeded test rows from DB")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be deleted"
    )
    parser.add_argument("--confirm", action="store_true", help="Perform deletions")
    args = parser.parse_args()
    if args.confirm and args.dry_run:
        print("Use either --dry-run or --confirm, not both")
        raise SystemExit(2)
    rc = main(dry_run=not args.confirm)
    raise SystemExit(rc)
