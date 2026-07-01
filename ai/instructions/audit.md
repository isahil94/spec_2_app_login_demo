# Audit Instructions

**Version:** 1.0.0  
**Status:** Shared Platform Capability  
**Last Updated:** 2026-07-01

This document provides unified audit guidance for all agents in the Agentic SDLC platform.

**Purpose:** Ensure all consequential agent decisions are recorded with complete traceability for compliance, recovery, and governance.

## Overview

Auditing captures **decisions** and **changes**, not just actions. Every audit record creates an immutable trail showing what changed, who made the decision, why it was made, and what inputs drove it.

Audit records are different from logs:
- **Logs** = what happened (actions and events)
- **Audit records** = what changed and why (decisions with justification)

The Supervisor aggregates all audit records to support compliance, forensics, and decision review.

## Audit Record Structure

Use the template `ai/templates/audit-entry.md` for all audit records.

Every audit record **must** contain:

### Required Fields
- **Audit ID**: Unique identifier (UUID format or sequential)
- **Timestamp**: ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sssZ)
- **Agent**: Name of the agent making the decision
- **Action**: Type of decision (e.g., "artifact_generated", "requirement_rejected", "approval_requested")
- **Reason**: Brief explanation of why this decision was made
- **Input Artifacts**: List of artifacts consumed to make this decision
- **Output Artifacts**: List of artifacts produced by this decision
- **Decision**: The actual decision made (e.g., "APPROVED", "REJECTED", "REQUIRES_CLARIFICATION")
- **Confidence**: Confidence score (0.0 to 1.0) in the decision

### Optional Fields
- **Approval Information**: Approval request ID, status, decision reason (if approval is involved)
- **Version**: Version identifier (commit hash, timestamp, or semantic version)
- **Justification**: Extended explanation (Markdown) of reasoning
- **Alternative Options**: Other options considered and why they were rejected
- **Risk Assessment**: Any risks identified with this decision
- **Metadata**: Key-value pairs for contextual information
- **Previous Decision**: Reference to prior audit record if this is a reversal or update

## When to Audit

Every agent **must** create an audit record when:

1. **Artifact generation**: Creating a new artifact
2. **Major decisions**: Accepting/rejecting requirements, choosing architecture patterns, etc.
3. **Approval requests**: Requesting human approval
4. **Approval decisions**: Recording approval outcome
5. **Quality gates**: Passing or failing validation
6. **Traceability decisions**: Linking artifacts to requirements
7. **Escalations**: Escalating issues or blockers

**Do NOT audit**: Routine reads, temporary calculations, routine logs.

## Audit Patterns

### Pattern 1: Artifact Generation Decision

```
Audit Record:
- Audit ID: audit-20260701-001
- Timestamp: 2026-07-01T14:22:33.125Z
- Agent: business_analyst
- Action: artifact_generated
- Reason: "Requirements analysis complete. Artifact ready for handoff to Solution Architect."
- Input Artifacts:
  - specification.md (v1.0.0)
  - Figma URL from specification.md (if present)
- Output Artifacts:
  - requirements_spec.md (v1.0.0)
  - user_stories.md (v1.0.0)
  - acceptance_criteria.md (v1.0.0)
- Decision: APPROVED_FOR_HANDOFF
- Confidence: 0.95
- Justification: "All requirements extracted and validated. Acceptance criteria well-defined."
- Metadata:
  - requirement_count: 42
  - story_count: 18
  - validation_score: 0.94
```

### Pattern 2: Approval Request

```
Audit Record:
- Audit ID: audit-20260701-002
- Timestamp: 2026-07-01T15:45:20.800Z
- Agent: solution_architect
- Action: approval_requested
- Reason: "Architecture design requires approval due to complexity score of 0.78 exceeding 0.70 threshold."
- Input Artifacts:
  - requirements_spec.md (v1.0.0)
- Output Artifacts:
  - architecture-design.md (v1.0.0, pending approval)
- Decision: AWAITING_APPROVAL
- Confidence: 0.88
- Approval Information:
  - approval_request_id: apr-20260701-001
  - status: pending
  - required_reviewers: ["solution-architect-lead", "backend-tech-lead"]
- Risk Assessment: "High complexity architecture may require additional documentation."
```

### Pattern 3: Approval Decision

