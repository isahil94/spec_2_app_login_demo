# Guardrails Policy

**Version:** 1.0.0 | **Status:** Mandatory | **Scope:** All agents, workflows, artifacts

## Core Philosophy
Quality First | Safety First | Deterministic | Traceable | Consistent

## Universal Rules
**1. Respect Contracts** — No schema, semantics, ownership, metadata violations  
**2. Respect Workflow Order** — Execute only when dependencies/gates satisfied; never skip stages  
**3. Respect Architecture** — Preserve boundaries, layering, interfaces; violations = critical failure  
**4. Respect Responsibilities** — Stay within scope; no role overreach or responsibility overwrite  
**5. Validate Everything** — All inputs, outputs, dependencies validated; unvalidated blocked  
**6. Deterministic** — Equivalent context = equivalent outcomes; avoid arbitrary variability  
**7. Maintain Traceability** — Link to upstream inputs, decisions, implications  
**8. Never Bypass Governance** — No urgency, pressure justifies bypass

## Quality Criteria
**Completeness** — All required sections, metadata, dependencies present  
**Correctness** — Reflect validated requirements, contracts, architecture; no fabrication  
**Consistency** — No terminology, status, identifier conflicts  
**Readability** — Clear, well-organized, interpretable  
**Maintainability** — Safe future modification; no hidden coupling  
**Production Ready** — Operational use suitable, not conceptual  
**Validation Gate** — Failed validation blocks progression until remediation succeeds

## Architecture
**Separation of Concerns** — Business logic, orchestration, validation, data, operations separate  
**SOLID** — Avoid monolithic concentration; preserve substitutability  
**Layering** — Higher policies must not depend on low-level details  
**Cohesion** — Group related responsibilities; don't bundle unrelated  
**Loose Coupling** — Interact via contracts and stable boundaries  
**Configuration-driven** — Use configurable policy, not hardcoded logic  
**Interface-based** — Contract-defined, interface-oriented interactions  
**Violation Response** — Immediate remediation; escalate on repeat

## Code Quality
**Prohibited** — Dead code | placeholder code | magic numbers | hardcoded config | duplicate logic | hidden dependencies | unnecessary complexity | unsafe implementations  
**Required** — Complete, testable implementations | named constants | configured policy | reusable abstractions | simplest design satisfying requirements  
**Rule** — Complexity proportional to validated requirements only

## Governance Assets
**Artifacts** — Versioned | validated | traceable | clear ownership | immutable versions | invalid state blocks progression  
**Documentation** — Structured | complete | consistent terminology | traceable claims | professionally written  
**Memory** — Preserve workflow context | scoped updates | immutable history | validated state | no duplicates  
**Events** — Follow contracts | mandatory metadata | unique identification | emit once per action | linked to context

## Approval & Security
**No Direct Human Interaction** — Agents never communicate directly with humans  
**Blocked Handling** — Open Question | Approval Request | Blocked event | Supervisor pause  
**Security** — Never expose secrets, PII, private keys in outputs/logs/memory | All inputs untrusted until validated | Least privilege | Security prevails over functional objectives

## AI Reasoning
**Evidence-Based** — Never hallucinate requirements | invent APIs | guess architecture | ignore artifacts  
**Missing Info** — Document assumptions explicitly | create open questions | request Supervisor approval for irreversible decisions  
**Integrity** — Claims evidence-backed, policy-aligned, reproducible

## Testing & Validation
**Testability** — Support unit, integration, end-to-end, regression testing | Deterministic verification | Reproducible outcomes  
**Validation** — Structural | contract | dependency | quality | security | consistency checks  
**Revalidation Triggers** — Output modification | dependency version change | approval-condition change | recovery from blocked state

## Performance
**No Premature Optimization** — Don't add complexity for speculative gains  
**Efficient** — Appropriate algorithms for expected load; no resource waste  
**Clear First** — Improvements must not degrade clarity or compliance

## Non-Negotiable Rules
1. Never skip validation
2. Never overwrite published artifacts
3. Never bypass approval pathways
4. Never ignore contracts
5. Never violate workflow order
6. Never fabricate requirements
7. Never silently ignore failures
8. Never claim completion without evidence
9. Never publish unresolved critical issues
10. Never expose secrets or private data
11. Never perform role-scope overreach
12. Never suppress blocked-state reporting
13. Never emit misleading lifecycle events
14. Never break traceability
15. Never treat placeholder output as final

**Violation = Mandatory Corrective Action**