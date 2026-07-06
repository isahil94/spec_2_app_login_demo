# Business Rules

## Metadata
- Version: 1.0
- Author: Business Analyst
- Date: 2026-07-05
- Status: Draft
- Workflow ID: WF-20260705-001

## Business Rules

### Rule ID: BR-001
- Rule Name: Single Owner and Assignee
- Description: Every task must have one owner and at most one assignee.
- Business Justification: Prevents ambiguous ownership and responsibility.
- Applies To: Task creation and assignment.
- Validation: The task must have an owner and assignee assignment state that satisfies the rule.
- Exception: Administrators may override assignment if the business process requires it.
- Priority: Critical
- Related Stories: US-002, US-005

### Rule ID: BR-002
- Rule Name: Permanent Delete Restriction
- Description: Only administrators may permanently delete tasks.
- Business Justification: Protects task history and governance.
- Applies To: Task deletion.
- Validation: Delete actions are allowed only for administrators.
- Exception: Standard users may archive their own tasks.
- Priority: High
- Related Stories: US-002, US-005

### Rule ID: BR-003
- Rule Name: Archived Task Read-Only
- Description: Archived tasks remain searchable but are read-only until restored by an authorized role.
- Business Justification: Preserves historical visibility while preventing accidental edits.
- Applies To: Archived tasks.
- Validation: Archived tasks cannot be edited except through restore and authorized flows.
- Exception: Administrators may restore or reconfigure archived tasks.
- Priority: High
- Related Stories: US-002

### Rule ID: BR-004
- Rule Name: Status Lifecycle
- Description: Task status transitions must follow the approved workflow: Todo, In Progress, Review, Completed, Blocked.
- Business Justification: Ensures consistent workflow handling and reporting.
- Applies To: Task status changes.
- Validation: The target state must be allowed by the lifecycle rules.
- Exception: Administrators may perform exceptional recovery actions when required.
- Priority: High
- Related Stories: US-002

### Rule ID: BR-005
- Rule Name: Completed Task Protection
- Description: Completed tasks cannot be edited except by administrators.
- Business Justification: Protects completed work from unintended modification.
- Applies To: Completed tasks.
- Validation: Edit requests on completed tasks are blocked unless the actor is an administrator.
- Exception: Administrators may reopen or adjust completed tasks when approved.
- Priority: High
- Related Stories: US-002

### Rule ID: BR-006
- Rule Name: Audit History
- Description: Every task update records audit information.
- Business Justification: Supports traceability and accountability.
- Applies To: Task create, edit, archive, restore, and status changes.
- Validation: Each save action must create a history record.
- Exception: Unavailable persistence services must surface a dependency state.
- Priority: Critical
- Related Stories: US-002, US-004, US-007

### Rule ID: BR-007
- Rule Name: Collaboration Visibility
- Description: Users may only contribute to tasks they can view and that are relevant to their role.
- Business Justification: Protects task confidentiality and team scope.
- Applies To: Comments, attachments, and task discussions.
- Validation: Permission checks occur before allowing contribution.
- Exception: Administrators may override scope if required by governance.
- Priority: High
- Related Stories: US-004

### Rule ID: BR-008
- Rule Name: Notification Relevance
- Description: Notifications are triggered only for relevant task events such as assignment, update, comment, reminder, or overdue state.
- Business Justification: Reduces noise and improves responsiveness.
- Applies To: Notifications and reminders.
- Validation: Notification rules apply based on task events and recipient role.
- Exception: Users may configure their notification preferences.
- Priority: Medium
- Related Stories: US-006

## Notes
- Rules are business-oriented and testable.
- Implementation detail is intentionally omitted.
