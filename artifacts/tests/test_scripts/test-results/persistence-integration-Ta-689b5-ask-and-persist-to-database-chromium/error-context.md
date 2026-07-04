# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: persistence-integration.spec.ts >> Task Persistence and Comment Integration Tests >> should create a task and persist to database
- Location: tests\persistence-integration.spec.ts:71:3

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: "This task is created via E2E test and persisted to DB"
Received: undefined
```

# Test source

```ts
  1   | import { test, expect, Page } from '@playwright/test';
  2   | 
  3   | const API_BASE_URL = 'http://localhost:8001/api/v1';
  4   | 
  5   | interface ApiResponse {
  6   |   data?: any;
  7   |   error?: any;
  8   | }
  9   | 
  10  | async function apiCall(
  11  |   method: string,
  12  |   endpoint: string,
  13  |   body?: any,
  14  |   token?: string
  15  | ): Promise<Response> {
  16  |   const headers: Record<string, string> = {
  17  |     'Content-Type': 'application/json',
  18  |   };
  19  | 
  20  |   if (token) {
  21  |     headers['Authorization'] = `Bearer ${token}`;
  22  |   }
  23  | 
  24  |   const response = await fetch(`${API_BASE_URL}${endpoint}`, {
  25  |     method,
  26  |     headers,
  27  |     body: body ? JSON.stringify(body) : undefined,
  28  |   });
  29  | 
  30  |   return response;
  31  | }
  32  | 
  33  | test.describe('Task Persistence and Comment Integration Tests', () => {
  34  |   let testEmail: string;
  35  |   let testPassword: string;
  36  |   let testUserId: string;
  37  |   let authToken: string;
  38  |   let taskId: string;
  39  | 
  40  |   test.beforeAll(async () => {
  41  |     // Generate unique test credentials
  42  |     testEmail = `e2e-test-${Date.now()}@example.com`;
  43  |     testPassword = 'E2ETestPass123!SecurePassword';
  44  | 
  45  |     // Register a new test user
  46  |     const registerResponse = await apiCall('POST', '/auth/register', {
  47  |       email: testEmail,
  48  |       password: testPassword,
  49  |       full_name: 'E2E Test User',
  50  |     });
  51  | 
  52  |     expect(registerResponse.status).toBe(200);
  53  |     const registerData: ApiResponse = await registerResponse.json();
  54  |     testUserId = registerData.data?.userId || registerData.data?.user_id;
  55  |     expect(testUserId).toBeTruthy();
  56  |   });
  57  | 
  58  |   test.beforeEach(async () => {
  59  |     // Login before each test
  60  |     const loginResponse = await apiCall('POST', '/auth/login', {
  61  |       email: testEmail,
  62  |       password: testPassword,
  63  |     });
  64  | 
  65  |     expect(loginResponse.status).toBe(200);
  66  |     const loginData: ApiResponse = await loginResponse.json();
  67  |     authToken = loginData.data?.token;
  68  |     expect(authToken).toBeTruthy();
  69  |   });
  70  | 
  71  |   test('should create a task and persist to database', async () => {
  72  |     const taskTitle = `Task ${Date.now()}`;
  73  |     const taskDescription = 'This task is created via E2E test and persisted to DB';
  74  | 
  75  |     const createResponse = await apiCall(
  76  |       'POST',
  77  |       '/tasks',
  78  |       {
  79  |         title: taskTitle,
  80  |         description: taskDescription,
  81  |         status: 'todo',
  82  |         priority: 'high',
  83  |         due_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
  84  |       },
  85  |       authToken
  86  |     );
  87  | 
  88  |     expect(createResponse.status).toBe(200);
  89  |     const createData: ApiResponse = await createResponse.json();
  90  |     taskId = createData.data?.taskId || createData.data?.task_id;
  91  |     expect(taskId).toBeTruthy();
  92  |     expect(createData.data?.title).toBe(taskTitle);
> 93  |     expect(createData.data?.description).toBe(taskDescription);
      |                                          ^ Error: expect(received).toBe(expected) // Object.is equality
  94  |     expect(createData.data?.status).toBe('todo');
  95  | 
  96  |     // Verify task was persisted by fetching it
  97  |     const getResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
  98  |     expect(getResponse.status).toBe(200);
  99  |     const getData: ApiResponse = await getResponse.json();
  100 |     expect(getData.data?.title).toBe(taskTitle);
  101 |     expect(getData.data?.description).toBe(taskDescription);
  102 |   });
  103 | 
  104 |   test('should add a comment and persist to database', async () => {
  105 |     // First, create a task
  106 |     const createTaskResponse = await apiCall(
  107 |       'POST',
  108 |       '/tasks',
  109 |       {
  110 |         title: `Comment Test Task ${Date.now()}`,
  111 |         description: 'Task for comment persistence test',
  112 |         status: 'todo',
  113 |         priority: 'medium',
  114 |       },
  115 |       authToken
  116 |     );
  117 | 
  118 |     expect(createTaskResponse.status).toBe(200);
  119 |     const taskData: ApiResponse = await createTaskResponse.json();
  120 |     taskId = taskData.data?.taskId || taskData.data?.task_id;
  121 |     expect(taskId).toBeTruthy();
  122 | 
  123 |     // Add a comment
  124 |     const commentContent = `Comment created at ${new Date().toISOString()}`;
  125 |     const addCommentResponse = await apiCall(
  126 |       'POST',
  127 |       `/tasks/${taskId}/comments`,
  128 |       { content: commentContent },
  129 |       authToken
  130 |     );
  131 | 
  132 |     expect(addCommentResponse.status).toBe(200);
  133 |     const commentData: ApiResponse = await addCommentResponse.json();
  134 |     const commentId = commentData.data?.commentId || commentData.data?.comment_id;
  135 |     expect(commentId).toBeTruthy();
  136 |     expect(commentData.data?.content).toBe(commentContent);
  137 | 
  138 |     // Verify comment was persisted by fetching task details
  139 |     const getTaskResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
  140 |     expect(getTaskResponse.status).toBe(200);
  141 |     const getTaskData: ApiResponse = await getTaskResponse.json();
  142 | 
  143 |     const comments = getTaskData.data?.comments || [];
  144 |     expect(comments.length).toBeGreaterThan(0);
  145 | 
  146 |     const persistedComment = comments.find(
  147 |       (c: any) => (c.commentId || c.comment_id) === commentId
  148 |     );
  149 |     expect(persistedComment).toBeTruthy();
  150 |     expect(persistedComment?.content).toBe(commentContent);
  151 |   });
  152 | 
  153 |   test('should add multiple comments and retrieve in order', async () => {
  154 |     // Create a task
  155 |     const createTaskResponse = await apiCall(
  156 |       'POST',
  157 |       '/tasks',
  158 |       {
  159 |         title: `Multi-Comment Task ${Date.now()}`,
  160 |         description: 'Task for testing multiple comments',
  161 |         status: 'in_progress',
  162 |         priority: 'medium',
  163 |       },
  164 |       authToken
  165 |     );
  166 | 
  167 |     expect(createTaskResponse.status).toBe(200);
  168 |     taskId = (await createTaskResponse.json()).data?.taskId;
  169 |     expect(taskId).toBeTruthy();
  170 | 
  171 |     // Add multiple comments
  172 |     const comments = [
  173 |       'First comment - Initial investigation',
  174 |       'Second comment - Found the root cause',
  175 |       'Third comment - Working on the fix',
  176 |     ];
  177 | 
  178 |     const commentIds: string[] = [];
  179 | 
  180 |     for (const comment of comments) {
  181 |       const addResponse = await apiCall(
  182 |         'POST',
  183 |         `/tasks/${taskId}/comments`,
  184 |         { content: comment },
  185 |         authToken
  186 |       );
  187 | 
  188 |       expect(addResponse.status).toBe(200);
  189 |       const data: ApiResponse = await addResponse.json();
  190 |       const cId = data.data?.commentId || data.data?.comment_id;
  191 |       commentIds.push(cId);
  192 |     }
  193 | 
```