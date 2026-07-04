# Centralized Test Infrastructure Directory Structure

## Current State (After Configuration Update)

```
artifacts/tests/test_scripts/
├── tests/                    ← READY: 12 test spec files (~120 tests)
│   ├── auth.spec.ts
│   ├── tasks.spec.ts
│   ├── comments.spec.ts
│   ├── comments-history.spec.ts
│   ├── profile-settings.spec.ts
│   ├── dashboard.spec.ts
│   ├── team-and-history.spec.ts
│   ├── admin-management.spec.ts
│   ├── session-landing.spec.ts
│   ├── dependency-unavailable.spec.ts
│   ├── integration.spec.ts
│   └── persistence-integration.spec.ts  ← 8 database persistence tests
│
├── test-results/             ← READY: Playwright HTML reports & traces
│   ├── .last-run.json
│   └── [test-results-directories]
│
├── seed_data.py              ← ✅ MOVED: Test data generation
├── run-all-tests.py          ← ✅ CREATED: Master test runner
├── run-integration-tests.py   ← ✅ CREATED: Persistence E2E runner
├── run-integration-tests.bat  ← ✅ CREATED: Windows runner
├── run-integration-tests.sh   ← ✅ CREATED: Unix/Mac runner
├── README.md                 ← Test execution guide
├── MIGRATION.md              ← ✅ NEW: Migration instructions
└── TEST_INFRASTRUCTURE_SUMMARY.md ← ✅ NEW: This summary

apps/frontend/
├── playwright.config.ts      ← ✅ UPDATED: testDir → ../../../artifacts/tests/test_scripts/tests
├── package.json              ← npm test works with new config
└── [other frontend files]
```

## Pre-Migration State (What Needs to Be Moved)

```
apps/frontend/tests/           ← To be moved to: artifacts/tests/test_scripts/tests/
├── auth.spec.ts
├── tasks.spec.ts
├── comments.spec.ts
├── comments-history.spec.ts
├── profile-settings.spec.ts
├── dashboard.spec.ts
├── team-and-history.spec.ts
├── admin-management.spec.ts
├── session-landing.spec.ts
├── dependency-unavailable.spec.ts
├── integration.spec.ts
└── persistence-integration.spec.ts

apps/frontend/test-results/    ← To be moved to: artifacts/tests/test_scripts/test-results/
├── .last-run.json
└── [test-results-directories]
```

## Test File Organization

### Backend Tests (After Migration)
```
artifacts/tests/test_scripts/backend_tests/  ← Backend unit tests centralized here
├── unit/
│   ├── test_auth_service.py
│   ├── test_admin_endpoints.py
│   ├── test_reporting_service.py
│   └── test_task_schema_aliases.py
└── [other test directories]
```

### Frontend Tests (After Migration)
```
artifacts/tests/test_scripts/tests/  ← ALL frontend tests centralized here
├── auth.spec.ts              (7 tests)
├── tasks.spec.ts             (21 tests)
├── comments.spec.ts          (10 tests)
├── comments-history.spec.ts  (4 tests)
├── profile-settings.spec.ts  (26 tests)
├── dashboard.spec.ts         (6 tests)
├── team-and-history.spec.ts  (4 tests)
├── admin-management.spec.ts  (3 tests)
├── session-landing.spec.ts   (5 tests)
├── dependency-unavailable.spec.ts (3 tests)
├── integration.spec.ts       (3 tests)
└── persistence-integration.spec.ts (8 tests - database focused)

Total: ~120 tests in 12 files
```

## Test Data Structure

```
artifacts/tests/test_scripts/
├── seed_data.py              ← Test data generation script
│   Creates:
│   - 4 test users (alice, bob, charlie, diana)
│   - 2 test teams (Engineering, Design)
│   - 5 test tasks (various statuses & priorities)
│   - 6 test comments (on tasks)
│
└── apps/data/task_management.db  ← Populated by seed_data.py
    (SQLite database with test data)
```

## Execution Flow

### Master Test Runner Paths

```
run-all-tests.py
├── --unit → pytest artifacts/tests/test_scripts/backend_tests/unit/
├── --persistence → npm test -- persistence-integration.spec.ts
├── --frontend → npm test -- [11 test files excluding persistence]
└── --all → All tests sequentially (NO DUPLICATES)
```

### Playwright Configuration

```
apps/frontend/playwright.config.ts
├── testDir: '../../../artifacts/tests/test_scripts/tests'
├── baseURL: 'http://localhost:4173'
├── reporter: 'html'
└── Generates → artifact/tests/test_scripts/test-results/
```

## Verification Checklist

After migration, the directory structure should look like:

```
✅ artifacts/tests/test_scripts/
   ├── tests/                (contains 12 .spec.ts files)
   ├── test-results/         (contains test reports)
   ├── seed_data.py          (moved from apps/backend)
   ├── run-all-tests.py
   ├── run-integration-tests.py
   ├── README.md
   ├── MIGRATION.md
   └── TEST_INFRASTRUCTURE_SUMMARY.md

✅ apps/frontend/
   ├── playwright.config.ts  (testDir updated)
   └── [NO tests directory]  (moved to artifacts/tests/test_scripts/)

✅ Master runner functions:
   - python run-all-tests.py --unit       ← runs backend tests
   - python run-all-tests.py --persistence ← runs only 8 persistence tests
   - python run-all-tests.py --frontend   ← runs 110+ non-persistence tests
   - python run-all-tests.py --all        ← runs all once (NO duplicates)
```

## Key Improvements

| Aspect | Before | After |
|--------|--------|-------|
| **Centralization** | Tests scattered across frontend/backend | All in `artifacts/tests/test_scripts/` |
| **Duplicates** | Persistence tests run twice in full suite | Zero duplicates in `--all` mode |
| **QA Access** | Hard to find test location | Single unified entry point |
| **Documentation** | References spread across files | Centralized guides |
| **Scalability** | Difficult to add new tests | Clear structure for new tests |
| **CI/CD Ready** | Requires manual path updates | Works out of the box |

## File Locations Summary

### Test Files
- **Backend Unit Tests**: `artifacts/tests/test_scripts/backend_tests/unit/`
- **Frontend E2E Tests**: `artifacts/tests/test_scripts/tests/`
- **Persistence E2E Tests**: `artifacts/tests/test_scripts/tests/persistence-integration.spec.ts`

### Configuration
- **Playwright Config**: `apps/frontend/playwright.config.ts`
- **Master Runner**: `artifacts/tests/test_scripts/run-all-tests.py`
- **Integration Runner**: `artifacts/tests/test_scripts/run-integration-tests.py`

### Test Data & Results
- **Seed Script**: `artifacts/tests/test_scripts/seed_data.py`
- **Test Database**: `apps/data/task_management.db`
- **Test Reports**: `artifacts/tests/test_scripts/test-results/`

### Documentation
- **QA Skills**: `ai/skills/qa.md`
- **Test Scripts README**: `artifacts/tests/test_scripts/README.md`
- **Migration Guide**: `artifacts/tests/test_scripts/MIGRATION.md`
- **Infrastructure Summary**: `artifacts/tests/test_scripts/TEST_INFRASTRUCTURE_SUMMARY.md`

---

**Ready for Migration:**  
All configuration is updated. Only pending: Copy test files from `apps/frontend` to `artifacts/tests/test_scripts/`
