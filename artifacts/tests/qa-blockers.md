# QA Blockers & Critical Issues

## Executive Summary

**Status:** 🔴 RELEASE BLOCKED
**Critical Issues:** 3
**High Priority Issues:** 10
**Test Execution Date:** 2026-07-05

Three critical issues must be resolved before release. All are backend/API related and
prevent core user stories from functioning.

---

## Critical Issues (Release Blockers)

### 1. Comment API Endpoint Returns 404 (CRITICAL)

**Severity:** CRITICAL | **Category:** API/Backend | **User Stories Affected:** US-004
**Status:** 🔴 BLOCKED
**Target Agent:** Backend Developer

**Description:**
POST `/tasks/{taskId}/comments` endpoint is returning HTTP 404 (Not Found) instead of
creating comments and returning HTTP 200 with comment ID.

**Acceptance Criteria Blocked:**
- AC-013: Add comment or attachment to task (BLOCKED)
- AC-016: Handle collaboration service unavailable (PARTIALLY BLOCKED)

**Failing Tests (8 total):**
1. persistence-integration.spec.ts:71 - "should create a task and persist to database"
2. persistence-integration.spec.ts:104 - "should add a comment and persist to database"
3. persistence-integration.spec.ts:153 - "should add multiple comments and retrieve in order"
4. persistence-integration.spec.ts:219 - "should update task status and persist changes"
5. persistence-integration.spec.ts:274 - "should track task history with comments and status changes"
6. persistence-integration.spec.ts:329 - "should persist task and comments across multiple API calls"
7. persistence-integration.spec.ts:399 - "should handle comment updates and persist changes"
8. persistence-integration.spec.ts:454 - "complete workflow: register → create task → add comments → update status"

**Root Cause (Investigation Required):**
- POST `/tasks/{taskId}/comments` endpoint not registered in router
- Task ID parameter not being passed correctly to handler
- Route middleware filtering out comment requests
- Database transaction/connection issue

**Impact Analysis:**
- **Functional Impact:** Users cannot add comments to tasks; entire collaboration feature non-functional
- **User Story Impact:** US-004 (Collaboration) is blocked; cannot proceed to production
- **Risk Level:** CRITICAL (core feature)

**Expected vs. Actual:**
```text
Expected: POST /tasks/{taskId}/comments → HTTP 200 + {commentId: "...", content: "...", ...}
Actual: POST /tasks/{taskId}/comments → HTTP 404 + {error: "Not Found"}
```

**Error Evidence:**
```text
Error: expect(received).toBe(expected)
Expected: 200
Received: 404
at persistence-integration.spec.ts:506:36
```

**Recommended Fix (Backend Team):**
1. Verify route definition exists in FastAPI `main.py` for
   `POST /api/v1/tasks/{task_id}/comments`
2. Check that task_id parameter is correctly extracted from URL path
3. Verify comment creation endpoint handler is wired to database save operation
4. Test with curl:

```text
curl -X POST http://localhost:8001/api/v1/tasks/test-id/comments \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{"content": "test"}'
```

1. Add route-level logging to debug request flow

**QA Reproduction Steps (performed locally):**

- Start backend (from project root using `.venv`):

```text
.\.venv\Scripts\python.exe -m uvicorn apps.backend.main:app --host 127.0.0.1 --port 8001
```

- Register a test user (examples):

```text
python scripts/qa_post_register.py
# or using system curl.exe
curl.exe -X POST "http://127.0.0.1:8001/api/v1/auth/register" -H "Content-Type: application/json" --data-binary @- <<'JSON'
{"email":"qa+bot@example.com","password":"Password123!","fullName":"QA Bot"}
JSON
```

- Create a task and post a comment (examples):

```text
python scripts/qa_comment_test.py
# or curl example (replace <token> and <task_id>):
curl.exe -X POST "http://127.0.0.1:8001/api/v1/tasks/<task_id>/comments" \
   -H "Authorization: Bearer <token>" \
   -H "Content-Type: application/json" \
   --data-binary @- <<'JSON'
{"content":"This is a test comment from QA bot"}
JSON
```

