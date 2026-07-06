# UI Live Test Report

## Summary
- Executed against the live frontend at http://127.0.0.1:4173/ and the live backend at http://127.0.0.1:8001/.
- Playwright run command: `npx playwright test --workers=1`
- Result: 101 tests executed, 99 passed, 2 failed.

## Failed Scenarios
1. Comments flow timed out while clicking the Post Comment action.
2. Task details did not render the expected dependency-unavailable state when the task service returned an error.

## Evidence
- The failing cases were captured from the Playwright run output and correspond to the live browser interaction tests under the QA test scripts suite.
- The failures are tracked in the QA blocker report and should be routed to the frontend team for investigation.
