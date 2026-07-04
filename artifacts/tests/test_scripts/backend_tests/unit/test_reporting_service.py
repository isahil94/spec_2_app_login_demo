from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import Base
from src.models.models import Task, TaskStatus, User
from src.services.collaboration_service import ReportingService


def test_get_dashboard_metrics_handles_naive_and_aware_due_dates():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    user = User(
        email="reporter@example.com", password_hash="secret", full_name="Reporter"
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    now = datetime.now(timezone.utc)
    today = now.replace(hour=12, minute=0, second=0, microsecond=0)
    naive_due = datetime(now.year, now.month, now.day, 23, 59, 59)
    aware_due = datetime(
        now.year, now.month, now.day + 1, 23, 59, 59, tzinfo=timezone.utc
    )

    task_naive = Task(
        title="Naive Due Date Task",
        owner_id=user.id,
        due_date=naive_due,
        status=TaskStatus.TODO,
    )
    task_aware = Task(
        title="Aware Due Date Task",
        owner_id=user.id,
        due_date=aware_due,
        status=TaskStatus.TODO,
    )
    completed_task = Task(
        title="Completed Task",
        owner_id=user.id,
        due_date=now - timedelta(days=1),
        status=TaskStatus.COMPLETED,
    )

    session.add_all([task_naive, task_aware, completed_task])
    session.commit()

    service = ReportingService(session)
    metrics = service.get_dashboard_metrics(user.id)

    assert metrics["total_tasks"] == 3
    assert metrics["pending_tasks"] == 2
    assert metrics["completed_tasks"] == 1
    assert metrics["overdue_tasks"] == 0
    assert metrics["due_today_tasks"] == 1
    assert any(
        item["title"] == "Aware Due Date Task" for item in metrics["upcoming_deadlines"]
    )
