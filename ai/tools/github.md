# GitHub Tool

Interact with GitHub API for repository management, pull requests, issues, releases, and workflows.

---

## Purpose

Provide agents with the ability to interact with GitHub for repository operations, pull request management, issue tracking, workflow status, and release management.

---

## When to Use

- Creating and managing pull requests
- Creating and updating issues
- Checking GitHub Actions workflow status
- Publishing releases
- Managing repository metadata
- Creating deployments
- Checking branch protection rules
- Adding comments to PRs/issues

---

## Available Operations

### Pull Request Operations
- Create pull request
- Update pull request (title, description)
- Merge pull request
- Close pull request
- Request review
- Dismiss reviews
- Check merge status

### Issue Operations
- Create issue
- Update issue (title, description, labels)
- Close issue
- Add labels
- Assign issue
- Add comments

### Workflow Operations
- Check workflow status
- List recent workflow runs
- Trigger workflow manually
- Cancel workflow run
- Get workflow artifacts

### Release Operations
- Create release
- Update release
- Delete release
- Publish release
- Get release information

### Repository Operations
- Get repository metadata
- Check branch protection
- Get collaborators
- Update repository settings

### Deployment Operations
- Create deployment
- Update deployment status
- Get deployment history

---

## Inputs

### Pull Request
- **Title** (required): PR title
- **Description** (required): PR description
- **Head** (required): Source branch
- **Base** (required): Target branch (default: main)
- **Draft** (optional): Create as draft

### Issue
- **Title** (required): Issue title
- **Description** (required): Issue description
- **Labels** (optional): List of labels
- **Assignee** (optional): GitHub username

### Workflow
- **Workflow ID** (required): Workflow identifier
- **Ref** (optional): Branch or tag to run on

### Release
- **Tag Name** (required): Release tag
- **Name** (optional): Release name
- **Body** (required): Release notes
- **Draft** (optional): Create as draft
- **Prerelease** (optional): Mark as prerelease

---

## Outputs

### Pull Request Output
- **PR Number**: Pull request number
- **URL**: PR URL
- **Status**: Draft/Open/Merged/Closed
- **Merge Status**: Can merge/Conflicts/etc.

### Issue Output
- **Issue Number**: Issue number
- **URL**: Issue URL
- **Status**: Open/Closed
- **Labels**: Assigned labels

### Workflow Output
- **Status**: Success/Failure/Running
- **Conclusion**: Neutral/Success/Failure/etc.
- **Artifacts**: Available artifacts
- **Duration**: Execution time

### Release Output
- **Release URL**: GitHub release URL
- **Tag**: Release tag
- **Status**: Published/Draft
- **Artifacts**: Release assets

---

## Dependencies

- **GitHub MCP Server** - Provides GitHub API access
- **GitHub Account** - Authenticated GitHub access
- **Repository Permissions** - Appropriate access level
- **GitHub CLI** - Optional for local operations

---

## Execution

**Method:** GitHub MCP Server

**How it works:**
1. Agent specifies GitHub operation
2. GitHub MCP server authenticates with GitHub
3. API request executed
4. Response parsed and formatted
5. Results returned to agent

**Authentication via GitHub token stored in environment.**

---

## Constraints

- Requires GitHub authentication (token in environment)
- Limited by GitHub API rate limits (5000 requests/hour)
- Repository permissions required for operations
- Cannot delete repositories
- Cannot modify protected branches directly
- PR/Issue operations limited by branch protection rules

---

## Best Practices

### Pull Requests
- Include detailed description of changes
- Reference related issues
- Request reviews from relevant team members
- Verify CI checks pass before merging
- Use drafts for work-in-progress

### Issues
- Use clear, descriptive titles
- Include steps to reproduce
- Add relevant labels
- Assign to responsible party
- Link related issues

### Workflow Management
- Monitor workflow status
- Cancel long-running workflows
- Review workflow artifacts
- Check for required checks
- Verify deployment approvals

### Release Management
- Update CHANGELOG before release
- Tag consistently (e.g., v1.0.0)
- Include comprehensive release notes
- Test release artifacts
- Follow semantic versioning

### Rate Limiting
- Batch operations when possible
- Implement caching for frequently accessed data
- Check rate limit status
- Respect rate limit headers

---

## Error Handling

### Common Failures

**Authentication Failed**
- Cause: Invalid or missing GitHub token
- Recovery: Check token in environment, refresh if expired
- Log: Token status and expiration

**Permission Denied**
- Cause: Insufficient permissions for operation
- Recovery: Check repository permissions, request access
- Log: Required permissions and current level

**Branch Protection**
- Cause: Cannot push to protected branch
- Recovery: Create PR instead, get required approvals
- Log: Branch protection rules

**Rate Limit Exceeded**
- Cause: Too many API calls
- Recovery: Wait for rate limit reset, batch operations
- Log: Rate limit reset time

**Merge Conflict**
- Cause: PR has conflicts
- Recovery: Resolve conflicts locally, push updated branch
- Log: Conflicting files

**CI Check Failed**
- Cause: Required checks failed
- Recovery: Fix failures, re-run checks
- Log: Failed check names and logs

---

## Tool Integration Examples

### Create Pull Request
```
GitHub: Create PR
Title: "Add new feature"
Description: "Implements feature X"
Head: feature/new-feature
Base: main
Purpose: Submit code for review
Output: PR #123, URL
```

### Check Workflow Status
```
GitHub: Check workflow status
Workflow: CI Pipeline
Purpose: Verify tests pass
Output: Status, artifacts, duration
```

### Create Release
```
GitHub: Create release
Tag: v1.0.0
Body: Release notes
Purpose: Publish new version
Output: Release URL, assets
```

### Create Issue
```
GitHub: Create issue
Title: "Bug: Format fails on Windows"
Labels: bug, windows
Purpose: Track bug fix
Output: Issue #456
```

---

## See Also

- **Git Tool** - For local git operations before GitHub operations
- **Terminal Tool** - For GitHub CLI commands
- **Workflow Operations** - Integration with GitHub Actions

Reference: `shared.md` for common guidance on validation and error handling.
