import { test, expect } from '@playwright/test';

const API_BASE_URL = 'http://localhost:8001/api/v1';

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

test.describe.serial('Dashboard & Reporting API Tests', () => {
  let authToken: string;
  const testEmail = `dashboard-test-${Date.now()}@example.com`;
  const testPassword = 'DashboardTestPass123!';

  test.beforeAll(async () => {
    // Register and login
    await apiCall('POST', '/auth/register', {
      email: testEmail,
      password: testPassword,
      full_name: 'Dashboard Tester',
    });

    const loginResponse = await apiCall('POST', '/auth/login', {
      email: testEmail,
      password: testPassword,
    });
    const loginData = await loginResponse.json();
    authToken = loginData.data?.token || 'unknown';

    // Create multiple tasks for metrics testing
    // Task 1: Completed
    await apiCall('POST', '/tasks', {
      title: 'Completed Task',
      status: 'completed',
      priority: 'high',
    }, authToken);

    // Task 2: In Progress
    await apiCall('POST', '/tasks', {
      title: 'In Progress Task',
      status: 'in_progress',
      priority: 'medium',
    }, authToken);

    // Task 3: Todo (due today)
    const today = new Date();
    today.setHours(23, 59, 59, 999);
    await apiCall('POST', '/tasks', {
      title: 'Due Today Task',
      status: 'todo',
      priority: 'medium',
      due_date: today.toISOString(),
    }, authToken);

    // Task 4: Todo (overdue)
    const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000);
    await apiCall('POST', '/tasks', {
      title: 'Overdue Task',
      status: 'todo',
      priority: 'critical',
      due_date: yesterday.toISOString(),
    }, authToken);

    // Task 5: Todo (future)
    const futureDate = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
    await apiCall('POST', '/tasks', {
      title: 'Future Task',
      status: 'todo',
      priority: 'low',
      due_date: futureDate.toISOString(),
    }, authToken);
  });

  test('GET /dashboard/metrics - should retrieve dashboard metrics', async () => {
    const response = await apiCall('GET', '/dashboard/metrics', undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
    expect(data.data.total_tasks).toBeDefined();
    expect(data.data.completed_tasks).toBeDefined();
    expect(data.data.pending_tasks).toBeDefined();
    expect(data.data.overdue_tasks).toBeDefined();
    expect(data.data.due_today_tasks).toBeDefined();
    expect(data.data.completion_rate).toBeDefined();
  });

  test('GET /dashboard/metrics - should calculate correct metrics', async () => {
    const response = await apiCall('GET', '/dashboard/metrics', undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    const metrics = data.data;

    // Verify metrics calculations
    expect(metrics.total_tasks).toBe(5); // 5 tasks created
    expect(metrics.completed_tasks).toBe(1); // 1 completed
    expect(metrics.pending_tasks).toBe(4); // 4 non-completed
    expect(metrics.overdue_tasks).toBeGreaterThanOrEqual(1); // At least the overdue one
    expect(metrics.due_today_tasks).toBeGreaterThanOrEqual(1); // At least the due today one

    // Verify completion rate
    const expectedRate = (1 / 5) * 100;
    expect(Math.abs(metrics.completion_rate - expectedRate)).toBeLessThan(1);
  });

  test('GET /dashboard/metrics - should fail without authentication', async () => {
    const response = await apiCall('GET', '/dashboard/metrics');

    expect(response.status).toBe(401);
  });

  test('GET /dashboard/metrics - should have numeric metrics', async () => {
    const response = await apiCall('GET', '/dashboard/metrics', undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    const metrics = data.data;

    expect(typeof metrics.total_tasks).toBe('number');
    expect(typeof metrics.completed_tasks).toBe('number');
    expect(typeof metrics.pending_tasks).toBe('number');
    expect(typeof metrics.overdue_tasks).toBe('number');
    expect(typeof metrics.due_today_tasks).toBe('number');
    expect(typeof metrics.completion_rate).toBe('number');

    // Verify non-negative
    expect(metrics.total_tasks).toBeGreaterThanOrEqual(0);
    expect(metrics.completed_tasks).toBeGreaterThanOrEqual(0);
    expect(metrics.pending_tasks).toBeGreaterThanOrEqual(0);
    expect(metrics.overdue_tasks).toBeGreaterThanOrEqual(0);
    expect(metrics.due_today_tasks).toBeGreaterThanOrEqual(0);
    expect(metrics.completion_rate).toBeGreaterThanOrEqual(0);
    expect(metrics.completion_rate).toBeLessThanOrEqual(100);
  });

  test('GET /dashboard/metrics - metrics should sum correctly', async () => {
    const response = await apiCall('GET', '/dashboard/metrics', undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    const metrics = data.data;

    // pending + completed should equal total
    expect(metrics.pending_tasks + metrics.completed_tasks).toBe(metrics.total_tasks);
  });

  test('GET /health - should return healthy status', async () => {
    const response = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/health`);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.status).toBe('healthy');
    expect(data.timestamp).toBeDefined();
  });
});
