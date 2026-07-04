import { test, expect } from '@playwright/test';

const API_BASE_URL = 'http://localhost:8001/api/v1';

async function createTestUser(request: any, email: string, password: string) {
  const response = await request.post(`${API_BASE_URL}/auth/register`, {
    data: {
      email,
      password,
      full_name: 'Session Landing Tester',
    },
  });

  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  return body.data;
}

test.describe.serial('Session & Landing Page Behavior', () => {
  const testEmail = `landing-test-${Date.now()}@example.com`;
  const testPassword = 'LandingTestPass123!';
  let userId: string;

  async function loginAsUser(page: any) {
    await page.goto('/login');
    await page.locator('input[type="email"]').fill(testEmail);
    await page.locator('input[type="password"]').fill(testPassword);
    await page.locator('button', { hasText: /sign in/i }).click();
    await expect(page).toHaveURL(/\/dashboard$/);
    await expect(page.locator('h1', { hasText: 'Dashboard' })).toBeVisible();
  }

  test.beforeAll(async ({ request }) => {
    const user = await createTestUser(request, testEmail, testPassword);
    userId = user.userId || user.user_id || user.id;
  });

  test('should redirect unauthenticated root to /login', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveURL(/\/login$/);
  });

  test('should login and redirect to dashboard', async ({ page }) => {
    await loginAsUser(page);
    const authToken = await page.evaluate(() => window.localStorage.getItem('authToken'));
    expect(authToken).toBeTruthy();
  });

  test('should preserve session and redirect root to dashboard after refresh', async ({ page }) => {
    await loginAsUser(page);
    await page.goto('/dashboard');
    await expect(page).toHaveURL(/\/dashboard$/);
    await page.reload();
    await expect(page).toHaveURL(/\/dashboard$/);
  });

  test('should redirect authenticated root access to /dashboard', async ({ page }) => {
    await loginAsUser(page);
    await page.goto('/');
    await expect(page).toHaveURL(/\/dashboard$/);
  });

  test('should sign out automatically when the dashboard request returns an expired token error', async ({ page }) => {
    await loginAsUser(page);

    await page.route('**/api/v1/dashboard/metrics', async (route) => {
      await route.fulfill({
        status: 401,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Invalid or expired token' }),
      });
    });

    await page.reload();
    await expect(page).toHaveURL(/\/login$/);

    const authToken = await page.evaluate(() => window.localStorage.getItem('authToken'));
    const authUserId = await page.evaluate(() => window.localStorage.getItem('authUserId'));
    const authRole = await page.evaluate(() => window.localStorage.getItem('authRole'));

    expect(authToken).toBeNull();
    expect(authUserId).toBeNull();
    expect(authRole).toBeNull();
  });

  test('should logout and redirect to login, clearing session state', async ({ page }) => {
    await loginAsUser(page);
    await page.locator('button', { hasText: /sign out/i }).click();
    await expect(page).toHaveURL(/\/login$/);

    const authToken = await page.evaluate(() => window.localStorage.getItem('authToken'));
    expect(authToken).toBeNull();

    await page.goto('/dashboard');
    await expect(page).toHaveURL(/\/login$/);
  });
});
