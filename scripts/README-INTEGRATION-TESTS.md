# Integration Testing Scripts

This directory contains scripts to set up and run integration tests for the Task Management System.

## Quick Start

### Windows
```powershell
scripts\run-integration-tests.bat
```

### macOS/Linux
```bash
bash scripts/run-integration-tests.sh
```

### Cross-Platform (Python)
```bash
python scripts/run-integration-tests.py
```

## Prerequisites

Before running the tests, ensure:

1. **Backend Running**: The FastAPI backend must be running on `http://localhost:8001`
   ```bash
   cd apps/backend
   .\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8001
   ```

2. **Database**: SQLite database at `apps/data/task_management.db` (created automatically on first backend start)

3. **Node.js**: Version 18+ with npm installed

4. **Playwright**: Installed in the frontend (run `npm install` in `apps/frontend`)

## What the Scripts Do

The setup scripts perform these checks and actions:

1. **Backend Health Check**: Verifies the backend API is responding
2. **Database Check**: Checks if the SQLite database exists
3. **Database Seeding**: Automatically seeds the database with test data if empty
4. **Frontend Setup**: Verifies frontend dependencies are installed
5. **Test Execution**: Runs the integration test suite

## Test Data

When the database is seeded, the following test users are created:

| Email | Password | Role |
|-------|----------|------|
| alice@example.com | SecurePass123! | TEAM_LEAD |
| bob@example.com | SecurePass123! | TEAM_MEMBER |
| charlie@example.com | SecurePass123! | TEAM_MEMBER |
| diana@example.com | SecurePass123! | ADMIN |

Plus sample teams, tasks, and comments for testing.

## Script Details

### run-integration-tests.py
**Language**: Python
**Platforms**: Windows, macOS, Linux
**Features**:
- Colored output
- Detailed status messages
- Database state checking
- Automatic seeding
- Full error reporting

### run-integration-tests.bat
**Language**: Batch/CMD
**Platforms**: Windows only
**Features**:
- Checks Python installation
- Database status verification
- Automatic dependency installation
- Frontend setup validation

### run-integration-tests.sh
**Language**: Bash
**Platforms**: macOS, Linux
**Features**:
- Colored terminal output
- Database state detection
- Automatic seeding with feedback
- Node.js installation check

## Troubleshooting

### Backend Not Running
**Error**: `Backend is not responding`

**Solution**:
```bash
cd apps/backend
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8001
```

### Database Locked
**Error**: `database is locked`

**Solution**:
1. Stop the backend
2. Delete `apps/data/task_management.db`
3. Restart the backend

### Frontend Dependencies Missing
**Error**: `node_modules not found`

**Solution**:
```bash
cd apps/frontend
npm install
```

### Tests Timeout
**Error**: Tests timeout waiting for API responses

**Solution**:
1. Check backend is running and responsive
2. Verify database performance
3. Check system resources

## Manual Testing

To manually run specific tests without the setup script:

```bash
# Run all integration tests
cd apps/frontend
npm test

# Run specific test file
npm test -- persistence-integration.spec.ts

# Run specific test case
npm test -- persistence-integration.spec.ts -g "should create a task"

# Debug mode (opens Playwright Inspector)
PWDEBUG=1 npm test
```

## Continuous Integration

For CI/CD pipelines, use the Python script:

```bash
python scripts/run-integration-tests.py
```

Exit code:
- `0` - All tests passed
- `1` - Tests failed or prerequisites not met

## Adding New Tests

New integration tests should be added to `artifacts/tests/test_scripts/tests/persistence-integration.spec.ts`.

Follow the pattern:
1. Use the `apiCall()` helper for API interactions
2. Create unique test data (use timestamps)
3. Verify persistence by fetching the created data
4. Handle both success and error cases

Example:
```typescript
test('should persist new data', async () => {
  const token = await login();
  const response = await apiCall('POST', '/api/endpoint', payload, token);
  
  expect(response.status).toBe(200);
  const data = await response.json();
  
  // Verify persistence
  const getResponse = await apiCall('GET', `/api/endpoint/${data.id}`, undefined, token);
  expect(getResponse.status).toBe(200);
  const getData = await getResponse.json();
  expect(getData.data).toEqual(data.data);
});
```

## Related Documentation

- [Integration Testing Guide](../docs/integration-testing-guide.md)
- [API Documentation](../docs/api-documentation.md)
- [Backend README](../apps/backend/README.md)
- [Frontend README](../apps/frontend/README.md)

---

**Last Updated**: 2024-01-01
