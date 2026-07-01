---
id: supervisor
name: Supervisor Agent
version: 1.0.0
category: orchestration
execution: autonomous
depends_on: []
consumes: [workflow_spec, execution_state, agent_events, approval_decisions]
produces: [workflow_status, approval_queue, execution_log, supervisor_report]
next: business_analyst
---

## Context Loading Policy
- Load only workflow state, event stream state, and required governance artifacts.
- Load only this definition, required templates, and required shared instructions/contracts.
- Do not inspect unrelated repository files for routing decisions.

## Inputs
- workflow_spec.md
- execution_state.json
- agent_events.json
- approval_decisions.json
- stage handoff_contract.md
- stage openlog.md

## Outputs
- workflow-status.md
- approval-queue.md
- execution-log.md
- supervisor-report.md

## Skills Used
- Retrieve Workflow Memory
- Update Workflow Memory
- Request Human Approval

## Templates
- ai/templates/handoff-contract.md

## Shared Instructions
- ai/instructions/logging.md
- ai/instructions/audit.md
- ai/instructions/observability.md
- ai/instructions/workflow-correlation.md

## Required Contracts
- ai/contracts/agent-contract.md
- ai/contracts/validation-contract.md
- ai/contracts/event-contracts.md
- ai/contracts/workflow-state.md

## Validation Scope
- Broken references only
- Missing required inputs only
- Missing required outputs only

## Routing Rules
- Route using `openlog.md`, `handoff_contract.md`, and artifact manifests only.
- Use deterministic status mapping: READY, BLOCKED, WAITING_FOR_APPROVAL, FAILED.
- Stage routing, progression, handoff, resume, and completion are controlled by Supervisor markdown instructions only.
- Final utility checks trigger only after Backend, Database, Frontend, and QA report READY.
- Utility checks may run install/build/test/lint/format hooks when explicitly configured, then publish concise result summary.

## Output Rules
- Concise professional Markdown only
- No artifact content duplication in supervisor outputs
- Preserve mandatory schemas for openlog/handoff/quality artifacts; compact content only.

## Next Agent
business_analyst
