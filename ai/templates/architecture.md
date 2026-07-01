# Architecture Template

## Purpose
Describe system structure, component boundaries, interfaces, and architectural decisions.

## Metadata
- Version: [Version]
- Author: [Author]
- Date: [Date]
- Status: [Draft | In Review | Approved]
- Architecture ID: [Architecture ID]
- Workflow ID: [Workflow ID]
- Traceability: [Requirements, ADRs, Contracts]

## Executive Summary
[Architecture overview and intent]

## Architectural Overview
- [System decomposition summary]

## Architectural Goals
- [Goal]

## Constraints
- [Constraint]

## System Context
[High-level context and external dependencies]

## Component Decomposition
- [Component | Responsibility | Dependencies]

## Design Decisions
- [Decision ID | Decision | Rationale | Tradeoff | Impacted Components]

## Epic/Feature/Story Coverage
- [Epic ID | Feature IDs | User Story IDs | Architecture Modules | Coverage Status]

## Layer Responsibilities
- [Layer: Presentation | Business | Data | Responsibilities | Owned Modules]

## Folder Structure Boundaries
- [Area: Presentation | Business | Data | Shared | Configuration | Tests | Assets | Documentation | Ownership Boundary]

## Interface Boundaries
- [Interface | Producer | Consumer | Contract]

## Interaction Model
- [Interaction ID | Source Layer/Component | Target Layer/Component | Sync/Async | Purpose]

## Data and State Considerations
- [Data flow or state concern]

## Navigation, Workflow, and State Transitions
- [Flow ID | Start State | Trigger | End State | Constraints | Error/Exception Path]

## Responsibility Allocation
- [Component | Service Responsibility | Repository Responsibility | Database Responsibility]

## Module Responsibilities
- [Module | Responsibility | Public Interfaces | Dependencies | Inputs | Outputs | Error Conditions | Security Responsibilities | Logging Responsibilities | Configuration Requirements]

## Database Design Considerations
- [Business Entity | Relationships | Cardinality | Constraints | Keys | Data Ownership | Audit Fields | Soft Delete Strategy | Versioning Strategy | Performance Considerations | Security Considerations]

## Contract Coverage
- API Contracts: [Contract IDs]
- Data Contracts: [Contract IDs]
- Integration Contracts: [Contract IDs]

## Integration Points
- [Integration ID | Consumer | Provider | Contract | Failure Handling]

## Architecture Constraints
- [Constraint ID | Category: Security/Validation/Authorization/Error Handling | Rule]

## Security Design
- [Area: Authentication | Authorization | Secrets Management | Data Protection | Input Validation | Output Encoding | Secure Communication | Audit Logging | Threat Considerations | Architecture Rule]

## Error Handling Strategy
- [Scope | Error Category | Handling Strategy | Escalation Rule]

## Logging Strategy
- [Scope | Required Log Events | Correlation Requirements]

## Audit Strategy
- [Scope | Auditable Events | Retention/Traceability Expectations]

## Observability Strategy
- [Metric/Signal | Purpose | Alert/Review Expectation]

## Performance Strategy
- [Concern | Target/Constraint | Strategy]

## Scalability Strategy
- [Concern | Growth Pattern | Strategy]

## Availability Strategy
- [Concern | Availability Objective | Strategy]

## Deployment Considerations
- [Environment Concern | Constraint | Architecture Consideration]

## Scalability, Security, and Performance Notes
- [Concern | Strategy]

## Cross-Cutting Concerns
- [Concern: Logging/Configuration/Observability/Auditing/Performance | Architectural Approach]

## Risks and Tradeoffs
- [Decision | Tradeoff | Rationale]

## Traceability Mapping
- [Business Requirement | Architecture Component | Module | API | Database Entity | UI Screen | Test Case | Status: Covered/Partial/Missing]

## Missing Traceability
- [List each missing mapping and impacted downstream stage]

## Open Questions
Record unresolved architecture questions in `openlog.md` using the openlog schema.

## Approval
- Prepared By: [Name]
- Reviewed By: [Name]
- Approved By: [Name]
