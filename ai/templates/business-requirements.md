# Business Requirements Template

## Purpose
Define the master business specification in a traceable, implementation-ready format.

## Downstream Readiness Expectations
- Produce business artifacts that are detailed enough for UI/UX, Backend, and Database agents to implement without inferencing missing behavior.
- Capture user journeys, validation rules, state transitions, permissions, notifications, audit expectations, and data constraints explicitly.
- Include Mermaid flow diagrams in business_process_flows.md for non-trivial workflows and lifecycle paths.
- Include concise supporting diagrams or visual structure in requirements_spec.md or ui_observations.md where they improve downstream clarity.
- Ensure the generated artifacts are directly consumable by downstream stages without needing extra interpretation.

## Metadata
- Version: [Version]
- Author: [Author]
- Date: [Date]
- Status: [Draft | In Review | Approved | Deprecated]
- Workflow ID: [Workflow ID]
- Artifact ID: [Artifact ID]
- Related Artifacts: [Links or IDs]
- Traceability: [Source Requirement IDs]

## Document Control
- Document ID: [REQ-SPEC-001]
- Owner: [Business Analyst]
- Version History: [Version | Date | Author | Change Summary]
- Approvers: [Name | Role | Status]

## Executive Summary
[Summary of business intent and expected value]

## Business Goals
- [Goal ID | Goal Statement | Success Metric]

## Scope
---

### In Scope
- [In-scope item]

### Out of Scope
- [Out-of-scope item]

## Stakeholders
- [Stakeholder | Role | Interest]

## Business Context
- [Current-state summary]
- [Problem statement]
- [Target outcome]

## Epics
- [Epic ID | Name | Business Goal | Business Value | Scope | Features Included]

## Features
- [Feature ID | Name | Business Purpose | Primary User Journey | Related Screens | Business Rules | Required Permissions | Validation Summary | Success Outcome | Failure Outcome | Dependencies | Priority | Related Functional Requirements]

## Decomposition Coverage
- [Epic ID | Feature IDs | Coverage Status: Complete/Partial/Missing]
- [Feature ID | User Story IDs | Coverage Status: Complete/Partial/Missing]

## Functional Requirements
- [Requirement ID | Description | Inputs | Outputs | Preconditions | Postconditions | Business Rules | Validation Rules | Dependencies | Error Conditions | Required Permissions | Related Screens | Security Expectations | Audit Expectations | Priority | MoSCoW]

## Feature-Level Business Detail Coverage
- Feature ID: [FEAT-001]
- Applicable business rules: [BR IDs or N/A]
- Validation rules: [VAL IDs or N/A]
- Permissions and visibility: [PERM IDs or N/A]
- Navigation, workflow, and state transitions: [FLOW IDs or N/A]
- Scenario coverage: [Success | Failure | Empty | Loading | Exception]
- Search/filter/sort/pagination behavior: [N/A or details]
- Data constraints and defaults: [Required vs optional | allowed values | defaults | uniqueness | relationships]
- Lifecycle/status transitions: [Status model or N/A]
- Notifications and audit requirements: [N/A or details]
- Non-functional constraints: [NFR refs or N/A]

## UI Requirements and Constraints
- [UI Requirement ID | Screen/Flow | Required Behavior | Approved Design Reference]
- Constraints: [No redesign | Responsive behavior | Accessibility expectation]

## Business Rules
- [Rule ID | Statement | Applies To | Rationale]

## Input Validation Rules
- [Validation ID | Input/Field | Rule | Error Outcome | Related Requirement ID]

## Authentication and Authorization Behavior
- [Auth Rule ID | Actor | Precondition | Allowed Action | Restricted Action | Business Outcome]

## Permissions and Visibility Rules
- [Rule ID | Role/Actor | Visible To | Hidden From | Condition | Business Outcome]

## Navigation, Workflow, and State Transitions
- [Flow ID | Start State | Trigger | End State | Constraints | Exception Handling]

## Scenario Coverage
- [Requirement/Feature ID | Success | Failure | Empty | Loading | Exception | Coverage Status]

## Business Capability Requirements
- [Capability Area | The system shall allow/provide | Business Outcome]

## Stable Assumptions
- [Constraint]
- [Assumption]

## Conceptual Business Data Model
- [Entity | Business meaning | Relationship summary]

## Prioritization
- Must Have: [Items]
- Should Have: [Items]
- Could Have: [Items]
- Won't Have (Current Release): [Items]

## Risks and Dependencies
- [Risk or Dependency | Impact | Mitigation]

## Glossary
- [Term | Definition]

## Out of Scope
- [Item]

## Success Metrics
- [Metric | Target]

## OpenLog References
- Record open questions, assumptions, risks, decisions, and escalations in `openlog.md`.
- Do not create separate governance artifacts.

## Approval
- Prepared By: [Name]
- Reviewed By: [Name]
- Approved By: [Name]

## Boundary Rules
- Do not include endpoints, HTTP methods, or payload definitions.
- Do not include authentication implementation choices.
- Do not include technology, architecture, or deployment decisions.
- Do not include physical database schema details.
- Ensure each functional requirement is traceable to user stories and acceptance criteria.
