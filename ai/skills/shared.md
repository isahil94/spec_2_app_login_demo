# Shared Skills

This document defines shared, reusable capabilities used across all agents in the SDLC platform.

---

## Skill: Read Artifact

### Purpose
Load and parse artifacts from the workspace storage, making their content available for processing by agents.

### When to Use
- Loading requirements specifications
- Loading architecture documents
- Loading test plans or design documents
- Loading any previously generated artifact for downstream agents

### Inputs
- `artifact_path` (string): Relative path to the artifact file
- `artifact_type` (string): Expected format (markdown, json, yaml, openapi)
- `encoding` (string, optional): File encoding (default: utf-8)

### Outputs
- `content` (string): Raw file content
- `metadata` (object): Extracted frontmatter or header metadata
- `parsed` (object): Parsed content in structured format if applicable
- `format_valid` (boolean): Whether content matches expected format

### Dependencies
- Artifact storage directory must exist
- File must be readable and well-formed

### Execution Steps
1. Validate artifact path exists and is accessible
2. Load file content with specified encoding
3. Parse format-specific metadata (YAML frontmatter, JSON schema, etc.)
4. Validate content structure matches expected format
5. Return structured representation
6. Log artifact read event to audit trail

### Validation Checklist
- [ ] File exists and is readable
- [ ] File encoding is correct
- [ ] Content is well-formed (valid YAML, JSON, or Markdown)
- [ ] Metadata can be extracted successfully
- [ ] File size is reasonable (< 10MB)
- [ ] No sensitive data is exposed in logging

### Success Criteria
- Artifact loaded without parsing errors
- All expected fields present in content
- Metadata extracted and accessible
- Content hash computed for integrity verification

### Failure Conditions
- File not found or inaccessible
- Invalid encoding or corrupted content
- Unparseable format (malformed JSON, YAML, etc.)
- File exceeds size limits
- Required metadata missing

---

## Skill: Write Artifact

### Purpose
Persist generated content to the workspace storage with proper formatting, metadata, and versioning.

### When to Use
- Saving requirements documentation
- Saving architecture designs
- Saving generated code or tests
- Saving any deliverable artifact for downstream agents or review

### Inputs
- `artifact_path` (string): Target path relative to workspace
- `content` (string): Raw content to write
- `artifact_type` (string): Format type (markdown, json, yaml, code)
- `metadata` (object): Header metadata to include
- `overwrite` (boolean, optional): Allow overwriting existing files (default: false)

### Outputs
- `written_path` (string): Full path to written artifact
- `file_size` (integer): Size of written file in bytes
- `content_hash` (string): SHA-256 hash for integrity verification
- `timestamp` (datetime): Write timestamp
- `version` (string): Version identifier if applicable

### Dependencies
- Output directory must exist or be creatable
- Sufficient disk space available
- User has write permissions to target directory

### Execution Steps
1. Validate output directory exists (create if needed)
2. Prepare content with format-specific wrapping (YAML frontmatter, etc.)
3. Compute content hash before writing
4. Write file atomically (write to temp, then move)
5. Verify write success by reading back
6. Emit artifact written event to audit trail
7. Return artifact metadata

### Validation Checklist
- [ ] Output directory is writable
- [ ] Content is valid for target format
- [ ] Metadata includes required fields (id, version, agent, timestamp)
- [ ] No existing file will be overwritten without permission
- [ ] Content hash can be computed and verified
- [ ] File permissions are appropriate

### Success Criteria
- File written successfully to disk
- Content matches exactly what was intended
- Metadata persisted with artifact
- Content hash matches computed hash
- Artifact is readable by downstream agents

### Failure Conditions
- Output directory not writable or cannot be created
- Invalid content for target format
- Insufficient disk space
- Permission denied on write operation
- Content hash verification fails after write

---

## Skill: Validate Artifact

### Purpose
Verify that artifacts meet quality standards, structural requirements, and business rules before they proceed downstream.

