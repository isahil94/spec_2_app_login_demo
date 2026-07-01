"""
Supervisor - Lightweight workflow coordinator.

Responsibilities:
- Load 10-agent workflow DAG
- Coordinate via VS Code tasks
- Manage file-based artifacts
- Report workflow structure

NOTE: This is NOT an AI orchestrator. Copilot Agent Mode handles reasoning.
This coordinator invokes tasks and manages file artifacts.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


# 10-agent workflow DAG
WORKFLOW_DAG = [
    {
        "id": 1,
        "name": "business_analyst",
        "description": "Analyze requirements and create user stories",
        "requires": [],
        "approval_gate_after": False,
        "parallel": False,
    },
    {
        "id": 2,
        "name": "solution_architect",
        "description": "Design system architecture and API contracts",
        "requires": ["business_analyst"],
        "approval_gate_after": True,  # Architecture review gate
        "parallel": False,
    },
    {
        "id": 3,
        "name": "ui_ux_developer",
        "description": "Generate UI/UX components and design system",
        "requires": ["solution_architect"],
        "approval_gate_after": False,
        "parallel": True,
    },
    {
        "id": 4,
        "name": "backend_developer",
        "description": "Generate backend API and services",
        "requires": ["solution_architect"],
        "approval_gate_after": False,
        "parallel": True,
    },
    {
        "id": 5,
        "name": "database_developer",
        "description": "Design database schema and migrations",
        "requires": ["solution_architect"],
        "approval_gate_after": False,
        "parallel": True,
    },
    {
        "id": 6,
        "name": "qa_engineer",
        "description": "Generate and run tests",
        "requires": ["ui_ux_developer", "backend_developer", "database_developer"],
        "approval_gate_after": False,
        "parallel": False,
    },
    {
        "id": 7,
        "name": "reviewer",
        "description": "Review code quality and provide recommendations",
        "requires": ["qa_engineer"],
        "approval_gate_after": True,  # Final review gate
        "parallel": False,
    },
    {
        "id": 8,
        "name": "documentation",
        "description": "Generate complete documentation",
        "requires": ["reviewer"],
        "approval_gate_after": False,
        "parallel": False,
    },
    {
        "id": 9,
        "name": "devops",
        "description": "Build Docker image and prepare deployment",
        "requires": ["documentation"],
        "approval_gate_after": False,
        "parallel": False,
    },
]


class Supervisor:
    """Lightweight workflow coordinator for VS Code tasks."""

    def __init__(self, output_dir: Path):
        """
        Initialize supervisor.

        Args:
            output_dir: Output directory for artifacts
        """
        self.output_dir = Path(output_dir)
        self.project_root = Path(__file__).parent.parent.parent
        self.artifacts_dir = self.output_dir / "requirements"
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Supervisor initialized (artifacts: {self.artifacts_dir})")

    def get_workflow_dag(self) -> List[Dict]:
        """
        Get the 10-agent workflow DAG.
        
        Returns:
            List of agent configurations in execution order
        """
        return WORKFLOW_DAG.copy()

    def validate_workflow(self, spec_file: Path) -> bool:
        """
        Validate that workflow can be executed.

        Args:
            spec_file: Path to specification file

        Returns:
            True if workflow prerequisites are met
        """
        if not spec_file.exists():
            logger.error(f"Specification file not found: {spec_file}")
            return False

        if not spec_file.is_file():
            logger.error(f"Not a file: {spec_file}")
            return False

        try:
            with open(spec_file, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    logger.error("Specification file is empty")
                    return False
        except IOError as e:
            logger.error(f"Cannot read specification: {e}")
            return False

        logger.info("✓ Workflow validation passed")
        return True

    def get_agent_config(self, agent_name: str) -> Optional[Dict]:
        """
        Get configuration for agent.
        
        Args:
            agent_name: Agent name
            
        Returns:
            Agent configuration or None
        """
        for config in WORKFLOW_DAG:
            if config["name"] == agent_name:
                return config
        return None

    def get_next_agents(self, agent_name: str) -> List[str]:
        """
        Get next agents after given agent.
        
        Args:
            agent_name: Current agent name
            
        Returns:
            List of next agent names
        """
        next_agents = []
        for config in WORKFLOW_DAG:
            if agent_name in config.get("requires", []):
                next_agents.append(config["name"])
        return next_agents

    def save_workflow_info(self, spec_file: Path) -> None:
        """
        Save workflow information for reference.
        
        Args:
            spec_file: Path to specification file
        """
        workflow_info = {
            "specification": str(spec_file),
            "workflow_dag": WORKFLOW_DAG,
            "approval_gates": [
                "after_solution_architect",
                "after_reviewer"
            ],
            "artifacts_dir": str(self.artifacts_dir),
        }
        
        info_file = self.artifacts_dir / "workflow_info.json"
        try:
            with open(info_file, "w", encoding="utf-8") as f:
                json.dump(workflow_info, f, indent=2)
            logger.info(f"Saved workflow info to {info_file}")
        except IOError as e:
            logger.error(f"Failed to save workflow info: {e}")

    def display_workflow(self) -> None:
        """Display workflow structure."""
        print("\n" + "=" * 60)
        print("WORKFLOW: 10-AGENT SDLC PIPELINE")
        print("=" * 60)
        print()
        
        for i, agent in enumerate(WORKFLOW_DAG, 1):
            gate_after = " [APPROVAL GATE]" if agent.get("approval_gate_after") else ""
            parallel = " (parallel)" if agent.get("parallel") else ""
            print(f"{i}. {agent['name'].upper()}{parallel}{gate_after}")
            print(f"   {agent['description']}")
            print()
        
        print("=" * 60)
        print("Orchestration: VS Code Chat Modes + Tasks")
        print("AI Reasoning: GitHub Copilot Agent Mode")
        print("Artifacts: Git + artifacts/ directory")
        print("=" * 60 + "\n")
