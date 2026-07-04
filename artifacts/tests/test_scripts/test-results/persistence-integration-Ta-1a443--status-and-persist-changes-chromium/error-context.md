# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: persistence-integration.spec.ts >> Task Persistence and Comment Integration Tests >> should update task status and persist changes
- Location: tests\persistence-integration.spec.ts:219:3

# Error details

```
Error: expect(received).toBeTruthy()

Received: undefined
```

# Test source

```ts
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
> 235 |     expect(taskId).toBeTruthy();
      |                    ^ Error: expect(received).toBeTruthy()
  236 | 
  237 |     // Update status to in_progress
  238 |     const updateResponse = await apiCall(
  239 |       'PATCH',
  240 |       `/tasks/${taskId}`,
  241 |       { status: 'in_progress' },
  242 |       authToken
  243 |     );
  244 | 
  245 |     expect(updateResponse.status).toBe(200);
  246 |     const updateData: ApiResponse = await updateResponse.json();
  247 |     expect(updateData.data?.status).toBe('in_progress');
  248 | 
  249 |     // Verify status change was persisted
  250 |     const getResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
  251 |     expect(getResponse.status).toBe(200);
  252 |     const getData: ApiResponse = await getResponse.json();
  253 |     expect(getData.data?.status).toBe('in_progress');
  254 | 
  255 |     // Update to completed
  256 |     const completeResponse = await apiCall(
  257 |       'PATCH',
  258 |       `/tasks/${taskId}`,
  259 |       { status: 'completed' },
  260 |       authToken
  261 |     );
  262 | 
  263 |     expect(completeResponse.status).toBe(200);
  264 |     const completeData: ApiResponse = await completeResponse.json();
  265 |     expect(completeData.data?.status).toBe('completed');
  266 | 
  267 |     // Verify final status
  268 |     const finalGetResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
  269 |     expect(finalGetResponse.status).toBe(200);
  270 |     const finalData: ApiResponse = await finalGetResponse.json();
  271 |     expect(finalData.data?.status).toBe('completed');
  272 |   });
  273 | 
  274 |   test('should track task history with comments and status changes', async () => {
  275 |     // Create task
  276 |     const createResponse = await apiCall(
  277 |       'POST',
  278 |       '/tasks',
  279 |       {
  280 |         title: `History Test Task ${Date.now()}`,
  281 |         description: 'Task for testing history tracking',
  282 |         status: 'todo',
  283 |         priority: 'high',
  284 |       },
  285 |       authToken
  286 |     );
  287 | 
  288 |     expect(createResponse.status).toBe(200);
  289 |     taskId = (await createResponse.json()).data?.taskId;
  290 | 
  291 |     // Add a comment
  292 |     const commentResponse = await apiCall(
  293 |       'POST',
  294 |       `/tasks/${taskId}/comments`,
  295 |       { content: 'Initial progress update' },
  296 |       authToken
  297 |     );
  298 |     expect(commentResponse.status).toBe(200);
  299 | 
  300 |     // Change status
  301 |     const statusResponse = await apiCall(
  302 |       'PATCH',
  303 |       `/tasks/${taskId}`,
  304 |       { status: 'in_progress' },
  305 |       authToken
  306 |     );
  307 |     expect(statusResponse.status).toBe(200);
  308 | 
  309 |     // Add another comment
  310 |     const comment2Response = await apiCall(
  311 |       'POST',
  312 |       `/tasks/${taskId}/comments`,
  313 |       { content: 'Almost done with the implementation' },
  314 |       authToken
  315 |     );
  316 |     expect(comment2Response.status).toBe(200);
  317 | 
  318 |     // Fetch task with full history
  319 |     const getResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
  320 |     expect(getResponse.status).toBe(200);
  321 |     const getData: ApiResponse = await getResponse.json();
  322 | 
  323 |     // Verify all updates were tracked
  324 |     expect(getData.data?.status).toBe('in_progress');
  325 |     expect(getData.data?.comments?.length).toBeGreaterThanOrEqual(2);
  326 |     expect(getData.data?.history).toBeTruthy();
  327 |   });
  328 | 
  329 |   test('should persist task and comments across multiple API calls', async () => {
  330 |     // Create a task
  331 |     const taskTitle = `Persistence Test ${Date.now()}`;
  332 |     const createResponse = await apiCall(
  333 |       'POST',
  334 |       '/tasks',
  335 |       {
```