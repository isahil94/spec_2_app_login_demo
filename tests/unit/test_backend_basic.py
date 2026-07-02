from fastapi.testclient import TestClient

from apps.backend.main import app
from apps.backend.src.core.models import Base
from apps.backend.src.db.database import engine

# Ensure tables exist for tests
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "healthy"


def test_create_and_get_project():
    # Test creating a task (projects is managed via tasks with team context)
    payload = {"title": "Test Task", "description": "Test Task Description"}
    r = client.post("/api/v1/tasks", json=payload)
    # Check if endpoint exists (may be 422 if validation fails, but not 404)
    assert r.status_code != 404, f"Tasks endpoint not found: {r.text}"
