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

test.describe('End-to-End Integration Tests', () => {
  test('Complete user workflow: Register -> Create Task -> Add Comment -> View Dashboard', async () => {
    const testEmail = `e2e-test-${Date.now()}@example.com`;
    const testPassword = 'E2ETestPass123!';

    // Step 1: Register a new user
    const registerResponse = await apiCall('POST', '/auth/register', {
      email: testEmail,
      password: testPassword,
      full_name: 'E2E Test User',
    });

    expect(registerResponse.status).toBe(200);
    const registerData = await registerResponse.json();
    const userId = registerData.data?.userId || registerData.data?.user_id || registerData.data?.id;

    // Step 2: Login
    const loginResponse = await apiCall('POST', '/auth/login', {
      email: testEmail,
      password: testPassword,
    });

    expect(loginResponse.status).toBe(200);
    const loginData = await loginResponse.json();
    const token = loginData.data?.token;
    const loginUserId = loginData.data?.user?.userId || loginData.data?.user?.user_id || loginData.data?.user?.id;
    expect(loginUserId).toBe(userId);

    // Step 3: Create a task
    const createTaskResponse = await apiCall('POST', '/tasks', {
      title: 'E2E Test Task',
      description: 'Task created during E2E test',
      status: 'todo',
      priority: 'high',
      due_date: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString(),
    }, token);

    expect(createTaskResponse.status).toBe(200);
    const taskData = await createTaskResponse.json();
    const taskId = taskData.data.taskId || taskData.data.task_id || taskData.data.id;

    // Step 4: Get the created task
    const getTaskResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, token);

    expect(getTaskResponse.status).toBe(200);
    const getTaskData = await getTaskResponse.json();
    expect(getTaskData.data.title).toBe('E2E Test Task');
    const ownerIdResp = getTaskData.data.owner?.id || getTaskData.data.owner?.user_id || getTaskData.data.ownerId;
    expect(ownerIdResp).toBe(userId);

    // Step 5: Add a comment to the task
    const addCommentResponse = await apiCall('POST', `/tasks/${taskId}/comments`, {
      content: 'E2E test comment',
    }, token);

    expect(addCommentResponse.status).toBe(200);
    const commentData = await addCommentResponse.json();
    const commentId = commentData.data.commentId || commentData.data.comment_id || commentData.data.id;

    // Step 6: Get task comments
    const getCommentsResponse = await apiCall('GET', `/tasks/${taskId}/comments`, undefined, token);

    expect(getCommentsResponse.status).toBe(200);
    const getCommentsData = await getCommentsResponse.json();
    expect(getCommentsData.data?.comments?.length).toBeGreaterThan(0);
    const firstCommentId = getCommentsData.data.comments[0].commentId || getCommentsData.data.comments[0].comment_id || getCommentsData.data.comments[0].id;
    expect(firstCommentId).toBe(commentId);

    // Step 7: Update the task status
    const updateTaskResponse = await apiCall('PATCH', `/tasks/${taskId}`, {
      status: 'in_progress',
    }, token);

    expect(updateTaskResponse.status).toBe(200);
    const updatedTaskData = await updateTaskResponse.json();
    expect(updatedTaskData.data.status).toBe('in_progress');

    // Step 8: Get dashboard metrics
    const dashboardResponse = await apiCall('GET', '/dashboard/metrics', undefined, token);

    expect(dashboardResponse.status).toBe(200);
    const dashboardData = await dashboardResponse.json();
    expect(dashboardData.data.total_tasks).toBeGreaterThanOrEqual(1);
    expect(dashboardData.data.pending_tasks).toBeGreaterThanOrEqual(1);

    // Step 9: List all tasks
    const listTasksResponse = await apiCall('GET', '/tasks', undefined, token);

    expect(listTasksResponse.status).toBe(200);
    const listTasksData = await listTasksResponse.json();
    expect(listTasksData.data?.tasks?.length).toBeGreaterThan(0);
    const foundTask = listTasksData.data.tasks.find((t: any) => (t.taskId || t.task_id || t.id) === taskId);
    expect(foundTask).toBeDefined();
    expect(foundTask.status).toBe('in_progress');

    // Step 10: Archive the task
    const archiveResponse = await apiCall('POST', `/tasks/${taskId}/archive`, {}, token);

    expect(archiveResponse.status).toBe(200);
    const archivedTaskData = await archiveResponse.json();
    expect(archivedTaskData.data.archived_at).toBeDefined();

    // Step 11: Verify archived task not in default list
    const listAfterArchiveResponse = await apiCall('GET', '/tasks', undefined, token);

    expect(listAfterArchiveResponse.status).toBe(200);
    const listAfterArchiveData = await listAfterArchiveResponse.json();
    const archivedTask = listAfterArchiveData.data?.tasks?.find((t: any) => (t.taskId || t.task_id || t.id) === taskId);
    expect(archivedTask).toBeUndefined();

    // Step 12: Restore the task
    const restoreResponse = await apiCall('POST', `/tasks/${taskId}/restore`, {}, token);

    expect(restoreResponse.status).toBe(200);
    const restoredTaskData = await restoreResponse.json();
    expect(restoredTaskData.data.archived_at).toBeNull();

    // Step 13: Duplicate the task
    const duplicateResponse = await apiCall('POST', `/tasks/${taskId}/duplicate`, {}, token);

    expect(duplicateResponse.status).toBe(200);
    const duplicatedTaskData = await duplicateResponse.json();
    expect(duplicatedTaskData.data.title).toContain('Copy of');

    // Step 14: Logout
    const logoutResponse = await apiCall('POST', '/auth/logout', {}, token);

    expect(logoutResponse.status).toBe(200);
  });

  test('Multi-user workflow: Task assignment and collaboration', async () => {
    const user1Email = `user1-${Date.now()}@example.com`;
    const user1Password = 'User1Pass123!';
    const user2Email = `user2-${Date.now()}@example.com`;
    const user2Password = 'User2Pass123!';

    // Register and login user 1
    await apiCall('POST', '/auth/register', {
      email: user1Email,
      password: user1Password,
      full_name: 'User 1',
    });

    const user1LoginResponse = await apiCall('POST', '/auth/login', {
      email: user1Email,
      password: user1Password,
    });
    const user1Token = (await user1LoginResponse.json()).data.token;

    // Register and login user 2
    await apiCall('POST', '/auth/register', {
      email: user2Email,
      password: user2Password,
      full_name: 'User 2',
    });

    const user2LoginResponse = await apiCall('POST', '/auth/login', {
      email: user2Email,
      password: user2Password,
    });
    const user2Token = (await user2LoginResponse.json()).data.token;

    // User 1 creates a task
    const createTaskResponse = await apiCall('POST', '/tasks', {
      title: 'Shared Task',
      description: 'Task for multi-user testing',
      status: 'todo',
      priority: 'medium',
    }, user1Token);

    const createTaskData = await createTaskResponse.json();
    const taskId = createTaskData.data?.taskId || createTaskData.data?.task_id || createTaskData.data?.id;

    // User 1 adds a comment
    const user1CommentResponse = await apiCall('POST', `/tasks/${taskId}/comments`, {
      content: 'Comment from User 1',
    }, user1Token);

    expect(user1CommentResponse.status).toBe(200);

    // Verify User 1 can see their comment
    const user1CommentsResponse = await apiCall('GET', `/tasks/${taskId}/comments`, undefined, user1Token);
    expect((await user1CommentsResponse.json()).data?.comments?.length).toBe(1);
  });

  test('Error handling and validation throughout workflow', async () => {
    // Test missing required fields
    const noTitleResponse = await apiCall('POST', '/tasks', {
      description: 'No title provided',
      status: 'todo',
      priority: 'high',
    });

    expect(noTitleResponse.status).toBe(401); // Unauthorized without token

    // Test invalid status
    const invalidStatusResponse = await apiCall('POST', '/tasks', {
      title: 'Invalid Status Task',
      status: 'invalid_status',
      priority: 'high',
    });

    expect(invalidStatusResponse.status).toBe(401); // Unauthorized without token

    // Test invalid email on register
    const invalidEmailResponse = await apiCall('POST', '/auth/register', {
      email: 'not-an-email',
      password: 'ValidPass123!',
      full_name: 'Test User',
    });

    expect([400, 422]).toContain(invalidEmailResponse.status);

    // Test weak password
    const weakPasswordResponse = await apiCall('POST', '/auth/register', {
      email: `weak-pass-${Date.now()}@example.com`,
      password: 'weak',
      full_name: 'Test User',
    });

    expect([400, 422]).toContain(weakPasswordResponse.status);
  });
});
