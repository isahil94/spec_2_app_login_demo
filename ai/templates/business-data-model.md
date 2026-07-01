# Business Data Model Template

## Purpose

Define conceptual business entities and relationships only.

## Metadata

- Version: [Version]
- Author: [Author]
- Date: [Date]
- Status: [Draft | In Review | Approved]
- Workflow ID: [Workflow ID]
- Traceability: [Requirement IDs]

## Conceptual Entities

- [Entity Name]: [Business meaning]
- [Entity Name]: [Business meaning]

## Entity Relationships

- [Entity A] relates to [Entity B] because [business reason]
- [Entity C] relates to [Entity D] because [business reason]

## Key Business Attributes (Conceptual)

- [Entity]: [Business attributes described in plain language]

## Ownership and Stewardship

- [Entity]: [Business owner]

## Data Lifecycle (Business View)

- Creation context:
- Update context:
- Retention expectation:

## Privacy and Compliance Considerations

- [Consideration]

## Open Questions

Use the structured format from `ai/templates/open-questions.md`.

- Include one or more `OQ-xxx` entries.
- Include Open Question Summary: Total Questions, Blocking Questions, Approval Requests Required, Workflow Status, Next Agent.

## Boundary Rules

- Do not define tables, columns, primary keys, foreign keys, indexes, or migrations.
- Do not include SQL, ORM mappings, or schema syntax.
- Do not include physical database design decisions.
