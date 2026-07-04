# User Flow Specification

## Purpose
Define screen navigation, workflows, and state transitions for the Task Management System.

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-04
- Status: Draft
- Artifact ID: USER-FLOW-001
- Figma Reference: https://www.figma.com/make/YnxUzBz6USzrnokLtV4Jd0/Task-Management-System-Screens

---

## Navigation Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   PUBLIC ROUTES (No Auth)                   │
├─────────────────────────────────────────────────────────────┤
│ /login           - Authentication entry point              │
│ /register        - Account creation                         │
│ /forgot-password - Password recovery initiation             │
│ /reset-password  - Password reset with recovery token       │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  Authenticated?      │
        └──────────┬──────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│              PROTECTED ROUTES (Auth Required)               │
├─────────────────────────────────────────────────────────────┤
│ /dashboard       - Summary metrics and recent activity      │
│ /tasks           - Task list with search/filter             │
│ /tasks/:id       - Task details and collaboration           │
│ /tasks/create    - New task form                            │
│ /profile         - User profile management                  │
│ /settings        - Preferences and administration           │
│ /teams           - Team management (admin/lead only)        │
│ /reports         - Workload reports (team lead/admin)       │
└─────────────────────────────────────────────────────────────┘
```

---

## Screen Flows

### Authentication Flow

```
Entry
  │
  ├─→ [Login Screen]
  │      │
  │      ├─ Valid Credentials → [Dashboard]
  │      ├─ Invalid Credentials → Error message + stay on Login
  │      ├─ Forgot Password link → [Forgot Password Screen]
  │      └─ No Account link → [Register Screen]
  │
  ├─→ [Register Screen]
  │      │
  │      ├─ Valid input + unique email → Account created → [Login Screen] or [Dashboard] (auto-login)
  │      ├─ Invalid input → Error message + stay on Register
  │      ├─ Duplicate email → Error message + option to login or recover password
  │      └─ Already have account link → [Login Screen]
  │
  ├─→ [Forgot Password Screen]
  │      │
  │      ├─ Enter email → Email sent → [Check Email confirmation]
  │      └─ Try to login link → [Login Screen]
  │
  └─→ [Reset Password Screen] (from email link)
         │
         ├─ Valid recovery token + valid password → Password updated → [Login Screen]
         ├─ Expired token → Error message → [Forgot Password Screen]
         ├─ Invalid new password → Validation error → stay on form
         └─ Already know password → [Login Screen]
```

---

### Task Management Flow

```
[Dashboard]
  │
  ├─→ View metrics (total, completed, pending, overdue, due today)
  ├─→ View recent activity
  ├─→ Click task or "View All" → [Task List]
  └─→ Navigate via sidebar → [Task List], [Profile], [Settings], [Reports]

[Task List]
  │
  ├─→ Search tasks (title, description, labels)
  ├─→ Filter by: status, priority, assignee, due date, created date, team
  ├─→ Sort by: recently updated, due date, priority, status, created date
  ├─→ Pagination (20 items per page default)
  │
  ├─→ Click task → [Task Details]
  │
  ├─→ "Create Task" button → [Create Task Form]
  │
  ├─→ Bulk select + action menu
  │      ├─ Bulk status update
  │      ├─ Bulk priority update
  │      ├─ Bulk delete (admin only)
  │      └─ Cancel → back to list
  │
  └─→ Dependency unavailable → Show error state + allow retry

[Create Task]
  │
  ├─ Enter: title (required), description (optional), status, priority, assignee, due date
  ├─ Validation on change (due date not in past, title required, etc.)
  │
  ├─→ Save → [Task Details] (show new task)
  ├─→ Cancel → [Task List]
  └─→ Validation error → Show field-level error + stay on form

