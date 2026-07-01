"""
Workflow Execution Engine

Executes workflow stages from Markdown-based agent definitions.

Does NOT perform AI reasoning - only coordinates execution through:
- Agent definitions in ai/agents/*.md
- Chat modes (AI reasoning via Copilot)
- Shared contracts/templates/skills referenced by agent definitions
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


class StageConfig:
    """Configuration for a workflow stage"""

    def __init__(
        self,
        stage_name: str,
        agent_file: str,
        chat_mode: str,
        description: str,
        input_artifacts: List[str],
        output_artifacts: List[str],
        output_targets: Optional[List[str]] = None,
        requires_approval: bool = False,
        timeout_seconds: int = 3600,
    ):
        self.stage_name = stage_name
        self.agent_file = agent_file
        self.chat_mode = chat_mode
        self.description = description
        self.input_artifacts = input_artifacts
        self.output_artifacts = output_artifacts
        self.output_targets = output_targets or []
        self.requires_approval = requires_approval
        self.timeout_seconds = timeout_seconds


STAGE_AGENT_FILES = {
    "business-analyst": "01-business-analyst.md",
    "solution-architect": "02-solution-architect.md",
    "ui-ux-developer": "03-ui-ux-developer.md",
    "backend-developer": "04-backend-developer.md",
    "database-developer": "05-database-developer.md",
    "qa-engineer": "06-qa-engineer.md",
    "reviewer": "07-reviewer.md",
    "documentation": "08-documentation.md",
    "devops": "09-devops.md",
}

STAGE_CHATMODE_OVERRIDES = {
    "devops": "devops-release",
}

APPROVAL_REQUIRED_STAGES = {
    "solution-architect",
    "reviewer",
}


class ExecutionResult:
    """Result of stage execution"""

    def __init__(
        self,
        stage_name: str,
        success: bool,
        output: str,
        error: Optional[str] = None,
        artifacts: Optional[List[str]] = None,
        duration_seconds: Optional[float] = None,
    ):
        self.stage_name = stage_name
        self.success = success
        self.output = output
        self.error = error
        self.artifacts = artifacts or []
        self.duration_seconds = duration_seconds
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "stage": self.stage_name,
            "success": self.success,
            "output_length": len(self.output),
            "error": self.error,
            "artifacts": self.artifacts,
            "duration_seconds": self.duration_seconds,
            "timestamp": self.timestamp.isoformat(),
        }


class ExecutionEngine:
    """Executes workflow stages"""

    def __init__(self, project_root: Path = None):
        """Initialize execution engine"""
        self.project_root = project_root or Path.cwd()
        self.vscode_dir = self.project_root / ".vscode"
        self.chat_mode_dir = self.project_root / ".github" / "chatmodes"
        self.agents_dir = self.project_root / "ai" / "agents"
        self._stage_configs = self._load_stage_configs()

    def execute_stage(
        self,
        stage_name: str,
        input_artifacts: Dict[str, str],
        specification: str,
    ) -> ExecutionResult:
        """
        Execute a workflow stage

        Args:
            stage_name: Name of the stage (e.g., 'business-analyst')
            input_artifacts: Dictionary of artifact name -> content
            specification: Project specification

        Returns:
            ExecutionResult with output and artifacts
        """
        start_time = datetime.now()

        try:
            config = self._stage_configs.get(stage_name)
            if not config:
                return ExecutionResult(
                    stage_name=stage_name,
                    success=False,
                    output="",
                    error=f"Unknown stage: {stage_name}",
                )

            # Hard rule: required inputs must exist before stage execution.
            available_inputs = self._build_available_inputs_map(stage_name, input_artifacts)
            is_valid, missing = self.validate_stage_inputs(stage_name, available_inputs)
            if not is_valid:
                missing_str = ", ".join(sorted(missing))
                return ExecutionResult(
                    stage_name=stage_name,
                    success=False,
                    output="",
                    error=(
                        f"Missing required input artifacts for stage '{stage_name}': {missing_str}. "
                        "Stage execution stopped by fail-fast input policy."
                    ),
                )

            # Build prompt for chat mode
            prompt = self._build_stage_prompt(
                stage_name=stage_name,
                config=config,
                input_artifacts=input_artifacts,
                specification=specification,
            )

            # Invoke chat mode through VS Code
            output = self._invoke_chat_mode(stage_name, config.chat_mode, prompt, config.agent_file)

            # Extract artifacts from output
            artifacts = self._extract_artifacts(output, stage_name, config)

            if not artifacts:
                return ExecutionResult(
                    stage_name=stage_name,
                    success=False,
                    output=output,
                    error=(
                        f"No output artifacts materialized for stage '{stage_name}'. "
                        f"Expected: {', '.join(config.output_targets)}"
                    ),
                )

            duration_seconds = (datetime.now() - start_time).total_seconds()

            return ExecutionResult(
                stage_name=stage_name,
                success=True,
                output=output,
                artifacts=artifacts,
                duration_seconds=duration_seconds,
            )

        except Exception as e:
            duration_seconds = (datetime.now() - start_time).total_seconds()
            return ExecutionResult(
                stage_name=stage_name,
                success=False,
                output="",
                error=str(e),
                duration_seconds=duration_seconds,
            )

    def _build_stage_prompt(
        self,
        stage_name: str,
        config: StageConfig,
        input_artifacts: Dict[str, str],
        specification: str,
    ) -> str:
        """Build prompt for stage execution"""
        prompt = f"""
