# Architecture and Coding Governance (Role-Specific)

Document Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved  
Authority: Platform AI Governance Council

**Scope:** Applies to agents responsible for architecture, design, or code generation. Required for Solution Architect, Backend Developer, Frontend Developer, and Database Developer agents.

---

## 1. Architecture Principles
All agents must align outputs with enterprise architecture fundamentals.

1. Separation of Concerns
Keep business, orchestration, validation, and operational concerns distinct.

2. SOLID
Preserve single-responsibility behavior and extensible contracts.

3. Clean Architecture
Keep boundaries explicit and dependencies directional.

4. High Cohesion
Group related responsibilities together.

5. Loose Coupling
Minimize unnecessary cross-component dependencies.

6. Interface-driven design
Favor explicit contracts for interactions.

7. Configuration over hardcoding
Represent behavior through configurable policy where possible.

8. Modularity
Design outputs in composable units.

9. Scalability
Support increasing scope without structural collapse.

10. Production readiness
Ensure operability, observability, and resilience are considered.

## 2. Coding Standards
When producing code-oriented outputs, agents must ensure:

1. Readable structure and naming.
2. Maintainable modular design.
3. Reusable components and interfaces.
4. Secure behavior and defaults.
5. Performance-aware decisions.
6. Consistent conventions.
7. Structured error handling.
8. Minimal accidental complexity.
9. Testability by design.
10. Operational diagnosability.

Code quality constraints:

1. Avoid unnecessary deep nesting.
2. Avoid duplication where reusable abstractions are justified.
3. Avoid hidden side effects.
4. Avoid brittle cross-layer dependencies.
5. Avoid incomplete error pathways.

---

**Agent Scope:** Load this file if your agent definition includes architecture or code generation responsibilities:
- Solution Architect: **Required** (section 7)
- Backend Developer: **Required** (sections 7, 8)
- Frontend Developer: **Required** (sections 7, 8)
- Database Developer: **Required** (section 7)

**Non-Applicability:** Business Analyst and QA Engineer agents may reference for context but are not required to implement these standards in their own outputs.
