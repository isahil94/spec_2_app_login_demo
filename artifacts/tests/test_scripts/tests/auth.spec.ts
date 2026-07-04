import { test, expect } from '@playwright/test';

const API_BASE_URL = 'http://localhost:8001/api/v1';

// Helper to make API calls
async function apiCall(method: string, endpoint: string, body?: any, token?: string) {
  const headers: any = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  return response;
}

test.describe.serial('Authentication API Tests', () => {
  const testEmail = `test-${Date.now()}@example.com`;
  const testPassword = 'TestPassword123!';
  const testName = 'Test User';
  let authToken: string;
  let userId: string;

  test('POST /auth/register - should register a new user', async () => {
    const response = await apiCall('POST', '/auth/register', {
      email: testEmail,
      password: testPassword,
      full_name: testName,
    });

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
    expect(data.data.email).toBe(testEmail);
    userId = data.data.userId || data.data.user_id || data.data.id;
  });

  test('POST /auth/register - should fail with duplicate email', async () => {
    const response = await apiCall('POST', '/auth/register', {
      email: testEmail,
      password: testPassword,
      full_name: testName,
    });

    expect(response.status).toBe(400);
    const data = await response.json();
    expect(data.error?.code || data.code).toBe('DUPLICATE_RESOURCE');
  });

  test('POST /auth/register - should fail with short password', async () => {
    const response = await apiCall('POST', '/auth/register', {
      email: `short-${Date.now()}@example.com`,
      password: 'short',
      full_name: 'Test User',
    });

    expect([400, 422]).toContain(response.status);
    const data = await response.json();
    if (response.status === 422) {
      // Pydantic validation error - just check it's a validation error
      expect(data.detail || data.error || data.code).toBeDefined();
    } else {
      expect(data.error?.code || data.code).toBe('INVALID_INPUT');
    }
  });

  test('POST /auth/login - should login successfully', async () => {
    const response = await apiCall('POST', '/auth/login', {
      email: testEmail,
      password: testPassword,
      remember_me: false,
    });

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data.token).toBeDefined();
    expect(data.data.user).toBeDefined();
    expect(data.data.user.email).toBe(testEmail);
    expect(data.data.expiresIn || data.data.expires_in).toBeGreaterThan(0);
    authToken = data.data.token;
  });

  test('POST /auth/login - should fail with invalid credentials', async () => {
    const response = await apiCall('POST', '/auth/login', {
      email: testEmail,
      password: 'WrongPassword123!',
      remember_me: false,
    });

    expect(response.status).toBe(401);
    const data = await response.json();
    expect(data.error?.code || data.code).toBe('UNAUTHORIZED');
  });

  test('POST /auth/login - should fail with non-existent email', async () => {
    const response = await apiCall('POST', '/auth/login', {
      email: 'nonexistent@example.com',
      password: testPassword,
      remember_me: false,
    });

    expect(response.status).toBe(401);
    const data = await response.json();
    expect(data.error?.code || data.code).toBe('UNAUTHORIZED');
  });

  test('POST /auth/logout - should logout successfully', async () => {
    const response = await apiCall('POST', '/auth/logout', {}, authToken);
    expect(response.status).toBe(200);
  });
});
