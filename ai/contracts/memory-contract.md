# Memory Contract

Contract Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved

## 1. Purpose and Scope
This document defines shared runtime memory used by the Supervisor, orchestration engine, and all agents. Memory stores references and execution context only.

Related contracts:
- artifact-contracts.md
- event-contracts.md
- workflow-state.md
- approval-contract.md

## 2. Core Rule
Do not store artifacts inside memory. Store only references, metadata, and summaries required for orchestration.

## 3. Memory Domains

### 3.1 Workflow Memory
Scope: Entire workflow lifecycle.

Required fields:
- workflowId
- workflowVersion
- currentState
- activeExecutionId
- artifactIndex (references only)
- openQuestionsIndex
- approvalIndex
- eventIndex

Optional fields:
- policyOverrides
- priority

### 3.2 Execution Memory
Scope: One execution attempt within a workflow.

Required fields:
- executionId
- workflowId
- attemptNumber
- startedAt
- lastUpdatedAt
- state
- participatingAgents
- retryMetadataRef

Optional fields:
- timeoutMetadata
- schedulerMetadata

### 3.3 Agent Memory
Scope: One agent within one execution.

Required fields:
- agentId
- executionId
- inputArtifactRefs
- outputArtifactRefs
- validationSummaryRef
- qualityReportRef

Optional fields:
- localDecisionNotes
- warningRefs

### 3.4 Artifact References
Reference schema:
- artifactId
- artifactType
- version
- ownerAgentId
- locationRef
- checksum
- status

### 3.5 Open Questions
Required fields:
- questionId
- sourceAgentId
- workflowId
- executionId
- category: Business | Functional | UX | Security | Performance | Compliance | Data | Integration | Architecture | Testing | Documentation | Deployment
- questionText
- reason
- impactLevel: Low | Medium | High
- defaultAssumption
- blocking: Yes | No
- approvalRequired: Yes | No
- targetStage: Business Analysis | Solution Architecture | UI/UX | Backend | Database | QA | Documentation | DevOps
- confidence: 0-100
- owner
- relatedRequirements
- potentialRisk
- raisedAt
- status: Open | Resolved | Deferred

Optional fields:
- relatedArtifactRef
- approvalRef

Workflow summary fields (required when persisting open-question sets):
- totalQuestions
- blockingQuestions
- approvalRequestsRequired
- workflowStatus: REQUIRES HUMAN APPROVAL | READY
- nextAgent

### 3.6 Retry Metadata
Required fields:
- retryRecordId
- executionId
- agentId
- retryCount
- retryLimit
- retryReason
- backoffPolicy
- lastRetryAt

Optional fields:
- retryOutcomeSummary

### 3.7 Approval Metadata
Required fields:
- approvalId
- workflowId
- executionId
- requestedBy
- requestedAt
- decisionStatus
- decisionAt
- decisionBy
- rationale

Optional fields:
- escalationRef
- timeoutRef

### 3.8 Event History
Required fields:
- eventId
- eventName
- category
- timestamp
- status
- correlationId

Optional fields:
- causationEventId

## 4. Persistence Model
1. Memory entries are append-only records with immutable historical versions.
2. Current view is derived from the latest valid version per key.
3. Every write includes:
   - memoryEntryId
   - memoryScope
   - version
   - createdAt
   - createdBy
   - changeReason

## 5. Versioning
- Memory schema versioning uses semantic versioning.
- Entries include schemaVersion field.
- Consumers must reject unsupported major versions.

## 6. Retention Policy
- Workflow Memory: Retain for 365 days after terminal workflow state.
- Execution Memory: Retain for 180 days after execution completion.
- Agent Memory: Retain for 180 days.
- Event History Index: Retain for 365 days; archive summary after 90 days.
- Open Questions and Approval Metadata: Retain for 365 days minimum for audit.

## 7. Cleanup Policy
1. Cleanup is policy-driven and non-destructive for records under legal or audit hold.
2. Cleanup must preserve reference integrity.
3. Cleanup operations emit Memory category events.
4. Archived entries remain queryable through archive index.

## 8. Concurrency Rules
1. Write model: optimistic concurrency with version precondition.
2. Conflict behavior:
   - Reject conflicting write.
   - Emit Failure or Retry event based on policy.
   - Re-read latest version and retry if permitted.
3. Supervisor has arbitration authority for unresolved write conflicts.
4. Per-key serialization required for state-critical memory keys:
   - workflow state pointer
   - active execution pointer
   - approval decision pointer

## 9. Example Memory Structures
```yaml
workflowMemory:
  workflowId: wf-2026-06-30-001
  workflowVersion: 1.0.0
  currentState: Running
  activeExecutionId: exec-0142
  artifactIndex:
    - artifactId: art-requirements-0003
      artifactType: requirements.md
      version: 1.0.0
      locationRef: artifacts/requirements/requirements.md

executionMemory:
  executionId: exec-0142
  workflowId: wf-2026-06-30-001
  attemptNumber: 2
  state: Retrying
  retryMetadataRef: retry-0142-02

agentMemory:
  agentId: qa-engineer
  executionId: exec-0142
  inputArtifactRefs:
    - art-backend-spec-0011@1.1.0
  outputArtifactRefs:
    - art-qa-report-0002@1.0.0
  qualityReportRef: qr-qa-0142
```

## 10. Compliance and Audit
- All memory mutations must be attributable to agentId or Supervisor.
- All approval-linked memory entries must be auditable against approval-contract.md.
- Memory references to artifacts must align with artifact-contracts.md reference schema.