# {config.description.title()}

## Context

### Specification
{specification}

## Input Artifacts
"""
        for artifact_name, artifact_content in input_artifacts.items():
            prompt += f"\n### {artifact_name}\n{artifact_content}\n"

        prompt += f"""
## Task

You are the {stage_name.replace('-', ' ').title()} agent.
    Execution runtime is GitHub Copilot Agent Mode using the agent definition file at:
    - {config.agent_file}

Your role:
- {config.description}
- Generate the following artifacts:
  {chr(10).join(f'  - {art}' for art in config.output_artifacts)}
- Validate your output
- Report any blockers

## Expected Output Artifacts

{chr(10).join(f'- {art}' for art in config.output_artifacts)}

## Instructions

1. Review the input artifacts
2. Execute your responsibilities
3. Generate output artifacts
4. Validate quality
5. Report any issues

Use your available tools to accomplish the task.
"""
        return prompt

    def _invoke_chat_mode(self, stage_name: str, chat_mode: str, prompt: str, agent_file: str) -> str:
        """Invoke chat mode through VS Code"""
        return (
            f"[Chat mode '{chat_mode}' execution for {stage_name}]\n"
            f"[Agent definition: {agent_file}]\n"
            f"{prompt[:400]}..."
        )

    def _extract_artifacts(self, output: str, stage_name: str, config: StageConfig) -> List[str]:
        """Extract generated artifacts that physically exist on disk."""
        artifacts: List[str] = []

        for target in config.output_targets:
            resolved_path = self._resolve_artifact_path(target, stage_name)
            if resolved_path is not None:
                artifacts.append(self._normalize_artifact_name(target))

        # Fallback to legacy output markers only if they also resolve on disk.
        if artifacts:
            return artifacts

        for artifact_name in config.output_artifacts:
            pattern = f"## {artifact_name}|# {artifact_name}"
            if re.search(pattern, output, re.IGNORECASE):
                resolved_path = self._resolve_artifact_path(artifact_name, stage_name)
                if resolved_path is not None:
                    artifacts.append(artifact_name)

        return artifacts

    def _resolve_artifact_path(self, target: str, stage_name: str) -> Optional[Path]:
        """Resolve a configured artifact target to a real file path under the project."""
        normalized = target.replace("\\", "/").strip("/")
        if not normalized:
            return None

        candidates: List[Path] = []

        direct = self.project_root / normalized
        candidates.append(direct)

        if normalized.startswith("artifacts/"):
            candidates.append(self.project_root / normalized)
        else:
            candidates.extend(
                [
                    self.project_root / "artifacts" / normalized,
                    self.project_root / "artifacts" / "requirements" / normalized,
                    self.project_root / "artifacts" / stage_name / normalized,
                ]
            )

        artifact_root = self.project_root / "artifacts"
        if artifact_root.exists():
            filename = Path(normalized).name
            if filename:
                search_results = list(artifact_root.rglob(filename))
                candidates.extend(search_results)

        seen = set()
        for candidate in candidates:
            if not candidate:
                continue
            try:
                resolved = candidate.resolve()
            except OSError:
                resolved = candidate
            if str(resolved) in seen:
                continue
            seen.add(str(resolved))
            if resolved.exists() and resolved.is_file():
                return resolved

        return None

    def validate_stage_inputs(
        self,
        stage_name: str,
        available_artifacts: Dict[str, bool],
    ) -> Tuple[bool, List[str]]:
        """
        Validate that required inputs are available

        Returns:
            (is_valid, missing_artifacts)
        """
        config = self._stage_configs.get(stage_name)
        if not config:
            return False, [stage_name]

        missing = [
            artifact for artifact in config.input_artifacts
            if not available_artifacts.get(artifact, False)
        ]

        return len(missing) == 0, missing

    def get_stage_config(self, stage_name: str) -> Optional[StageConfig]:
        """Get configuration for a stage"""
        return self._stage_configs.get(stage_name)

    def _build_available_inputs_map(
        self,
        stage_name: str,
        input_artifacts: Dict[str, str],
    ) -> Dict[str, bool]:
        """Determine availability of each declared input artifact."""
        config = self._stage_configs.get(stage_name)
        if not config:
            return {}

        provided = {self._normalize_artifact_name(name) for name in input_artifacts.keys()}
        availability: Dict[str, bool] = {}

        for artifact in config.input_artifacts:
            if artifact in provided:
                availability[artifact] = True
                continue

            resolved_path = self._resolve_artifact_path(artifact, stage_name)
            availability[artifact] = resolved_path is not None

        return availability

    def list_available_stages(self) -> List[str]:
        """List all available stages"""
        return list(self._stage_configs.keys())

    def get_execution_summary(self, results: List[ExecutionResult]) -> Dict[str, Any]:
        """Generate summary of execution results"""
        total_duration = sum(r.duration_seconds for r in results if r.duration_seconds)
        successful = sum(1 for r in results if r.success)

        return {
            "generated_at": datetime.now().isoformat(),
            "total_stages": len(results),
            "successful": successful,
            "failed": len(results) - successful,
            "total_duration_seconds": total_duration,
            "average_duration_seconds": total_duration / len(results) if results else 0,
            "results": [r.to_dict() for r in results],
        }

    def _load_stage_configs(self) -> Dict[str, StageConfig]:
        """Load stage configuration from Markdown agent definitions."""
        configs: Dict[str, StageConfig] = {}

        for stage_name, filename in STAGE_AGENT_FILES.items():
            agent_path = self.agents_dir / filename
            if not agent_path.exists():
                continue

            metadata, body = self._parse_agent_definition(agent_path)
            inputs = self._extract_section_bullets(body, "Inputs")
            outputs = self._extract_section_bullets(body, "Outputs")

            input_artifacts = [self._normalize_artifact_name(item) for item in inputs]
            output_artifacts = [self._normalize_artifact_name(item) for item in outputs]
            output_targets = [self._normalize_output_target(item) for item in outputs]

            config = StageConfig(
                stage_name=stage_name,
                agent_file=f"ai/agents/{filename}",
                chat_mode=STAGE_CHATMODE_OVERRIDES.get(stage_name, stage_name),
                description=str(metadata.get("name", stage_name.replace("-", " ").title())),
                input_artifacts=[item for item in input_artifacts if item],
                output_artifacts=[item for item in output_artifacts if item],
                output_targets=[item for item in output_targets if item],
                requires_approval=stage_name in APPROVAL_REQUIRED_STAGES,
                timeout_seconds=3600,
            )
            configs[stage_name] = config

        return configs

    def _parse_agent_definition(self, agent_path: Path) -> Tuple[Dict[str, Any], str]:
        """Parse YAML frontmatter and markdown body from an agent definition."""
        content = agent_path.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return {}, content

        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}, content

        metadata = yaml.safe_load(parts[1]) or {}
        body = parts[2]
        return metadata, body

    def _extract_section_bullets(self, markdown: str, section_name: str) -> List[str]:
        """Extract bullet list entries from a top-level markdown section."""
        header = f"## {section_name}".lower()
        in_section = False
        items: List[str] = []

        for line in markdown.splitlines():
            stripped = line.strip()
            if stripped.startswith("## "):
                if in_section:
                    break
                in_section = stripped.lower() == header
                continue

            if in_section and stripped.startswith("- "):
                items.append(stripped[2:].strip())

        return items

    def _normalize_artifact_name(self, entry: str) -> str:
        """Convert a configured output/input path into a stable artifact token."""
        token = entry.split("(", 1)[0].strip()
        token = token.replace("\\", "/")
        if token.startswith("artifacts/"):
            token = token[len("artifacts/"):]
        token = token.strip("/")
        if token.endswith(".md"):
            token = token[:-3]
        return token

    def _normalize_output_target(self, entry: str) -> str:
        """Convert configured output path entry into a project-root relative path."""
        target = entry.split("(", 1)[0].strip()
        return target.replace("\\", "/").strip("/")
