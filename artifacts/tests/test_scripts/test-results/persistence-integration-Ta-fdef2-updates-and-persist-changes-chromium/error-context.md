# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: persistence-integration.spec.ts >> Task Persistence and Comment Integration Tests >> should handle comment updates and persist changes
- Location: tests\persistence-integration.spec.ts:399:3

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: 200
Received: 404
```

# Test source

```ts
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
> 424 |     expect(addResponse.status).toBe(200);
      |                                ^ Error: expect(received).toBe(expected) // Object.is equality
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
  475 |     expect(loginResponse.status).toBe(200);
  476 |     const loginData: ApiResponse = await loginResponse.json();
  477 |     const token = loginData.data?.token;
  478 |     expect(token).toBeTruthy();
  479 | 
  480 |     // Step 3: Create task
  481 |     const taskTitle = 'Complete Workflow Task';
  482 |     const createTaskResponse = await apiCall(
  483 |       'POST',
  484 |       '/tasks',
  485 |       {
  486 |         title: taskTitle,
  487 |         description: 'Task created in complete workflow test',
  488 |         status: 'todo',
  489 |         priority: 'high',
  490 |       },
  491 |       token
  492 |     );
  493 | 
  494 |     expect(createTaskResponse.status).toBe(200);
  495 |     const taskData: ApiResponse = await createTaskResponse.json();
  496 |     const taskId = taskData.data?.taskId;
  497 | 
  498 |     // Step 4: Add comment
  499 |     const commentResponse = await apiCall(
  500 |       'POST',
  501 |       `/tasks/${taskId}/comments`,
  502 |       { content: 'Starting implementation' },
  503 |       token
  504 |     );
  505 | 
  506 |     expect(commentResponse.status).toBe(200);
  507 | 
  508 |     // Step 5: Update status
  509 |     const updateResponse = await apiCall(
  510 |       'PATCH',
  511 |       `/tasks/${taskId}`,
  512 |       { status: 'in_progress' },
  513 |       token
  514 |     );
  515 | 
  516 |     expect(updateResponse.status).toBe(200);
  517 | 
  518 |     // Step 6: Add another comment
  519 |     const comment2Response = await apiCall(
  520 |       'POST',
  521 |       `/tasks/${taskId}/comments`,
  522 |       { content: 'Implementation complete' },
  523 |       token
  524 |     );
```