### When to Use
- Validating requirements completeness
- Validating architecture coherence
- Validating generated code compiles/parses correctly
- Validating test coverage meets thresholds
- Validating data conforms to schema

### Inputs
- `artifact` (object): Artifact to validate
- `schema` (object): Validation schema or requirements
- `rules` (array): List of validation rules to apply
- `strict` (boolean, optional): Apply strict validation (default: false)

### Outputs
- `is_valid` (boolean): Overall validation result
- `errors` (array): List of validation errors with locations
- `warnings` (array): List of non-blocking issues
- `score` (number): Quality score 0-100
- `report` (object): Detailed validation report

### Dependencies
- Validation schema must be defined
- Artifact must be readable in expected format
- Validation rules must be consistent and non-contradictory

### Execution Steps
1. Load artifact and validation schema
2. Check structural compliance (required fields, types)
3. Validate business rules and constraints
4. Validate cross-references and dependencies
5. Compute quality metrics and scoring
6. Aggregate errors, warnings, and score
7. Generate detailed validation report
8. Return validation results

### Validation Checklist
- [ ] All required fields are present
- [ ] Field types match schema requirements
- [ ] Business rules are satisfied
- [ ] Cross-references are valid
- [ ] No circular dependencies
- [ ] Quality score meets minimum threshold

### Success Criteria
- `is_valid` returns true
- No critical errors present
- Quality score >= minimum acceptable level
- All warnings logged for review
- Validation report generated

### Failure Conditions
- Critical validation errors present
- Required fields missing
- Quality score below threshold
- Business rules violated
- Schema or rules not available

---

## Skill: Publish Artifact

### Purpose
Make artifacts officially available to downstream agents and stakeholders by moving them through the artifact lifecycle.

### When to Use
- Marking requirements as complete and ready for architecture
- Marking architecture as ready for implementation
- Marking code ready for testing
- Marking any artifact as ready for next stage

### Inputs
- `artifact_path` (string): Path to artifact to publish
- `target_stage` (string): Next stage in workflow (e.g., "ready_for_implementation")
- `notes` (string, optional): Publication notes
- `metadata_updates` (object, optional): Additional metadata to include

### Outputs
- `published` (boolean): Publication successful
- `publication_timestamp` (datetime): When published
- `previous_state` (string): Previous workflow state
- `new_state` (string): Current workflow state
- `publication_event` (object): Event emitted to workflow bus

### Dependencies
- Artifact must exist and be valid
- Target stage must be valid in workflow DAG
- Publication rules must allow transition

### Execution Steps
1. Load artifact and verify it's valid
2. Validate target stage is valid in workflow
3. Check publication preconditions (artifact quality, dependencies)
4. Update artifact metadata with publication info
5. Write updated artifact to storage
6. Emit publication event to event bus
7. Log to audit trail
8. Notify downstream agents via event system

### Validation Checklist
- [ ] Artifact exists and is accessible
- [ ] Artifact passes validation
- [ ] Target stage is valid for artifact type
- [ ] Publication preconditions met
- [ ] Metadata can be updated
- [ ] Event bus is available

### Success Criteria
- Artifact metadata updated with publication state
- Event emitted to workflow bus
- Downstream agents can access published artifact
- Audit trail reflects publication

### Failure Conditions
- Artifact does not exist or is invalid
- Target stage invalid or unreachable
- Preconditions not met
- Event bus unavailable
- Permission denied on publication

---

## Skill: Request Human Approval

### Purpose
Create formal approval requests for decisions that require human oversight, blocking workflow until approved.

### When to Use
- Requesting approval of requirements interpretation
- Requesting approval of architectural decisions
- Requesting approval before implementation
- Requesting final review before deployment

### Inputs
- `approval_type` (string): Type of approval needed (design_review, architecture_review, code_review, deployment_approval)
- `artifact_paths` (array): Paths to artifacts requiring approval
- `context` (object): Context information for approvers
- `deadline` (datetime, optional): Approval deadline
- `approvers` (array, optional): Specific roles/people to approve

