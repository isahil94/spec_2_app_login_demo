import { test, expect } from '@playwright/test';

const API_BASE_URL = 'http://localhost:8001/api/v1';

async function apiCall(method: string, endpoint: string, body?: any) {
  const headers: any = { 'Content-Type': 'application/json' };
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  return response;
}

test.describe.serial('AC-028 UI: Dependency-Unavailable States', () => {
  let userId: string;
  const email = `dep-test-${Date.now()}@example.com`;
  const password = 'DepTestPass123!';
  const fullName = 'Dependency Tester';

  test.beforeAll(async () => {
    const r = await apiCall('POST', '/auth/register', { email, password, full_name: fullName });
    const jr = await r.json();
    userId = jr.data?.userId || jr.data?.user_id || jr.data?.id;

    const login = await apiCall('POST', '/auth/login', { email, password });
    const lj = await login.json();
    const token = lj.data?.token;

    // Persist auth to localStorage format used by the app
    // Tests will set on the page before navigation
    test.info().annotations.push({ type: 'note', description: `userId=${userId}` });
    (global as any)._dep_test = { token, userId, fullName };
  });

  test('Profile page falls back to authFullName when profile service unavailable', async ({ page }) => {
    // Initialize auth state in localStorage so the app boots authenticated
    const { token, userId, fullName } = (global as any)._dep_test;
    await page.goto('/');
    await page.evaluate(({ token, userId, fullName }) => {
      window.localStorage.setItem('authToken', token);
      window.localStorage.setItem('authUserId', userId);
      window.localStorage.setItem('authFullName', fullName);
      window.localStorage.setItem('authRole', 'TEAM_MEMBER');
    }, { token, userId, fullName });

    // Intercept profile GET to simulate dependency failure and navigate
    await page.route('**/api/v1/users/*/profile', (route) => {
      route.fulfill({ status: 503, body: 'Service Unavailable' });
    });

    await page.goto('/profile');

    // Wait for profile heading to render and then assert fallback full name is visible in header
    await expect(page.getByRole('heading', { name: 'Profile' }).first()).toBeVisible();
    await expect(page.locator(`text=${fullName}`).first()).toBeVisible();
  });

  test('Settings page shows loading when settings service unavailable', async ({ page }) => {
    const { token, userId, fullName } = (global as any)._dep_test;
    await page.goto('/');
    await page.evaluate(({ token, userId, fullName }) => {
      window.localStorage.setItem('authToken', token);
      window.localStorage.setItem('authUserId', userId);
      window.localStorage.setItem('authFullName', fullName);
      window.localStorage.setItem('authRole', 'TEAM_MEMBER');
    }, { token, userId, fullName });

    await page.route('**/api/v1/users/*/settings', (route) => {
      route.fulfill({ status: 503, body: 'Service Unavailable' });
    });

    await page.goto('/settings');

    // The page should still show the loading state or not crash
    await expect(page.locator('text=Loading settings...')).toBeVisible();
  });

  test('Settings save failure shows graceful error message', async ({ page }) => {
    const { token, userId, fullName } = (global as any)._dep_test;
    await page.goto('/');
    await page.evaluate(({ token, userId, fullName }) => {
      window.localStorage.setItem('authToken', token);
      window.localStorage.setItem('authUserId', userId);
      window.localStorage.setItem('authFullName', fullName);
      window.localStorage.setItem('authRole', 'TEAM_MEMBER');
    }, { token, userId, fullName });

    await page.route('**/api/v1/users/*/settings', (route, request) => {
      if (request.method() === 'PATCH') {
        route.fulfill({ status: 500, body: 'Internal Error' });
      } else {
        route.continue();
      }
    });

    await page.goto('/settings');

    // Wait for settings to load
    await expect(page.locator('text=Theme')).toBeVisible();

    // Click Save Settings and expect graceful message
    await page.getByRole('button', { name: 'Save Settings' }).click();
    await expect(page.locator('text=Unable to save settings at this time.')).toBeVisible();
  });
});
