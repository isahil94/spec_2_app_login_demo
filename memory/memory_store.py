"""
Memory Store for workflow state persistence.

Persists workflow execution state to enable:
- Resumable workflows (if interrupted, resume from checkpoint)
- Agent-to-agent artifact passing
- Complete audit trail
- State recovery on failure
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


class MemoryStore:
    """Persistent memory for workflow state."""

    def __init__(self, storage_dir: Path):
        """
        Initialize memory store.

        Args:
            storage_dir: Directory to store memory files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.workflow_state_file = self.storage_dir / "workflow_state.json"
        self.agent_outputs_file = self.storage_dir / "agent_outputs.json"
        self.execution_log_file = self.storage_dir / "execution_log.jsonl"

        # Load existing state or initialize new
        self.workflow_state = self._load_workflow_state()
        self.agent_outputs = self._load_agent_outputs()

        logger.info(f"MemoryStore initialized at {self.storage_dir}")

    def _load_workflow_state(self) -> Dict[str, Any]:
        """Load workflow state from file."""
        if self.workflow_state_file.exists():
            try:
                with open(self.workflow_state_file, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    logger.info("Loaded existing workflow state")
                    return state
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load workflow state: {e}")

        # Initialize new workflow state
        return {
            "started_at": datetime.now().isoformat(),
            "completed_agents": [],
            "current_agent": None,
            "approval_gates": {},
            "status": "initialized",
        }

    def _load_agent_outputs(self) -> Dict[str, Dict[str, Any]]:
        """Load agent outputs from file."""
        if self.agent_outputs_file.exists():
            try:
                with open(self.agent_outputs_file, "r", encoding="utf-8") as f:
                    outputs = json.load(f)
                    logger.info("Loaded existing agent outputs")
                    return outputs
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load agent outputs: {e}")

        return {}

    def save_workflow_state(self) -> None:
        """Save workflow state to file."""
        try:
            with open(self.workflow_state_file, "w", encoding="utf-8") as f:
                json.dump(self.workflow_state, f, indent=2)
                logger.debug("Saved workflow state")
        except IOError as e:
            logger.error(f"Failed to save workflow state: {e}")

    def save_agent_outputs(self) -> None:
        """Save agent outputs to file."""
        try:
            with open(self.agent_outputs_file, "w", encoding="utf-8") as f:
                json.dump(self.agent_outputs, f, indent=2)
                logger.debug("Saved agent outputs")
        except IOError as e:
            logger.error(f"Failed to save agent outputs: {e}")

    def log_execution(self, message: str, level: str = "INFO", data: Optional[Dict] = None) -> None:
        """Log execution event to audit trail."""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": level,
                "message": message,
                "data": data or {},
            }
            with open(self.execution_log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except IOError as e:
            logger.error(f"Failed to log execution: {e}")

    # Workflow state management
    def mark_agent_completed(self, agent_name: str) -> None:
        """Mark agent as completed."""
        if agent_name not in self.workflow_state["completed_agents"]:
            self.workflow_state["completed_agents"].append(agent_name)
            self.workflow_state["current_agent"] = None
            self.save_workflow_state()
            self.log_execution(f"Marked agent as completed: {agent_name}", data={"agent": agent_name})

    def get_completed_agents(self) -> List[str]:
        """Get list of completed agents."""
        return self.workflow_state["completed_agents"].copy()

    def is_agent_completed(self, agent_name: str) -> bool:
        """Check if agent has completed."""
        return agent_name in self.workflow_state["completed_agents"]

    def set_current_agent(self, agent_name: str) -> None:
        """Set current agent being executed."""
        self.workflow_state["current_agent"] = agent_name
        self.save_workflow_state()

    def get_current_agent(self) -> Optional[str]:
        """Get current agent being executed."""
        return self.workflow_state.get("current_agent")

    def set_workflow_status(self, status: str) -> None:
        """Set workflow status."""
        self.workflow_state["status"] = status
        self.save_workflow_state()

    def get_workflow_status(self) -> str:
        """Get workflow status."""
        return self.workflow_state.get("status", "unknown")

    # Approval gate management
    def record_approval_gate(self, gate_name: str, approved: bool, decision_by: str = "user") -> None:
        """Record approval decision."""
        self.workflow_state["approval_gates"][gate_name] = {
            "approved": approved,
            "decided_at": datetime.now().isoformat(),
            "decided_by": decision_by,
        }
        self.save_workflow_state()
        self.log_execution(
            f"Approval gate decision: {gate_name}",
            data={"gate": gate_name, "approved": approved, "decided_by": decision_by},
        )

    def is_gate_approved(self, gate_name: str) -> Optional[bool]:
        """Check if approval gate was approved."""
        gate = self.workflow_state["approval_gates"].get(gate_name)
        return gate.get("approved") if gate else None

    # Agent output management
    def store_agent_output(
        self, agent_name: str, output_name: str, content: Any
    ) -> None:
        """Store agent output in memory."""
        if agent_name not in self.agent_outputs:
            self.agent_outputs[agent_name] = {}

        self.agent_outputs[agent_name][output_name] = {
            "content": content,
            "stored_at": datetime.now().isoformat(),
        }
        self.save_agent_outputs()
        self.log_execution(
            f"Stored agent output: {agent_name}/{output_name}",
            data={"agent": agent_name, "output": output_name},
        )

    def get_agent_output(self, agent_name: str, output_name: str) -> Optional[Any]:
        """Retrieve agent output from memory."""
        try:
            return (
                self.agent_outputs.get(agent_name, {})
                .get(output_name, {})
                .get("content")
            )
        except (KeyError, TypeError):
            return None

    def get_agent_all_outputs(self, agent_name: str) -> Dict[str, Any]:
        """Get all outputs from agent."""
        outputs = {}
        for output_name, output_data in self.agent_outputs.get(agent_name, {}).items():
            outputs[output_name] = output_data.get("content")
        return outputs

    def has_agent_output(self, agent_name: str, output_name: str) -> bool:
        """Check if agent output exists in memory."""
        return (
            agent_name in self.agent_outputs
            and output_name in self.agent_outputs[agent_name]
        )

    # State summary
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of current workflow state."""
        return {
            "status": self.get_workflow_status(),
            "started_at": self.workflow_state.get("started_at"),
            "completed_agents": self.get_completed_agents(),
            "current_agent": self.get_current_agent(),
            "approval_gates": self.workflow_state.get("approval_gates", {}),
            "agent_count": len(self.agent_outputs),
        }

    def reset_state(self) -> None:
        """Reset workflow state (for restarting workflow)."""
        logger.warning("Resetting workflow state")
        self.workflow_state = {
            "started_at": datetime.now().isoformat(),
            "completed_agents": [],
            "current_agent": None,
            "approval_gates": {},
            "status": "reset",
        }
        self.agent_outputs = {}
        self.save_workflow_state()
        self.save_agent_outputs()

    def cleanup(self) -> None:
        """Clean up old memory files (keep audit trail)."""
        logger.info("Cleaning up old memory files")
        # Keep execution_log_file, clean others
        for file in [self.workflow_state_file, self.agent_outputs_file]:
            if file.exists():
                try:
                    file.unlink()
                    logger.info(f"Cleaned up {file.name}")
                except OSError as e:
                    logger.error(f"Failed to clean up {file.name}: {e}")
