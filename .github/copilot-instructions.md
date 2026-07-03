# GitHub Copilot Instructions

## Project Philosophy

This project is a **local-first**, **AI-native**, **configuration-driven** Agentic SDLC platform.

The platform transforms a software specification (and optional Figma design) into a running application using autonomous AI agents coordinated by a Supervisor.

### Principles

- Configuration over code
- Markdown over hardcoded prompts
- Artifacts over conversations
- Autonomous execution
- Human approval through Supervisor only
- Local-first
- Single runtime
- Deterministic workflows

---

## Architecture

### Agent Pipeline

```text
Specification
    ↓
Supervisor
    ↓
    ## Agent Definitions

    Agent behavior must be defined in Markdown under `.github/agents`.
Business Analyst
    ↓
Solution Architect
    ↓
 ┌──────────────┬──────────────────┬─────────────────┐
 │              │                  │
 ▼              ▼                  ▼
UI/UX      Backend           Database
Developer  Developer         Developer
 └──────────────┴──────────────────┘
                ↓
          QA Engineer
                ↓
            Reviewer
                ↓
       DevOps & Release
                ↓
         Documentation
```

UI, Backend and Database agents may execute in parallel after the Solution Architect publishes contracts.

---

## Repository Structure

```text
ai/
    agents/
    prompts/
    skills/
    templates/
    hooks/
    guardrails/
    workflows/

orchestration/
    supervisor/
    workflow/
    execution/
    memory/
    event-bus/
    approval/
    tools/
    artifacts/
    audit/
    observability/

configs/
apps/
docs/
tests/
scripts/
```

Do not invent new top-level folders unless required.

---

## Agent Definitions

Agent behavior must be defined in Markdown under `.github/agents`.

Never hardcode prompts or responsibilities.

Every agent definition should contain:

- Metadata
- Role
- Mission
- Inputs
- Consumes
- Produces
- Execution Policy
- Responsibilities
- Skills
- Validation
- Self Review
- Guardrails
- Events
- Handoff
- Success Criteria

---

## Autonomous Execution Model

Every agent follows the same lifecycle:

```text
Plan
↓
Read Inputs
↓
Reason
↓
Execute Skills
↓
Generate Artifacts
↓
Validate
↓
Self Review
↓
Publish Artifacts
↓
Emit Event
↓
Next Agent
```

Agents must never ask users questions.

---

## Human Approval

Agents never communicate directly with humans.

When blocked:

- Generate `blocker-report.md`
- Generate `open-questions.md`
- Emit `<AgentName>Blocked`

Supervisor creates an approval request through the Approval Service.

The Approval Service presents the request in the local dashboard or CLI.

Supervisor resumes execution after approval.

---

## Artifact Driven Communication

Agents communicate only through:

- Published artifacts
- Shared workflow memory
- Structured events

Never rely on conversational context.

Persist every important output.

Each artifact has one owner.

Agents may read artifacts from other agents but must not overwrite them.

---

## Event Driven Workflow

Every agent emits lifecycle events.

Examples:

- BusinessRequirementsCompleted
- ArchitectureCompleted
- UIDevelopmentCompleted
- BackendCompleted
- DatabaseCompleted
- QACompleted
- ReviewCompleted
- ReleaseCompleted
- DocumentationCompleted

Blocked events:

- BusinessRequirementsBlocked
- ArchitectureBlocked
- BackendBlocked
- DatabaseBlocked

---

## Coding Standards

Prefer:

- Small modules
- SOLID principles
- Dependency Injection
- Composition
- Interfaces
- Immutable models
- Configuration over conditionals

Avoid:

- God objects
- Giant classes
- Global mutable state
- Hardcoded prompts
- Duplicated logic

---

## Validation Pipeline

Every AI output must pass:

```text
LLM Output
↓
Schema Validation
↓
Business Validation
↓
Guardrails
↓
Quality Review
↓
Published Artifact
```

Never bypass validation.

---

## Retry Policy

Retry only after validation failure.

Use:

- Previous output
- Validation feedback
- Retry count

Never retry indefinitely.

---

## Logging

Emit structured logs containing:

- workflow
- executionId
- agent
- status
- duration
- retries

---

## Security

Always:

- Validate AI outputs
- Sanitize inputs
- Protect secrets
- Verify generated artifacts

Never:

- Execute arbitrary AI output
- Trust model responses without validation

---

## Testing

Generate:

- Unit tests
- Integration tests
- Workflow tests

Prefer deterministic tests.

---

## Default Demo Application

Do not assume a default application type. Always derive scope, entry point, and features solely from specification.md. Never fall back to a generic demo app.

---

## Code Generation Rules

When generating code:

1. Load agent definitions from Markdown.
2. Keep orchestration separate from AI content.
3. Persist intermediate artifacts.
4. Use typed models.
5. Prefer configuration over hardcoded behavior.
6. Support plugin-style extensibility.
7. Design for local execution.
8. Use artifact contracts between agents.
9. Keep business logic out of prompts.
10. Produce production-quality code, tests and documentation.
