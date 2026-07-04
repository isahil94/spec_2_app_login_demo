import { test, expect, Page } from '@playwright/test';

const API_BASE_URL = 'http://localhost:8001/api/v1';

interface ApiResponse {
  data?: any;
  error?: any;
}

async function apiCall(
  method: string,
  endpoint: string,
  body?: any,
  token?: string
): Promise<Response> {
  const headers: Record<string, string> = {
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

test.describe('Task Persistence and Comment Integration Tests', () => {
  let testEmail: string;
  let testPassword: string;
  let testUserId: string;
  let authToken: string;
  let taskId: string;

  test.beforeAll(async () => {
    // Generate unique test credentials
    testEmail = `e2e-test-${Date.now()}@example.com`;
    testPassword = 'E2ETestPass123!SecurePassword';

    // Register a new test user
    const registerResponse = await apiCall('POST', '/auth/register', {
      email: testEmail,
      password: testPassword,
      full_name: 'E2E Test User',
    });

    expect(registerResponse.status).toBe(200);
    const registerData: ApiResponse = await registerResponse.json();
    testUserId = registerData.data?.userId || registerData.data?.user_id;
    expect(testUserId).toBeTruthy();
  });

  test.beforeEach(async () => {
    // Login before each test
    const loginResponse = await apiCall('POST', '/auth/login', {
      email: testEmail,
      password: testPassword,
    });

    expect(loginResponse.status).toBe(200);
    const loginData: ApiResponse = await loginResponse.json();
    authToken = loginData.data?.token;
    expect(authToken).toBeTruthy();
  });

  test('should create a task and persist to database', async () => {
    const taskTitle = `Task ${Date.now()}`;
    const taskDescription = 'This task is created via E2E test and persisted to DB';

    const createResponse = await apiCall(
      'POST',
      '/tasks',
      {
        title: taskTitle,
        description: taskDescription,
        status: 'todo',
        priority: 'high',
        due_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
      },
      authToken
    );

    expect(createResponse.status).toBe(200);
    const createData: ApiResponse = await createResponse.json();
    taskId = createData.data?.taskId || createData.data?.task_id;
    expect(taskId).toBeTruthy();
    expect(createData.data?.title).toBe(taskTitle);
    expect(createData.data?.description).toBe(taskDescription);
    expect(createData.data?.status).toBe('todo');

    // Verify task was persisted by fetching it
    const getResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
    expect(getResponse.status).toBe(200);
    const getData: ApiResponse = await getResponse.json();
    expect(getData.data?.title).toBe(taskTitle);
    expect(getData.data?.description).toBe(taskDescription);
  });

  test('should add a comment and persist to database', async () => {
    // First, create a task
    const createTaskResponse = await apiCall(
      'POST',
      '/tasks',
      {
        title: `Comment Test Task ${Date.now()}`,
        description: 'Task for comment persistence test',
        status: 'todo',
        priority: 'medium',
      },
      authToken
    );

    expect(createTaskResponse.status).toBe(200);
    const taskData: ApiResponse = await createTaskResponse.json();
    taskId = taskData.data?.taskId || taskData.data?.task_id;
    expect(taskId).toBeTruthy();

    // Add a comment
    const commentContent = `Comment created at ${new Date().toISOString()}`;
    const addCommentResponse = await apiCall(
      'POST',
      `/tasks/${taskId}/comments`,
      { content: commentContent },
      authToken
    );

    expect(addCommentResponse.status).toBe(200);
    const commentData: ApiResponse = await addCommentResponse.json();
    const commentId = commentData.data?.commentId || commentData.data?.comment_id;
    expect(commentId).toBeTruthy();
    expect(commentData.data?.content).toBe(commentContent);

    // Verify comment was persisted by fetching task details
    const getTaskResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
    expect(getTaskResponse.status).toBe(200);
    const getTaskData: ApiResponse = await getTaskResponse.json();

    const comments = getTaskData.data?.comments || [];
    expect(comments.length).toBeGreaterThan(0);

    const persistedComment = comments.find(
      (c: any) => (c.commentId || c.comment_id) === commentId
    );
    expect(persistedComment).toBeTruthy();
    expect(persistedComment?.content).toBe(commentContent);
  });

  test('should add multiple comments and retrieve in order', async () => {
    // Create a task
    const createTaskResponse = await apiCall(
      'POST',
      '/tasks',
      {
        title: `Multi-Comment Task ${Date.now()}`,
        description: 'Task for testing multiple comments',
        status: 'in_progress',
        priority: 'medium',
      },
      authToken
    );

    expect(createTaskResponse.status).toBe(200);
    taskId = (await createTaskResponse.json()).data?.taskId;
    expect(taskId).toBeTruthy();

    // Add multiple comments
    const comments = [
      'First comment - Initial investigation',
      'Second comment - Found the root cause',
      'Third comment - Working on the fix',
    ];

    const commentIds: string[] = [];

    for (const comment of comments) {
      const addResponse = await apiCall(
        'POST',
        `/tasks/${taskId}/comments`,
        { content: comment },
        authToken
      );

      expect(addResponse.status).toBe(200);
      const data: ApiResponse = await addResponse.json();
      const cId = data.data?.commentId || data.data?.comment_id;
      commentIds.push(cId);
    }

    // Fetch all comments and verify order and content
    const getCommentsResponse = await apiCall(
      'GET',
      `/tasks/${taskId}/comments`,
      undefined,
      authToken
    );

    expect(getCommentsResponse.status).toBe(200);
    const commentsData: ApiResponse = await getCommentsResponse.json();
    const retrievedComments = commentsData.data?.comments || [];

    // Verify all comments were persisted
    expect(retrievedComments.length).toBeGreaterThanOrEqual(comments.length);

    // Verify comments are in order
    comments.forEach((comment, index) => {
      const retrieved = retrievedComments.find(
        (c: any) => (c.commentId || c.comment_id) === commentIds[index]
      );
      expect(retrieved).toBeTruthy();
      expect(retrieved?.content).toBe(comment);
    });
  });

  test('should update task status and persist changes', async () => {
    // Create a task
    const createResponse = await apiCall(
      'POST',
      '/tasks',
      {
        title: `Status Update Task ${Date.now()}`,
        description: 'Task for testing status updates',
        status: 'todo',
        priority: 'low',
      },
      authToken
    );

    expect(createResponse.status).toBe(200);
    taskId = (await createResponse.json()).data?.taskId;
    expect(taskId).toBeTruthy();

    // Update status to in_progress
    const updateResponse = await apiCall(
      'PATCH',
      `/tasks/${taskId}`,
      { status: 'in_progress' },
      authToken
    );

    expect(updateResponse.status).toBe(200);
    const updateData: ApiResponse = await updateResponse.json();
    expect(updateData.data?.status).toBe('in_progress');

    // Verify status change was persisted
    const getResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
    expect(getResponse.status).toBe(200);
    const getData: ApiResponse = await getResponse.json();
    expect(getData.data?.status).toBe('in_progress');

    // Update to completed
    const completeResponse = await apiCall(
      'PATCH',
      `/tasks/${taskId}`,
      { status: 'completed' },
      authToken
    );

    expect(completeResponse.status).toBe(200);
    const completeData: ApiResponse = await completeResponse.json();
    expect(completeData.data?.status).toBe('completed');

    // Verify final status
    const finalGetResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
    expect(finalGetResponse.status).toBe(200);
    const finalData: ApiResponse = await finalGetResponse.json();
    expect(finalData.data?.status).toBe('completed');
  });

  test('should track task history with comments and status changes', async () => {
    // Create task
    const createResponse = await apiCall(
      'POST',
      '/tasks',
      {
        title: `History Test Task ${Date.now()}`,
        description: 'Task for testing history tracking',
        status: 'todo',
        priority: 'high',
      },
      authToken
    );

    expect(createResponse.status).toBe(200);
    taskId = (await createResponse.json()).data?.taskId;

    // Add a comment
    const commentResponse = await apiCall(
      'POST',
      `/tasks/${taskId}/comments`,
      { content: 'Initial progress update' },
      authToken
    );
    expect(commentResponse.status).toBe(200);

    // Change status
    const statusResponse = await apiCall(
      'PATCH',
      `/tasks/${taskId}`,
      { status: 'in_progress' },
      authToken
    );
    expect(statusResponse.status).toBe(200);

    // Add another comment
    const comment2Response = await apiCall(
      'POST',
      `/tasks/${taskId}/comments`,
      { content: 'Almost done with the implementation' },
      authToken
    );
    expect(comment2Response.status).toBe(200);

    // Fetch task with full history
    const getResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
    expect(getResponse.status).toBe(200);
    const getData: ApiResponse = await getResponse.json();

    // Verify all updates were tracked
    expect(getData.data?.status).toBe('in_progress');
    expect(getData.data?.comments?.length).toBeGreaterThanOrEqual(2);
    expect(getData.data?.history).toBeTruthy();
  });

  test('should persist task and comments across multiple API calls', async () => {
    // Create a task
    const taskTitle = `Persistence Test ${Date.now()}`;
    const createResponse = await apiCall(
      'POST',
      '/tasks',
      {
        title: taskTitle,
        description: 'Task for testing data persistence across calls',
        status: 'todo',
        priority: 'medium',
      },
      authToken
    );

    expect(createResponse.status).toBe(200);
    taskId = (await createResponse.json()).data?.taskId;

    // Simulate multiple API interactions
    const interactions = [
      {
        action: 'update_priority',
        body: { priority: 'high' },
        comment: 'Priority increased',
      },
      {
        action: 'update_status',
        body: { status: 'in_progress' },
        comment: 'Started working on this',
      },
      {
        action: 'update_priority',
        body: { priority: 'critical' },
        comment: 'This is now critical',
      },
    ];

    for (const interaction of interactions) {
      // Update task
      const updateResponse = await apiCall(
        'PATCH',
        `/tasks/${taskId}`,
        interaction.body,
        authToken
      );
      expect(updateResponse.status).toBe(200);

      // Add comment
      if (interaction.comment) {
        const commentResponse = await apiCall(
          'POST',
          `/tasks/${taskId}/comments`,
          { content: interaction.comment },
          authToken
        );
        expect(commentResponse.status).toBe(200);
      }
    }

    // Verify all changes were persisted
    const finalResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
    expect(finalResponse.status).toBe(200);
    const finalData: ApiResponse = await finalResponse.json();

    expect(finalData.data?.title).toBe(taskTitle);
    expect(finalData.data?.priority).toBe('critical');
    expect(finalData.data?.status).toBe('in_progress');
    expect(finalData.data?.comments?.length).toBeGreaterThanOrEqual(3);
  });

  test('should handle comment updates and persist changes', async () => {
    // Create task
    const createResponse = await apiCall(
      'POST',
      '/tasks',
      {
        title: `Comment Update Test ${Date.now()}`,
        description: 'Task for testing comment updates',
        status: 'todo',
        priority: 'low',
      },
      authToken
    );

    expect(createResponse.status).toBe(200);
    taskId = (await createResponse.json()).data?.taskId;

    // Add initial comment
    const addResponse = await apiCall(
      'POST',
      `/tasks/${taskId}/comments`,
      { content: 'Original comment text' },
      authToken
    );

    expect(addResponse.status).toBe(200);
    const commentId = (await addResponse.json()).data?.commentId;

    // Update the comment
    const updatedContent = 'Updated comment text with more details';
    const updateResponse = await apiCall(
      'PATCH',
      `/tasks/${taskId}/comments/${commentId}`,
      { content: updatedContent },
      authToken
    );

    expect(updateResponse.status).toBe(200);
    const updateData: ApiResponse = await updateResponse.json();
    expect(updateData.data?.content).toBe(updatedContent);

    // Verify update was persisted
    const getResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
    expect(getResponse.status).toBe(200);
    const getData: ApiResponse = await getResponse.json();

    const updatedComment = getData.data?.comments?.find(
      (c: any) => (c.commentId || c.comment_id) === commentId
    );
    expect(updatedComment).toBeTruthy();
    expect(updatedComment?.content).toBe(updatedContent);
  });
});

test.describe('Complete User Workflow with Persistence', () => {
  test('complete workflow: register -> create task -> add comments -> update status', async () => {
    const testEmail = `workflow-${Date.now()}@example.com`;
    const testPassword = 'WorkflowTest123!';

    // Step 1: Register
    const registerResponse = await apiCall('POST', '/auth/register', {
      email: testEmail,
      password: testPassword,
      full_name: 'Workflow Test User',
    });

    expect(registerResponse.status).toBe(200);
    const userData: ApiResponse = await registerResponse.json();
    const userId = userData.data?.userId;

    // Step 2: Login
    const loginResponse = await apiCall('POST', '/auth/login', {
      email: testEmail,
      password: testPassword,
    });

    expect(loginResponse.status).toBe(200);
    const loginData: ApiResponse = await loginResponse.json();
    const token = loginData.data?.token;
    expect(token).toBeTruthy();

    // Step 3: Create task
    const taskTitle = 'Complete Workflow Task';
    const createTaskResponse = await apiCall(
      'POST',
      '/tasks',
      {
        title: taskTitle,
        description: 'Task created in complete workflow test',
        status: 'todo',
        priority: 'high',
      },
      token
    );

    expect(createTaskResponse.status).toBe(200);
    const taskData: ApiResponse = await createTaskResponse.json();
    const taskId = taskData.data?.taskId;

    // Step 4: Add comment
    const commentResponse = await apiCall(
      'POST',
      `/tasks/${taskId}/comments`,
      { content: 'Starting implementation' },
      token
    );

    expect(commentResponse.status).toBe(200);

    // Step 5: Update status
    const updateResponse = await apiCall(
      'PATCH',
      `/tasks/${taskId}`,
      { status: 'in_progress' },
      token
    );

    expect(updateResponse.status).toBe(200);

    // Step 6: Add another comment
    const comment2Response = await apiCall(
      'POST',
      `/tasks/${taskId}/comments`,
      { content: 'Implementation complete' },
      token
    );

    expect(comment2Response.status).toBe(200);

    // Step 7: Final update to completed
    const completeResponse = await apiCall(
      'PATCH',
      `/tasks/${taskId}`,
      { status: 'completed' },
      token
    );

    expect(completeResponse.status).toBe(200);

    // Step 8: Verify everything was persisted
    const finalResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, token);
    expect(finalResponse.status).toBe(200);
    const finalData: ApiResponse = await finalResponse.json();

    expect(finalData.data?.title).toBe(taskTitle);
    expect(finalData.data?.status).toBe('completed');
    expect(finalData.data?.comments?.length).toBeGreaterThanOrEqual(2);
  });
});
