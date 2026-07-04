# Test Scripts & Execution Guide

This directory contains all test execution scripts and documentation for the Task Management System QA framework.

## 📂 Directory Structure

```
test_scripts/
├── run-all-tests.py                    # Master test runner (all tests)
├── run-integration-tests.py            # Integration/persistence E2E tests (Python)
├── run-integration-tests.bat           # Windows batch runner
├── run-integration-tests.sh            # Unix/Mac bash runner
├── README.md                           # This file
├── ../seed_data_examples.md           # Test data generation examples
├── ../../api-documentation.md         # API reference for tests
└── ../../integration-testing-guide.md # Detailed testing guide
```

## 🚀 Quick Start

### Run All Tests

**Windows:**
```powershell
cd artifacts/tests/test_scripts
python run-all-tests.py --all
```

**Mac/Linux:**
```bash
cd artifacts/tests/test_scripts
python3 run-all-tests.py --all
```

### Run Specific Test Types

**Backend Unit Tests Only:**
```bash
python run-all-tests.py --unit
```

**Persistence E2E Tests Only:**
```bash
python run-all-tests.py --persistence
```

**Frontend E2E Tests Only:**
```bash
python run-all-tests.py --frontend
```

## 🧪 Test Types & Coverage

### 1. Backend Unit Tests
**Location:** `artifacts/tests/test_scripts/backend_tests/unit/`  
**Files:**
- `test_auth_service.py` - Authentication service tests
- `test_admin_endpoints.py` - Admin endpoint tests
- `test_reporting_service.py` - Dashboard metrics tests
- `test_task_schema_aliases.py` - Task schema validation tests

**Coverage:**
- ✅ User registration and login
- ✅ Password validation
- ✅ Admin operations
- ✅ Schema validation
- ✅ Database constraints

**Run:**
```bash
python run-all-tests.py --unit
```

### 2. Persistence E2E Tests (Database Integration)
**Location:** `artifacts/tests/test_scripts/tests/persistence-integration.spec.ts`  
**Test Count:** 8 critical tests

**What It Tests:**
- ✅ Task creation and database persistence
- ✅ Comment addition and retrieval
- ✅ Multiple comments ordering
- ✅ Task status updates
- ✅ Task history tracking
- ✅ Multi-step workflows
- ✅ Comment edits
- ✅ Complete user journeys

**Run:**
```bash
python run-integration-tests.py      # Auto setup & run
# OR
npm test -- persistence-integration.spec.ts  # Direct from apps/frontend
```

### 3. Frontend E2E Tests (UI Behavior)
**Location:** `artifacts/tests/test_scripts/tests/*.spec.ts`  
**Test Files:** 12 test suites, ~120 tests

**Coverage:**
- ✅ Authentication flows (auth.spec.ts - 7 tests)
- ✅ Task management (tasks.spec.ts - 21 tests)
- ✅ Comments (comments.spec.ts - 10 tests)
- ✅ Comment history (comments-history.spec.ts - 4 tests)
- ✅ User profiles (profile-settings.spec.ts - 26 tests)
- ✅ Dashboard metrics (dashboard.spec.ts - 6 tests)
- ✅ Teams and history (team-and-history.spec.ts - 4 tests)
- ✅ Admin management (admin-management.spec.ts - 3 tests)
- ✅ Session management (session-landing.spec.ts - 5 tests)
- ✅ Error handling (dependency-unavailable.spec.ts - 3 tests)
- ✅ Integration workflows (integration.spec.ts - 3 tests)
- ✅ And more...

**Run:**
```bash
cd apps/frontend
npm test                              # All tests
npm test -- <test-file>.spec.ts      # Specific test
```

## 🔧 Individual Test Runners

### Windows Batch Runner
For persistence/integration tests only.

```bash
cd artifacts/tests/test_scripts
run-integration-tests.bat
```

**What it does:**
1. Checks Python availability
2. Verifies backend is running
3. Checks database status
4. Automatically seeds database if empty
5. Installs frontend dependencies if needed
6. Runs persistence E2E tests

### Unix/Mac Bash Runner
For persistence/integration tests only.

```bash
cd artifacts/tests/test_scripts
bash run-integration-tests.sh
```

**Features:** Same as batch runner but for Unix systems.

### Python Setup Script
Generic cross-platform runner.

```bash
cd artifacts/tests/test_scripts
python run-integration-tests.py
```

## 📋 Prerequisites

### For All Tests
- Python 3.8+
- Node.js 18+
- npm or yarn

