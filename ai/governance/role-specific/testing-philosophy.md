# Testing Philosophy (Role-Specific Governance)

Document Version: 1.0.0  
Effective Date: 2026-06-30  
Status: Approved  
Authority: Platform AI Governance Council

**Scope:** Applies to all agents and outputs that include testing, validation, or quality verification responsibilities. Required for QA Engineer, Backend Developer, and Frontend Developer agents.

---

## 20. Testing Philosophy
Testing discipline is foundational to output trust.

1. Encourage testability by design.
2. Encourage validation and verification at each stage.
3. Encourage outputs that are independently reviewable.
4. Encourage quality-first decision behavior.
5. Encourage detection of regressions and integration breakage.

Testing expectations per output:

1. Unit-level testability for modular components.
2. Integration-level testability for interfaces and dependencies.
3. End-to-end testability for workflow outcomes.
4. Negative-path testability for failure behavior.

---

**Agent Scope:** Load this file only if your agent definition explicitly references testing responsibilities. For QA Engineer, Backend Developer, and Frontend Developer agents, this is mandatory.

**Non-Applicability:** Business Analyst, Solution Architect, and Database Developer agents may reference this for context but are not required to implement testing-specific outputs.
