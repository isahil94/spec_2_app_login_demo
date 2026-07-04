import requests

url = 'http://127.0.0.1:8001/api/v1/auth/register'
payload = {'email':'test-qa@example.com','password':'Password123!','full_name':'QA Test'}
try:
    r = requests.post(url, json=payload, timeout=5)
    print('STATUS', r.status_code)
    print('TEXT', r.text)
except Exception as e:
    print('ERROR', e)
