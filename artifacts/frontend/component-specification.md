# Component Specification

## Purpose
Describe the reusable UI components required to implement the workflow screens and states.

## Metadata
- Version: 1.0
- Author: UI/UX Developer
- Date: 2026-07-04
- Status: Draft
- Artifact ID: COMP-SPEC-001
- Source References: artifacts/requirements/user_stories.md, artifacts/requirements/acceptance_criteria.md, artifacts/architecture/module-design.md

## Component Inventory

### AuthForm
- Purpose: Collect login or registration credentials.
- Inputs: email, password, optional full name and recovery controls.
- States: default, validation error, loading, success, dependency-unavailable.
- Accessibility: labeled fields, keyboard support, error summaries.

### TaskCard
- Purpose: Display a task summary in a list.
- Inputs: title, status, priority, due date, assignee, owner.
- States: default, selected, archived, completed, blocked, empty.

### TaskForm
- Purpose: Create or edit a task.
- Inputs: title, description, status, priority, due date, assignee, team.
- Validation: required title, valid due date, allowed status and priority values.
- States: editing, validation error, save success, dependency-unavailable.

### MetricsPanel
- Purpose: Show dashboard summary metrics.
- Inputs: task counts and workload values.
- States: populated, empty, permission-restricted, dependency-unavailable.

### FilterBar
- Purpose: Support search, filter, and sort controls.
- Inputs: search query, status, priority, assignee, due date, team, sort option.
- States: active filters, no results, dependency-unavailable.

### ActivityFeed
- Purpose: Present comments, attachments, and activity history.
- Inputs: task activity entries.
- States: populated, empty, permission-restricted, loading, error.

### EmptyState / DependencyUnavailableState
- Purpose: Explain missing content or unavailable dependencies without misleading the user.
- Use across list, dashboard, reports, profile, and settings screens.

### ProtectedRouteGate
- Purpose: Enforce authentication and role-based access at the route level.
- Behavior: show nothing sensitive for unauthenticated users and route them to the public entry experience.