[Task Details]
  │
  ├─ Display: title, description, status, priority, owner, assignee, due date, labels
  ├─ Display: task history (status changes, edits)
  │
  ├─→ "Edit Task" button → [Edit Task Form]
  │      │
  │      ├─ Modify: title, status, priority, assignee, due date
  │      │
  │      ├─ Status update → Validate allowed transition
  │      │ ├─ Completed task protection (non-admin cannot edit)
  │      │ └─ Blocked status allowed from any state
  │      │
  │      ├─→ Save → [Task Details] (show updated values)
  │      ├─→ Cancel → [Task Details]
  │      └─→ Concurrent edit conflict → Show conflict resolution (reload/merge options)
  │
  ├─→ "Archive Task" button
  │      └─→ Confirm → Task archived → Back to [Task List]
  │
  ├─→ "Restore Task" button (if archived)
  │      └─→ Confirm → Task restored → Back to [Task Details]
  │
  ├─→ "Duplicate Task" button
  │      ├─ Enter new title
  │      └─→ Create → New task created → Go to [New Task Details]
  │
  ├─→ "Delete Task" button (admin only)
  │      └─→ Confirm → Task deleted → Back to [Task List]
  │
  ├─ Comments section
  │      ├─→ Add comment → [Comment Form] → Save → Comment added → Show in list
  │      ├─→ Edit comment → [Comment Form] → Update → Comment updated
  │      ├─→ Delete comment (author/admin) → Confirm → Comment deleted
  │      └─→ View comment history → Show previous versions
  │
  ├─ Attachments section
  │      ├─→ Add attachment → File upload → Show in list
  │      ├─→ Download attachment → Browser download
  │      └─→ Delete attachment (owner/admin) → Confirm → Removed
  │
  ├─ Activity feed
  │      └─ Show: creation, edits, status changes, comments, attachments (chronological)
  │
  ├─→ Back to [Task List] link/button
  └─→ Dependency unavailable → Show which features are unavailable + allow view-only mode

[Edit Task] - Similar to Create Task with pre-filled values
```

---

### Collaboration Flow

```
[Task Details]
  │
  ├─ Comments Section
  │   │
  │   ├─→ "Add Comment" input field
  │   │     │
  │   │     ├─ User types comment
  │   │     ├─ Optional: @mention user
  │   │     ├─→ Submit → Comment created
  │   │     │     ├─ Notify: task owner, assignee, other commenters
  │   │     │     ├─ Notification respects user preferences
  │   │     │     └─ Comment appears in activity feed
  │   │     │
  │   │     └─→ Cancel → Discard comment
  │   │
  │   ├─ Comment List
  │   │   │
  │   │   ├─→ Hover comment → Show edit/delete options (if authorized)
  │   │   │     │
  │   │   │     ├─→ Edit → [Comment Edit Form] → Update → Comment updated (show "edited" marker)
  │   │   │     │
  │   │   │     └─→ Delete → Confirm → Comment deleted
  │   │   │
  │   │   └─ Show: author, timestamp, content, edit history if edited
  │   │
  │   └─→ Pagination (20 comments per page if many)
  │
  ├─ Attachment Section
  │   │
  │   ├─→ "Add Attachment" button → File picker
  │   │     │
  │   │     ├─ Select file → Upload → Show in attachment list
  │   │     ├─ Size limit validation (e.g., 10MB)
  │   │     ├─ Format validation (common file types)
  │   │     └─→ Cancel upload
  │   │
  │   └─ Attachment List
  │       │
  │       ├─ Show: filename, size, upload date, uploader
  │       │
  │       ├─→ Click → Download file
  │       │
  │       └─→ Delete (uploader/admin) → Confirm → Attachment removed
  │
  └─→ Return to Task Details main view
```

---

### Notification & Preference Flow

```
[Settings]
  │
  ├─ Notification Preferences section
  │   │
  │   ├─→ Toggle: "In-app Notifications" (required)
  │   │
  │   ├─→ Toggle: "Email Notifications" (optional)
  │   │
  │   ├─→ Per-event preferences (if email enabled)
  │   │     ├─ Email on task assignment
  │   │     ├─ Email on task status change
  │   │     ├─ Email on comment added
  │   │     └─ Email when mentioned
  │   │
  │   ├─→ Save preferences → Confirmation message → Preferences updated
  │   └─→ Related AC: AC-014
  │
  └─ Other settings...

[Notification Center] (optional sidebar/icon)
  │
  ├─ Unread notification count badge
  │
  ├─→ Click bell icon → Notification dropdown
  │     │
  │     ├─ List unread notifications (newest first)
  │     │   │
  │     │   ├─ Task created notification
  │     │   ├─ Task status changed notification
  │     │   ├─ Comment added notification
  │     │   ├─ Assigned to task notification
  │     │   └─ Mentioned in comment notification
  │     │
  │     ├─→ Click notification → Navigate to [Task Details]
  │     │     └─ Mark notification as read
  │     │
  │     ├─→ "Mark all as read" button
  │     │
  │     └─→ "Settings" link → [Settings] Notification Preferences
  │
  └─ In-app notification toast
      │
      ├─ Show as non-intrusive toast (top-right)
      ├─ Auto-dismiss after 5 seconds
      ├─ Include action link (go to task, dismiss)
      └─ Respect notification preferences
