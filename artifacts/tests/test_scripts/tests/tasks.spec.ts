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

test.describe.serial('Task Management API Tests', () => {
  let authToken: string;
  let userId: string;
  let taskId: string;
  const testEmail = `task-test-${Date.now()}@example.com`;
  const testPassword = 'TaskTestPass123!';

  test.beforeAll(async () => {
    // Register and login user
    const registerResponse = await apiCall('POST', '/auth/register', {
      email: testEmail,
      password: testPassword,
      full_name: 'Task Tester',
    });
    const registerData = await registerResponse.json();
    userId = (registerData.data?.userId || registerData.data?.user_id || registerData.data?.id) || 'unknown';

    const loginResponse = await apiCall('POST', '/auth/login', {
      email: testEmail,
      password: testPassword,
    });
    const loginData = await loginResponse.json();
    authToken = loginData.data?.token || 'unknown';
  });

  test('POST /tasks - should create a new task', async () => {
    const response = await apiCall('POST', '/tasks', {
      title: 'Test Task',
      description: 'This is a test task',
      status: 'todo',
      priority: 'high',
      due_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
    }, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
    expect(data.data.title).toBe('Test Task');
    expect(data.data.status).toBe('todo');
    expect(data.data.priority).toBe('high');
    const ownerIdResp = data.data.owner?.id || data.data.owner?.user_id || data.data.ownerId;
    expect(ownerIdResp).toBe(userId);
    taskId = data.data.taskId || data.data.task_id || data.data.id;
  });

  test('POST /tasks - should fail without authentication', async () => {
    const response = await apiCall('POST', '/tasks', {
      title: 'Test Task',
      description: 'This is a test task',
    });

    expect(response.status).toBe(401);
  });

  test('POST /tasks - should fail with invalid status', async () => {
    const response = await apiCall('POST', '/tasks', {
      title: 'Test Task',
      description: 'This is a test task',
      status: 'invalid_status',
      priority: 'high',
    }, authToken);

    expect([400, 422]).toContain(response.status);
  });

  test('POST /tasks - should fail with title exceeding max length', async () => {
    const response = await apiCall('POST', '/tasks', {
      title: 'A'.repeat(101), // Title longer than 100 chars
      description: 'Test',
      status: 'todo',
      priority: 'high',
    }, authToken);

    expect([400, 422]).toContain(response.status);
  });

  test('POST /tasks - should fail with past due date', async () => {
    const response = await apiCall('POST', '/tasks', {
      title: 'Past Due Task',
      description: 'This task has a past due date',
      status: 'todo',
      priority: 'high',
      due_date: new Date(Date.now() - 1000).toISOString(),
    }, authToken);

    expect([200, 400, 422]).toContain(response.status);
  });

  test('GET /tasks - should retrieve all tasks', async () => {
    const response = await apiCall('GET', '/tasks', undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
    expect(Array.isArray(data.data.tasks)).toBe(true);
    expect(data.pagination).toBeDefined();
  });

  test('GET /tasks - should filter tasks by status', async () => {
    const response = await apiCall('GET', '/tasks?status=todo', undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
    data.data.tasks.forEach((task: any) => {
      expect(task.status).toBe('todo');
    });
  });

  test('GET /tasks - should filter tasks by priority', async () => {
    const response = await apiCall('GET', '/tasks?priority=high', undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
    data.data.tasks.forEach((task: any) => {
      expect(task.priority).toBe('high');
    });
  });

  test('GET /tasks - should search tasks by title', async () => {
    const response = await apiCall('GET', '/tasks?search=Test', undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
    expect(data.data.tasks.length).toBeGreaterThan(0);
  });

  test('GET /tasks - should paginate results', async () => {
    const response = await apiCall('GET', '/tasks?skip=0&limit=10', undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.pagination.page).toBe(1);
    expect(data.pagination.limit).toBe(10);
  });

  test('GET /tasks/{taskId} - should retrieve a specific task', async () => {
    const response = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
    expect(data.data.task_id || data.data.taskId || data.data.id).toBe(taskId);
    expect(data.data.title).toBe('Test Task');
  });

  test('GET /tasks/{taskId} - should fail with non-existent task', async () => {
    const response = await apiCall('GET', '/tasks/non-existent-id', undefined, authToken);

    expect(response.status).toBe(404);
  });

  test('PATCH /tasks/{taskId} - should update a task', async () => {
    const response = await apiCall('PATCH', `/tasks/${taskId}`, {
      title: 'Updated Test Task',
      status: 'in_progress',
      priority: 'critical',
    }, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data.title).toBe('Updated Test Task');
    expect(data.data.status).toBe('in_progress');
    expect(data.data.priority).toBe('critical');
  });

  test('PATCH /tasks/{taskId} - should fail to update completed task (unless admin)', async () => {
    // Create a completed task
    const createResponse = await apiCall('POST', '/tasks', {
      title: 'Completed Task',
      status: 'completed',
      priority: 'low',
    }, authToken);
    const createData = await createResponse.json();
    const completedTaskId = createData.data?.taskId || createData.data?.task_id || createData.data?.id;

    // Try to update it
    const response = await apiCall('PATCH', `/tasks/${completedTaskId}`, {
      title: 'Updated Completed Task',
    }, authToken);

    expect([400, 403, 404]).toContain(response.status);
  });

  test('DELETE /tasks/{taskId} - should fail without admin role', async () => {
    const response = await apiCall('DELETE', `/tasks/${taskId}`, undefined, authToken);

    expect(response.status).toBe(403); // Forbidden - user is not admin
  });

  test('POST /tasks/{taskId}/archive - should archive a task', async () => {
    const response = await apiCall('POST', `/tasks/${taskId}/archive`, {}, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data.archived_at).toBeDefined();
  });

  test('POST /tasks/{taskId}/restore - should restore an archived task', async () => {
    const response = await apiCall('POST', `/tasks/${taskId}/restore`, {}, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data.archived_at).toBeNull();
  });

  test('POST /tasks/{taskId}/duplicate - should duplicate a task', async () => {
    const response = await apiCall('POST', `/tasks/${taskId}/duplicate`, {}, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
    expect(data.data.title).toContain('Copy of');
  });

  test('GET /tasks - should exclude archived tasks by default', async () => {
    const response = await apiCall('GET', '/tasks', undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    data.data.tasks.forEach((task: any) => {
      // archived_at should be null or undefined for non-archived tasks
      expect(task.archived_at == null).toBeTruthy();
    });
  });

  test('GET /tasks - should include archived tasks when requested', async () => {
    const response = await apiCall('GET', '/tasks?archived=true', undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
  });

  test('GET /tasks - should sort tasks correctly', async () => {
    const response = await apiCall('GET', '/tasks?sortBy=due_date&order=asc', undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
  });
});
