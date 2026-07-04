@echo off
REM Integration Testing Setup Script for Windows
REM This script checks prerequisites and runs integration tests

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo Integration Testing Setup ^& Execution
echo ============================================================
echo.

REM Colors not supported in batch, so using text
echo [INFO] Checking prerequisites...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    exit /b 1
)

REM Check if backend is running
echo [INFO] Checking if backend is running on http://localhost:8001...
python -c "import requests; requests.get('http://localhost:8001/health', timeout=2)" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Backend is not responding. Please start it first.
    echo.
    echo Start the backend with:
    echo   cd apps\backend
    echo   .\..\..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8001
    exit /b 1
)
echo [SUCCESS] Backend is running

REM Check if database exists
if exist "apps\data\task_management.db" (
    echo [SUCCESS] Database exists
) else (
    echo [WARNING] Database does not exist yet (will be created on backend startup)
)

REM Check if we should seed the database
echo [INFO] Checking if database needs seeding...
python -c "
import sqlite3
from pathlib import Path
db_path = Path('apps/data/task_management.db')
if db_path.exists():
    try:
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        user_count = cur.fetchone()[0]
        conn.close()
        if user_count == 0:
            print('EMPTY')
        else:
            print('HAS_DATA')
    except:
        print('ERROR')
else:
    print('NO_DB')
" > db_status.txt
set /p DB_STATUS=<db_status.txt
del db_status.txt

if "%DB_STATUS%"=="EMPTY" (
    echo [WARNING] Database is empty. Seeding with test data...
    cd apps\backend
    python seed_data.py
    cd ..\..
) else if "%DB_STATUS%"=="HAS_DATA" (
    echo [SUCCESS] Database already contains test data
) else (
    echo [WARNING] Could not determine database state, skipping seeding
)

REM Check if frontend dependencies are installed
echo [INFO] Checking frontend dependencies...
if not exist "apps\frontend\node_modules" (
    echo [WARNING] Frontend dependencies not installed
    echo [INFO] Installing frontend dependencies...
    cd apps\frontend
    call npm install
    cd ..\..
)
echo [SUCCESS] Frontend dependencies are installed

REM Run the integration tests
echo.
echo ============================================================
echo Running Integration Tests
echo ============================================================
echo.

cd apps\frontend
call npm test -- persistence-integration.spec.ts
set TEST_RESULT=%errorlevel%

REM Summary
echo.
echo ============================================================
if %TEST_RESULT% equ 0 (
    echo [SUCCESS] Integration testing completed successfully!
) else (
    echo [ERROR] Integration testing had failures
)
echo ============================================================
echo.

exit /b %TEST_RESULT%
