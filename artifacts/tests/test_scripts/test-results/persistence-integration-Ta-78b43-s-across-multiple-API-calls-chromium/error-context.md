# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: persistence-integration.spec.ts >> Task Persistence and Comment Integration Tests >> should persist task and comments across multiple API calls
- Location: tests\persistence-integration.spec.ts:329:3

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: 200
Received: 404
```

# Test source

```ts
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
> 374 |       expect(updateResponse.status).toBe(200);
      |                                     ^ Error: expect(received).toBe(expected) // Object.is equality
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
  399 |   test('should handle comment updates and persist changes', async () => {
  400 |     // Create task
  401 |     const createResponse = await apiCall(
  402 |       'POST',
  403 |       '/tasks',
  404 |       {
  405 |         title: `Comment Update Test ${Date.now()}`,
  406 |         description: 'Task for testing comment updates',
  407 |         status: 'todo',
  408 |         priority: 'low',
  409 |       },
  410 |       authToken
  411 |     );
  412 | 
  413 |     expect(createResponse.status).toBe(200);
  414 |     taskId = (await createResponse.json()).data?.taskId;
  415 | 
  416 |     // Add initial comment
  417 |     const addResponse = await apiCall(
  418 |       'POST',
  419 |       `/tasks/${taskId}/comments`,
  420 |       { content: 'Original comment text' },
  421 |       authToken
  422 |     );
  423 | 
  424 |     expect(addResponse.status).toBe(200);
  425 |     const commentId = (await addResponse.json()).data?.commentId;
  426 | 
  427 |     // Update the comment
  428 |     const updatedContent = 'Updated comment text with more details';
  429 |     const updateResponse = await apiCall(
  430 |       'PATCH',
  431 |       `/tasks/${taskId}/comments/${commentId}`,
  432 |       { content: updatedContent },
  433 |       authToken
  434 |     );
  435 | 
  436 |     expect(updateResponse.status).toBe(200);
  437 |     const updateData: ApiResponse = await updateResponse.json();
  438 |     expect(updateData.data?.content).toBe(updatedContent);
  439 | 
  440 |     // Verify update was persisted
  441 |     const getResponse = await apiCall('GET', `/tasks/${taskId}`, undefined, authToken);
  442 |     expect(getResponse.status).toBe(200);
  443 |     const getData: ApiResponse = await getResponse.json();
  444 | 
  445 |     const updatedComment = getData.data?.comments?.find(
  446 |       (c: any) => (c.commentId || c.comment_id) === commentId
  447 |     );
  448 |     expect(updatedComment).toBeTruthy();
  449 |     expect(updatedComment?.content).toBe(updatedContent);
  450 |   });
  451 | });
  452 | 
  453 | test.describe('Complete User Workflow with Persistence', () => {
  454 |   test('complete workflow: register -> create task -> add comments -> update status', async () => {
  455 |     const testEmail = `workflow-${Date.now()}@example.com`;
  456 |     const testPassword = 'WorkflowTest123!';
  457 | 
  458 |     // Step 1: Register
  459 |     const registerResponse = await apiCall('POST', '/auth/register', {
  460 |       email: testEmail,
  461 |       password: testPassword,
  462 |       full_name: 'Workflow Test User',
  463 |     });
  464 | 
  465 |     expect(registerResponse.status).toBe(200);
  466 |     const userData: ApiResponse = await registerResponse.json();
  467 |     const userId = userData.data?.userId;
  468 | 
  469 |     // Step 2: Login
  470 |     const loginResponse = await apiCall('POST', '/auth/login', {
  471 |       email: testEmail,
  472 |       password: testPassword,
  473 |     });
  474 | 
```