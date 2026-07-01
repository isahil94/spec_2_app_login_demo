# User Stories Template

## Purpose
Capture implementation-ready user stories without duplicating acceptance criteria.

## Metadata
- Version: [Version]
- Author: [Author]
- Date: [Date]
- Status: [Draft | In Review | Approved]
- Workflow ID: [Workflow ID]
- Artifact ID: [Artifact ID]

## User Stories
- Story ID: [US-001]
- Epic: [EPIC-001]
- Feature: [FEAT-001]
- Related Functional Requirements: [REQ IDs]
- Related Screen(s): [Screen IDs or names]
- Related API(s): [Business reference only]
- Related Database Entity: [Business reference only]
- Story Statement: As a [role], I want [capability], so that [business outcome].
- Business Value: [Value statement]
- Preconditions: [Conditions required before trigger]
- Trigger: [Event/user action/system event]
- User Entry Point: [Screen/state where user starts]
- User Exit Point: [Screen/state where flow completes]
- Primary Flow: [Concise step sequence]
- Alternate Flow: [Concise variant]
- Exception Flow: [Concise error/exception path]
- Expected User Feedback: [Validation/success/error feedback summary]
- Business Validation Rules: [Validation statements]
- Security Expectations: [Business-level auth/permission expectations]
- Audit Expectations: [Business events that must be auditable]
- Business Rules (story-specific only): [BR references]
- Authentication/Authorization Behavior: [Business behavior constraints for this story]
- Permission/Visibility Rules: [Who can see/do what under which condition]
- Dependencies: [Upstream stories, features, decisions]
- Business Detail Coverage: [BR/VAL/PERM/STATE/SCENARIO refs]
- Data Constraints: [Required vs optional | defaults | allowed values | uniqueness | relationships]
- Priority: [Must Have | Should Have | Could Have]
- Story Points (optional): [Number]
- Owner: [Role/Team]
- Acceptance Criteria Reference: See `acceptance_criteria.md` under this Story ID.
- Traceability Check: [REQ IDs, AC IDs present and complete]

## OpenLog References
- Record open questions and assumptions in `openlog.md`.
- Do not duplicate governance entries in this artifact.

## Boundary Rules
- Do not include implementation details.
- Do not include API or architecture design.
- Do not duplicate acceptance criteria content.
- Ensure validation and auth behavior are explicit where applicable.
