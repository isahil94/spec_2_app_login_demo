import importlib.util
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Load app module directly from file to avoid package import issues
main_path = Path(__file__).resolve().parents[1] / "apps" / "backend" / "main.py"
spec = importlib.util.spec_from_file_location("backend_main", str(main_path))
backend_main = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = backend_main
spec.loader.exec_module(backend_main)

client = TestClient(backend_main.app)

# Register user
r = client.post(
    "/api/v1/auth/register",
    json={
        "email": "qa@example.com",
        "password": "password123",
        "fullName": "QA Tester",
    },
)
print("register", r.status_code, r.json())

# Login
r = client.post(
    "/api/v1/auth/login", json={"email": "qa@example.com", "password": "password123"}
)
print("login", r.status_code, r.json())
if r.status_code != 200:
    raise SystemExit("login failed")

token = r.json()["data"]["token"]
headers = {"Authorization": f"Bearer {token}"}

# Create task
r = client.post(
    "/api/v1/tasks", json={"title": "QA Task", "description": "test"}, headers=headers
)
print("create task", r.status_code, r.json())
if r.status_code != 200:
    raise SystemExit("create task failed")

task_id = r.json()["data"]["task_id"]

# Add comment
r = client.post(
    f"/api/v1/tasks/{task_id}/comments",
    json={"content": "hello world"},
    headers=headers,
)
print("add comment", r.status_code, r.json())
if r.status_code != 200:
    raise SystemExit("add comment failed")

# Get task
r = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
print("get task", r.status_code)
print(r.json())

# Check comments
data = r.json().get("data", {})
if "comments" in data and len(data["comments"]) > 0:
    print("COMMENTS_PRESENT")
else:
    print("COMMENTS_MISSING")
