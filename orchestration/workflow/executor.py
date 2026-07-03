"""
Workflow Execution Engine

-Executes workflow stages from Markdown-based agent definitions.

Does NOT perform AI reasoning - only coordinates execution through:
- Agent definitions in .github/agents/*.md
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
        optional_input_artifacts: List[str],
        output_artifacts: List[str],
        prompt_template: Optional[str] = None,
        output_targets: Optional[List[str]] = None,
        requires_approval: bool = False,
        timeout_seconds: int = 3600,
    ):
        self.stage_name = stage_name
        self.agent_file = agent_file
        self.chat_mode = chat_mode
        self.description = description
        self.input_artifacts = input_artifacts
        self.optional_input_artifacts = optional_input_artifacts
        self.output_artifacts = output_artifacts
        self.prompt_template = prompt_template
        self.output_targets = output_targets or []
        self.requires_approval = requires_approval
        self.timeout_seconds = timeout_seconds


STAGE_AGENT_FILES = {
    "business-analyst": "01-business-analyst.agent.md",
    "solution-architect": "02-solution-architect.agent.md",
    "ui-ux-developer": "03-ui-ux-developer.agent.md",
    "backend-developer": "04-backend-developer.agent.md",
    "database-developer": "05-database-developer.agent.md",
    "qa-engineer": "06-qa-engineer.agent.md",
    "reviewer": "07-reviewer.agent.md",
    "documentation": "08-documentation.agent.md",
    "devops": "09-devops.agent.md",
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
        self.agents_dir = self.project_root / ".github" / "agents"
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
            available_inputs = self._build_available_inputs_map(
                stage_name, input_artifacts
            )
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
            output = self._invoke_chat_mode(
                stage_name, config.chat_mode, prompt, config.agent_file
            )

            # Extract artifacts from output and verify all expected outputs are materialized
            artifacts, missing_outputs = self._extract_artifacts(
                output, stage_name, config
            )

            if missing_outputs:
                missing_str = ", ".join(sorted(missing_outputs))
                return ExecutionResult(
                    stage_name=stage_name,
                    success=False,
                    output=output,
                    error=(
                        f"No output artifacts materialized for stage '{stage_name}'. "
                        f"The following expected output artifacts were not materialized or were invalid placeholders: {missing_str}. "
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

"""
        if config.prompt_template:
            prompt_template_path = self.project_root / config.prompt_template
            if prompt_template_path.exists():
                prompt += f"""
## Agent Prompt Template
{prompt_template_path.read_text(encoding='utf-8')}

"""
            else:
                prompt += f"""
## Agent Prompt Template
WARNING: Prompt template not found at {prompt_template_path}

"""

        chat_mode_file = self._resolve_chat_mode_file(config.chat_mode)
        if chat_mode_file:
            prompt += f"""
## Chat Mode Entry
{chat_mode_file.read_text(encoding='utf-8')}

"""

        prompt += f"""
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
"""
        if config.prompt_template:
            prompt += f"\n    Prompt template: {config.prompt_template}\n"
        prompt += f"""

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

    def _invoke_chat_mode(
        self, stage_name: str, chat_mode: str, prompt: str, agent_file: str
    ) -> str:
        """Resolve chat mode entry and materialize stage artifacts from workflow context."""
        config = self._stage_configs.get(stage_name)
        if not config:
            return f"[Unknown stage: {stage_name}]"

        chat_mode_file = self._resolve_chat_mode_file(chat_mode)
        stage_folder = self._stage_artifact_folder(stage_name)
        output_lines = [
            f"[Chat mode: {chat_mode}]\n",
            f"[Agent definition: {agent_file}]\n",
        ]

        if chat_mode_file:
            output_lines.append(
                f"[Resolved chat mode file: {chat_mode_file.relative_to(self.project_root)}]\n"
            )
        else:
            output_lines.append(
                f"[Chat mode entry file not found: {chat_mode}.chatmode.md]\n"
            )

        if stage_folder:
            stage_folder.mkdir(parents=True, exist_ok=True)

        output_targets = config.output_targets or config.output_artifacts
        existing_paths: Dict[str, Path] = {}
        ignored_placeholders: Dict[str, Path] = {}

        for artifact_target in output_targets:
            resolved_path = self._resolve_artifact_path(artifact_target, stage_name)
            if resolved_path is None or not resolved_path.exists():
                continue

            artifact_file = resolved_path
            if resolved_path.is_dir():
                artifact_file = resolved_path / "artifact.md"

            if not artifact_file.exists():
                continue

            if self._is_placeholder_artifact(artifact_file):
                ignored_placeholders[artifact_target] = artifact_file
                continue

            existing_paths[artifact_target] = artifact_file

        if existing_paths:
            output_lines.append(
                "[Preserved existing artifacts from actual agent runtime or prior workflow execution]\n"
            )
            for target, path in existing_paths.items():
                output_lines.append(f"- {path.relative_to(self.project_root)}\n")

        if ignored_placeholders:
            output_lines.append(
                "[Ignored placeholder artifacts generated by the workflow engine; real agent output is required.]\n"
            )
            for target, path in ignored_placeholders.items():
                output_lines.append(f"- {path.relative_to(self.project_root)}\n")

        if not existing_paths:
            output_lines.append(
                "[No real artifacts found on disk for this stage. Real agent execution is required.]\n"
            )

        output_lines.append(f"{prompt[:200]}...")
        return "".join(output_lines)

    def _prepare_output_path(self, artifact_target: str, stage_name: str) -> Path:
        """Return a writable file path for an artifact target, including directory-style targets."""
        normalized = artifact_target.replace("\\", "/").strip("/")
        if not normalized:
            return (
                self._stage_artifact_folder(stage_name)
                or self.project_root / "artifacts"
            )

        existing = self._resolve_artifact_path(artifact_target, stage_name)
        if existing is not None and existing.is_dir():
            return existing / "artifact.md"

        candidate = Path(normalized)
        if candidate.suffix:
            return self.project_root / normalized

        if normalized.startswith("artifacts/"):
            return self.project_root / normalized / "artifact.md"

        if normalized.startswith(("apps/", "tests/", "review/", "docs/", "docs")):
            return self.project_root / normalized / "artifact.md"

        stage_folder = self._stage_artifact_folder(stage_name)
        if stage_folder:
            return stage_folder / normalized / "artifact.md"

        return self.project_root / "artifacts" / normalized / "artifact.md"

    def _resolve_chat_mode_file(self, chat_mode: str) -> Optional[Path]:
        """Resolve a chat mode entry file for the given stage chat mode."""
        if not chat_mode:
            return None

        candidate = self.chat_mode_dir / f"{chat_mode}.chatmode.md"
        if candidate.exists():
            return candidate

        alt_candidate = (
            self.project_root / ".github" / "chatmodes" / f"{chat_mode}.chatmode.md"
        )
        if alt_candidate.exists():
            return alt_candidate

        return None

    def _is_placeholder_artifact(self, artifact_path: Path) -> bool:
        """Detect whether an artifact file was generated by the workflow engine stub."""
        if not artifact_path.exists() or not artifact_path.is_file():
            return False

        try:
            content = artifact_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return False

        placeholder_signatures = [
            "Generated from workflow inputs by",
            "This artifact was derived from the workflow specification and the stage inputs.",
            "The document is ready for downstream review and handoff.",
        ]

        return any(signature in content for signature in placeholder_signatures)

    def _build_artifact_content(
        self, stage_name: str, artifact_name: str, prompt: str
    ) -> str:
        """Create meaningful stage-specific artifact content from the workflow prompt."""
        title = Path(artifact_name).name.replace("_", " ").replace("-", " ").title()
        summary = self._summarize_prompt(prompt)
        stage_label = stage_name.replace("-", " ").title()
        artifact_kind = (
            Path(artifact_name).stem.replace("_", " ").replace("-", " ").title()
        )

        content = [
            f"# {title}",
            "",
            f"Generated from workflow inputs by {stage_label}.",
            "",
            f"## Summary",
            summary,
            "",
            f"## {artifact_kind} Notes",
            f"- This artifact was derived from the workflow specification and the stage inputs.",
            f"- {stage_label} produced a concrete implementation plan for the requested capability.",
            "- The content is intended to be refined by the corresponding agent execution when richer context is available.",
            "",
            "## Validation",
            "- Artifact content is grounded in the provided workflow inputs.",
            "- The document is ready for downstream review and handoff.",
        ]
        return "\n".join(content) + "\n"

    def _summarize_prompt(self, prompt: str) -> str:
        """Create a concise summary from the supplied prompt text."""
        cleaned = re.sub(r"\s+", " ", prompt or "")
        cleaned = cleaned.strip()
        if not cleaned:
            return "No additional context was provided."

        if len(cleaned) <= 220:
            return cleaned

        return cleaned[:220].rstrip() + "..."

    def _extract_artifacts(
        self, output: str, stage_name: str, config: StageConfig
    ) -> Tuple[List[str], List[str]]:
        """Extract generated artifacts that physically exist on disk and detect missing outputs."""
        artifacts: List[str] = []
        missing_targets: List[str] = []

        for target in config.output_targets:
            resolved_path = self._resolve_artifact_path(target, stage_name)
            if resolved_path is not None and resolved_path.exists():
                if resolved_path.is_dir():
                    artifacts.append(self._normalize_artifact_name(target))
                    continue

                if not self._is_placeholder_artifact(resolved_path):
                    artifacts.append(self._normalize_artifact_name(target))
                    continue

            fallback_path = self._prepare_output_path(target, stage_name)
            if fallback_path.exists() and not self._is_placeholder_artifact(
                fallback_path
            ):
                artifacts.append(self._normalize_artifact_name(target))
                continue

            missing_targets.append(target)

        return artifacts, missing_targets

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
            stage_folder = self._stage_artifact_folder(stage_name)
            if stage_folder:
                candidates.append(stage_folder / normalized)

            candidates.extend(
                [
                    self.project_root / "artifacts" / normalized,
                    self.project_root / "artifacts" / "requirements" / normalized,
                    self.project_root / "artifacts" / stage_name / normalized,
                ]
            )

        if normalized.endswith("/"):
            normalized = normalized.rstrip("/")

        artifact_root = self.project_root / "artifacts"
        if artifact_root.exists():
            filename = Path(normalized).name
            if filename:
                stage_matches = []
                for path in artifact_root.rglob(filename):
                    if self._is_stage_artifact_match(path, stage_name):
                        stage_matches.append(path)
                candidates.extend(stage_matches)

                if not stage_matches:
                    candidates.extend(list(artifact_root.rglob(filename)))

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
            if resolved.exists() and (resolved.is_file() or resolved.is_dir()):
                return resolved

        return None

    def _stage_artifact_folder(self, stage_name: str) -> Optional[Path]:
        """Return the preferred artifact folder for a stage."""
        stage_map = {
            "business-analyst": "requirements",
            "solution-architect": "architecture",
            "ui-ux-developer": "frontend",
            "backend-developer": "backend",
            "database-developer": "database",
            "qa-engineer": "tests",
            "reviewer": "review",
            "documentation": "documentation",
            "devops": "deployment",
        }
        folder = stage_map.get(stage_name)
        if not folder:
            return None
        return self.project_root / "artifacts" / folder

    def _is_stage_artifact_match(self, path: Path, stage_name: str) -> bool:
        """Check whether a file belongs to the current stage's artifact folder."""
        stage_folder = self._stage_artifact_folder(stage_name)
        if not stage_folder:
            return True
        try:
            return stage_folder in path.resolve().parents
        except OSError:
            return False

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
            artifact
            for artifact in config.input_artifacts
            if not available_artifacts.get(artifact, False)
        ]

        if len(missing) == 0:
            return True, []

        if any(artifact in available_artifacts for artifact in missing):
            missing = [
                artifact
                for artifact in missing
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

        provided = {
            self._normalize_artifact_name(name) for name in input_artifacts.keys()
        }
        availability: Dict[str, bool] = {}

        for artifact in config.input_artifacts + config.optional_input_artifacts:
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
            agent_path = self._resolve_agent_path(filename)
            if not agent_path:
                continue

            metadata, body = self._parse_agent_definition(agent_path)
            inputs = self._extract_section_bullets(body, "Inputs")
            outputs = self._extract_section_bullets(body, "Outputs")
            outputs = [
                item
                for item in outputs
                if item and not item.startswith("**") and not item.startswith("All")
            ]

            parsed_inputs = []
            for item in inputs:
                parsed_inputs.extend(self._parse_input_artifact(item))

            required_inputs = [
                item for item, optional in parsed_inputs if item and not optional
            ]
            optional_inputs = [
                item for item, optional in parsed_inputs if item and optional
            ]
            output_artifacts = [self._normalize_artifact_name(item) for item in outputs]
            output_targets = [self._normalize_output_target(item) for item in outputs]

            config = StageConfig(
                stage_name=stage_name,
                agent_file=f".github/agents/{filename}",
                chat_mode=STAGE_CHATMODE_OVERRIDES.get(stage_name, stage_name),
                description=str(
                    metadata.get("name", stage_name.replace("-", " ").title())
                ),
                input_artifacts=[item for item in required_inputs if item],
                optional_input_artifacts=[item for item in optional_inputs if item],
                output_artifacts=[item for item in output_artifacts if item],
                prompt_template=(
                    str(metadata.get("prompt_template"))
                    if metadata.get("prompt_template")
                    else None
                ),
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
        header_prefix = f"## {section_name}".lower()
        in_section = False
        items: List[str] = []
        current_item: Optional[str] = None

        for line in markdown.splitlines():
            stripped = line.strip()
            if stripped.startswith("## "):
                if in_section:
                    break
                in_section = stripped.lower().startswith(header_prefix)
                continue

            if not in_section:
                continue

            if stripped.startswith("- "):
                if current_item is not None:
                    items.append(current_item.strip())
                current_item = stripped[2:].strip()
            elif (
                current_item is not None
                and stripped
                and line.startswith(" ")
                and not stripped.startswith("**")
                and not stripped.startswith("All")
                and not stripped.startswith("If")
                and not stripped.startswith("Never")
                and not stripped.startswith("Only")
            ):
                current_item = f"{current_item} {stripped.strip()}"

        if current_item is not None:
            items.append(current_item.strip())

        return items

    def _parse_input_artifact(self, entry: str) -> List[Tuple[Optional[str], bool]]:
        """Parse an input entry line into artifact(s) and optional flag."""
        raw = entry.split("(", 1)[0].strip()
        if not raw:
            return []

        normalized_parts = [
            segment.strip() for segment in re.split(r"\s*,\s*", raw) if segment.strip()
        ]
        is_optional = (
            "optional" in entry.lower()
            or "fallback" in entry.lower()
            or "reference" in entry.lower()
        )
        is_multiline_reference = len(normalized_parts) > 1 and any(
            segment.endswith((".md", ".txt", ".yaml", ".yml", ".json"))
            for segment in normalized_parts[1:]
        )
        if is_multiline_reference:
            is_optional = True

        parsed: List[Tuple[Optional[str], bool]] = []
        base_prefix = None
        for segment in normalized_parts:
            cleaned = segment.replace("\\", "/").strip()
            if not cleaned:
                continue

            if cleaned.startswith("artifacts/"):
                rel_path = cleaned[len("artifacts/") :]
                base_prefix = (
                    str(Path(rel_path).parent).replace("\\", "/")
                    if str(Path(rel_path).parent) != "."
                    else None
                )
                candidate = f"artifacts/{rel_path}"
            elif cleaned.startswith(("./", "../")):
                candidate = cleaned
                base_prefix = (
                    str(Path(cleaned).parent).replace("\\", "/")
                    if str(Path(cleaned).parent) != "."
                    else None
                )
            elif "/" in cleaned:
                candidate = f"artifacts/{cleaned}"
                base_prefix = (
                    str(Path(cleaned).parent).replace("\\", "/")
                    if str(Path(cleaned).parent) != "."
                    else None
                )
            elif base_prefix:
                candidate = f"artifacts/{base_prefix}/{cleaned}"
            else:
                candidate = f"artifacts/{cleaned}"

            if not re.search(
                r"[\w\-./]+\.(md|txt|yaml|yml|json)$", candidate, re.IGNORECASE
            ):
                continue

            parsed.append((self._normalize_artifact_name(candidate), is_optional))

        return parsed

    def _resolve_agent_path(self, filename: str) -> Optional[Path]:
        """Resolve an agent definition path from the canonical or legacy locations."""
        candidates = []
        for root in [self.agents_dir, self.project_root / "ai" / "agents"]:
            candidates.append(root / filename)
            if filename.endswith(".agent.md"):
                candidates.append(root / filename.replace(".agent.md", ".md"))
            elif filename.endswith(".md"):
                candidates.append(root / filename.replace(".md", ".agent.md"))

        for candidate in candidates:
            if candidate.exists():
                return candidate

        return None

    def _normalize_artifact_name(self, entry: str) -> str:
        """Convert a configured output/input path into a stable artifact token."""
        token = entry.split("(", 1)[0].strip()
        token = token.replace("\\", "/")
        token = token.strip("`")
        if token.startswith("artifacts/"):
            token = token[len("artifacts/") :]
        token = token.strip("/")
        if token.endswith(".md"):
            token = token[:-3]
        return token

    def _normalize_output_target(self, entry: str) -> str:
        """Convert configured output path entry into a project-root relative path."""
        target = entry.split("(", 1)[0].strip()
        target = target.replace("\\", "/").strip()
        target = target.strip("`")
        return target.strip("/")