```

---

### Reporting & Dashboard Flow

```
[Dashboard]
  │
  ├─ Summary Metrics Section
  │   │
  │   ├─ Total Tasks (all visible to user)
  │   ├─ Completed Tasks (status = completed)
  │   ├─ Pending Tasks (status != completed and not archived)
  │   ├─ Overdue Tasks (due_date < today and status != completed)
  │   ├─ Due Today Tasks (due_date = today and status != completed)
  │   │
  │   └─ Metrics calculated from visible task set:
  │       ├─ Admin: sees all tasks
  │       ├─ Team Lead: sees team tasks + own tasks
  │       └─ Team Member: sees own + assigned + team tasks
  │
  ├─ Recent Activity Feed
  │   │
  │   ├─ Show: task creation, status changes, comments (recent first)
  │   ├─ Show: author, action, task link, timestamp
  │   │
  │   └─→ Click activity → Navigate to [Task Details]
  │
  ├─→ "View All Tasks" link → [Task List]
  │
  ├─→ "View Overdue" quick link → [Task List] filtered to overdue
  │
  ├─→ "View Due Today" quick link → [Task List] filtered to due today
  │
  └─ Dependency unavailable
      └─ Show: "Metrics loading..." or explicit error → Allow retry

[Reports] (Team Lead/Admin only)
  │
  ├─ Team selector (admin sees all teams)
  │
  ├─ Workload Report
  │   │
  │   ├─ Show: tasks per team member
  │   ├─ Show: completion rate per member
  │   ├─ Show: overdue count per member
  │   │
  │   └─→ Click member → Filter [Task List] to member's tasks
  │
  ├─ Productivity Report
  │   │
  │   ├─ Date range selector
  │   │
  │   ├─ Show: tasks completed per day/week/month
  │   ├─ Show: average time to completion
  │   ├─ Show: status distribution trends
  │   │
  │   └─→ Drill down → [Task List] for period
  │
  └─ Export reports (future feature)
```

---

### Profile & Settings Flow

```
[Profile]
  │
  ├─ Display User Information
  │   │
  │   ├─ Avatar (image)
  │   ├─ Full Name
  │   ├─ Email (read-only)
  │   ├─ Contact Information
  │   ├─ Role (read-only, admin-assigned)
  │   ├─ Member Since (read-only, account creation date)
  │   │
  │   └─→ "Edit Profile" button → Enter edit mode
  │        │
  │        ├─ Avatar: "Change Avatar" → File picker → Upload
  │        ├─ Full Name: Edit text field
  │        ├─ Contact Info: Edit text field
  │        │
  │        ├─→ Save changes → Validate → Profile updated → Show confirmation
  │        ├─→ Cancel → Discard edits → Back to view mode
  │        └─ Validation errors show inline
  │
  ├─ Security Section
  │   │
  │   └─→ "Change Password" button
  │        │
  │        ├─ Old password field (required)
  │        ├─ New password field (min 8 chars, required)
  │        ├─ Confirm password field (must match)
  │        │
  │        ├─→ Submit → Validate password → Update → Confirmation + "Please log in again"
  │        │              → Auto-logout → [Login Screen]
  │        │
  │        └─→ Cancel → Back to profile
  │
  └─→ [Settings] button → [Settings Screen]

[Settings]
  │
  ├─ Appearance Preferences
  │   ├─ Theme: Light, Dark, System default
  │   ├─ Language: English, Spanish, French, etc.
  │   └─ Timezone: Select from list
  │
  ├─ Notification Preferences (see Collaboration Flow above)
  │
  ├─ Privacy Preferences
  │   ├─ Profile visibility (public to team, private)
  │   ├─ Task default visibility (personal, team, organization)
  │   └─ Data retention preferences
  │
  ├─→ Save settings → Confirmation → Settings persisted
  │
  ├─→ Reset to defaults → Confirm → Back to default preferences
  │
  ├─ Administrative Controls (admin only)
  │   ├─→ User Management link → [User Management] (future)
  │   ├─→ Team Management link → [Team Management] (future)
  │   └─→ System Settings link → [System Settings] (future)
  │
  └─→ Logout button
       └─→ Confirm → Session terminated → [Login Screen]
