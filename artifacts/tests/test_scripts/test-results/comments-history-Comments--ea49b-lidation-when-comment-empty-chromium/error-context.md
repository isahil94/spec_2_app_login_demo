# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: comments-history.spec.ts >> Comments and Comment History Edge Cases >> should show client-side validation when comment empty
- Location: tests\comments-history.spec.ts:20:3

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: page.click: Test timeout of 30000ms exceeded.
Call log:
  - waiting for locator('text=Post Comment')
    - locator resolved to <button type="submit" class="rounded-2xl bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-400">Post Comment</button>
  - attempting click action
    - waiting for element to be visible, enabled and stable
    - element is not stable
  - retrying click action
    - waiting for element to be visible, enabled and stable
    - element is visible, enabled and stable
    - scrolling into view if needed
    - done scrolling
    - element is outside of the viewport
  - retrying click action
    - waiting 20ms
    2 × waiting for element to be visible, enabled and stable
      - element is not stable
    - retrying click action
      - waiting 100ms
    - waiting for" http://localhost:4173/login" navigation to finish...
    - navigated to "http://localhost:4173/login"
    - waiting for element to be visible, enabled and stable
  - element was detached from the DOM, retrying

```

# Page snapshot

```yaml
- generic [ref=e4]:
  - complementary [ref=e5]:
    - generic [ref=e7]:
      - generic [ref=e8]:
        - generic [ref=e9]: TF
        - generic [ref=e10]:
          - paragraph [ref=e11]: TaskFlow
          - paragraph [ref=e12]: Modern task management for teams.
      - generic [ref=e13]:
        - heading "Work smarter together." [level=1] [ref=e14]
        - paragraph [ref=e15]: Collaborate across teams, manage priorities, and keep every task moving with clarity.
    - generic [ref=e16]:
      - generic [ref=e17]:
        - paragraph [ref=e18]: 68%
        - paragraph [ref=e19]: Team alignment score
      - generic [ref=e20]:
        - paragraph [ref=e21]: "14"
        - paragraph [ref=e22]: Tasks due today
    - generic [ref=e23]:
      - paragraph [ref=e24]: Built for fast onboarding
      - generic [ref=e25]:
        - generic [ref=e26]: Task List
        - generic [ref=e27]: Task Detail
        - generic [ref=e28]: Profile
  - generic [ref=e31]:
    - generic [ref=e32]:
      - heading "Welcome back" [level=1] [ref=e33]
      - paragraph [ref=e34]: Sign in to continue to your task workspace.
    - generic [ref=e35]:
      - generic [ref=e36]:
        - generic [ref=e37]: Email Address
        - textbox "you@example.com" [ref=e39]
      - generic [ref=e40]:
        - generic [ref=e41]: Password
        - textbox "Enter your password" [ref=e43]
      - generic [ref=e44]:
        - button "Sign In" [ref=e45] [cursor=pointer]
        - generic [ref=e46]:
          - link "Forgot password?" [ref=e47] [cursor=pointer]:
            - /url: /forgot-password
          - link "Create account" [ref=e48] [cursor=pointer]:
            - /url: /register
