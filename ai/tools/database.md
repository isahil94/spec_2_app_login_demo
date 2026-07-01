# Database Tool

Inspect, query, and validate database schemas and data.

---

## Purpose

Provide agents with the ability to inspect database schemas, execute SQL queries, validate migrations, and interact with databases for testing and data operations.

---

## When to Use

- Inspecting database schema
- Executing queries during development
- Validating migrations
- Generating schema documentation
- Testing data operations
- Debugging data issues
- Creating test data
- Validating database configuration

---

## Available Operations

### Schema Inspection
- List tables and views
- Describe table structure (columns, types, constraints)
- Get indexes and foreign keys
- Get stored procedures/functions
- Generate schema documentation

### Query Execution
- Execute SELECT queries
- Execute INSERT/UPDATE/DELETE
- Execute stored procedures
- View query results
- Export results to file

### Migration Operations
- List applied migrations
- Show pending migrations
- Validate migration syntax
- Rollback migrations
- Create new migrations

### Data Validation
- Validate data integrity
- Check constraints
- Find orphaned records
- Validate foreign keys
- Generate data quality reports

### Testing Operations
- Create test databases
- Load test data
- Seed databases
- Clear test data
- Reset database state

---

## Inputs

### Query Execution
- **Query** (required): SQL query string
- **Database** (optional): Database connection name
- **Format** (optional): Output format (table/json/csv)
- **Limit** (optional): Limit results

### Schema Inspection
- **Table** (optional): Specific table name
- **Database** (optional): Database name
- **Format** (optional): Output format

### Migration
- **Action** (required): validate/list/apply/rollback
- **Count** (optional): Number of migrations

---

## Outputs

### Query Results
- **Rows**: Result rows
- **Row Count**: Number of results
- **Columns**: Column names and types
- **Format**: Formatted output (table/json/csv)

### Schema Output
- **Tables**: List of tables with descriptions
- **Columns**: Column definitions with types
- **Indexes**: Index information
- **Constraints**: Foreign keys and constraints
- **Procedures**: Stored procedures if any

### Migration Output
- **Status**: Applied/Pending migrations
- **History**: Migration history
- **Validation**: Migration validation results

---

## Dependencies

- **Database MCP Server** - Provides database access
- **Database Client** - SQL client for connection
- **Database Configuration** - Connection details
- **Migration Tool** - For migration operations (optional)

---

## Execution

**Method:** Database MCP Server

**How it works:**
1. Agent specifies database operation
2. Database MCP server connects to database
3. Query/operation executes
4. Results retrieved and formatted
5. Output returned to agent

**Supported:** PostgreSQL, MySQL, SQLite, others via MCP

---

## Constraints

- Read-only for production databases (safety)
- Write operations for dev/test databases
- Query timeout enforced (prevents long-running queries)
- Result set size limited
- No access to credentials (via MCP security)
- Must use connection pool for efficiency

---

## Best Practices

### Query Safety
- Use parameterized queries (prevent SQL injection)
- Test queries on dev database first
- Limit results to prevent memory issues
- Use transactions for data modifications
- Validate data before inserting

### Schema Understanding
- Review schema before querying
- Understand relationships and constraints
- Check indexes for performance
- Document any custom logic
- Keep schema documentation current

### Migration Management
- Write clear migration descriptions
- Test migrations on dev first
- Create rollback migrations
- Validate migration syntax
- Keep migration history clean

### Data Integrity
- Validate constraints are enforced
- Check for orphaned records
- Monitor for data quality issues
- Document data validation rules
- Test foreign key relationships

### Performance
- Use indexes appropriately
- Analyze query plans
- Avoid N+1 queries
- Batch operations when possible
- Monitor long-running queries

---

## Error Handling

### Common Failures

**Connection Failed**
- Cause: Cannot connect to database
- Recovery: Check connection config, verify database is running
- Log: Connection error details

**Syntax Error**
- Cause: Invalid SQL syntax
- Recovery: Review query, fix syntax
- Log: SQL error message and line

**Permission Denied**
- Cause: User lacks permissions
- Recovery: Check user role, grant permissions
- Log: Attempted operation and required permissions

**Constraint Violation**
- Cause: Data violates constraints
- Recovery: Check constraints, fix data
- Log: Constraint type and conflicting data

**Timeout**
- Cause: Query takes too long
- Recovery: Optimize query, add indexes, split query
- Log: Query duration and timeout value

**Migration Error**
- Cause: Migration fails to apply
- Recovery: Review migration, fix issue, retry
- Log: Migration error details

---

## Tool Integration Examples

### Inspect Table Schema
```
Database: Describe table users
Purpose: Understand data structure
Output: Columns, types, constraints, indexes
```

### Execute Query
```
Database: Execute query
SQL: SELECT COUNT(*) FROM users WHERE active = true
Purpose: Get user count
Output: Results in table format
```

### Validate Migrations
```
Database: Validate migrations
Database: myapp
Purpose: Ensure migrations are correct
Output: Validation results, any issues
```

### Generate Schema Documentation
```
Database: Generate schema docs
Database: myapp
Purpose: Document database structure
Output: Schema documentation
```

### Create Test Data
```
Database: Load test data
Database: myapp_test
File: tests/fixtures/data.sql
Purpose: Seed test database
Output: Rows inserted
```

---

## See Also

- **Filesystem Tool** - For reading/writing migration files
- **Terminal Tool** - For migration commands
- **Testing Tool** - For database testing

Reference: `shared.md` for common guidance on validation and security.
