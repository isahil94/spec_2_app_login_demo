from fastapi.testclient import TestClient

from apps.backend.db import Base, engine
from apps.backend.main import app

# Ensure tables exist for tests
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_create_and_get_project():
    payload = {"name": "Example Project", "description": "Test"}
    r = client.post("/projects", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Example Project"
    pid = data["id"]

    r2 = client.get(f"/projects/{pid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == pid
