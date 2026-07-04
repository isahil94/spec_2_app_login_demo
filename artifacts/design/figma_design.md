# Figma Design Reference — TaskFlow

> Reconstructed from the `.make` export and the exported source tree. This document captures the business-facing design system, screens, interactions, and validation patterns found in the application source.

## Brand & Visual Intent

- Product name: **TaskFlow**
- Brand voice: modern productivity, team collaboration, and clarity.
- Core visual mood: clean enterprise SaaS with bright blue accents, soft card surfaces, and calm neutral backgrounds.
- Auth page uses a split-screen marketing-centric hero panel plus a focused form card.
- Workspace screens use a persistent sidebar, a top utility bar, and content-first cards.

## Design Tokens

### Primary palette

| Token | Purpose | Value |
|---|---|---|
| `--primary` | Primary action and accent | `#2563eb` |
| `--primary-foreground` | Text/icon on primary surfaces | `#ffffff` |
| `--secondary` | Secondary highlights and backgrounds | `#eff6ff` |
| `--secondary-foreground` | Secondary text/icon | `#1e40af` |
| `--accent` | Highlight states and subtle surfaces | `#dbeafe` |
| `--accent-foreground` | Accent text/icon | `#1e40af` |
| `--destructive` | Negative actions and errors | `#dc2626` |
| `--destructive-foreground` | Destructive text/icon | `#ffffff` |

### Neutral surfaces

| Token | Purpose | Value |
|---|---|---|
| `--background` | Page background | `#f0f4ff` |
| `--foreground` | Primary text color | `#0f172a` |
| `--card` | Card/background surface | `#ffffff` |
| `--card-foreground` | Card text color | `#0f172a` |
| `--popover` | Popover/modal background | `#ffffff` |
| `--border` | Border strokes | `rgba(15, 23, 42, 0.08)` |
| `--muted` | Secondary surface | `#f1f5f9` |
| `--muted-foreground` | Secondary text | `#64748b` |

### Sidebar / dark theme palette

| Token | Purpose | Light value | Dark value |
|---|---|---|---|
| `--sidebar` | Sidebar background | `oklch(0.985 0 0)` | `oklch(0.205 0 0)` |
| `--sidebar-foreground` | Sidebar text | `oklch(0.145 0 0)` | `oklch(0.985 0 0)` |
| `--sidebar-primary` | Sidebar accent | `#030213` | `oklch(0.488 0.243 264.376)` |
| `--sidebar-border` | Sidebar border | `oklch(0.922 0 0)` | `oklch(0.269 0 0)` |

### Utility tokens

| Token | Purpose | Value |
|---|---|---|
| `--input` | Input overlay | `transparent` |
| `--input-background` | Input field surface | `#f8fafc` |
| `--switch-background` | Toggle background | `#cbd5e1` |
| `--ring` | Focus / validation ring | `#2563eb` |
| `--radius` | Corner radius base | `0.75rem` |
| `--font-weight-medium` | Medium text weight | `500` |
| `--font-weight-normal` | Normal text weight | `400` |

### Data visualization tokens

| Token | Purpose | Value |
|---|---|---|
| `--chart-1` | Chart color 1 | `oklch(0.646 0.222 41.116)` |
| `--chart-2` | Chart color 2 | `oklch(0.6 0.118 184.704)` |
| `--chart-3` | Chart color 3 | `oklch(0.398 0.07 227.392)` |
| `--chart-4` | Chart color 4 | `oklch(0.828 0.189 84.429)` |
| `--chart-5` | Chart color 5 | `oklch(0.769 0.188 70.08)` |

## Typography

- Primary fonts: **Inter**, **Plus Jakarta Sans**.
- Base text size is `16px`.
- Headings and brand labels use **Plus Jakarta Sans**.
- Body and form text use **Inter**.

## Screen Inventory

### Authentication flow

- **Login**: email, password, remember me, forgot password, sign in action.
- **Register**: full name, work email, password, confirm password, terms acceptance, create account action.
- **Auth layout**: split-screen hero panel with marketing metrics, testimonial, and brand lockup.

### Workspace flow

