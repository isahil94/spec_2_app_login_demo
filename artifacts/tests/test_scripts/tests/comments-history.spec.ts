import { test, expect } from '@playwright/test';

test.describe('Comments and Comment History Edge Cases', () => {
  const mockTaskEmpty = {
    data: {
      taskId: 'task-999',
      title: 'Comment Test Task',
      description: 'Task for comment tests',
      owner: { fullName: 'Owner', email: 'owner@example.com' },
      assignee: null,
      createdAt: new Date().toISOString(),
      dueDate: null,
      status: 'OPEN',
      priority: 'LOW',
      history: [],
      comments: []
    }
  };

  test('should show client-side validation when comment empty', async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => {
      window.localStorage.setItem('authToken', 'dev-token');
      window.localStorage.setItem('authUserId', 'user-1');
      window.localStorage.setItem('authFullName', 'Dev User');
      window.localStorage.setItem('authRole', 'TEAM_MEMBER');
    });

    await page.route('**/api/v1/tasks/task-999', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockTaskEmpty) }));

    await page.goto('/tasks/task-999');
    await expect(page.getByRole('heading', { name: 'Task details' }).first()).toBeVisible();

    // Submit empty comment
    await page.fill('#comment', '   ');
    await page.click('text=Post Comment');

    await expect(page.locator('text=Comment text is required.')).toBeVisible();
  });

  test('should append new comment on successful POST', async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => {
      window.localStorage.setItem('authToken', 'dev-token');
      window.localStorage.setItem('authUserId', 'user-1');
      window.localStorage.setItem('authFullName', 'Dev User');
      window.localStorage.setItem('authRole', 'TEAM_MEMBER');
    });

    // initial GET returns empty comments
    await page.route('**/api/v1/tasks/task-999', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockTaskEmpty) }));

    // intercept POST to return created comment
    await page.route('**/api/v1/tasks/task-999/comments', (route, request) => {
      if (request.method() === 'POST') {
        const created = {
          comment_id: 'c-1',
          content: 'This is a test comment',
          created_at: new Date().toISOString(),
          author: { full_name: 'Dev User', email: 'dev@example.com' }
        };
        route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: created }) });
      } else {
        route.continue();
      }
    });

    await page.goto('/tasks/task-999');
    await page.fill('#comment', 'This is a test comment');
    await page.click('text=Post Comment');

    const commentEl = page.locator('text=This is a test comment').first();
    await expect(commentEl).toBeVisible();
    // check author within the comment card via ancestor lookup
    const author = commentEl.locator('xpath=ancestor::li[1]//p[normalize-space(text())="Dev User"]');
    await expect(author).toBeVisible();
  });

  test('should show error when posting comment fails', async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => {
      window.localStorage.setItem('authToken', 'dev-token');
      window.localStorage.setItem('authUserId', 'user-1');
      window.localStorage.setItem('authFullName', 'Dev User');
      window.localStorage.setItem('authRole', 'TEAM_MEMBER');
    });

    await page.route('**/api/v1/tasks/task-999', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockTaskEmpty) }));

    await page.route('**/api/v1/tasks/task-999/comments', (route, request) => {
      if (request.method() === 'POST') {
        route.fulfill({ status: 500, body: 'Internal Error' });
      } else {
        route.continue();
      }
    });

    await page.goto('/tasks/task-999');
    await page.fill('#comment', 'Will fail');
    await page.click('text=Post Comment');

    await expect(page.locator('text=Unable to post comment.')).toBeVisible();
  });

  test('should display history entries when present', async ({ page }) => {
    const mockWithHistory = JSON.parse(JSON.stringify(mockTaskEmpty));
    mockWithHistory.data.history = [
      { action: 'CREATED', timestamp: new Date().toISOString() },
      { action: 'COMMENT_ADDED', timestamp: new Date().toISOString() }
    ];

    await page.goto('/');
    await page.evaluate(() => {
      window.localStorage.setItem('authToken', 'dev-token');
      window.localStorage.setItem('authUserId', 'user-1');
      window.localStorage.setItem('authFullName', 'Dev User');
      window.localStorage.setItem('authRole', 'TEAM_MEMBER');
    });

    await page.route('**/api/v1/tasks/task-999', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockWithHistory) }));

    await page.goto('/tasks/task-999');
    await expect(page.getByRole('heading', { name: 'History' }).first()).toBeVisible();
    await expect(page.locator('text=CREATED').first()).toBeVisible();
    await expect(page.locator('text=COMMENT ADDED').first()).toBeVisible();
  });
});
