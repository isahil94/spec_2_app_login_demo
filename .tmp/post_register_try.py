import requests

url = "http://127.0.0.1:8001/api/v1/auth/register"

payload1 = {
    "email": "vss465-test1@example.com",
    "password": "Password123!",
    "full_name": "VSS465 Test1",
}
payload2 = {
    "email": "vss465-test2@example.com",
    "password": "Password123!",
    "fullName": "VSS465 Test2",
}

for i, payload in enumerate((payload1, payload2), start=1):
    try:
        r = requests.post(url, json=payload, timeout=5)
        print(f"Attempt {i}: status={r.status_code}")
        print(r.text)
    except Exception as e:
        print(f"Attempt {i} error: {e}")
