# Filesystem Tool

Read, write, search, and manage files and directories in the project.

---

## Purpose

Provide agents with the ability to read and write files, search repository contents, create directories, and manage project filesystem operations.

---

## When to Use

- Reading source code files
- Writing new files or updating existing ones
- Searching for specific code patterns
- Creating new directories or structures
- Listing directory contents
- Checking file existence
- Reading configuration files
- Writing generated content

---

## Available Operations

### Read Operations
- Read file contents
- Read directory listing
- Search files by name/pattern
- Search file contents
- Get file metadata (size, modified time, etc.)

### Write Operations
- Create new files
- Update existing files
- Append to files
- Create directories
- Delete files (with safety checks)

### Search Operations
- Search by filename
- Search by content (grep pattern)
- Find files by extension
- Recursive search

### Metadata Operations
- Check file exists
- Get file size
- Get modification time
- Get file permissions

---

## Inputs

### Read File
- **Path** (required): File path relative to project root
- **Start Line** (optional): Line number to start reading (1-indexed)
- **End Line** (optional): Line number to end reading

### Write File
- **Path** (required): File path relative to project root
- **Content** (required): File content to write
- **Overwrite** (optional): Allow overwriting existing file (default: false)

### Search
- **Query** (required): Search term or regex pattern
- **Path** (optional): Directory to search (default: project root)
- **Include Pattern** (optional): File glob pattern
- **Recursive** (optional): Search recursively (default: true)

### Directory Operations
- **Path** (required): Directory path
- **Create Parents** (optional): Create parent directories (default: true)

---

## Outputs

### Read File Output
- **Content**: File contents as string
- **Line Count**: Number of lines in file
- **Encoding**: File encoding (usually UTF-8)

### Write File Output
- **Status**: Success/failure
- **Path**: Full path to file
- **Size**: File size in bytes

### Search Output
- **Matches**: List of matching files
- **Match Count**: Total matches found
- **Locations**: File paths and line numbers

### Directory Output
- **Contents**: List of files/directories
- **Count**: Number of items
- **Size**: Total directory size

---

## Dependencies

- **Filesystem MCP Server** - Provides file system access
- **VS Code File API** - Built-in file access
- **Project Root** - Must have access to workspace root

---

## Execution

**Method:** Filesystem MCP Server

**How it works:**
1. Agent specifies file operation (read, write, search, etc.)
2. Filesystem MCP server receives request
3. Operation executes on local filesystem
4. Results captured and returned
5. Appropriate formatting applied

**Constraints:**
- All paths relative to project root
- No access outside project directory
- Read-only for system files (outside project)
- Safe delete (confirmation required)

---

## Constraints

- All operations scoped to project root
- No access to files outside project
- Large files may be read in chunks
- Search limited to reasonable file size (prevents hanging on large files)
- No simultaneous writes to same file
- Safe deletion enforced (no rm -rf)

---

## Best Practices

### Path Handling
- Always use relative paths from project root
- Use forward slashes (converted automatically)
- Verify path safety before operations
- Check file exists before reading

### Reading
- For large files, read specific line ranges
- Check line count before reading
- Use appropriate encoding handling
- Log file paths for debugging

### Writing
- Create parent directories if needed
- Use atomic writes where possible
- Backup before overwriting critical files
- Validate content before writing

### Searching
- Use specific patterns to avoid noise
- Limit search scope when possible
- Escape special characters in patterns
- Handle large result sets

### Error Prevention
- Validate paths before operations
- Check permissions
- Verify file operations succeeded
- Handle encoding issues gracefully

---

## Error Handling

### Common Failures

**File Not Found**
- Cause: Specified file doesn't exist
- Recovery: Verify path, list directory, check spelling
- Log: Requested path and suggested corrections

**Permission Denied**
- Cause: No read/write permission
- Recovery: Check file permissions, request access
- Log: Path and permission requirements

**Path Outside Project**
- Cause: Attempted to access file outside project root
- Recovery: Use path relative to project root
- Log: Attempted path and project boundaries

**Encoding Error**
- Cause: File encoding not supported
- Recovery: Try different encoding, convert file
- Log: File path and detected encoding

**Disk Full**
- Cause: No space to write file
- Recovery: Free up disk space, split writes
- Log: Required space and available space

**Large File**
- Cause: File too large to process
- Recovery: Read in chunks, search instead of read
- Log: File size and memory available

---

## Tool Integration Examples

### Reading Agent Definition
```
Filesystem: Read file ai/agents/01-business-analyst.md
Purpose: Load agent instructions
Output: Agent definition content
```

### Writing Generated Code
```
Filesystem: Write file apps/backend/src/main.py
Content: Generated backend code
Purpose: Create implementation
Output: File path, size
```

### Searching for Patterns
```
Filesystem: Search for "TODO" in scripts/
Purpose: Find incomplete implementations
Output: List of files with TODOs
```

### Creating Directory Structure
```
Filesystem: Create directory apps/backend/src
Purpose: Prepare application structure
Output: Directory path
```

---

## See Also

- **Git Tool** - For version control of files
- **Code Analysis Tool** - For analyzing file contents
- **Terminal Tool** - For file operations via shell

Reference: `shared.md` for common guidance on validation and error handling.
