"""Seed script to populate test data in the database."""

import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Add backend directory to path for imports
backend_dir = Path(__file__).parent.parent.parent.parent / "apps" / "backend"
sys.path.insert(0, str(backend_dir))

# Set UTF-8 encoding for stdout if on Windows
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from sqlalchemy.orm import Session
from src.db.database import Base, SessionLocal, engine
from src.models.models import (
    Comment,
    Task,
    TaskPriority,
    TaskStatus,
    Team,
    User,
    UserRole,
)
from src.utils.password import hash_password


def create_test_users(db: Session):
    """Create test users."""
    users = []

    test_users_data = [
        {
            "email": "alice@example.com",
            "password": "SecurePass123!",
            "full_name": "Alice Johnson",
            "role": UserRole.TEAM_LEAD,
            "contact_information": "alice@company.com",
        },
        {
            "email": "bob@example.com",
            "password": "SecurePass123!",
            "full_name": "Bob Smith",
            "role": UserRole.TEAM_MEMBER,
            "contact_information": "bob@company.com",
        },
        {
            "email": "charlie@example.com",
            "password": "SecurePass123!",
            "full_name": "Charlie Brown",
            "role": UserRole.TEAM_MEMBER,
            "contact_information": "charlie@company.com",
        },
        {
            "email": "diana@example.com",
            "password": "SecurePass123!",
            "full_name": "Diana Prince",
            "role": UserRole.ADMIN,
            "contact_information": "diana@company.com",
        },
    ]

    for user_data in test_users_data:
        user = User(
            email=user_data["email"],
            password_hash=hash_password(user_data["password"]),
            full_name=user_data["full_name"],
            role=user_data["role"],
            contact_information=user_data["contact_information"],
            theme="light",
            language="en",
            timezone="UTC",
            privacy="private",
            notifications_in_app=True,
            notifications_email=True,
        )
        db.add(user)
        users.append(user)

    db.commit()
    for user in users:
        db.refresh(user)

    return users


def create_test_teams(db: Session, users: list):
    """Create test teams and assign users."""
    teams = []

    team1 = Team(
        name="Engineering",
        description="Engineering team for product development",
    )
    team1.members = [users[0], users[1], users[2]]  # Alice, Bob, Charlie
    db.add(team1)
    teams.append(team1)

    team2 = Team(
        name="Design",
        description="Design team for UX/UI work",
    )
    team2.members = [users[0], users[2]]  # Alice, Charlie
    db.add(team2)
    teams.append(team2)

    db.commit()
    for team in teams:
        db.refresh(team)

    return teams


def create_test_tasks(db: Session, users: list, teams: list):
    """Create test tasks with various statuses and priorities."""
    tasks = []
    now = datetime.now(timezone.utc)

    task_data = [
        {
            "title": "Fix authentication bug",
            "description": "Users unable to log in on mobile devices",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.CRITICAL,
            "owner": users[0],  # Alice
            "assignee": users[1],  # Bob
            "team": teams[0],  # Engineering
            "due_date": now + timedelta(days=1),
        },
        {
            "title": "Design new dashboard layout",
            "description": "Create mockups for the updated dashboard",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "owner": users[0],  # Alice
            "assignee": users[2],  # Charlie
            "team": teams[1],  # Design
            "due_date": now + timedelta(days=5),
        },
        {
            "title": "Write API documentation",
            "description": "Document all REST API endpoints with examples",
            "status": TaskStatus.REVIEW,
            "priority": TaskPriority.MEDIUM,
            "owner": users[1],  # Bob
            "assignee": None,
            "team": teams[0],  # Engineering
            "due_date": now + timedelta(days=3),
        },
        {
            "title": "Implement comment feature",
            "description": "Add comment functionality to tasks with real-time updates",
            "status": TaskStatus.COMPLETED,
            "priority": TaskPriority.HIGH,
            "owner": users[1],  # Bob
            "assignee": users[1],  # Bob
            "team": teams[0],  # Engineering
            "due_date": now - timedelta(days=2),
        },
        {
            "title": "Setup CI/CD pipeline",
            "description": "Configure automated testing and deployment",
            "status": TaskStatus.BLOCKED,
            "priority": TaskPriority.HIGH,
            "owner": users[2],  # Charlie
            "assignee": None,
            "team": teams[0],  # Engineering
            "due_date": now + timedelta(days=7),
        },
    ]

    for data in task_data:
        task = Task(
            title=data["title"],
            description=data["description"],
            status=data["status"],
            priority=data["priority"],
            owner=data["owner"],
            assignee=data["assignee"],
            team=data["team"],
            due_date=data["due_date"],
        )
        db.add(task)
        tasks.append(task)

    db.commit()
    for task in tasks:
        db.refresh(task)

    return tasks


