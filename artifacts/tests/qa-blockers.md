# QA Blockers

## Metadata
- Workflow ID: WF-1783344648928
- Correlation ID: WF-1783344648928
- Stage: QA
- Status: BLOCKED

## Critical Issues

### B1 - Comment submission UI is unstable
- Severity: Major
- Target Agent: frontend
- User Story / Requirement: US-004 / AC-016, AC-017
- Evidence: The Playwright comments flow timed out while clicking Post Comment because the button detached from the DOM during the interaction.
- Impact: Users may be unable to add comments reliably from the task-details view.

### B2 - Dependency-unavailable state is not shown for task detail failures
- Severity: Major
- Target Agent: frontend
- User Story / Requirement: US-002 / AC-010
- Evidence: The task-details page did not render the expected dependency-unavailable message after a simulated 500 response from the task service.
- Impact: Error handling for unavailable services is not matching the documented acceptance criteria.

## Notes
- The backend health endpoint and backend unit test passed.
- The full Playwright run produced 99 passing tests and 2 failing scenarios.