```

---

### Team Management Flow (Admin/Team Lead)

```
[Teams]
  │
  ├─ List of teams (current user is member of)
  │
  ├─→ Click team → [Team Details]
  │
  ├─→ "Create Team" button (admin only)
  │     │
  │     ├─ Team name (required, unique)
  │     ├─ Description (optional)
  │     │
  │     ├─→ Create → Team created → [Team Details]
  │     └─→ Cancel → Back to [Teams]
  │
  └─ Filter by: owner, membership status

[Team Details]
  │
  ├─ Team Information
  │   ├─ Name
  │   ├─ Description
  │   ├─ Owner
  │   ├─ Created date
  │   │
  │   └─→ "Edit Team" (owner/admin only)
  │        ├─ Update name, description
  │        ├─→ Save → Update confirmed
  │        └─→ Cancel → Discard edits
  │
  ├─ Members Section
  │   │
  │   ├─ List team members with roles
  │   │
  │   ├─→ "Add Member" button (owner/admin)
  │   │     │
  │   │     ├─ Select user from dropdown
  │   │     ├─ Assign role (Team Lead, Team Member)
  │   │     │
  │   │     ├─→ Add → Member added → Update list
  │   │     └─→ Cancel → Back to member list
  │   │
  │   ├─→ Remove member (owner/admin)
  │   │     └─→ Confirm → Member removed → Update list
  │   │
  │   └─ Show: member name, email, role, joined date
  │
  ├─→ "View Team Tasks" link → [Task List] filtered to team
  │
  └─→ Back to [Teams]
```

---

## Permission-Based Visibility

| Screen | Admin | Team Lead | Team Member | Anonymous |
|--------|-------|-----------|-------------|-----------|
| Login | ✓ | ✓ | ✓ | ✓ |
| Register | ✓ | ✓ | ✓ | ✓ |
| Dashboard | ✓ | ✓ | ✓ | ✗ |
| Task List | ✓ (all) | ✓ (team+own) | ✓ (own+assigned) | ✗ |
| Task Details | ✓ (all) | ✓ (team+own) | ✓ (own+assigned) | ✗ |
| Create Task | ✓ | ✓ | ✓ | ✗ |
| Edit Task | ✓ | ✓ (team+own) | ✓ (own+assigned) | ✗ |
| Delete Task | ✓ | ✗ | ✗ | ✗ |
| Profile | ✓ (own+all) | ✓ (own) | ✓ (own) | ✗ |
| Settings | ✓ (own+all) | ✓ (own) | ✓ (own) | ✗ |
| Teams | ✓ (all) | ✓ (member) | ✓ (member) | ✗ |
| Reports | ✓ (all) | ✓ (team) | ✗ | ✗ |
| Administration | ✓ | ✗ | ✗ | ✗ |

---

## Error & Dependency-Unavailable States

Each screen handles unavailable dependencies gracefully:

```
Scenario: Task database unavailable
  │
  ├─→ Task List: Show "Tasks unavailable, please try again"
  ├─→ Task Details: Show read-only view with "Updates unavailable"
  ├─→ Create Task: Show form with "Save unavailable, try again"
  └─→ Dashboard: Show cached metrics with "Real-time data unavailable"
```

---

## State Transitions & Validation

### Task Status Transitions
```
Todo ──→ In Progress ──→ Review ──→ Completed
  ↓          ↓            ↓           ↓
  └─ Blocked ←──── Blocked ←──── Blocked
```

- From any state → Blocked (temporary hold)
- From Blocked → Previous state or next state (manual reset)
- Cannot bypass states (no Todo → Review)
- Completed tasks locked from editing (non-admin)
- Admin can force any transition

---

## Responsive Behavior

- **Desktop (1024px+):** Full sidebar navigation, multi-column layouts
- **Tablet (768px-1023px):** Collapsed sidebar, stacked layouts, touch-friendly buttons
- **Mobile (< 768px):** Hidden sidebar (hamburger menu), single-column, large touch targets

---

## Related Documents

- [api-specifications.md](api-specifications.md) – API endpoints supporting these flows
- [architecture-design.md](architecture-design.md) – Routing layer design
- Figma Design: https://www.figma.com/make/YnxUzBz6USzrnokLtV4Jd0/Task-Management-System-Screens

---

## Document Control

- **Document ID:** USER-FLOW-001
- **Version:** 1.0
- **Author:** Solution Architect
- **Status:** Ready for UI/UX Developer Handoff
