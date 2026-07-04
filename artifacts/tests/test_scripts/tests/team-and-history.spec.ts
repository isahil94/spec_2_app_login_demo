import { test, expect } from '@playwright/test';

test.describe('Team membership and Task history UI tests', () => {
  const mockTeam = {
    data: { teams: [
      { teamId: 'team-1', name: 'Alpha Team', description: 'Testing team', owner: { fullName: 'Owner One', email: 'owner@example.com' }, memberCount: 3 }
    ] }
  };

  const mockTask = {
    data: {
      taskId: 'task-123',
      title: 'Test Task',
      description: 'A task used in tests',
      owner: { fullName: 'Owner One', email: 'owner@example.com' },
      assignee: null,
      createdAt: new Date().toISOString(),
      dueDate: null,
      status: 'OPEN',
      priority: 'MEDIUM',
      history: [
        { action: 'CREATED', timestamp: new Date().toISOString() },
        { action: 'UPDATED_DESCRIPTION', timestamp: new Date().toISOString() }
      ],
      comments: []
    }
  };

  test('Teams page displays mocked team and member count', async ({ page }) => {
    // Seed auth via localStorage to avoid UI login flow
    await page.goto('/');
    // create a fake authenticated user
    await page.evaluate(() => {
      window.localStorage.setItem('authToken', 'dev-token');
      window.localStorage.setItem('authUserId', 'user-1');
      window.localStorage.setItem('authFullName', 'Dev User');
      window.localStorage.setItem('authRole', 'ADMIN');
    });

    // Mock teams API
    await page.route('**/api/v1/teams', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockTeam) }));

    await page.goto('/teams');
    await expect(page.getByRole('heading', { name: 'Teams' }).first()).toBeVisible();
    await expect(page.locator('text=Alpha Team').first()).toBeVisible();
    await expect(page.locator('text=Members:').first()).toBeVisible();
    await expect(page.locator('text=3').first()).toBeVisible();
  });

  test('Task details page shows history entries', async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => {
      window.localStorage.setItem('authToken', 'dev-token');
      window.localStorage.setItem('authUserId', 'user-1');
      window.localStorage.setItem('authFullName', 'Dev User');
      window.localStorage.setItem('authRole', 'TEAM_MEMBER');
    });

    // Mock task detail API
    await page.route('**/api/v1/tasks/task-123', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockTask) }));

    await page.goto('/tasks/task-123');
    await expect(page.getByRole('heading', { name: 'History' }).first()).toBeVisible();
    await expect(page.locator('text=CREATED').first()).toBeVisible();
    await expect(page.locator('text=UPDATED DESCRIPTION').first()).toBeVisible();
  });

  test('Teams page shows dependency-unavailable banner when API fails', async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => {
      window.localStorage.setItem('authToken', 'dev-token');
      window.localStorage.setItem('authUserId', 'user-1');
      window.localStorage.setItem('authFullName', 'Dev User');
      window.localStorage.setItem('authRole', 'TEAM_MEMBER');
    });

    await page.route('**/api/v1/teams', (route) => route.fulfill({ status: 503, body: 'Service Unavailable' }));
    await page.goto('/teams');
    await expect(page.locator('text=Dependency unavailable')).toBeVisible();
  });

  test('Task details shows dependency-unavailable when task service fails', async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => {
      window.localStorage.setItem('authToken', 'dev-token');
      window.localStorage.setItem('authUserId', 'user-1');
      window.localStorage.setItem('authFullName', 'Dev User');
      window.localStorage.setItem('authRole', 'TEAM_MEMBER');
    });

    await page.route('**/api/v1/tasks/task-404', (route) => route.fulfill({ status: 500, body: 'Internal Error' }));
    await page.goto('/tasks/task-404');
    await expect(page.locator('text=Dependency unavailable')).toBeVisible();
  });
});