**Local Verification Result:** Using `scripts/qa_comment_test.py` the POST to
`/api/v1/tasks/{task_id}/comments` returned HTTP 200 and a `comment_id`
(successful creation). This indicates the endpoint is implemented and working on a
correctly started backend. If CI/tests receive a 404, likely causes are: backend
not running during the test, test runner targeting a different base URL, or test
environment route prefix differences. Add logging to the test infra to capture
full request URL and headers.

**Estimated Effort:** 2-4 hours
**Blocker Resolution Priority:** IMMEDIATE

---

### 2. Dashboard Metrics - Due Today Calculation Returns 0 (CRITICAL)

**Severity:** CRITICAL | **Category:** Business Logic/Backend | **User Stories Affected:** US-005
**Status:** 🔴 BLOCKED
**Target Agent:** Backend Developer

**Description:**
Dashboard metrics endpoint calculates `due_today_tasks` as 0 when tasks exist with
today's due date. This breaks business reporting and team lead workload visibility.

**Acceptance Criteria Blocked:**
- AC-017: View dashboard metrics with correct totals (PARTIALLY BLOCKED - retrieval works; calculation fails)
- AC-018: Team lead workload shows due-today count (BLOCKED)

**Failing Test (1 total):**
- dashboard.spec.ts:101 - "GET /dashboard/metrics - should calculate correct metrics"

**Root Cause (Investigation Required):**
- Due date comparison logic using wrong timezone
- Today's date calculation not accounting for user timezone
- Database query filtering excludes today's tasks
- Date field format mismatch (ISO string vs. date object)

**Impact Analysis:**
- **Functional Impact:** Dashboard shows incomplete metrics; team leads cannot see accurate workload
- **User Story Impact:** US-005 (Reporting/Dashboard) degraded; metrics unreliable
- **Risk Level:** CRITICAL (impacts management decision-making)

**Expected vs. Actual:**
```text
Expected: metrics.due_today_tasks ≥ 1 (when tasks have today's due date)
Actual: metrics.due_today_tasks = 0
```

**Error Evidence:**
```text
Error: expect(metrics.due_today_tasks).toBeGreaterThanOrEqual(1)
Received: 0
at dashboard.spec.ts:113:37
```

**Recommended Fix (Backend Team):**
1. Review `get_dashboard_metrics()` endpoint logic in `apps/backend/main.py`
2. Check timezone handling: Is user's timezone applied to today's date calculation?
3. Inspect SQL query that filters tasks by due_date: Is it comparing dates correctly?
4. Test edge cases:
   - Task with ISO due_date: "2026-07-05T23:59:59Z"
   - Task with date-only due_date: "2026-07-05"
   - Timezones with negative UTC offsets (e.g., US timezones)
5. Add debug logging:
   `print(f"Today: {today}, Task due_date: {task.due_date}, Match: {today == task.due_date}")`

**Test to Verify Fix:**
```python
def test_dashboard_due_today_calculation():
    # Create task with today's date
    today = datetime.now().date()
    task = create_task(due_date=today)
    metrics = get_dashboard_metrics()
    assert metrics["due_today_tasks"] >= 1
```

**Estimated Effort:** 1-2 hours
**Blocker Resolution Priority:** IMMEDIATE

---

### 3. Settings Page Missing Dependency-Unavailable UI State (CRITICAL)

**Severity:** CRITICAL | **Category:** Frontend/UX | **User Stories Affected:** US-007
**Status:** 🔴 BLOCKED
**Target Agent:** Frontend Developer

**Description:**
Settings page does not display "Loading settings..." or error state when settings
service is unavailable. User sees blank page with no feedback, causing confusion
during service outages.

**Acceptance Criteria Blocked:**
- AC-028: Dependency-unavailable state displays graceful message (PARTIALLY BLOCKED - other pages OK; settings missing)

**Failing Test (1 total):**
- dependency-unavailable.spec.ts:59 - "Settings page shows loading when settings service unavailable"

