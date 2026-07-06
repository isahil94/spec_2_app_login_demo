# Architecture Decision Records

## Purpose
Capture major architecture decisions, rationale, alternatives, and consequences for traceability and implementation alignment.

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-04
- Status: Draft
- Workflow ID: WF-20260704-001

---

## ADR-001: Three-Tier Architecture
### Context
The Task Management System must support clear separation of concerns, scalability, and testability across frontend, backend, and database responsibilities.

### Decision
Adopt a three-tier architecture with Presentation, Business, and Data layers.

### Alternatives Considered
- Monolithic service: simpler but harder to test and scale.
- Microservices: excessive complexity for MVP.

### Consequences
- Positive: clear boundaries, easier maintenance, parallel development.
- Negative: requires discipline around API contracts and integration testing.

### References
- architecture-design.md
- module-design.md
- api-specifications.md

---

## ADR-002: REST API Contract with Versioning
### Context
Multiple clients may consume the API and the requirement set may evolve.

### Decision
Implement RESTful HTTP APIs with explicit versioning (v1) and resource-based routes.

### Alternatives Considered
- GraphQL: flexible but adds complexity and learning curve.
- RPC-style endpoints: less expressive for resource-oriented workflows.

### Consequences
- Positive: straightforward frontend integration, predictable contract evolution.
- Negative: may require additional endpoints for complex aggregated queries.

### References
- api-specifications.md
- user-flow-specification.md

---

## ADR-003: JWT Token-Based Authentication
### Context
The frontend is a SPA and the system must authenticate users without maintaining server-side session state.

### Decision
Use JWT bearer tokens with 24-hour expiry for authentication.

### Alternatives Considered
- Stateful server sessions: more secure but requires session store.
- OAuth/OIDC: overkill for MVP.

### Consequences
- Positive: stateless scaling, simple token-based access.
- Negative: token revocation complexity; refresh tokens may be needed later.

### References
- security-architecture.md
- api-specifications.md

---

## ADR-004: Role-Based Access Control (RBAC)
### Context
Users have distinct permissions based on Admin, Team Lead, and Team Member roles.

### Decision
Enforce RBAC in service layer and API authorization middleware.

### Alternatives Considered
- Attribute-based access control: too granular for Phase 1.
- Client-side only role checks: insecure.

### Consequences
- Positive: secure authorization, consistent behavior across clients.
- Negative: requires careful mapping of permissions to actions.

### References
- security-architecture.md
- module-design.md

---

## ADR-005: Repository Pattern for Data Access
### Context
Query complexity, testability, and database portability must be managed cleanly.

### Decision
Use repository classes/interfaces for all data access from service layer.

### Alternatives Considered
- Direct ORM access in services: faster but less testable.
- Raw SQL in services: error-prone and harder to evolve.

### Consequences
- Positive: abstraction layer, easier mocking, clearer isolation.
- Negative: additional boilerplate and interface maintenance.

### References
- lld.md
- database-strategy.md

---

## ADR-006: Soft Delete with Admin Hard Delete
### Context
Task lifecycle requires archive support while preserving audit history and allowing restoration.

### Decision
Implement soft-delete semantics for tasks and accounts; allow permanent delete only for Admins with retention policies.

### Alternatives Considered
- Hard delete only: loses history and violates audit requirements.
- Soft delete without admin purge: accumulates stale data indefinitely.

### Consequences
- Positive: audit preservation, restore capability.
- Negative: query filters must consistently exclude archived records.

### References
- database-strategy.md
- security-architecture.md

---

## ADR-007: Immutable Audit Log
### Context
Regulatory and traceability requirements demand a permanent history of state changes.

### Decision
Use an append-only audit log table with no update/delete operations.

### Alternatives Considered
- Event sourcing: heavier implementation complexity.
- Audit fields on entities only: insufficient for full event history.

### Consequences
- Positive: strong change history, compliance-friendly.
- Negative: additional storage and query complexity for audit views.

### References
- security-architecture.md
- database-strategy.md

---