### For Backend Tests
- Backend dependencies installed (`pip install -r requirements.txt`)
- SQLite database at `apps/data/task_management.db`

### For Frontend E2E Tests
- Frontend dependencies installed (`npm install`)
- Backend running on `http://localhost:8001`
- Database seeded with test data

### For Persistence Tests
- Backend running on `http://localhost:8001`
- Database at `apps/data/task_management.db`
- Playwright installed (`npm install` in apps/frontend)

## 📊 Test Execution Matrix

| Test Type | Framework | Coverage | Time | Scope |
|-----------|-----------|----------|------|-------|
| Unit | pytest | Backend logic | ~10s | Single functions/services |
| Persistence E2E | Playwright | Database persistence | ~2-3m | Real DB + API |
| Frontend E2E | Playwright | UI + API | ~5-10m | Full workflows |
| **All** | Mixed | Full system | ~15-20m | End-to-end system |

## 🔍 Common Commands

### Run Tests by Category

```bash
# All unit tests
python -m pytest artifacts/tests/test_scripts/backend_tests/unit -v

# All integration tests
npm test -- persistence-integration.spec.ts

# Specific test file
npm test -- auth.spec.ts

# Run single test
npm test -- auth.spec.ts -g "should register a new user"

# With debugging
PWDEBUG=1 npm test
```

### Database Operations

```bash
# Seed database with test data
python artifacts/tests/test_scripts/seed_data.py

# Inspect database
python -c "
import sqlite3
conn = sqlite3.connect('apps/data/task_management.db')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM users')
print('Users:', cur.fetchone()[0])
conn.close()
"

# Clear database
rm apps/data/task_management.db  # Will recreate on backend start
```

## 🚨 Troubleshooting

### Backend Not Running
```bash
cd apps/backend
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8001
```

### Database Errors
```bash
# Remove corrupted database
Remove-Item apps/data/task_management.db -ErrorAction SilentlyContinue

# Reseed
python artifacts/tests/test_scripts/seed_data.py
```

### Frontend Dependency Issues
```bash
cd apps/frontend
npm install
npm test
```

### Playwright Issues
```bash
# Reinstall Playwright
npm install --save-dev @playwright/test

# Run in debug mode
PWDEBUG=1 npm test
```

## 📈 Test Reports

### Backend Unit Tests
```
pytest output → stdout/stderr
```

### Frontend E2E Tests
```
apps/frontend/.playwright/test-results/
apps/artifacts/tests/e2e/screenshots/  (on failure)
```

### Persistence E2E Tests
```
Playwright HTML report available after test run
```

## 🎯 QA Agent Integration

The QA agent can:
1. **Generate tests** - Create new test cases from requirements
2. **Run tests** - Execute all test suites
3. **Report results** - Generate failure reports
4. **Validate persistence** - Verify database changes
5. **Create test data** - Seed realistic scenarios

**QA Skill Location:** `ai/skills/qa.md`

## 📚 Related Documentation

- [API Documentation](../../api-documentation.md) - REST API reference
- [Integration Testing Guide](../../integration-testing-guide.md) - Detailed test guides
- [QA Skills](../../../ai/skills/qa.md) - QA Agent capabilities
- [Seed Data Script](../seed_data.py) - Test data generation

## 🔄 CI/CD Integration

To run tests in CI/CD pipelines:

```yaml
# GitHub Actions Example
- name: Run Backend Unit Tests
  run: python -m pytest artifacts/tests/test_scripts/backend_tests/unit -v

- name: Run Persistence Tests
  run: python artifacts/tests/test_scripts/run-all-tests.py --persistence

- name: Run Frontend Tests
  run: |
    cd apps/frontend
    npm test
```

## 📝 Notes

- All scripts detect platform automatically
- Database is auto-seeded if empty
- Tests are independent and can run in any order
- Failed tests produce detailed logs
- Screenshots captured on Playwright test failures
- Backend must be running for E2E tests
- Tests use unique email addresses (timestamp-based) to avoid conflicts

## 🤝 Contributing

When adding new tests:
1. Place unit tests in `artifacts/tests/test_scripts/backend_tests/unit/`
2. Place E2E tests in `artifacts/tests/test_scripts/tests/`
3. Place persistence tests in `artifacts/tests/test_scripts/tests/persistence-*.spec.ts`
4. Update this README with test descriptions
5. Ensure tests are independent and idempotent
6. Add test data generation to `artifacts/tests/test_scripts/seed_data.py`

---

**Last Updated:** 2024-01-01  
**Maintained by:** QA Team  
**Test Coverage:** ~140+ automated tests