```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | 
  3   | test.describe('Comments and Comment History Edge Cases', () => {
  4   |   const mockTaskEmpty = {
  5   |     data: {
  6   |       taskId: 'task-999',
  7   |       title: 'Comment Test Task',
  8   |       description: 'Task for comment tests',
  9   |       owner: { fullName: 'Owner', email: 'owner@example.com' },
  10  |       assignee: null,
  11  |       createdAt: new Date().toISOString(),
  12  |       dueDate: null,
  13  |       status: 'OPEN',
  14  |       priority: 'LOW',
  15  |       history: [],
  16  |       comments: []
  17  |     }
  18  |   };
  19  | 
  20  |   test('should show client-side validation when comment empty', async ({ page }) => {
  21  |     await page.goto('/');
  22  |     await page.evaluate(() => {
  23  |       window.localStorage.setItem('authToken', 'dev-token');
  24  |       window.localStorage.setItem('authUserId', 'user-1');
  25  |       window.localStorage.setItem('authFullName', 'Dev User');
  26  |       window.localStorage.setItem('authRole', 'TEAM_MEMBER');
  27  |     });
  28  | 
  29  |     await page.route('**/api/v1/tasks/task-999', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockTaskEmpty) }));
  30  | 
  31  |     await page.goto('/tasks/task-999');
  32  |     await expect(page.getByRole('heading', { name: 'Task details' }).first()).toBeVisible();
  33  | 
  34  |     // Submit empty comment
  35  |     await page.fill('#comment', '   ');
> 36  |     await page.click('text=Post Comment');
      |                ^ Error: page.click: Test timeout of 30000ms exceeded.
  37  | 
  38  |     await expect(page.locator('text=Comment text is required.')).toBeVisible();
  39  |   });
  40  | 
  41  |   test('should append new comment on successful POST', async ({ page }) => {
  42  |     await page.goto('/');
  43  |     await page.evaluate(() => {
  44  |       window.localStorage.setItem('authToken', 'dev-token');
  45  |       window.localStorage.setItem('authUserId', 'user-1');
  46  |       window.localStorage.setItem('authFullName', 'Dev User');
  47  |       window.localStorage.setItem('authRole', 'TEAM_MEMBER');
  48  |     });
  49  | 
  50  |     // initial GET returns empty comments
  51  |     await page.route('**/api/v1/tasks/task-999', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockTaskEmpty) }));
  52  | 
  53  |     // intercept POST to return created comment
  54  |     await page.route('**/api/v1/tasks/task-999/comments', (route, request) => {
  55  |       if (request.method() === 'POST') {
  56  |         const created = {
  57  |           comment_id: 'c-1',
  58  |           content: 'This is a test comment',
  59  |           created_at: new Date().toISOString(),
  60  |           author: { full_name: 'Dev User', email: 'dev@example.com' }
  61  |         };
  62  |         route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: created }) });
  63  |       } else {
  64  |         route.continue();
  65  |       }
  66  |     });
  67  | 
  68  |     await page.goto('/tasks/task-999');
  69  |     await page.fill('#comment', 'This is a test comment');
  70  |     await page.click('text=Post Comment');
  71  | 
  72  |     const commentEl = page.locator('text=This is a test comment').first();
  73  |     await expect(commentEl).toBeVisible();
  74  |     // check author within the comment card via ancestor lookup
  75  |     const author = commentEl.locator('xpath=ancestor::li[1]//p[normalize-space(text())="Dev User"]');
  76  |     await expect(author).toBeVisible();
  77  |   });
  78  | 
  79  |   test('should show error when posting comment fails', async ({ page }) => {
  80  |     await page.goto('/');
  81  |     await page.evaluate(() => {
  82  |       window.localStorage.setItem('authToken', 'dev-token');
  83  |       window.localStorage.setItem('authUserId', 'user-1');
  84  |       window.localStorage.setItem('authFullName', 'Dev User');
  85  |       window.localStorage.setItem('authRole', 'TEAM_MEMBER');
  86  |     });
  87  | 
  88  |     await page.route('**/api/v1/tasks/task-999', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockTaskEmpty) }));
  89  | 
  90  |     await page.route('**/api/v1/tasks/task-999/comments', (route, request) => {
  91  |       if (request.method() === 'POST') {
  92  |         route.fulfill({ status: 500, body: 'Internal Error' });
  93  |       } else {
  94  |         route.continue();
  95  |       }
  96  |     });
  97  | 
  98  |     await page.goto('/tasks/task-999');
  99  |     await page.fill('#comment', 'Will fail');
  100 |     await page.click('text=Post Comment');
  101 | 
  102 |     await expect(page.locator('text=Unable to post comment.')).toBeVisible();
  103 |   });
  104 | 
  105 |   test('should display history entries when present', async ({ page }) => {
  106 |     const mockWithHistory = JSON.parse(JSON.stringify(mockTaskEmpty));
  107 |     mockWithHistory.data.history = [
  108 |       { action: 'CREATED', timestamp: new Date().toISOString() },
  109 |       { action: 'COMMENT_ADDED', timestamp: new Date().toISOString() }
  110 |     ];
  111 | 
  112 |     await page.goto('/');
  113 |     await page.evaluate(() => {
  114 |       window.localStorage.setItem('authToken', 'dev-token');
  115 |       window.localStorage.setItem('authUserId', 'user-1');
  116 |       window.localStorage.setItem('authFullName', 'Dev User');
  117 |       window.localStorage.setItem('authRole', 'TEAM_MEMBER');
  118 |     });
  119 | 
  120 |     await page.route('**/api/v1/tasks/task-999', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockWithHistory) }));
  121 | 
  122 |     await page.goto('/tasks/task-999');
  123 |     await expect(page.getByRole('heading', { name: 'History' }).first()).toBeVisible();
  124 |     await expect(page.locator('text=CREATED').first()).toBeVisible();
  125 |     await expect(page.locator('text=COMMENT ADDED').first()).toBeVisible();
  126 |   });
  127 | });
  128 | 
```