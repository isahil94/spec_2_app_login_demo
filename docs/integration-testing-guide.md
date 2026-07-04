# Integration Testing Guide

This guide explains how to set up and run the end-to-end integration tests that validate task and comment persistence in the Task Management System.

## Prerequisites

1. **Backend Running**: The FastAPI backend must be running on `http://localhost:8001`
2. **Database**: SQLite database at `apps/data/task_management.db` (created automatically)
3. **Node.js**: Version 18+ installed
4. **Playwright**: Installed and configured for the frontend tests

## Quick Start

### 1. Setup Phase

#### Install Backend Dependencies (if not already done)

```bash
cd apps/backend
pip install -r requirements.txt
```

#### Seed the Database (Optional - for manual testing)

```bash
cd apps/backend
python seed_data.py
```

This creates test users and sample data:
- **Alice** (alice@example.com) - TEAM_LEAD
- **Bob** (bob@example.com) - TEAM_MEMBER
- **Charlie** (charlie@example.com) - TEAM_MEMBER
- **Diana** (diana@example.com) - ADMIN

### 2. Start the Backend

In one terminal window:

```bash
cd f:\Projects\Specs_to_APP- mini
.\.venv\Scripts\python.exe -m uvicorn apps.backend.main:app --host 127.0.0.1 --port 8001 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete
```

### 3. Run Integration Tests

In another terminal window:

```bash
cd apps/frontend
npm test -- persistence-integration.spec.ts
```

Or run all tests:

```bash
npm test
```

## Test Structure

### Integration Test Files

#### `persistence-integration.spec.ts` (NEW)
Comprehensive end-to-end tests for task and comment persistence:
- **Task Persistence**: Create tasks and verify they're saved to the database
- **Comment Persistence**: Add comments and verify retrieval
- **Multiple Comments**: Test ordering and retrieval of multiple comments
- **Status Updates**: Verify status changes are persisted
- **History Tracking**: Test that changes are tracked in task history
- **Comment Updates**: Verify comment edits are persisted
- **Complete Workflows**: Test realistic user scenarios

#### `integration.spec.ts` (EXISTING)
Basic end-to-end workflow tests with database persistence.

#### Other Test Files
- `comments-history.spec.ts`: Comments and history edge cases
- `comments.spec.ts`: Comment functionality
- `tasks.spec.ts`: Task management features
- `auth.spec.ts`: Authentication flows
- `profile-settings.spec.ts`: User profile and settings
- etc.

## API Endpoints Used by Integration Tests

The tests validate the following API endpoints:

### Authentication
- `POST /api/v1/auth/register` - Create new user
- `POST /api/v1/auth/login` - Authenticate user

### Tasks
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks` - List tasks
- `GET /api/v1/tasks/{taskId}` - Get task details with comments and history
- `PATCH /api/v1/tasks/{taskId}` - Update task (status, priority, etc.)

### Comments
- `POST /api/v1/tasks/{taskId}/comments` - Add comment
- `GET /api/v1/tasks/{taskId}/comments` - Get task comments
- `PATCH /api/v1/tasks/{taskId}/comments/{commentId}` - Update comment

See [API Documentation](../api-documentation.md) for complete endpoint details.

## Database

### Database Location
- **Path**: `apps/data/task_management.db`
- **Type**: SQLite3
- **Initialization**: Automatic on first backend startup

### Tables
The database includes:
- `users` - User accounts and profiles
- `teams` - Team groups
- `tasks` - Task items
- `comments` - Task comments
- `notifications` - User notifications
- `audit_entries` - Activity audit log
- And supporting tables for relationships

### Clearing Database (for fresh tests)

To delete and recreate the database:

```bash
# Windows PowerShell
Remove-Item apps/data/task_management.db -ErrorAction SilentlyContinue
# Backend will recreate on next startup
```

### Inspecting Database

To view database contents:

```bash
# Using Python
python -c "
import sqlite3
conn = sqlite3.connect('apps/data/task_management.db')
cur = conn.cursor()

# List all tables
cur.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")
print('Tables:', [row[0] for row in cur.fetchall()])

# Count records
for table in ['users', 'tasks', 'comments']:
    try:
        cur.execute(f'SELECT COUNT(*) FROM {table}')
        count = cur.fetchone()[0]
        print(f'{table}: {count} records')
    except:
        pass

