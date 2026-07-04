# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: dependency-unavailable.spec.ts >> AC-028 UI: Dependency-Unavailable States >> Settings page shows loading when settings service unavailable
- Location: tests\dependency-unavailable.spec.ts:59:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('text=Loading settings...')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('text=Loading settings...')

```

```yaml
- paragraph: Current page
- heading "Settings" [level=1]
- button "DT Dependency Tester Team Member":
  - text: DT
  - paragraph: Dependency Tester
  - paragraph: Team Member
- complementary:
  - text: TF
  - paragraph: TaskFlow
  - paragraph: Dependency Tester
  - navigation:
    - link "Dashboard":
      - /url: /dashboard
    - link "Tasks":
      - /url: /tasks
    - link "Profile":
      - /url: /profile
    - link "Settings":
      - /url: /settings
  - paragraph: Sprint Health
  - paragraph: 68%
  - paragraph: On track
  - paragraph: "14"
  - paragraph: Due today
  - button "+ New Task"
  - button "Sign Out"
- main:
  - heading "Dependency unavailable" [level=2]
  - paragraph: Unable to load settings at this time.
```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | 
  3   | const API_BASE_URL = 'http://localhost:8001/api/v1';
  4   | 
  5   | async function apiCall(method: string, endpoint: string, body?: any) {
  6   |   const headers: any = { 'Content-Type': 'application/json' };
  7   |   const response = await fetch(`${API_BASE_URL}${endpoint}`, {
  8   |     method,
  9   |     headers,
  10  |     body: body ? JSON.stringify(body) : undefined,
  11  |   });
  12  |   return response;
  13  | }
  14  | 
  15  | test.describe.serial('AC-028 UI: Dependency-Unavailable States', () => {
  16  |   let userId: string;
  17  |   const email = `dep-test-${Date.now()}@example.com`;
  18  |   const password = 'DepTestPass123!';
  19  |   const fullName = 'Dependency Tester';
  20  | 
  21  |   test.beforeAll(async () => {
  22  |     const r = await apiCall('POST', '/auth/register', { email, password, full_name: fullName });
  23  |     const jr = await r.json();
  24  |     userId = jr.data?.userId || jr.data?.user_id || jr.data?.id;
  25  | 
  26  |     const login = await apiCall('POST', '/auth/login', { email, password });
  27  |     const lj = await login.json();
  28  |     const token = lj.data?.token;
  29  | 
  30  |     // Persist auth to localStorage format used by the app
  31  |     // Tests will set on the page before navigation
  32  |     test.info().annotations.push({ type: 'note', description: `userId=${userId}` });
  33  |     (global as any)._dep_test = { token, userId, fullName };
  34  |   });
  35  | 
  36  |   test('Profile page falls back to authFullName when profile service unavailable', async ({ page }) => {
  37  |     // Initialize auth state in localStorage so the app boots authenticated
  38  |     const { token, userId, fullName } = (global as any)._dep_test;
  39  |     await page.goto('/');
  40  |     await page.evaluate(({ token, userId, fullName }) => {
  41  |       window.localStorage.setItem('authToken', token);
  42  |       window.localStorage.setItem('authUserId', userId);
  43  |       window.localStorage.setItem('authFullName', fullName);
  44  |       window.localStorage.setItem('authRole', 'TEAM_MEMBER');
  45  |     }, { token, userId, fullName });
  46  | 
  47  |     // Intercept profile GET to simulate dependency failure and navigate
  48  |     await page.route('**/api/v1/users/*/profile', (route) => {
  49  |       route.fulfill({ status: 503, body: 'Service Unavailable' });
  50  |     });
  51  | 
  52  |     await page.goto('/profile');
  53  | 
  54  |     // Wait for profile heading to render and then assert fallback full name is visible in header
  55  |     await expect(page.getByRole('heading', { name: 'Profile' }).first()).toBeVisible();
  56  |     await expect(page.locator(`text=${fullName}`).first()).toBeVisible();
  57  |   });
  58  | 
  59  |   test('Settings page shows loading when settings service unavailable', async ({ page }) => {
  60  |     const { token, userId, fullName } = (global as any)._dep_test;
  61  |     await page.goto('/');
  62  |     await page.evaluate(({ token, userId, fullName }) => {
  63  |       window.localStorage.setItem('authToken', token);
  64  |       window.localStorage.setItem('authUserId', userId);
  65  |       window.localStorage.setItem('authFullName', fullName);
  66  |       window.localStorage.setItem('authRole', 'TEAM_MEMBER');
  67  |     }, { token, userId, fullName });
  68  | 
  69  |     await page.route('**/api/v1/users/*/settings', (route) => {
  70  |       route.fulfill({ status: 503, body: 'Service Unavailable' });
  71  |     });
  72  | 
  73  |     await page.goto('/settings');
  74  | 
  75  |     // The page should still show the loading state or not crash
> 76  |     await expect(page.locator('text=Loading settings...')).toBeVisible();
      |                                                            ^ Error: expect(locator).toBeVisible() failed
  77  |   });
  78  | 
  79  |   test('Settings save failure shows graceful error message', async ({ page }) => {
  80  |     const { token, userId, fullName } = (global as any)._dep_test;
  81  |     await page.goto('/');
  82  |     await page.evaluate(({ token, userId, fullName }) => {
  83  |       window.localStorage.setItem('authToken', token);
  84  |       window.localStorage.setItem('authUserId', userId);
  85  |       window.localStorage.setItem('authFullName', fullName);
  86  |       window.localStorage.setItem('authRole', 'TEAM_MEMBER');
  87  |     }, { token, userId, fullName });
  88  | 
  89  |     await page.route('**/api/v1/users/*/settings', (route, request) => {
  90  |       if (request.method() === 'PATCH') {
  91  |         route.fulfill({ status: 500, body: 'Internal Error' });
  92  |       } else {
  93  |         route.continue();
  94  |       }
  95  |     });
  96  | 
  97  |     await page.goto('/settings');
  98  | 
  99  |     // Wait for settings to load
  100 |     await expect(page.locator('text=Theme')).toBeVisible();
  101 | 
  102 |     // Click Save Settings and expect graceful message
  103 |     await page.getByRole('button', { name: 'Save Settings' }).click();
  104 |     await expect(page.locator('text=Unable to save settings at this time.')).toBeVisible();
  105 |   });
  106 | });
  107 | 
```