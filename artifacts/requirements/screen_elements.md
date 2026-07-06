# Screen Elements

## Metadata
- Version: 1.0
- Author: Business Analyst
- Date: 2026-07-06
- Status: Draft
- Workflow ID: WF-20260705-001
- Artifact ID: SCREEN-ELEMENTS-001
- Related Artifacts: specification.md, ui_observations.md, figma_design_intake.md

## Screens

### Screen Name: Login
- Purpose: Allow returning users to sign in securely.
- Component or Section: Authentication

| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Email Address | Input | Email | Enter your email | Yes | Must be a valid email format | None | Visible to all | Enabled when form is ready | Account access and identity validation | Clear label and error feedback |
| Password | Input | Password | Enter your password | Yes | Must meet password policy | None | Visible to all | Enabled when form is ready | Secure access | Masked input with clear error state |
| Remember Me | Checkbox | Remember me | None | No | Not applicable | Off | Visible to all | Always available | Session preference | Accessible label |
| Sign In | Button | Sign in | None | Yes | Must have valid credentials | None | Visible to all | Enabled when required fields are complete | Access granted to authorized users | Clear focus state |
| Forgot Password | Link | Forgot password? | None | No | Not applicable | None | Visible to all | Always available | Account recovery | Keyboard focusable |

### Screen Name: Register
- Purpose: Enable new users to create an account.
- Component or Section: Account creation

| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Full Name | Input | Full name | Enter your name | Yes | Required field | None | Visible to all | Enabled when form is ready | Identity creation | Clear label |
| Email Address | Input | Email | Enter your email | Yes | Valid email format | None | Visible to all | Enabled when form is ready | Account identity | Error feedback |
| Password | Input | Password | Create a password | Yes | Minimum length requirement | None | Visible to all | Enabled when form is ready | Secure account creation | Clear validation |
| Confirm Password | Input | Confirm password | Re-enter password | Yes | Must match password | None | Visible to all | Enabled when form is ready | Validation consistency | Error feedback |
| Create Account | Button | Create account | None | Yes | Required fields complete | None | Visible to all | Enabled when required fields are complete | Account creation | Clear focus and state |

### Screen Name: Dashboard
- Purpose: Provide a quick overview of work, deadlines, and recent activity.
- Component or Section: Summary and activity

| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Task Summary Cards | Read-only Text | Total tasks, completed, pending, overdue | None | No | Not applicable | None | Visible to authenticated users | Always available | Visibility of work status | Clear headings |
| Upcoming Deadlines | Read-only Text | Upcoming deadlines | None | No | Not applicable | None | Visible to authenticated users | Always available | Priority awareness | Scannable content |
| Recent Activity | Read-only Text | Recent activity | None | No | Not applicable | None | Visible to authenticated users | Always available | Transparency of work progress | Clear list structure |
| Team Workload Overview | Read-only Text | Team workload | None | No | Not applicable | None | Visible to users with team access | Depends on access | Team visibility | Clear groupings |

### Screen Name: Task List
- Purpose: Allow users to find and review relevant tasks.
- Component or Section: Task workspace

| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Search | Input | Search tasks | Search by title or label | No | Search across allowed fields | None | Visible to authenticated users | Always available | Relevant result discovery | Clear label |
| Status Filter | Select | Status | Select status | No | Allowed values only | None | Visible to authenticated users | Always available | Filter by workflow state | Clear selection state |
| Priority Filter | Select | Priority | Select priority | No | Allowed values only | None | Visible to authenticated users | Always available | Filter by urgency | Clear selection state |
| Sort | Select | Sort by | Sort by due date, priority, or update time | No | Allowed values only | Recently updated | Visible to authenticated users | Always available | Manage result ordering | Clear label |
| Create Task | Button | Create task | None | No | Not applicable | None | Visible to users with task creation rights | Enabled when permitted | Create work items | Clear focus state |
| Task Row | Read-only Text | Task details summary | None | No | Not applicable | None | Visible according to permissions | Always available | Visible task context | Scannable list |

### Screen Name: Task Details
- Purpose: Provide full context for a task and capture collaboration history.
- Component or Section: Task context and collaboration

| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Title | Read-only Text | Title | None | Yes | Required for task creation | None | Visible to permitted users | Always available | Core task identity | Clear structure |
| Description | Read-only Text | Description | None | No | Maximum length | None | Visible to permitted users | Always available | Work summary | Readable layout |
| Status | Select | Status | Select status | Yes | Allowed lifecycle values only | Todo | Visible to permitted users | Enabled when permissions allow | Workflow control | Clear state change feedback |
| Priority | Select | Priority | Select priority | Yes | Allowed values only | Medium | Visible to permitted users | Enabled when permissions allow | Urgency handling | Clear selection state |
| Assignee | Select | Assignee | Select assignee | No | Must be a valid team member | None | Visible to permitted users | Enabled when permissions allow | Ownership and accountability | Clear options |
| Comments | Input | Add comment | Write a comment | No | Content rules | None | Visible to permitted users | Enabled when user can contribute | Collaboration and audit | Clear help text |
| Attachments | Input | Add attachment | Upload a file | No | File constraints as defined by policy | None | Visible to permitted users | Enabled when user can contribute | Collaboration context | Clear status feedback |
| Activity History | Read-only Text | Activity history | None | No | Not applicable | None | Visible to permitted users | Always available | Audit transparency | Structured list |

### Screen Name: Create Task / Edit Task
- Purpose: Allow users to capture or update task details.
- Component or Section: Task form

| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Title | Input | Title | Enter a title | Yes | Required, maximum 100 characters | None | Visible to permitted users | Enabled when form is ready | Task identity | Clear label and validation |
| Description | Textarea | Description | Describe the task | No | Maximum 2000 characters | None | Visible to permitted users | Enabled when form is ready | Task context | Clear feedback |
| Due Date | Date | Due date | Select a date | No | Cannot be earlier than today | None | Visible to permitted users | Enabled when form is ready | Deadline expectations | Clear date guidance |
| Status | Select | Status | Select status | Yes | Required | Todo | Visible to permitted users | Enabled when form is ready | Workflow state | Clear options |
| Priority | Select | Priority | Select priority | Yes | Required | Medium | Visible to permitted users | Enabled when form is ready | Task urgency | Clear selection |
| Assignee | Select | Assignee | Select assignee | No | Must be a valid assignee | None | Visible to permitted users | Enabled when form is ready | Ownership and assignment | Clear options |
| Labels | Input | Labels | Add labels | No | Not applicable | None | Visible to permitted users | Enabled when form is ready | Task classification | Clear input guidance |
| Save | Button | Save | None | Yes | Must satisfy validation | None | Visible to permitted users | Enabled when required fields are complete | Task persistence | Clear focus state |

### Screen Name: Profile
- Purpose: Allow users to manage personal account details.
- Component or Section: User profile

| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Avatar | Input | Upload avatar | None | No | Not applicable | None | Visible to authenticated user | Always available | Profile personalization | Clear upload guidance |
| Contact Information | Input | Contact information | Enter contact details | No | Format validation where applicable | None | Visible to authenticated user | Enabled when editing | Account details | Clear labels |
| Change Password | Button | Change password | None | No | Password rules | None | Visible to authenticated user | Enabled when action selected | Account security | Clear confirmation |
| Save Changes | Button | Save changes | None | Yes | Must satisfy validation | None | Visible to authenticated user | Enabled when edits are made | Profile updates | Clear focus state |

### Screen Name: Settings
- Purpose: Allow users to configure personal and organizational preferences.
- Component or Section: Preferences and configuration

| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Theme | Select | Theme | Select theme | No | Allowed values only | System | Visible to authenticated user | Always available | Personal experience | Clear options |
| Notification Preferences | Toggle | Notifications | None | No | Not applicable | Enabled | Visible to authenticated user | Always available | Preference control | Clear state |
| Language | Select | Language | Select language | No | Allowed values only | System default | Visible to authenticated user | Always available | Localization | Clear options |
| Time Zone | Select | Time zone | Select time zone | No | Allowed values only | System default | Visible to authenticated user | Always available | Regional settings | Clear options |
| Privacy Preferences | Toggle | Privacy | None | No | Not applicable | Configurable | Visible to authenticated user | Always available | User control | Clear state |

## Notes
- The screen inventory is aligned to the business requirements and the supplied design reference.
- The content remains implementation-agnostic and suitable for downstream UI and business validation work.
