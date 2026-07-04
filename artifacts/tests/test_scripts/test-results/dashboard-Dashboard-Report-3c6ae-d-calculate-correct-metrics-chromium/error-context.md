# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: dashboard.spec.ts >> Dashboard & Reporting API Tests >> GET /dashboard/metrics - should calculate correct metrics
- Location: tests\dashboard.spec.ts:101:3

# Error details

```
Error: expect(received).toBeGreaterThanOrEqual(expected)

Expected: >= 1
Received:    0
```

# Test source

```ts
  13  | 
  14  |   const response = await fetch(`${API_BASE_URL}${endpoint}`, {
  15  |     method,
  16  |     headers,
  17  |     body: body ? JSON.stringify(body) : undefined,
  18  |   });
  19  | 
  20  |   return response;
  21  | }
  22  | 
  23  | test.describe.serial('Dashboard & Reporting API Tests', () => {
  24  |   let authToken: string;
  25  |   const testEmail = `dashboard-test-${Date.now()}@example.com`;
  26  |   const testPassword = 'DashboardTestPass123!';
  27  | 
  28  |   test.beforeAll(async () => {
  29  |     // Register and login
  30  |     await apiCall('POST', '/auth/register', {
  31  |       email: testEmail,
  32  |       password: testPassword,
  33  |       full_name: 'Dashboard Tester',
  34  |     });
  35  | 
  36  |     const loginResponse = await apiCall('POST', '/auth/login', {
  37  |       email: testEmail,
  38  |       password: testPassword,
  39  |     });
  40  |     const loginData = await loginResponse.json();
  41  |     authToken = loginData.data?.token || 'unknown';
  42  | 
  43  |     // Create multiple tasks for metrics testing
  44  |     // Task 1: Completed
  45  |     await apiCall('POST', '/tasks', {
  46  |       title: 'Completed Task',
  47  |       status: 'completed',
  48  |       priority: 'high',
  49  |     }, authToken);
  50  | 
  51  |     // Task 2: In Progress
  52  |     await apiCall('POST', '/tasks', {
  53  |       title: 'In Progress Task',
  54  |       status: 'in_progress',
  55  |       priority: 'medium',
  56  |     }, authToken);
  57  | 
  58  |     // Task 3: Todo (due today)
  59  |     const today = new Date();
  60  |     today.setHours(23, 59, 59, 999);
  61  |     await apiCall('POST', '/tasks', {
  62  |       title: 'Due Today Task',
  63  |       status: 'todo',
  64  |       priority: 'medium',
  65  |       due_date: today.toISOString(),
  66  |     }, authToken);
  67  | 
  68  |     // Task 4: Todo (overdue)
  69  |     const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000);
  70  |     await apiCall('POST', '/tasks', {
  71  |       title: 'Overdue Task',
  72  |       status: 'todo',
  73  |       priority: 'critical',
  74  |       due_date: yesterday.toISOString(),
  75  |     }, authToken);
  76  | 
  77  |     // Task 5: Todo (future)
  78  |     const futureDate = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
  79  |     await apiCall('POST', '/tasks', {
  80  |       title: 'Future Task',
  81  |       status: 'todo',
  82  |       priority: 'low',
  83  |       due_date: futureDate.toISOString(),
  84  |     }, authToken);
  85  |   });
  86  | 
  87  |   test('GET /dashboard/metrics - should retrieve dashboard metrics', async () => {
  88  |     const response = await apiCall('GET', '/dashboard/metrics', undefined, authToken);
  89  | 
  90  |     expect(response.status).toBe(200);
  91  |     const data = await response.json();
  92  |     expect(data.data).toBeDefined();
  93  |     expect(data.data.total_tasks).toBeDefined();
  94  |     expect(data.data.completed_tasks).toBeDefined();
  95  |     expect(data.data.pending_tasks).toBeDefined();
  96  |     expect(data.data.overdue_tasks).toBeDefined();
  97  |     expect(data.data.due_today_tasks).toBeDefined();
  98  |     expect(data.data.completion_rate).toBeDefined();
  99  |   });
  100 | 
  101 |   test('GET /dashboard/metrics - should calculate correct metrics', async () => {
  102 |     const response = await apiCall('GET', '/dashboard/metrics', undefined, authToken);
  103 | 
  104 |     expect(response.status).toBe(200);
  105 |     const data = await response.json();
  106 |     const metrics = data.data;
  107 | 
  108 |     // Verify metrics calculations
  109 |     expect(metrics.total_tasks).toBe(5); // 5 tasks created
  110 |     expect(metrics.completed_tasks).toBe(1); // 1 completed
  111 |     expect(metrics.pending_tasks).toBe(4); // 4 non-completed
  112 |     expect(metrics.overdue_tasks).toBeGreaterThanOrEqual(1); // At least the overdue one
> 113 |     expect(metrics.due_today_tasks).toBeGreaterThanOrEqual(1); // At least the due today one
      |                                     ^ Error: expect(received).toBeGreaterThanOrEqual(expected)
  114 | 
  115 |     // Verify completion rate
  116 |     const expectedRate = (1 / 5) * 100;
  117 |     expect(Math.abs(metrics.completion_rate - expectedRate)).toBeLessThan(1);
  118 |   });
  119 | 
  120 |   test('GET /dashboard/metrics - should fail without authentication', async () => {
  121 |     const response = await apiCall('GET', '/dashboard/metrics');
  122 | 
  123 |     expect(response.status).toBe(401);
  124 |   });
  125 | 
  126 |   test('GET /dashboard/metrics - should have numeric metrics', async () => {
  127 |     const response = await apiCall('GET', '/dashboard/metrics', undefined, authToken);
  128 | 
  129 |     expect(response.status).toBe(200);
  130 |     const data = await response.json();
  131 |     const metrics = data.data;
  132 | 
  133 |     expect(typeof metrics.total_tasks).toBe('number');
  134 |     expect(typeof metrics.completed_tasks).toBe('number');
  135 |     expect(typeof metrics.pending_tasks).toBe('number');
  136 |     expect(typeof metrics.overdue_tasks).toBe('number');
  137 |     expect(typeof metrics.due_today_tasks).toBe('number');
  138 |     expect(typeof metrics.completion_rate).toBe('number');
  139 | 
  140 |     // Verify non-negative
  141 |     expect(metrics.total_tasks).toBeGreaterThanOrEqual(0);
  142 |     expect(metrics.completed_tasks).toBeGreaterThanOrEqual(0);
  143 |     expect(metrics.pending_tasks).toBeGreaterThanOrEqual(0);
  144 |     expect(metrics.overdue_tasks).toBeGreaterThanOrEqual(0);
  145 |     expect(metrics.due_today_tasks).toBeGreaterThanOrEqual(0);
  146 |     expect(metrics.completion_rate).toBeGreaterThanOrEqual(0);
  147 |     expect(metrics.completion_rate).toBeLessThanOrEqual(100);
  148 |   });
  149 | 
  150 |   test('GET /dashboard/metrics - metrics should sum correctly', async () => {
  151 |     const response = await apiCall('GET', '/dashboard/metrics', undefined, authToken);
  152 | 
  153 |     expect(response.status).toBe(200);
  154 |     const data = await response.json();
  155 |     const metrics = data.data;
  156 | 
  157 |     // pending + completed should equal total
  158 |     expect(metrics.pending_tasks + metrics.completed_tasks).toBe(metrics.total_tasks);
  159 |   });
  160 | 
  161 |   test('GET /health - should return healthy status', async () => {
  162 |     const response = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/health`);
  163 | 
  164 |     expect(response.status).toBe(200);
  165 |     const data = await response.json();
  166 |     expect(data.status).toBe('healthy');
  167 |     expect(data.timestamp).toBeDefined();
  168 |   });
  169 | });
  170 | 
```