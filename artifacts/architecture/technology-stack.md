# Technology Stack

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-06
- Status: Draft
- Architecture ID: ARCH-004
- Workflow ID: WF-20260705-001
- Correlation ID: WF-1783335798071
- Traceability: requirements_spec.md, non_functional_requirements.md, screen_specification.md

## Presentation Layer
- Frontend: React with TypeScript
- Build Tooling: Vite
- Styling: Tailwind CSS
- State and Routing: React Router and client-side state management aligned to screen workflows
- Rationale: Matches the supplied technology constraints and supports responsive, accessible screen flows.

## Business Layer
- Runtime: Python
- API Framework: FastAPI
- Validation: Pydantic-style request and response validation
- Authorization: Role-aware service layer with ownership checks
- Rationale: Supports clear service boundaries, strong validation, and deterministic API contracts.

## Data Layer
- Database: PostgreSQL
- ORM: SQLAlchemy
- Persistence Strategy: Repository-style access with unit-of-work semantics for business entities
- Rationale: Supports transactional integrity, audit-friendly persistence, and scalable relational data models.

## Quality and Testing
- Unit and Integration Tests: Pytest
- End-to-End UI Validation: Playwright
- Documentation: Markdown-based architecture and implementation references
- Rationale: Aligns with the BA-driven acceptance criteria and non-functional requirements.

## Operations and Delivery
- Version Control: Git
- Local Development: VS Code with GitHub Copilot Agent Mode
- Deployment Packaging: Container-ready deployment model for frontend, backend, and database services
- Rationale: Supports local-first delivery while keeping future deployment paths explicit.
