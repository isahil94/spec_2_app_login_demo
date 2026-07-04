# Screen Elements

## Purpose
Describe the screens and their interactive elements in business terms only.

## Metadata
- Version: 1.0
- Author: Business Analyst
- Date: 2026-07-04
- Workflow ID: WF-20260704-001
- Status: Draft

## Screens

### Screen Name: Login
- Purpose: Allow existing users to access the system.
- Component or Section: Authentication

#### Elements
| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Email Address | Input | Email Address | Enter email | Yes | Must be a valid email format | None | Visible to all unauthenticated users | Enabled when form is available | Account access requires a registered email | Clear label and keyboard focus |
| Password | Input | Password | Enter password | Yes | Minimum 8 characters | None | Visible to all unauthenticated users | Enabled when form is available | Access requires valid credentials | Masked input with clear labeling |
| Sign In | Button | Sign In | None | Yes | None | None | Visible to all unauthenticated users | Enabled when required fields are present | Authenticates the session | Clearly identifiable action |
| Forgot Password | Link | Forgot Password | None | No | None | None | Visible to all unauthenticated users | Enabled when available | Initiates password recovery | Clearly identifiable link |

### Screen Name: Register
- Purpose: Allow new users to create an account.
- Component or Section: Authentication

#### Elements
| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Full Name | Input | Full Name | Enter full name | Yes | Required value | None | Visible to all users | Enabled when form is available | Account identity is required | Clear label and keyboard support |
| Email Address | Input | Email Address | Enter email | Yes | Must be a valid email format | None | Visible to all users | Enabled when form is available | Duplicate accounts are not allowed | Clear label and error feedback |
| Password | Input | Password | Enter password | Yes | Minimum 8 characters | None | Visible to all users | Enabled when form is available | Password policy must be satisfied | Masked input with clear guidance |
| Create Account | Button | Create Account | None | Yes | None | None | Visible to all users | Enabled when required fields are complete | Creates a new account | Clear action state |

### Screen Name: Dashboard
- Purpose: Summarize task and workload status at a glance.
- Component or Section: Summary and Overview

#### Elements
| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Total Tasks Metric | Read-only Text | Total Tasks | None | No | None | Zero | Visible to authenticated users | Always enabled | Reflects current visible task count | Clear reading order |
| Completed Tasks Metric | Read-only Text | Completed Tasks | None | No | None | Zero | Visible to authenticated users | Always enabled | Reflects current visible task count | Clear reading order |
| Pending Tasks Metric | Read-only Text | Pending Tasks | None | No | None | Zero | Visible to authenticated users | Always enabled | Reflects current visible task count | Clear reading order |
| Overdue Tasks Metric | Read-only Text | Overdue Tasks | None | No | None | Zero | Visible to authenticated users | Always enabled | Reflects current visible overdue count | Clear reading order |
| Recent Activity | Read-only Text | Recent Activity | None | No | None | None | Visible to authenticated users | Always enabled | Shows recent task events | Clear grouping |

### Screen Name: Task List
- Purpose: Present visible tasks with search, filter, sort, and action controls.
- Component or Section: Task Collection

#### Elements
| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Search Input | Input | Search | Search tasks | No | Text search against title, description, labels | None | Visible to authenticated users | Enabled | Search results limited to visible tasks | Clear label and keyboard support |
| Filter Controls | Select | Filter | None | No | Supported status, priority, assignee, due date, created date, team | None | Visible to authenticated users | Enabled | Filters the visible task set | Clear selection state |
| Sort Controls | Select | Sort | None | No | Supported order options | Recently Updated | Visible to authenticated users | Enabled | Reorders the visible task list | Clear label and state |
| Create Task | Button | Create Task | None | No | None | None | Visible to users with task creation rights | Enabled when available | Opens new task entry | Clear action state |
| Task Row | Link | Task Title | None | No | None | None | Visible for each visible task | Enabled when task is available | Opens task details | Clear focus order |

### Screen Name: Task Details
- Purpose: Show complete task details and allow related actions.
- Component or Section: Task Information

