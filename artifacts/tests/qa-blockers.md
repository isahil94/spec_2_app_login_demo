# QA Blockers

## Critical Blocker: Playwright Runtime Conflict

**Status:** BLOCKED
**Category:** Environment / Test Harness
**Impact:** Full frontend and persistence end-to-end test execution

**Details:**
- Backend unit tests passed, and backend service is healthy.
- Frontend dev server is running on `http://localhost:4174`.
- Playwright test runner fails with:
  - `Error: Requiring @playwright/test second time`
- The failure occurs before any browser test can execute.

**Required Action:**
- Resolve Playwright package/runtime conflict in `apps/frontend`
- Ensure `npx playwright test` or `npm run test` can execute successfully
- Re-run the full QA suite after environment fix

**Related Acceptance Criteria:**
- AC-001 through AC-028 (E2E test coverage blocked)
