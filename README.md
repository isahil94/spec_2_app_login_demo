# Specs to App

Specs to App is an end-to-end SDLC orchestration platform for turning a software specification into a working application with automated agent-driven execution. This repository demonstrates the workflow using a task management system as the generated sample application.

## Overview

This project is not just a task management application. It is a platform that combines:

- a specification-first workflow
- specialized AI agents for business analysis, architecture, UI/UX, backend, database, and QA
- artifact-based handoffs and validation checkpoints
- supervisor-driven approvals and blocked-state handling
- a runnable sample application generated from the workflow

## What the platform does

The workflow begins from a specification and progresses through a series of agent stages to produce implementation artifacts, application code, tests, and delivery outputs. The sample task management system is the concrete example produced by this pipeline.

## Core workflow

The SDLC flow is organized around stages such as:

1. Business analysis
2. Solution architecture
3. UI/UX implementation
4. Backend implementation
5. Database implementation
6. QA and validation

Each stage produces or updates artifacts, and the process can pause at approval gates or blocked states until the supervisor decides to continue.

### Human gate points

The workflow includes explicit human approval checkpoints after Solution Architecture and at the end of the pipeline:

- after Solution Architecture, the orchestrator pauses for review and approval before implementation proceeds
- at the final stage, the supervisor requests confirmation before the workflow is considered complete

These gates ensure that architecture decisions and final delivery outcomes are reviewed before moving forward.

## Agent-based orchestration

The repository includes five main agent roles in the workflow:

- Business Analyst
- Solution Architect
- UI/UX Developer
- Backend Developer
- Database Developer
- QA Engineer

The platform also supports a supervisor-driven execution model, where hooks and ticks monitor artifact changes and invoke the next stage automatically.

## Workflow execution model

The pipeline runs through a supervisor loop that:

1. watches artifact changes such as openlog, handoff-contract, and QA reports
2. triggers a supervisor tick on a timer or manual command
3. loads workflow state from the orchestrator state file
4. evaluates the current stage and next required action
5. invokes the relevant agent or approval gate
6. checks generated artifacts and completion status
7. pauses for human approval or blocked-item handling when required

## Hooks and supervisor flow

The system uses hooks that run in the background to monitor execution state and trigger the pipeline. The flow is:

1. a hook detects a relevant artifact change or a timer interval event
2. the supervisor tick is invoked
3. the orchestrator evaluates the current workflow stage
4. curated prompts are sent to the next agent in sequence
5. the agent generates or updates artifacts and implementation output
6. the hook observes the start/stop lifecycle of the agent execution
7. the workflow continues, pauses for approval, or enters a blocked state as needed

This is the mechanism that enables the platform to run end to end from specification to deliverable.

## Installation and compile steps

1. Unzip the project archive if necessary.

```bash
unzip sdlc-orchestrator-ext-VSCODE.zip
cd sdlc-orchestrator-ext
```

2. Install development dependencies and compile the extension.

```bash
npm install --save-dev @types/vscode @types/node typescript
npm run compile
```

## Open and run in VS Code

1. Open the extension folder in VS Code as seperate window.
2. Press F5 or select Run > Start Debugging.
3. A second VS Code window opens as the Extension Development Host.
4. Open your actual project folder in that host window.
5. Use a test workspace with stub agents first if needed.

## How the extension activates

When the extension activates in the target workspace, it:

- registers the command SDLC: Run Supervisor Tick
- watches artifacts for changes in openlog, handoff-contract, and QA report files
- starts a polling timer every 2 minutes
- registers the supervisor chat participant for approvals and human commands

## How to invoke the pipeline

The pipeline starts when:

- a watched artifact file changes
- the polling timer fires
- you run the supervisor tick command manually

The engine then:

- loads workflow state from the orchestrator state file
- runs kickoff prompts if needed
- evaluates the current stage
- invokes the next agent(s)
- checks artifact and implementation completion
- pauses for approvals or blocked-state resolution

## Kickoff prompts

On the first run, the workflow asks for:

1. the specification path
2. the artifact handling mode: clean, backup, or keep
3. the Figma or make-file input mode, if applicable

## Human commands via supervisor chat

You can interact with the supervisor through chat using commands such as:

- start — begin or continue the workflow from the current state
- pause — stop execution until resumed
- resume — continue execution after a pause
- restart from <stage> — restart from a named stage
- end — stop the pipeline immediately
- start fresh — reset the workflow state without deleting existing artifacts
- regenerate <file> — regenerate a specific artifact or code file

These controls let you manage the lifecycle of the run manually when approvals, blocked items, or review checkpoints require human intervention.

## Approval and blocked-state workflow

When a stage reaches an approval gate:

- the supervisor announces the gate
- the user replies with approve or reject: <reason>
- approval advances the workflow
- rejection can trigger review and remediation

If a stage is blocked or missing outputs:

- the supervisor records the blocked state
- the user is asked for the missing information or decision
- the workflow resumes once the blocker is resolved

## Governance, guardrails, and auditability

The platform is designed with governance and auditability as first-class concerns. The workflow uses:

- governance files and contracts to define artifact ownership and lifecycle expectations
- guardrails to restrict unsafe or invalid execution behavior
- audit logs and quality reports to track decisions, artifacts, and validation outcomes
- structured openlog and handoff artifacts to preserve context across stages

This ensures that every stage remains traceable, reviewable, and aligned with the intended SDLC process.

## Repository structure

```text
.github/
ai/
apps/
  backend/
  frontend/
artifacts/
  architecture/
  backend/
  database/
  frontend/
  requirements/
  tests/
docs/
scripts/
specs/
tests/
```

## Debugging and troubleshooting

Useful files and locations include:

- artifacts/supervisor/execution-log.md
- artifacts/supervisor/approval-queue.md
- .orchestrator-state.json
- src/extension.ts
- src/workflow.ts
- src/promptBuilder.ts
- src/prompts.ts
- src/classifier.ts
- src/chatSupervisor.ts
- docs/ARTIFACTS.md

## Local application setup

### Backend

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn apps.backend.main:app --host 127.0.0.1 --port 8001
```

### Frontend

```powershell
cd apps/frontend
npm install
npm run dev
```

## Testing

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## Summary

This repository shows how a specification can be transformed into a working application through an automated, agent-driven SDLC workflow with hooks, approvals, artifact management, and end-to-end execution.
