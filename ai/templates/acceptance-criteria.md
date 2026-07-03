# Acceptance Criteria Template

## Purpose
Define objective, verifiable conditions required for a story or feature to be accepted.

## Metadata
- Version: [Version]
- Author: [Author]
- Date: [Date]
- Status: [Draft | In Review | Approved]
- Artifact ID: [Artifact ID]
- Traceability: [Story IDs, Requirement IDs]

## Acceptance Criteria by User Story

### US-001
- AC-001: [Testable criterion]
- AC-002: [Testable criterion]
- AC-003: [Testable criterion]

### US-002
- AC-004: [Testable criterion]
- AC-005: [Testable criterion]

## Coverage Expectations
- Each story must include acceptance criteria for happy path, alternate path, validation, error, edge, authorization, and state transition behavior where applicable.
- Each criterion must be measurable, testable, and unambiguous.
- Each story must cover, where applicable: validation, success, failure, permissions, navigation, search, filtering, sorting, pagination, error handling, audit events, and security behavior.
- Dependency-Unavailable Criterion (mandatory per story): At least one criterion must state the literal expected behavior when a required backend or data dependency cannot be reached. Must specify exact expected screen/state name, not general phrases like "appropriate error message."

## Rules
- This file is the single source of truth for acceptance criteria.
- Do not duplicate story narrative here.
- Keep each AC atomic, measurable, and verifiable.
- Ensure each story's AC set covers success path, validation behavior, and authorization behavior where applicable.
- Ensure AC IDs map back to story IDs and related requirement IDs through traceability.
- Ensure AC set covers failure, empty, loading, and exception behavior where applicable.
- Ensure ACs define expected workflow/state-transition outcomes where applicable.
- Do not include implementation technology or design details.

## Approval
- Prepared By: [Name]
- Reviewed By: [Name]
- Approved By: [Name]
