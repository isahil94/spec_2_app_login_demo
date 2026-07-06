# Validation Rules

## Metadata
- Version: 1.0
- Author: Backend Developer
- Date: 2026-07-06
- Status: Draft
- Workflow ID: WF-20260705-001
- Correlation ID: WF-1783283413777
- Traceability: acceptance_criteria.md, business_rules.md

## Validation Rules
- Email values must conform to a valid email format for registration and profile updates.
- Passwords must meet the minimum policy for account creation and password changes.
- Task titles are required and must remain within the allowed length.
- Due dates cannot be earlier than the current date for new or updated tasks.
- Status and priority values must remain within the approved domain values.
- Permission and role changes must be validated against the current authorization model.

## Error Handling Expectations
- Validation failures should return explicit client-facing errors without performing unsafe state changes.
