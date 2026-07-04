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

test.describe.serial('Collaboration & Comments API Tests', () => {
  let authToken: string;
  let taskId: string;
  let commentId: string;
  const testEmail = `collab-test-${Date.now()}@example.com`;
  const testPassword = 'CollabTestPass123!';

  test.beforeAll(async () => {
    // Register and login
    await apiCall('POST', '/auth/register', {
      email: testEmail,
      password: testPassword,
      full_name: 'Collaboration Tester',
    });

    const loginResponse = await apiCall('POST', '/auth/login', {
      email: testEmail,
      password: testPassword,
    });
    const loginData = await loginResponse.json();
    authToken = loginData.data?.token || 'unknown';

    // Create a task
    const taskResponse = await apiCall('POST', '/tasks', {
      title: 'Collaboration Test Task',
      description: 'Task for testing comments',
      status: 'todo',
      priority: 'medium',
    }, authToken);
    const taskData = await taskResponse.json();
    taskId = taskData.data.taskId || taskData.data.task_id || taskData.data.id;
  });

  test('POST /tasks/{taskId}/comments - should add a comment', async () => {
    const response = await apiCall('POST', `/tasks/${taskId}/comments`, {
      content: 'This is a test comment',
    }, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
    expect(data.data.content).toBe('This is a test comment');
    expect(data.data.author).toBeDefined();
    commentId = data.data.commentId || data.data.comment_id || data.data.id;
  });

  test('POST /tasks/{taskId}/comments - should fail with empty content', async () => {
    const response = await apiCall('POST', `/tasks/${taskId}/comments`, {
      content: '',
    }, authToken);

    expect([400, 422]).toContain(response.status);
  });

  test('POST /tasks/{taskId}/comments - should fail without authentication', async () => {
    const response = await apiCall('POST', `/tasks/${taskId}/comments`, {
      content: 'Unauthorized comment',
    });

    expect(response.status).toBe(401);
  });

  test('GET /tasks/{taskId}/comments - should retrieve task comments', async () => {
    const response = await apiCall('GET', `/tasks/${taskId}/comments`, undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
    expect(Array.isArray(data.data?.comments)).toBe(true);
    expect(data.pagination).toBeDefined();
    expect(data.data?.comments?.length).toBeGreaterThan(0);
  });

  test('GET /tasks/{taskId}/comments - should paginate comments', async () => {
    const response = await apiCall('GET', `/tasks/${taskId}/comments?page=1&limit=10`, undefined, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.pagination.page).toBe(1);
    expect(data.pagination.limit).toBe(10);
  });

  test('PATCH /tasks/{taskId}/comments/{commentId} - should update a comment', async () => {
    const response = await apiCall('PATCH', `/tasks/${taskId}/comments/${commentId}`, {
      content: 'Updated test comment',
    }, authToken);

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data.content).toBe('Updated test comment');
  });

  test('PATCH /tasks/{taskId}/comments/{commentId} - should fail with non-author', async () => {
    // Create another user
    const anotherEmail = `another-${Date.now()}@example.com`;
    const anotherPassword = 'AnotherPass123!';

    await apiCall('POST', '/auth/register', {
      email: anotherEmail,
      password: anotherPassword,
      full_name: 'Another User',
    });

    const anotherLoginResponse = await apiCall('POST', '/auth/login', {
      email: anotherEmail,
      password: anotherPassword,
    });
    const anotherLoginData = await anotherLoginResponse.json();
    const anotherToken = anotherLoginData.data.token;

    // Try to update the comment
    const response = await apiCall('PATCH', `/tasks/${taskId}/comments/${commentId}`, {
      content: 'Unauthorized update',
    }, anotherToken);

    expect(response.status).toBe(403);
  });

  test('DELETE /tasks/{taskId}/comments/{commentId} - should delete a comment', async () => {
    // Create a comment to delete
    const createResponse = await apiCall('POST', `/tasks/${taskId}/comments`, {
      content: 'Comment to be deleted',
    }, authToken);
    const createData = await createResponse.json();
    const commentToDeleteId = createData.data.commentId || createData.data.comment_id || createData.data.id;

    // Delete the comment
    const response = await apiCall('DELETE', `/tasks/${taskId}/comments/${commentToDeleteId}`, undefined, authToken);

    expect(response.status).toBe(200);
  });

  test('DELETE /tasks/{taskId}/comments/{commentId} - should fail with non-author', async () => {
    // Create another user
    const anotherEmail = `another2-${Date.now()}@example.com`;
    const anotherPassword = 'AnotherPass123!';

    await apiCall('POST', '/auth/register', {
      email: anotherEmail,
      password: anotherPassword,
      full_name: 'Another User 2',
    });

    const anotherLoginResponse = await apiCall('POST', '/auth/login', {
      email: anotherEmail,
      password: anotherPassword,
    });
    const anotherLoginData = await anotherLoginResponse.json();
    const anotherToken = anotherLoginData.data.token;

    // Try to delete the comment
    const response = await apiCall('DELETE', `/tasks/${taskId}/comments/${commentId}`, undefined, anotherToken);

    expect(response.status).toBe(403);
  });

  test('GET /tasks/{taskId}/comments - should fail for non-existent task', async () => {
    const response = await apiCall('GET', '/tasks/non-existent-task-id/comments', undefined, authToken);

    expect(response.status).toBe(404);
  });
});
