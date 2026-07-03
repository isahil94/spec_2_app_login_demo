---
name: Supervisor
description: Orchestrate and coordinate the full SDLC workflow
category: workflow
icon: supervisor
order: 0
---

# Supervisor Chat Mode

**Entry Point:** See [ai/agents/00-supervisor.agent.md](../../ai/agents/00-supervisor.agent.md) for full role definition, workflow orchestration logic, approval gates, deterministic routing, artifact consumption, and completion criteria.

---

## Purpose

The Supervisor coordinates the complete 10-agent SDLC workflow, ensuring artifacts flow correctly between agents and managing approval gates.

## Reference

All orchestration details are in the agent definition file linked above. This chat mode exists as a manual entry point only—when you open this mode in the editor, it routes you to the authoritative agent specification.