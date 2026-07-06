# Business Process Flows Template

## Purpose
Document business workflows in a technology-agnostic manner for the Business Analyst stage.

## Metadata
- Version: [Version]
- Author: [Author]
- Date: [Date]
- Workflow ID: [Workflow ID]
- Status: [Draft | In Review | Approved]

## Business Process Flows

### Process Name: [Process Name]
- Objective: [Business objective of the process]
- Trigger: [What starts the process]
- Preconditions: [Conditions that must already be true]
- Main Flow:
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
- Alternate Flow:
  1. [Alternate step 1]
  2. [Alternate step 2]
- Exception Flow:
  1. [Exception step 1]
  2. [Exception step 2]
- Postconditions: [Conditions after completion]
- Related User Stories: [Story IDs]
- Related Screens: [Screen Names]
- Related Business Rules: [Rule IDs or descriptions]
- Related Acceptance Criteria: [AC IDs]

## Summary Diagram
```mermaid
flowchart TD
    A([Trigger]) --> B[Main flow]
    B --> C[Alternate flow]
    B --> D[Exception handling]
    D --> E[Postconditions]
```

## Notes
- Keep the content business-oriented and implementation-neutral.
- Do not include APIs, database, services, sequence diagrams, or infrastructure.