**Root Cause (Investigation Required):**
- Settings page component not implementing error/loading state UI
- Dependency-unavailable event handler not wired to settings page
- Loading spinner not rendered during API call
- Error message conditional not evaluating correctly

**Impact Analysis:**
- **Functional Impact:** Users receive no feedback during service outage; page appears broken/frozen
- **User Story Impact:** US-007 (Profile/Settings) degraded; user experience poor during failures
- **Risk Level:** CRITICAL (affects user experience during service issues)

**Expected vs. Actual:**
```text
Expected: Settings page shows "Loading settings..." message when API unavailable
Actual: Page appears blank; no visible loading state; user has no feedback
```

**Error Evidence:**
```text
Error: expect(locator).toBeVisible() failed
Locator: locator('text=Loading settings...')
Expected: visible
Timeout: 5000ms
```

**Recommended Fix (Frontend Team):**
1. In Settings page component, add loading state UI:
   ```tsx
   {isLoading && <div>Loading settings...</div>}
   {error && <ErrorBanner message={error} />}
   {data && <SettingsForm data={data} />}
   ```
2. Wire error handler to catch API failures
3. Set `isLoading = true` during fetch, `false` on response
4. Test with Network tab → Throttle to simulate slow/failed API
5. Verify error boundary catches and displays graceful message

**Test to Verify Fix:**
```typescript
test('Settings page shows loading state during API call', async ({ page }) => {
  await page.route('**/api/v1/users/*/settings', route => {
    // Simulate service delay/unavailability
    return route.abort();
  });
  await page.goto('http://localhost:4173/settings');
  await expect(page.locator('text=Loading settings...')).toBeVisible();
});
```

**Estimated Effort:** 1-2 hours
**Blocker Resolution Priority:** IMMEDIATE

---

## High Priority Issues (Follow-up Testing Required)

| Issue | Feature | Impact | Effort |
| --- | --- | --- | --- |
| Node.js process crash during persistence tests | Test infrastructure | Tests fail mid-run; unclear if bug or test issue | 1-2h investigation |
| Persistence-integration tests flaky | Test reliability | 8 tests fail sporadically; need deterministic reproduction | 1-2h investigation |
| Dashboard due_today metric incomplete | Reporting | Team lead workload view inaccurate | Covered in Critical #2 |

---

## Resolution Workflow

### Step 1: Backend Developer
1. Review and fix comment API endpoint (Critical #1)
2. Review and fix dashboard metrics calculation (Critical #2)
3. Push fixes to develop branch
4. Run backend unit tests: `python -m pytest artifacts/tests/test_scripts/backend_tests -v`
5. Verify all tests pass before handing off

### Step 2: Frontend Developer
1. Review and implement settings dependency-unavailable UI (Critical #3)
2. Update Settings component with loading/error state
3. Push fixes to develop branch
4. Run frontend tests: `npm test -- --workers=1` from `apps/frontend`
5. Verify failing tests now pass

### Step 3: QA Re-Test (After Fixes)
1. Re-run full test suite: Backend + Frontend
2. Focus on previously failing tests:
   - `persistence-integration.spec.ts` (should flip 8 tests to PASS)
   - `dashboard.spec.ts:101` (should PASS)
   - `dependency-unavailable.spec.ts:59` (should PASS)
3. Generate updated Quality Report
4. If all pass: Emit `QATestingComplete` event
5. If any fail: Repeat this cycle

---

## Sign-Off & Escalation

**QA Engineer Assessment:**
🔴 **RELEASE NOT READY** - Three critical issues block deployment

**Escalation Path:**
- Report to Supervisor immediately
- Supervisor routes Critical #1 and #2 to Backend Developer
- Supervisor routes Critical #3 to Frontend Developer
- Supervisor coordinates re-test cycle after fixes

**Next Actions:**
1. Developers implement fixes
2. Push to develop branch
3. QA re-runs full test suite
4. Once all tests pass: Emit `QATestingComplete` → Proceed to Reviewer stage

**Approval Decision:** **BLOCKED** - Cannot approve release until all critical issues resolved.
