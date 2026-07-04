# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: persistence-integration.spec.ts >> Task Persistence and Comment Integration Tests >> should track task history with comments and status changes
- Location: tests\persistence-integration.spec.ts:274:3

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: 200
Received: 404
```

# Test source

```ts
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
> 298 |     expect(commentResponse.status).toBe(200);
      |                                    ^ Error: expect(received).toBe(expected) // Object.is equality
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
  336 |         title: taskTitle,
  337 |         description: 'Task for testing data persistence across calls',
  338 |         status: 'todo',
  339 |         priority: 'medium',
  340 |       },
  341 |       authToken
  342 |     );
  343 | 
  344 |     expect(createResponse.status).toBe(200);
  345 |     taskId = (await createResponse.json()).data?.taskId;
  346 | 
  347 |     // Simulate multiple API interactions
  348 |     const interactions = [
  349 |       {
  350 |         action: 'update_priority',
  351 |         body: { priority: 'high' },
  352 |         comment: 'Priority increased',
  353 |       },
  354 |       {
  355 |         action: 'update_status',
  356 |         body: { status: 'in_progress' },
  357 |         comment: 'Started working on this',
  358 |       },
  359 |       {
  360 |         action: 'update_priority',
  361 |         body: { priority: 'critical' },
  362 |         comment: 'This is now critical',
  363 |       },
  364 |     ];
  365 | 
  366 |     for (const interaction of interactions) {
  367 |       // Update task
  368 |       const updateResponse = await apiCall(
  369 |         'PATCH',
  370 |         `/tasks/${taskId}`,
  371 |         interaction.body,
  372 |         authToken
  373 |       );
  374 |       expect(updateResponse.status).toBe(200);
  375 | 
  376 |       // Add comment
  377 |       if (interaction.comment) {
  378 |         const commentResponse = await apiCall(
  379 |           'POST',
  380 |           `/tasks/${taskId}/comments`,
  381 |           { content: interaction.comment },
  382 |           authToken
  383 |         );
  384 |         expect(commentResponse.status).toBe(200);
  385 |       }
  386 |     }
  387 | 
  388 |     // Verify all changes were persisted
  389 |     const finalResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
  390 |     expect(finalResponse.status).toBe(200);
  391 |     const finalData: ApiResponse = await finalResponse.json();
  392 | 
  393 |     expect(finalData.data?.title).toBe(taskTitle);
  394 |     expect(finalData.data?.priority).toBe('critical');
  395 |     expect(finalData.data?.status).toBe('in_progress');
  396 |     expect(finalData.data?.comments?.length).toBeGreaterThanOrEqual(3);
  397 |   });
  398 | 
```