def create_test_comments(db: Session, users: list, tasks: list):
    """Create test comments on tasks."""
    comments = []
    now = datetime.now(timezone.utc)

    # Add comments to the first task
    comment1 = Comment(
        task=tasks[0],
        author=users[1],  # Bob
        content="I've started investigating this issue. It seems to be related to the OAuth token refresh on mobile.",
    )
    db.add(comment1)
    comments.append(comment1)

    comment2 = Comment(
        task=tasks[0],
        author=users[0],  # Alice
        content="Great! Let me know if you need any additional information from the backend team.",
    )
    db.add(comment2)
    comments.append(comment2)

    comment3 = Comment(
        task=tasks[0],
        author=users[1],  # Bob
        content="Found the issue - the token expiry check was not accounting for timezone differences.",
    )
    db.add(comment3)
    comments.append(comment3)

    # Add comments to the second task
    comment4 = Comment(
        task=tasks[1],
        author=users[2],  # Charlie
        content="I've created initial wireframes. Please review and provide feedback.",
    )
    db.add(comment4)
    comments.append(comment4)

    comment5 = Comment(
        task=tasks[1],
        author=users[0],  # Alice
        content="Looks good! The layout is clean and user-friendly.",
    )
    db.add(comment5)
    comments.append(comment5)

    # Add comments to the completed task
    comment6 = Comment(
        task=tasks[3],
        author=users[1],  # Bob
        content="Feature implemented and tested. All edge cases handled.",
    )
    db.add(comment6)
    comments.append(comment6)

    db.commit()
    for comment in comments:
        db.refresh(comment)

    return comments


def seed_database():
    """Main function to seed the database."""
    print("[*] Starting database seeding...")

    try:
        # Create all tables
        print("[>] Creating database tables...")
        Base.metadata.create_all(bind=engine)

        # Create session
        db = SessionLocal()

        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("[!] Database already contains data. Skipping seeding.")
            db.close()
            return

        # Create test data
        print("[>] Creating test users...")
        users = create_test_users(db)
        print(f"   Created {len(users)} users")

        print("[>] Creating test teams...")
        teams = create_test_teams(db, users)
        print(f"   Created {len(teams)} teams")

        print("[>] Creating test tasks...")
        tasks = create_test_tasks(db, users, teams)
        print(f"   Created {len(tasks)} tasks")

        print("[>] Creating test comments...")
        comments = create_test_comments(db, users, tasks)
        print(f"   Created {len(comments)} comments")

        db.close()

        print("\n[SUCCESS] Database seeding completed successfully!")
        print(f"\nTest Credentials:")
        print(
            f"  - Email: alice@example.com | Password: SecurePass123! | Role: TEAM_LEAD"
        )
        print(
            f"  - Email: bob@example.com | Password: SecurePass123! | Role: TEAM_MEMBER"
        )
        print(
            f"  - Email: charlie@example.com | Password: SecurePass123! | Role: TEAM_MEMBER"
        )
        print(f"  - Email: diana@example.com | Password: SecurePass123! | Role: ADMIN")

    except Exception as e:
        print(f"[ERROR] Error seeding database: {e}")
        raise


if __name__ == "__main__":
    seed_database()