## ADR-008: Blue-Green Deployment Strategy
### Context
Production deployments must minimize downtime and support quick rollback.

### Decision
Adopt a blue-green deployment model for production releases.

### Alternatives Considered
- Rolling deployments: lower isolation during rollout.
- Canary without blue-green: less safe rollback path.

### Consequences
- Positive: zero-downtime releases, fast rollback path.
- Negative: higher infrastructure cost during deployment window.

### References
- deployment-architecture.md

---

## ADR-009: PostgreSQL in Production, SQLite for Local Development
### Context
Developers need low setup friction while production requires a robust relational database.

### Decision
Use SQLite for local development and PostgreSQL for test/staging/production, with CI validating PostgreSQL compatibility.

### Alternatives Considered
- PostgreSQL only: higher local setup burden.
- SQLite only: production risk due to feature differences.

### Consequences
- Positive: developer convenience with production-grade database in CI.
- Negative: potential compatibility gaps if not validated consistently.

### References
- technology-stack.md
- deployment-architecture.md

---

## ADR-010: In-App Notifications for MVP
### Context
The notifications requirement exists, but email delivery is not mandatory for initial release.

### Decision
Implement in-app notifications for MVP and defer email delivery to Phase 2.

### Alternatives Considered
- Build email delivery now: increases scope and infrastructure requirements.
- No notifications: violates user collaboration expectations.

### Consequences
- Positive: delivers core notification capability quickly.
- Negative: email channel not available in MVP.

### References
- openlog.md
- api-specifications.md

---

## ADR-011: Transactional Bulk Operations
### Context
Bulk task updates must preserve data integrity and audit consistency.

### Decision
Implement bulk task operations as all-or-nothing transactions.

### Alternatives Considered
- Partial success: easier to execute but harder to audit.
- Queue-based batch processing: higher complexity.

### Consequences
- Positive: consistent audit trail and reliable business state.
- Negative: may fail larger bulk requests due to single invalid task.

### References
- api-specifications.md
- lld.md

---

## ADR-012: Dependency-Unavailable Response Handling
### Context
External dependencies such as database or cache may become temporarily unavailable.

### Decision
Return explicit 503 responses for dependency failures and render graceful UI fallback states.

### Alternatives Considered
- Retry blindly: delays failure detection.
- Silent errors: poor user experience.

### Consequences
- Positive: clear failure modes and better user feedback.
- Negative: additional error handling paths required.

### References
- security-architecture.md
- user-flow-specification.md

---

## ADR-013: Access Control in Service Layer
### Context
Authorization must be enforced consistently regardless of frontend behavior.

### Decision
Perform authorization checks in backend service methods, not solely in route middleware or frontend.

### Alternatives Considered
- Middleware-only authorization: easier but risk bypass in service calls.
- UI-only authorization: insecure.

### Consequences
- Positive: stronger security and consistent enforcement.
- Negative: more checks in service implementation.

### References
- security-architecture.md
- module-design.md

---

## ADR-014: Role-Based Reporting Access
### Context
Dashboard and reports must show different data based on user roles.

### Decision
Scope reporting results by role: Admin sees full data, Team Lead sees team-level, Member sees own tasks.

### Alternatives Considered
- Single view for all roles: not compliant with access requirements.
- Attribute-based filtering: excessive for MVP.

### Consequences
- Positive: appropriate data exposure and role separation.
- Negative: additional data scoping logic in reporting service.

### References
- security-architecture.md
- user-flow-specification.md

---

## ADR-015: Soft Attachment Storage for MVP
### Context
Attachments are part of collaboration, but file storage strategy is not clearly defined in requirements.

### Decision
Store attachment metadata in the database and defer actual file storage implementation to Phase 2.

### Alternatives Considered
- Implement S3/GCS now: adds infrastructure scope.
- Store files in database BLOBs now: not optimal for scalability.

### Consequences
- Positive: keeps MVP scope manageable.
- Negative: attachment uploading not fully available at launch.

### References
- openlog.md
- database-strategy.md