### Outputs
- `approval_request_id` (string): Unique identifier for this request
- `created_timestamp` (datetime): When request was created
- `status` (string): Initial status (pending, approved, rejected, expired)
- `notification_sent` (boolean): Whether notification was sent
- `approval_url` (string): Link to approval interface

### Dependencies
- Approval service must be available
- Artifacts must exist and be readable
- Approver roles must be defined
- Notification system must be configured

### Execution Steps
1. Validate approval type and artifacts
2. Generate approval request document
3. Create approval request record
4. Send notifications to approvers
5. Start approval timeout timer if deadline set
6. Emit approval_requested event
7. Block dependent tasks until approval received
8. Return approval request details

### Validation Checklist
- [ ] Approval type is valid
- [ ] All referenced artifacts exist
- [ ] Approvers are defined and available
- [ ] Context is complete and clear
- [ ] Deadline is reasonable if specified
- [ ] Notification recipients are configured

### Success Criteria
- Approval request created and persisted
- Notifications sent to approvers
- Workflow blocks pending approval
- Approval request accessible in dashboard

### Failure Conditions
- Approval type not recognized
- Artifacts missing or inaccessible
- Approvers not available
- Notification delivery failed
- Approval service unavailable

---

## Skill: Retrieve Workflow Memory

### Purpose
Access shared workflow state and memory that persists across agent executions, enabling agents to maintain context.

### When to Use
- Accessing execution state from previous agents
- Reading shared configuration
- Accessing execution history
- Reading metrics or progress tracking

### Inputs
- `memory_key` (string): Key identifying the memory item
- `scope` (string, optional): Memory scope (global, workflow, agent)
- `default_value` (any, optional): Value to return if key not found

### Outputs
- `value` (any): The retrieved memory value
- `exists` (boolean): Whether key was found
- `last_updated` (datetime): When value was last modified
- `source_agent` (string): Which agent last wrote this value

### Dependencies
- Workflow memory service must be available
- Memory keys must follow naming convention

### Execution Steps
1. Validate memory key format
2. Query memory service for key
3. Deserialize value from storage
4. Apply scope filtering if specified
5. Return value or default

### Validation Checklist
- [ ] Memory key is valid format
- [ ] Scope is valid
- [ ] Memory service is accessible

### Success Criteria
- Value retrieved successfully
- Value is valid and deserializable
- Timestamp is accurate

### Failure Conditions
- Key not found and no default provided
- Memory service unavailable
- Value corrupted or undeserializable

---

## Skill: Update Workflow Memory

### Purpose
Persist data to shared workflow memory for use by downstream agents and workflow tracking.

### When to Use
- Storing execution state for next agent
- Updating progress metrics
- Storing configuration for workflow
- Recording decisions made

### Inputs
- `memory_key` (string): Key identifying the memory item
- `value` (any): Value to store (must be serializable)
- `scope` (string, optional): Memory scope (default: workflow)
- `ttl` (integer, optional): Time-to-live in seconds

### Outputs
- `stored` (boolean): Whether value was stored successfully
- `timestamp` (datetime): When value was stored
- `key` (string): Actual key used for retrieval

### Dependencies
- Workflow memory service must be available
- Value must be serializable to JSON

### Execution Steps
1. Validate memory key format
2. Serialize value to JSON
3. Write to memory service
4. Set TTL if specified
5. Return confirmation

### Validation Checklist
- [ ] Key format is valid
- [ ] Value is serializable
- [ ] Memory service is accessible
- [ ] TTL is reasonable if specified

### Success Criteria
- Value stored in memory service
- Retrievable by downstream agents
- Timestamp recorded accurately

### Failure Conditions
- Key format invalid
- Value not serializable
- Memory service unavailable
- Write permission denied
