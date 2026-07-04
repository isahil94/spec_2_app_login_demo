# QA Agent Test Infrastructure Usage Guide

## 🎯 Quick Start for QA Agent

The QA agent can now execute all test types using the centralized test runner. Here's how:

### Execute Tests

```bash
# Backend unit tests only
python artifacts/tests/test_scripts/run-all-tests.py --unit

# Database persistence tests only
python artifacts/tests/test_scripts/run-all-tests.py --persistence

# Frontend E2E tests only (UI workflows, excludes persistence)
python artifacts/tests/test_scripts/run-all-tests.py --frontend

# All tests (comprehensive validation)
python artifacts/tests/test_scripts/run-all-tests.py --all
```

### Generate Test Data

```bash
# Seed database with 4 users, 2 teams, 5 tasks, 6 comments
python artifacts/tests/test_scripts/seed_data.py

# Test credentials:
# - alice@example.com / SecurePass123! (TEAM_LEAD)
# - bob@example.com / SecurePass123! (TEAM_MEMBER)
# - charlie@example.com / SecurePass123! (TEAM_MEMBER)
# - diana@example.com / SecurePass123! (ADMIN)
```

## 📋 Test Capabilities by Type

### 1. Backend Unit Tests

**What it tests:**
- ✅ Authentication service (register, login, passwords)
- ✅ Admin operations and endpoints
- ✅ Dashboard metrics and reporting
- ✅ Task schema validation and aliases

**Test files:** `artifacts/tests/test_scripts/backend_tests/unit/`
- test_auth_service.py
- test_admin_endpoints.py
- test_reporting_service.py
- test_task_schema_aliases.py

**Execution:**
```bash
python artifacts/tests/test_scripts/run-all-tests.py --unit
# ~10 tests, ~10 seconds
```

**Create new test:**
Add test case to existing file in `artifacts/tests/test_scripts/backend_tests/unit/` or create new `test_*.py` file

---

### 2. Persistence E2E Tests

**What it tests:**
- ✅ Task creation and database persistence
- ✅ Comment addition and retrieval
- ✅ Multiple comments ordering
- ✅ Task status updates and persistence
- ✅ Task history tracking
- ✅ Multi-step workflows
- ✅ Comment edits and updates
- ✅ Complete user journeys (register → create → comment → update)

**Test file:** `artifacts/tests/test_scripts/tests/persistence-integration.spec.ts`

**Execution:**
```bash
python artifacts/tests/test_scripts/run-all-tests.py --persistence
# 8 tests, ~2-3 minutes
```

**Create new test:**
Add new test case to `artifacts/tests/test_scripts/tests/persistence-integration.spec.ts`

---

### 3. Frontend E2E Tests

**What it tests:**
- ✅ Authentication flows (signup, login)
- ✅ Task management (create, read, update, delete)
- ✅ Comments (create, edit, delete, display)
- ✅ User profiles and settings
- ✅ Dashboard and metrics
- ✅ Team management
- ✅ Admin operations
- ✅ Session management
- ✅ Error handling and edge cases

**Test files:** `artifacts/tests/test_scripts/tests/`
- auth.spec.ts (authentication, 7 tests)
- tasks.spec.ts (task CRUD, 21 tests)
- comments.spec.ts (comment operations, 10 tests)
- comments-history.spec.ts (comment history, 4 tests)
- profile-settings.spec.ts (user profile, 26 tests)
- dashboard.spec.ts (dashboard metrics, 6 tests)
- team-and-history.spec.ts (team operations, 4 tests)
- admin-management.spec.ts (admin features, 3 tests)
- session-landing.spec.ts (session handling, 5 tests)
- dependency-unavailable.spec.ts (error handling, 3 tests)
- integration.spec.ts (integration workflows, 3 tests)
- persistence-integration.spec.ts (database persistence, 8 tests - run separately)

**Execution:**
```bash
python artifacts/tests/test_scripts/run-all-tests.py --frontend
# ~110 tests (11 files), ~5-10 minutes
# Note: Does NOT include persistence-integration.spec.ts (handled by --persistence)
```

**Create new test:**
Add new file `artifacts/tests/test_scripts/tests/<feature-name>.spec.ts` with Playwright test cases

---

## 🔄 Complete Workflow Example

### 1. Prepare Environment