```
Audit Record:
- Audit ID: audit-20260701-003
- Timestamp: 2026-07-01T16:30:12.450Z
- Agent: supervisor
- Action: approval_decision
- Reason: "Architecture approved by 2 of 2 required reviewers."
- Input Artifacts:
  - architecture-design.md (v1.0.0)
  - approval_request: apr-20260701-001
- Output Artifacts:
  - architecture-design.md (v1.0.0, approved)
- Decision: APPROVED
- Confidence: 1.0
- Approval Information:
  - approval_request_id: apr-20260701-001
  - status: approved
  - approved_by: ["reviewer1", "reviewer2"]
  - approval_timestamp: 2026-07-01T16:30:00.000Z
  - approval_notes: "Architecture is well-documented and scalable."
- Version: architecture-design.md:v1.0.0
```

### Pattern 4: Quality Gate Decision

```
Audit Record:
- Audit ID: audit-20260701-004
- Timestamp: 2026-07-01T17:15:45.200Z
- Agent: qa_engineer
- Action: quality_gate_passed
- Reason: "All QA tests passed. API documentation complete. Test coverage: 94%."
- Input Artifacts:
  - backend-api.py (v2.1.3)
  - test-report.md (v1.0.0)
- Output Artifacts:
  - qa-approval.md (v1.0.0)
  - quality-report.md (v1.0.0)
- Decision: READY_FOR_RELEASE
- Confidence: 0.96
- Metadata:
  - test_count: 245
  - test_passed: 245
  - test_failed: 0
  - coverage_percent: 94
  - duration_minutes: 12
```

### Pattern 5: Requirement Rejection

```
Audit Record:
- Audit ID: audit-20260701-005
- Timestamp: 2026-07-01T10:05:22.600Z
- Agent: solution_architect
- Action: requirement_analysis
- Reason: "Requirement REQ-042 marked as unfeasible. Conflicts with architectural constraints."
- Input Artifacts:
  - requirements_spec.md (v1.0.0)
  - architecture-constraints.md (v1.0.0)
- Output Artifacts:
  - architecture-design.md (v1.0.0)
  - constraint-analysis.md (v1.0.0)
- Decision: REJECTED_WITH_RATIONALE
- Confidence: 0.92
- Justification: |
  Requirement REQ-042 requests real-time synchronization across 500+ concurrent users.
  Architecture uses REST API (pull-based). WebSocket implementation would require:
  - 6 weeks additional development
  - $40K infrastructure cost
  - Conflicts with MVP timeline by 8 weeks
  
  Recommendation: Phase as post-MVP enhancement.
- Alternative Options:
  - Option 1: Implement WebSocket → +8 weeks to MVP, deferred
  - Option 2: Use polling with 5-second intervals → Acceptable compromise
- Previous Decision: null (first decision on this requirement)
```

## Audit Trail Requirements

1. **Immutable**: Audit records are append-only. Decisions cannot be deleted or modified.
2. **Traceable**: Every decision must link to inputs and outputs by artifact name and version.
3. **Dated**: Every record includes timestamp and version information for temporal analysis.
4. **Justified**: Every decision must include reasoning sufficient for external review.
5. **Identifiable**: Every decision links to a specific agent (no anonymous decisions).
6. **Unique**: Every record has a unique audit ID for precise reference.

## Implementation Rules

1. **One record per decision**: Create one audit record per distinct decision point, not per step.
2. **Link artifacts by reference**: Reference artifacts by name and version, not by full content.
3. **Confidence scores**: Be conservative. Use 0.8-0.95 for routine decisions, 0.5-0.8 for uncertain ones.
4. **Immutable timestamps**: Use creation time, never adjust timestamps retroactively.
5. **Clear reasoning**: Justification must be clear to a reviewer unfamiliar with the work.
6. **Version tracking**: Always include artifact version for reproducibility.

## Audit Anti-Patterns

❌ **Do NOT:**
- Create audit records for trivial actions (reading config files)
- Omit reasoning from decisions
- Use vague action types
- Log PII in audit records
- Modify or delete prior audit entries
- Reference artifacts without version
- Create duplicate decisions
- Use non-standard audit IDs

## Reference Template

Use `ai/templates/audit-entry.md` for the complete template structure.

## Supervisor Responsibilities

The Supervisor:
- Collects audit records from all agents
- Creates unified audit trail in chronological order
- Validates audit record completeness
- Links audit records to artifacts for traceability
- Retains audit records indefinitely for compliance
- Provides audit reports by agent, decision type, and time period

**Agents do not need to implement custom audit collection or storage.**