- **Task list**: search, status/priority filters, sort, list/kanban toggle, row selection, pagination.
- **Task detail**: task metadata, description, attachments, comments, activity history, edit/delete, status selector.
- **Create/edit task**: title, description, status, priority, project, labels, assignees, due date, attachments.
- **User profile**: profile summary, contact info, activity snapshot, heatmap.
- **Settings**: tabbed general, appearance, notifications, security, integrations.

## Unauthenticated Access Behavior

- Unauthenticated users see only the auth screens and cannot access the workspace sidebar or task content.
- Sign-in and registration are separate entry points within the same auth layout.

## Default Route Behavior

- The product entry point is the auth flow.
- After authentication, the default workspace entry is the task experience with sidebar navigation.

## Interaction Patterns & Validation

### Sign-in / registration

- Email fields use native browser email validation.
- Password fields support toggle visibility.
- Registration submission is blocked if terms are not accepted.
- Confirm password shows an error when non-empty and not matching password.
- Password strength is displayed as empty, Weak, Fair, or Strong based on length.
- Submit buttons show a loading spinner while processing.

### Task creation / edit

- Required fields: title, status, priority, at least one assignee, due date.
- Title must be non-empty after trimming.
- At least one assignee must be selected.
- Due date must be selected.
- Labels can be added by typing a trimmed value and pressing Add.
- Save action shows success feedback: button text changes to `Saved!`.
- Past due date is flagged with warning text when selected.

### Task list

- Search filters tasks by title and project.
- Filters support all statuses and all priorities.
- Sort options include due date, priority, and status.
- Toggle between list view and kanban view.
- Row selection supports page-level select all.
- Pagination is explicit with page numbers and next/previous controls.

### Task detail & comments

- Comment submission is blocked for empty trimmed comments.
- Attachments surface file type icons and removable items.
- Delete task requires explicit confirmation.
- Activity history is presented as a timeline.

## Component Palette

### Form primitives

- `InputField`: label, icon, optional right action, inline error state.
- `FormSelect`: dropdown with placeholder, icon, inline error state.
- `FormTextarea`: multiline description field with error support.
- `FormLabel`: label with required indicator.
- `FormSection`: grouped section header.

### Content primitives

- `Card`: grouped content panel.
- `Badge`: status/priority/pill indicator.
- `Avatar`: initial-based user badge.

### Layout primitives

- `AuthLayout`: split auth screen wrapper.
- `AuthLeftPanel`: marketing side panel for auth flow.
- `Sidebar`: workspace navigation.
- `TopNav`: workspace actions and utilities.

### Icons

- `IcoTask`, `IcoHome`, `IcoList`, `IcoCalendar`, `IcoTeam`, `IcoAnalytics`, `IcoSettings`, `IcoBell`, `IcoSearch`, `IcoPlus`, `IcoEdit`, `IcoTrash`, `IcoAttach`, `IcoComment`, `IcoCopy`, `IcoSend`, `IcoLink`, `IcoFlag`, `IcoCheck`, `IcoChevron`, `IcoChevronLeft`, `IcoEye`, `IcoLock`, `IcoEmail`, `IcoGoogle`, `IcoHistory`, `IcoTrend`, `IcoUpload`, `IcoX`, `IcoDown`.

## Layout & Surface Patterns

- Auth uses a hero panel with gradient and layered graphical accents.
- Workspace uses cards, side panels, and a top bar for task/dashboard screens.
- Input fields are rounded with soft borders and focus ring highlight.
- Status chips and tags are small rounded pills.

## Notes from Source

- The auth panel emphasizes metrics and a testimonial for product value.
- Task create/edit supports new and edit modes with inline validation summary.
- Date input is browser-native and shows contextual due-date status.
- Assignees are selectable cards with selected-state styling.
- Task list offers both kanban and table/list workflows.

## Validation Patterns Detected

- Required field checks for task title and comments using trimmed input.
- Native email validation for email fields.
- Password strength from length thresholds: empty, <6, <10, >=10.
- Confirm password mismatch shown on non-empty confirmation.
- Submit buttons enter a loading state while processing.
- Validation summary banner appears when task save fields fail.

## Source Files

- `artifacts/design/source/src/styles/theme.css`
- `artifacts/design/source/src/styles/fonts.css`
- `artifacts/design/source/src/app/App.tsx`
