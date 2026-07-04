import json
import urllib.request

base = "http://127.0.0.1:8001"


def post(path, data):
    req = urllib.request.Request(
        base + path,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return r.read().decode("utf-8"), r.getcode()


try:
    reg_payload = {
        "email": "qa+bot@example.com",
        "password": "Password123!",
        "fullName": "QA Bot",
    }
    body, code = post("/api/v1/auth/register", reg_payload)
    print("REGISTER", code, body)
except Exception as e:
    print("REGISTER ERROR", repr(e))

try:
    login_payload = {"email": "qa+bot@example.com", "password": "Password123!"}
    body, code = post("/api/v1/auth/login", login_payload)
    print("LOGIN", code, body)
    data = json.loads(body)
    token = data.get("data", {}).get("token")
    print("TOKEN:", token)
except Exception as e:
    print("LOGIN ERROR", repr(e))
