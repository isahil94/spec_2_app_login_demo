import json
import urllib.request

base = "http://127.0.0.1:8001"


def request(path, method="GET", data=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data_bytes = None
    if data is not None:
        data_bytes = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        base + path, data=data_bytes, headers=headers, method=method
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.read().decode("utf-8"), r.getcode()
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8")
        except Exception:
            body = ""
        return body, e.code
    except Exception as e:
        return repr(e), 0


# Login (existing user created earlier)
login_payload = {"email": "qa+bot@example.com", "password": "Password123!"}
body, code = request("/api/v1/auth/login", method="POST", data=login_payload)
print("LOGIN", code, body)
try:
    token = json.loads(body)["data"]["token"]
except Exception:
    token = None

# Create a task
task_payload = {
    "title": "QA Test Task",
    "description": "Task for comment endpoint test",
}
body, code = request("/api/v1/tasks", method="POST", data=task_payload, token=token)
print("CREATE TASK", code, body)
try:
    task_id = json.loads(body)["data"]["task_id"]
except Exception:
    task_id = None

# Post a comment
if task_id:
    comment_payload = {"content": "This is a test comment from QA bot"}
    path = f"/api/v1/tasks/{task_id}/comments"
    body, code = request(path, method="POST", data=comment_payload, token=token)
    print("POST COMMENT", code, body)
else:
    print("No task_id; cannot post comment")