#### Elements
| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Title | Read-only Text | Title | None | Yes | Required | None | Visible to authorized users | Enabled when task data is available | Task must have a title | Clear text presentation |
| Description | Read-only Text | Description | None | No | Max 2000 characters | None | Visible to authorized users | Enabled when available | Task description is optional | Clear reading order |
| Status | Select | Status | None | Yes | Must be one of supported statuses | Todo | Visible to authorized users | Enabled for allowed transitions | Status progression follows business rules | Clear label and state |
| Priority | Select | Priority | None | Yes | Must be one of supported priorities | Medium | Visible to authorized users | Enabled for authorized users | Priority value must be valid | Clear selection state |
| Due Date | Date | Due Date | Select date | No | Must not be earlier than today | None | Visible to authorized users | Enabled for authorized users | Invalid due dates prevented | Clear calendar field semantics |
| Comments | Input | Add Comment | Add a comment | No | Comment cannot be empty | None | Visible to task participants | Enabled when task access exists | Collaboration requires permitted access | Clear feedback |
| Attachments | Button | Add Attachment | None | No | None | None | Visible to task participants | Enabled when supported | Attachment action available to permitted users | Clear action labeling |

### Screen Name: Create Task
- Purpose: Allow task creation with required business details.
- Component or Section: Task Form

#### Elements
| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Task Title | Input | Title | Enter task title | Yes | Required, max 100 characters | None | Visible to authenticated users with create rights | Enabled when form is available | Task title required | Label and error messaging |
| Description | Input | Description | Enter description | No | Max 2000 characters | None | Visible to authorized users | Enabled when form is available | Description optional | Clear field semantics |
| Status | Select | Status | None | Yes | One of supported statuses | Todo | Visible to authorized users | Enabled when form is available | Status must be valid | Clear selection state |
| Priority | Select | Priority | None | Yes | One of supported priorities | Medium | Visible to authorized users | Enabled when form is available | Priority must be valid | Clear selection state |
| Due Date | Date | Due Date | Select date | No | Must not be earlier than today | None | Visible to authorized users | Enabled when form is available | Invalid dates prevented | Clear date selection |
| Save Task | Button | Save | None | Yes | None | None | Visible to authorized users | Enabled when required fields are complete | Creates a task record | Clear action state |

### Screen Name: Edit Task
- Purpose: Allow authorized task updates while preserving history.
- Component or Section: Task Form

#### Elements
| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Task Title | Input | Title | Enter task title | Yes | Required, max 100 characters | Existing value | Visible to authorized users | Enabled when edit permitted | Task title required | Clear label and validation |
| Status | Select | Status | None | Yes | Allowed transition only | Existing value | Visible to authorized users | Disabled when completed and user is not administrator | Completed tasks restricted from edit | Clear state explanation |
| Priority | Select | Priority | None | Yes | One of supported priorities | Existing value | Visible to authorized users | Enabled when edit permitted | Priority must remain valid | Clear selection state |
| Due Date | Date | Due Date | Select date | No | Must not be earlier than today | Existing value | Visible to authorized users | Enabled when edit permitted | Invalid dates prevented | Clear date selection |
| Save Changes | Button | Save | None | Yes | None | None | Visible to authorized users | Enabled when edit permitted | Updates task record | Clear action state |

### Screen Name: Profile
- Purpose: Let users review and update personal account information.
- Component or Section: Account Profile

#### Elements
| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Avatar | Button | Upload Avatar | None | No | None | None | Visible to account owner | Enabled when upload available | Personal profile image update | Clear action state |
| Display Name | Input | Display Name | Enter display name | Yes | Required value | Existing value | Visible to account owner | Enabled when profile is editable | Identity is maintained | Clear label |
| Contact Information | Input | Contact Information | Enter contact details | No | Valid contact format where applicable | Existing value | Visible to account owner | Enabled when profile is editable | Personal details must remain valid | Clear field semantics |
| Change Password | Button | Change Password | None | No | Minimum 8 characters | None | Visible to account owner | Enabled when password change is allowed | Secures account access | Clear action state |

### Screen Name: Settings
- Purpose: Allow users and administrators to manage preferences and configuration.
- Component or Section: Preferences and Administration

#### Elements
| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Theme | Select | Theme | None | No | Supported values: Light, Dark, System | System | Visible to authenticated users | Enabled | Preference value must be supported | Clear selection state |
| Notification Preferences | Toggle | Notifications | None | No | Supported notification choices | Enabled | Visible to authenticated users | Enabled | Preferences control notifications | Clear on/off state |
| Language | Select | Language | None | No | Supported language values | System default | Visible to authenticated users | Enabled | Preference value must be supported | Clear selection state |
| Time Zone | Select | Time Zone | None | No | Supported timezone values | System default | Visible to authenticated users | Enabled | Preference value must be supported | Clear selection state |
| Privacy Preferences | Select | Privacy | None | No | Supported privacy values | Default | Visible to authenticated users | Enabled | Preference value must be supported | Clear selection state |
| Administration Controls | Button | Administration | None | No | Role-based | None | Visible to administrators | Enabled for administrators | Privileged controls available only to admins | Clear action state |
