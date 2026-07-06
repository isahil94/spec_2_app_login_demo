# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: team-and-history.spec.ts >> Team membership and Task history UI tests >> Task details shows dependency-unavailable when task service fails
- Location: tests\team-and-history.spec.ts:82:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('text=Dependency unavailable')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('text=Dependency unavailable')

```

```yaml
- complementary:
  - text: TF
  - paragraph: TaskFlow
  - paragraph: Modern task management for teams.
  - heading "Work smarter together." [level=1]
  - paragraph: Collaborate across teams, manage priorities, and keep every task moving with clarity.
  - paragraph: 68%
  - paragraph: Team alignment score
  - paragraph: "14"
  - paragraph: Tasks due today
  - paragraph: Built for fast onboarding
  - text: Task List Task Detail Profile
- heading "Welcome back" [level=1]
- paragraph: Sign in to continue to your task workspace.
- text: Email Address
- textbox "you@example.com"
- text: Password
- textbox "Enter your password"
- button "Sign In"
- link "Forgot password?":
  - /url: /forgot-password
- link "Create account":
  - /url: /register
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Team membership and Task history UI tests', () => {
  4  |   const mockTeam = {
  5  |     data: { teams: [
  6  |       { teamId: 'team-1', name: 'Alpha Team', description: 'Testing team', owner: { fullName: 'Owner One', email: 'owner@example.com' }, memberCount: 3 }
  7  |     ] }
  8  |   };
  9  | 
  10 |   const mockTask = {
  11 |     data: {
  12 |       taskId: 'task-123',
  13 |       title: 'Test Task',
  14 |       description: 'A task used in tests',
  15 |       owner: { fullName: 'Owner One', email: 'owner@example.com' },
  16 |       assignee: null,
  17 |       createdAt: new Date().toISOString(),
  18 |       dueDate: null,
  19 |       status: 'OPEN',
  20 |       priority: 'MEDIUM',
  21 |       history: [
  22 |         { action: 'CREATED', timestamp: new Date().toISOString() },
  23 |         { action: 'UPDATED_DESCRIPTION', timestamp: new Date().toISOString() }
  24 |       ],
  25 |       comments: []
  26 |     }
  27 |   };
  28 | 
  29 |   test('Teams page displays mocked team and member count', async ({ page }) => {
  30 |     // Seed auth via localStorage to avoid UI login flow
  31 |     await page.goto('/');
  32 |     // create a fake authenticated user
  33 |     await page.evaluate(() => {
  34 |       window.localStorage.setItem('authToken', 'dev-token');
  35 |       window.localStorage.setItem('authUserId', 'user-1');
  36 |       window.localStorage.setItem('authFullName', 'Dev User');
  37 |       window.localStorage.setItem('authRole', 'ADMIN');
  38 |     });
  39 | 
  40 |     // Mock teams API
  41 |     await page.route('**/api/v1/teams', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockTeam) }));
  42 | 
  43 |     await page.goto('/teams');
  44 |     await expect(page.getByRole('heading', { name: 'Teams' }).first()).toBeVisible();
  45 |     await expect(page.locator('text=Alpha Team').first()).toBeVisible();
  46 |     await expect(page.locator('text=Members:').first()).toBeVisible();
  47 |     await expect(page.locator('text=3').first()).toBeVisible();
  48 |   });
  49 | 
  50 |   test('Task details page shows history entries', async ({ page }) => {
  51 |     await page.goto('/');
  52 |     await page.evaluate(() => {
  53 |       window.localStorage.setItem('authToken', 'dev-token');
  54 |       window.localStorage.setItem('authUserId', 'user-1');
  55 |       window.localStorage.setItem('authFullName', 'Dev User');
  56 |       window.localStorage.setItem('authRole', 'TEAM_MEMBER');
  57 |     });
  58 | 
  59 |     // Mock task detail API
  60 |     await page.route('**/api/v1/tasks/task-123', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockTask) }));
  61 | 
  62 |     await page.goto('/tasks/task-123');
  63 |     await expect(page.getByRole('heading', { name: 'History' }).first()).toBeVisible();
  64 |     await expect(page.locator('text=CREATED').first()).toBeVisible();
  65 |     await expect(page.locator('text=UPDATED DESCRIPTION').first()).toBeVisible();
  66 |   });
  67 | 
  68 |   test('Teams page shows dependency-unavailable banner when API fails', async ({ page }) => {
  69 |     await page.goto('/');
  70 |     await page.evaluate(() => {
  71 |       window.localStorage.setItem('authToken', 'dev-token');
  72 |       window.localStorage.setItem('authUserId', 'user-1');
  73 |       window.localStorage.setItem('authFullName', 'Dev User');
  74 |       window.localStorage.setItem('authRole', 'TEAM_MEMBER');
  75 |     });
  76 | 
  77 |     await page.route('**/api/v1/teams', (route) => route.fulfill({ status: 503, body: 'Service Unavailable' }));
  78 |     await page.goto('/teams');
  79 |     await expect(page.locator('text=Dependency unavailable')).toBeVisible();
  80 |   });
  81 | 
  82 |   test('Task details shows dependency-unavailable when task service fails', async ({ page }) => {
  83 |     await page.goto('/');
  84 |     await page.evaluate(() => {
  85 |       window.localStorage.setItem('authToken', 'dev-token');
  86 |       window.localStorage.setItem('authUserId', 'user-1');
  87 |       window.localStorage.setItem('authFullName', 'Dev User');
  88 |       window.localStorage.setItem('authRole', 'TEAM_MEMBER');
  89 |     });
  90 | 
  91 |     await page.route('**/api/v1/tasks/task-404', (route) => route.fulfill({ status: 500, body: 'Internal Error' }));
  92 |     await page.goto('/tasks/task-404');
> 93 |     await expect(page.locator('text=Dependency unavailable')).toBeVisible();
     |                                                               ^ Error: expect(locator).toBeVisible() failed
  94 |   });
  95 | });
  96 | 
```