conn.close()
"
```

## Test Scenarios

### Scenario 1: Task Creation and Persistence
```
Register user → Create task → Verify in database → Fetch task → Confirm persistence
```

### Scenario 2: Comment Addition and Retrieval
```
Create task → Add comment → Fetch comments → Verify content and order
```

### Scenario 3: Status Updates
```
Create task (todo) → Update to in_progress → Update to completed → Verify all changes persisted
```

### Scenario 4: Complete Workflow
```
Register → Login → Create task → Add multiple comments → Update status → Update comment → Verify all data
```

## Debugging Tests

### View Test Details
```bash
npm test -- persistence-integration.spec.ts --reporter=verbose
```

### Run Single Test
```bash
npm test -- persistence-integration.spec.ts -g "should create a task"
```

### Enable Debug Logging
```bash
PWDEBUG=1 npm test
```

This opens Playwright Inspector for step-by-step debugging.

### Check Backend Logs
Monitor the terminal where the backend is running to see:
- Request logs
- Database queries
- Error messages
- Performance metrics

## Troubleshooting

### Backend Connection Error
**Error**: `Failed to connect to http://localhost:8001`

**Solution**:
1. Ensure backend is running: `python -m uvicorn apps.backend.main:app --host 127.0.0.1 --port 8001`
2. Check that port 8001 is not in use
3. Verify no firewall is blocking localhost:8001

### Database Locked Error
**Error**: `database is locked`

**Solution**:
1. Stop the backend
2. Delete `apps/data/task_management.db`
3. Restart the backend (it will recreate the database)

### Test Timeout
**Error**: Tests timeout waiting for API responses

**Solution**:
1. Ensure backend is running and responsive
2. Check database performance
3. Increase test timeout: `test.setTimeout(60000);` in test file

### Authentication Failures
**Error**: `401 Unauthorized` on protected endpoints

**Solution**:
1. Verify token is correctly extracted from login response
2. Check that Authorization header format is: `Bearer <token>`
3. Verify token is being passed to all protected endpoints

## Performance Considerations

### Database Optimization
- Database uses indexes on frequently queried columns (user_id, task_id, status, etc.)
- Comment queries are optimized for fetching by task_id

### Test Isolation
- Each test creates unique data (using timestamp-based emails)
- Tests are independent and can run in parallel

### CI/CD Integration

To run tests in CI/CD:

```yaml
# Example GitHub Actions
- name: Run Integration Tests
  run: |
    cd apps/backend
    python seed_data.py  # Optional: seed test data
    python -m uvicorn main:app --host 127.0.0.1 --port 8001 &
    sleep 2  # Wait for backend to start
    cd ../frontend
    npm test -- persistence-integration.spec.ts
```

## Success Criteria

Tests are passing if:
- ✅ All registration and login flows succeed
- ✅ Tasks are created and persisted to database
- ✅ Comments are added and retrieved correctly
- ✅ Task status updates are persisted
- ✅ Comment edits are persisted
- ✅ Task history is tracked
- ✅ Multiple operations maintain data consistency
- ✅ Complete workflows execute without errors

## Adding New Tests

To add new integration tests:

1. Add test function in `persistence-integration.spec.ts`
2. Use the `apiCall()` helper function
3. Follow the pattern:
   - Setup (create test data)
   - Action (perform API operation)
   - Verification (confirm persistence)
   - Cleanup (handled by test isolation)

Example:
```typescript
test('should do something and persist', async () => {
  // Setup
  const token = await login();

  // Action
  const response = await apiCall('POST', '/endpoint', payload, token);
  expect(response.status).toBe(200);
  const data = await response.json();

  // Verify persistence
  const getResponse = await apiCall('GET', `/endpoint/${data.id}`, undefined, token);
  expect(getResponse.status).toBe(200);
  const getData = await getResponse.json();
  expect(getData.data).toEqual(data.data);
});
```

## Related Documentation

- [API Documentation](../api-documentation.md) - Complete API reference
- [Backend Architecture](../docs/BACKEND_ARCHITECTURE.md) - Backend design
- [Database Schema](../docs/DATABASE_SCHEMA.md) - Database structure

---

**Last Updated**: 2024-01-01
**Maintained by**: Development Team
