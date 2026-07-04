# Business Rules

## Purpose
Capture canonical business rules for the Task Management System in a compact, traceable format.

## Metadata
- Version: 1.0
- Author: Business Analyst
- Date: 2026-07-04
- Status: Draft
- Workflow ID: WF-20260704-001

## Business Rules

### Rule ID: BR-001
- Rule Name: Single Ownership
- Description: Every task must have one owner and at most one assignee.
- Business Justification: Clear accountability improves task execution and visibility.
- Applies To: All tasks
- Validation: Ownership and assignee values must be present or optional according to policy and task state.
- Exception: Administrators may reassign ownership when required.
- Priority: Critical
- Related Stories: US-002

### Rule ID: BR-002
- Rule Name: Permanent Deletion Restriction
- Description: Only administrators may permanently delete tasks.
- Business Justification: Protect task integrity and audit history.
- Applies To: Task deletion actions
- Validation: Destructive actions require administrative permission.
- Exception: Standard users may archive their own tasks.
- Priority: High
- Related Stories: US-002

### Rule ID: BR-003
- Rule Name: Archive Visibility
- Description: Archived tasks remain searchable but are read-only for standard users.
- Business Justification: Preserve visibility while preventing unintended edits.
- Applies To: Archived tasks
- Validation: Archived tasks remain discoverable in search and list views.
- Exception: Administrators may restore or manage archived tasks.
- Priority: Medium
- Related Stories: US-002

### Rule ID: BR-004
- Rule Name: Completed Task Protection
- Description: Completed tasks cannot be edited by standard users.
- Business Justification: Prevent unauthorized alteration after completion.
- Applies To: Completed tasks
- Validation: The system blocks non-administrator edits for completed tasks.
- Exception: Administrators may override the restriction.
- Priority: High
- Related Stories: US-002

### Rule ID: BR-005
- Rule Name: Immutable History
- Description: Task history is immutable and every update records audit information.
- Business Justification: Maintain accountability and traceability.
- Applies To: Task updates and state changes
- Validation: Each update creates an auditable history entry.
- Exception: System-generated audit metadata is not editable by users.
- Priority: High
- Related Stories: US-002, US-004

### Rule ID: BR-006
- Rule Name: Due Date Policy
- Description: Due dates must not be earlier than the current date.
- Business Justification: Prevent invalid scheduling and missed-date misrepresentation.
- Applies To: Task creation and edit
- Validation: The system blocks due dates earlier than today.
- Exception: Administrators may adjust policy if business requirements change.
- Priority: High
- Related Stories: US-002

### Rule ID: BR-007
- Rule Name: Allowed Statuses
- Description: Supported task statuses are Todo, In Progress, Review, Completed, and Blocked.
- Business Justification: Standardize workflow states across the product.
- Applies To: Task status field
- Validation: Status values must be selected from the approved set.
- Exception: No unapproved status values are permitted.
- Priority: High
- Related Stories: US-002

### Rule ID: BR-008
- Rule Name: Allowed Priorities
- Description: Supported task priorities are Low, Medium, High, and Critical.
- Business Justification: Standardize prioritization language and reporting.
- Applies To: Task priority field
- Validation: Priority values must be selected from the approved set.
- Exception: No unapproved priority values are permitted.
- Priority: Medium
- Related Stories: US-002

## Notes
- The rules above are business-oriented and testable.
- No implementation, API, or database design detail is included.
