# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: persistence-integration.spec.ts >> Task Persistence and Comment Integration Tests >> should add a comment and persist to database
- Location: tests\persistence-integration.spec.ts:104:3

# Error details

```
Error: expect(received).toBeGreaterThan(expected)

Expected: > 0
Received:   0
```

# Test source

```ts
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
  93  |     expect(createData.data?.description).toBe(taskDescription);
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
> 144 |     expect(comments.length).toBeGreaterThan(0);
      |                             ^ Error: expect(received).toBeGreaterThan(expected)
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
  194 |     // Fetch all comments and verify order and content
  195 |     const getCommentsResponse = await apiCall(
  196 |       'GET',
  197 |       `/tasks/${taskId}/comments`,
  198 |       undefined,
  199 |       authToken
  200 |     );
  201 | 
  202 |     expect(getCommentsResponse.status).toBe(200);
  203 |     const commentsData: ApiResponse = await getCommentsResponse.json();
  204 |     const retrievedComments = commentsData.data?.comments || [];
  205 | 
  206 |     // Verify all comments were persisted
  207 |     expect(retrievedComments.length).toBeGreaterThanOrEqual(comments.length);
  208 | 
  209 |     // Verify comments are in order
  210 |     comments.forEach((comment, index) => {
  211 |       const retrieved = retrievedComments.find(
  212 |         (c: any) => (c.commentId || c.comment_id) === commentIds[index]
  213 |       );
  214 |       expect(retrieved).toBeTruthy();
  215 |       expect(retrieved?.content).toBe(comment);
  216 |     });
  217 |   });
  218 | 
  219 |   test('should update task status and persist changes', async () => {
  220 |     // Create a task
  221 |     const createResponse = await apiCall(
  222 |       'POST',
  223 |       '/tasks',
  224 |       {
  225 |         title: `Status Update Task ${Date.now()}`,
  226 |         description: 'Task for testing status updates',
  227 |         status: 'todo',
  228 |         priority: 'low',
  229 |       },
  230 |       authToken
  231 |     );
  232 | 
  233 |     expect(createResponse.status).toBe(200);
  234 |     taskId = (await createResponse.json()).data?.taskId;
  235 |     expect(taskId).toBeTruthy();
  236 | 
  237 |     // Update status to in_progress
  238 |     const updateResponse = await apiCall(
  239 |       'PATCH',
  240 |       `/tasks/${taskId}`,
  241 |       { status: 'in_progress' },
  242 |       authToken
  243 |     );
  244 | 
```