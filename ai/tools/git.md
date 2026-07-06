# Git Tool

Perform version control operations using Git.

---

## Purpose

Provide agents with the ability to check repository status, view diffs, commit changes, manage branches, and inspect repository history.

---

## When to Use

- Checking repository status
- Viewing diffs before committing
- Committing code changes
- Creating and switching branches
- Restoring files
- Viewing commit history
- Creating tags
- Checking git configuration

---

## Available Operations

### Status Operations
- Check repository status (modified, staged, untracked files)
- Check if repository is clean
- Get current branch name
- List all branches

### Diff Operations
- View unified diff of changes
- View diff for specific file
- Compare branches
- Compare commits

### Commit Operations
- Stage files
- Commit changes
- Amend last commit
- View commit messages

### Branch Operations
- Create branch
- Switch branch
- Delete branch
- List branches
- Merge branches

### File Operations
- Restore file to last committed version
- Discard changes in working directory
- Reset file staging

### History Operations
- View commit log
- View file history
- Blame specific lines
- Search commit messages

### Tag Operations
- Create tag
- Delete tag
- List tags
- Show tag information

---

## Inputs

### Commit
- **Message** (required): Commit message
- **Files** (optional): Specific files to commit (default: all staged)
- **Force** (optional): Skip hooks and validation

### Branch Operations
- **Branch Name** (required): Name of branch
- **Base Branch** (optional): Branch to base from (default: main)

### Diff
- **Path** (optional): Specific file to diff
- **From** (optional): Compare from specific commit
- **To** (optional): Compare to specific commit

### Log
- **Count** (optional): Number of commits to show (default: 10)
- **Path** (optional): Filter by specific path

---

## Outputs

### Status Output
- **Branch**: Current branch name
- **Modified**: List of modified files
- **Staged**: List of staged files
- **Untracked**: List of untracked files
- **Clean**: Boolean indicating if repository is clean

### Diff Output
- **Unified Diff**: Diff content
- **File Count**: Number of files changed
- **Additions**: Number of lines added
- **Deletions**: Number of lines deleted

### Commit Output
- **SHA**: Commit hash
- **Message**: Commit message
- **Author**: Commit author
- **Date**: Commit date/time

### Log Output
- **Commits**: List of commits (SHA, message, author, date)
- **Count**: Number of commits shown

---

## Dependencies

- **Git MCP Server** - Provides git operations
- **Git Installation** - System Git binary
- **Repository** - Valid Git repository in workspace
- **Git Configuration** - User name and email configured

---

## Execution

**Method:** Git MCP Server

**How it works:**
1. Agent specifies git operation
2. Git MCP server receives command
3. Git command executes in repository
4. Output parsed and formatted
5. Results returned to agent

**All operations executed in project repository.**

---

## Constraints

- All operations scoped to project repository
- Requires valid Git installation
- Requires Git user configuration (name, email)
- Cannot force-push to protected branches
- Large histories may be truncated
- Binary files handled specially

---

## Best Practices

### Commit Messages
- Use descriptive commit messages
- Follow project commit message format (enforced by hooks)
- Reference issues/PRs when relevant
- Keep messages concise but clear

### Branching
- Create feature branches for new work
- Use meaningful branch names
- Base from main/develop as appropriate
- Delete merged branches

### Before Committing
- Review diffs carefully
- Run tests before commit
- Format code before commit
- Verify no debugging code included

### History Inspection
- Check history before rebasing
- Review diffs before merging
- Understand blame context
- Use log filtering to find relevant commits

### Safety
- Never force-push to main branch
- Verify branch before pushing
- Create backups before destructive operations
- Commit frequently for safety

---

## Error Handling

### Common Failures

**Not a Git Repository**
- Cause: Working directory not a Git repository
- Recovery: Initialize repository or navigate to correct directory
- Log: Current path and repository status

**Uncommitted Changes**
- Cause: Trying to switch branches with uncommitted changes
- Recovery: Commit or stash changes first
- Log: List of conflicting files

**Merge Conflict**
- Cause: Attempting to merge conflicting changes
- Recovery: Resolve conflicts, complete merge or abort
- Log: Conflicting files and conflict markers

**Configuration Missing**
- Cause: Git user.name or user.email not configured
- Recovery: Configure with `git config user.name/email`
- Log: Missing configuration values

**Branch Already Exists**
- Cause: Creating branch with existing name
- Recovery: Use different name or delete existing branch
- Log: Existing branch name and hash

**Push Rejected**
- Cause: Remote has newer changes
- Recovery: Pull first, then push
- Log: Rejected reason and remote status

---

## Tool Integration Examples

### Check Repository Status
```
Git: Check status
Purpose: Determine what files need committing
Output: Modified, staged, untracked files
```

### Create Feature Branch
```
Git: Create branch feature/new-feature
Base: main
Purpose: Start new feature work
Output: Branch created and switched
```

### Review Changes Before Commit
```
Git: Show diff
Purpose: Verify changes are correct
Output: Unified diff with statistics
```

### Commit Changes
```
Git: Commit message: "[feat] add new capability"
Purpose: Save work to repository
Output: Commit hash, message
```

---

## See Also

- **GitHub Tool** - For remote operations (push, pull requests)
- **Terminal Tool** - For advanced Git commands
- **Filesystem Tool** - For viewing files in repository

Reference: `shared.md` for common guidance on validation and error handling.