```bash
# Verify backend is running
curl http://localhost:8001/api/v1/health

# Verify database exists
ls -la apps/data/task_management.db

# Seed test data if needed
python artifacts/tests/test_scripts/seed_data.py
```

### 2. Run Tests

```bash
# Run all tests for comprehensive validation
cd artifacts/tests/test_scripts
python run-all-tests.py --all

# Monitor output:
# - Backend Unit Tests (10 tests, ~10s)
# - Persistence E2E Tests (8 tests, ~2-3m)
# - Frontend E2E Tests (110+ tests, ~5-10m)
# - Summary: X passed, 0 failed
```

### 3. Verify Results

```bash
# Exit code 0 = all tests passed
# Exit code 1 = one or more tests failed

# Check failure details in:
- Terminal output (colored status)
- artifacts/tests/test_scripts/test-results/ (Playwright HTML reports)
- screenshot files (on test failures)
```

---

## 🛠️ Generate & Add New Tests

### Add Backend Unit Test

1. Create test file: `artifacts/tests/test_scripts/backend_tests/unit/test_feature.py`
2. Write test using pytest
3. Run: `python run-all-tests.py --unit`
4. Verify: All tests pass

### Add Frontend E2E Test

1. Create test file: `artifacts/tests/test_scripts/tests/feature.spec.ts`
2. Write test using Playwright
3. Run: `python run-all-tests.py --frontend`
4. Verify: All tests pass

### Add Persistence Test

1. Edit file: `artifacts/tests/test_scripts/tests/persistence-integration.spec.ts`
2. Add new test case for database validation
3. Run: `python run-all-tests.py --persistence`
4. Verify: All tests pass

---

## 📊 Test Matrix

| Test Type | Count | Duration | Command | Handled by QA |
|-----------|-------|----------|---------|---------------|
| Backend Unit | ~10 | ~10s | `--unit` | ✅ Yes |
| Persistence E2E | 8 | ~2-3m | `--persistence` | ✅ Yes |
| Frontend E2E | ~110 | ~5-10m | `--frontend` | ✅ Yes |
| **ALL (no duplicates)** | **~130+** | **~15-20m** | `--all` | **✅ Yes** |

---

## 🚀 QA Agent Responsibilities

The QA agent can now:

1. **Generate Tests**
   - Backend unit tests
   - Frontend E2E tests
   - Persistence validation tests
   
2. **Execute Tests**
   - Individual test types
   - Complete test suite
   - Generate coverage reports
   
3. **Generate Test Data**
   - Seed database with realistic data
   - Create test users, teams, tasks, comments
   
4. **Validate Results**
   - Pass/fail status
   - Failure artifacts (screenshots, logs)
   - Coverage metrics
   
5. **Report Status**
   - Test summary (passed, failed, skipped)
   - Execution time per test type
   - Recommendations for failures

---

## ⚠️ Important: No Duplicate Tests

**Critical Behavior:**

When running `python run-all-tests.py --all`:
- Persistence tests run **exactly ONCE**
- Frontend tests exclude `persistence-integration.spec.ts`
- Total tests: ~130+ (no duplicates)
- Duration: ~15-20 minutes

This prevents the persistence tests from being counted or executed twice.

---

## 🔍 Troubleshooting

### Backend Not Running
```bash
cd apps/backend
.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8001
```

### Database Issues
```bash
# Reseed database
python artifacts/tests/test_scripts/seed_data.py

# Or rebuild from scratch
rm apps/data/task_management.db
# (Database auto-created on backend startup)
```

### Frontend Dependencies Missing
```bash
cd apps/frontend
npm install
npm test
```

### Playwright Issues
```bash
cd apps/frontend
npm install --save-dev @playwright/test
npx playwright install
```

---

## 📚 Related Documentation

- [QA Skills](../../../ai/skills/qa.md) - QA Agent capabilities and workflows
- [Test Scripts README](./README.md) - Complete test execution guide
- [Migration Guide](./MIGRATION.md) - Directory migration steps
- [Infrastructure Summary](./TEST_INFRASTRUCTURE_SUMMARY.md) - Overview of changes
- [Directory Structure](./DIRECTORY_STRUCTURE.md) - File organization

---

## ✅ Ready to Use

The QA agent is now ready to:
- Execute all test types
- Generate new tests
- Seed test databases
- Report test results
- Validate complete system functionality

**No duplicates. No delays. Complete test coverage.**
