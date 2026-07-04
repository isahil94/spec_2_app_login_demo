from datetime import datetime, timezone

from src.schemas.schemas import TaskCreate, TaskUpdate


def test_task_create_accepts_camel_case_due_date_alias():
    payload = TaskCreate(title="Ship onboarding", dueDate="2026-07-10T12:00:00Z")

    assert payload.due_date is not None
    assert payload.due_date == datetime(2026, 7, 10, 12, 0, tzinfo=timezone.utc)


def test_task_update_accepts_camel_case_due_date_alias():
    payload = TaskUpdate(dueDate="2026-07-11T09:30:00Z")

    assert payload.due_date is not None
    assert payload.due_date == datetime(2026, 7, 11, 9, 30, tzinfo=timezone.utc)


def test_task_update_accepts_date_only_due_date_alias():
    payload = TaskUpdate(dueDate="2026-07-11")

    assert payload.due_date is not None
    assert payload.due_date == datetime(
        2026, 7, 11, 23, 59, 59, 999999, tzinfo=timezone.utc
    )
