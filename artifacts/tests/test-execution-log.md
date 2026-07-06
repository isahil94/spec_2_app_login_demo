# Test Execution Log

## Metadata
- Workflow ID: WF-1783340956452
- Correlation ID: WF-1783340956452
- Stage: QA
- Date: 2026-07-06
- Status: BLOCKED

## Commands Executed

### 1. Backend unit tests
Command:
```powershell
.\.venv\Scripts\python.exe -m pytest apps/backend/tests -v --tb=short
```
Observed output:
```text
============================= test session starts ==============================
platform win32 -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0 -- F:\Projects\Specs_to_APP- mini\.venv\Scripts\python.exe
collected 1 item

apps/backend/tests/test_user_repository.py::test_get_active_users_returns_only_active_users PASSED [100%]

============================== 1 passed in 0.13s ==============================
```

### 2. Backend startup
Command:
```powershell
Set-Location 'f:\Projects\Specs_to_APP- mini\apps\backend'; $env:PYTHONPATH='f:\Projects\Specs_to_APP- mini\apps\backend'; & 'f:\Projects\Specs_to_APP- mini\.venv\Scripts\python.exe' -m uvicorn main:app --host 127.0.0.1 --port 8000
```
Observed output:
```text
INFO:     Started server process [5384]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 3. Backend health check
Command:
```powershell
curl.exe -i http://127.0.0.1:8000/health
```
Observed output:
```text
HTTP/1.1 200 OK
content-type: application/json

{"status":"healthy","timestamp":"2026-07-06T12:39:57.034785+00:00"}
```

### 4. Registration API request
Command:
```powershell
$headers = @{ 'Content-Type' = 'application/json' }; $body = @{ email='qa.user@example.com'; password='StrongPass123!'; fullName='QA User' } | ConvertTo-Json; try { $response = Invoke-WebRequest -Method Post -Uri 'http://127.0.0.1:8000/api/v1/auth/register' -Headers $headers -Body $body -UseBasicParsing; Write-Host "STATUS:$($response.StatusCode)"; Write-Host $response.Content } catch { Write-Host "STATUS:$($_.Exception.Response.StatusCode.value__)"; $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream()); Write-Host $reader.ReadToEnd() }
```
Observed output:
```text
STATUS:500
```

### 5. Backend exception trace
Observed backend error excerpt:
```text
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: users.is_active
```

### 6. Frontend build
Command:
```powershell
cd 'f:\Projects\Specs_to_APP- mini\apps\frontend' ; npm run build
```
Observed output:
```text
> task-management-frontend@0.1.0 build
> tsc --noEmit && vite build

vite v5.4.21 building for production...
✓ built in 1.89s
```

### 7. Frontend startup
Command:
```powershell
cd 'f:\Projects\Specs_to_APP- mini\apps\frontend' ; npm run dev -- --host 127.0.0.1 --port 5173
```
Observed output:
```text
VITE v5.4.21 ready in 354 ms
Local: http://127.0.0.1:5173/
```

### 8. Frontend availability check
Command:
```powershell
curl.exe -I http://127.0.0.1:5173/
```
Observed output:
```text
HTTP/1.1 200 OK
Content-Type: text/html
```

## Conclusions
- Backend health endpoint works.
- One unit test passed.
- Registration flow is reproducibly failing with HTTP 500 and a database schema error.
- Frontend serves successfully over HTTP.
