# User Flow Specification

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-06
- Status: Draft
- Architecture ID: ARCH-007
- Workflow ID: WF-20260705-001
- Correlation ID: WF-1783283413777
- Traceability: screen_specification.md, user_stories.md

## Route and Flow Map
| Screen | Route | Auth Required | Primary API Domain | State Transition Notes |
|---|---|---:|---|---|
| Login | /login | No | Authentication | Redirects authenticated users to dashboard |
| Register | /register | No | Authentication | Returns to login on success or validation failure |
| Dashboard | /dashboard | Yes | Dashboard and task summary | Loads summary metrics and recent activity |
| Task List | /tasks | Yes | Task listing and search | Supports filters, sorting, and task selection |
| Task Details | /tasks/{id} | Yes | Task and collaboration | Supports edit, archive, restore, and history views |
| Create Task | /tasks/new | Yes | Task creation | Navigates to details on save |
| Edit Task | /tasks/{id}/edit | Yes | Task update | Requires editable task state |
| Profile | /profile | Yes | Profile and settings | Supports profile updates and password change |
| Settings | /settings | Yes | Profile and settings | Supports notification and preference updates |
| User Management | /admin/users | Yes | Administration | Restricted to authorized roles |
| Team Management | /admin/teams | Yes | Administration | Restricted to authorized roles |
| Notifications | /notifications | Yes | Notification service | Shows unread and recent notification state |
| Reports | /reports | Yes | Reporting service | Restricted to authorized roles |

## Workflow Notes
- Authentication paths use guarded routes and explicit unauthenticated state handling.
- Task flows preserve navigation context when validation, permission, or dependency failures occur.
- Admin and reporting flows require role-aware route guards and clear access-denied states.
- Empty, error, and dependency-unavailable states remain user-visible and consistent with BA acceptance criteria.
