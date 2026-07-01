"""
Base module for agent scripts.

Provides shared utilities for loading and executing SDLC agent definitions.
"""

import hashlib
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import yaml

logger = logging.getLogger(__name__)


def setup_logging(name: str, level: int = logging.INFO) -> logging.Logger:
    """Configure logging for agent scripts and return logger."""
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    log = logging.getLogger(name)
    log.setLevel(level)
    log.addHandler(handler)
    return log


def load_agent_definition(agent_filename: str) -> Dict[str, Any]:
    """
    Load an agent definition from the ai/agents directory.
    
    Args:
        agent_filename: Name of the agent markdown file (e.g., '01-business-analyst.md')
        
    Returns:
        Dictionary containing 'metadata' and 'content' keys
        
    Raises:
        FileNotFoundError: If agent file does not exist
        yaml.YAMLError: If YAML frontmatter is invalid
    """
    workspace_root = Path(__file__).parent.parent
    agent_path = workspace_root / 'ai' / 'agents' / agent_filename
    
    if not agent_path.exists():
        raise FileNotFoundError(f"Agent definition not found: {agent_path}")
    
    content = agent_path.read_text(encoding='utf-8')
    
    # Parse YAML frontmatter
    if not content.startswith('---'):
        raise ValueError(f"Invalid agent definition format in {agent_path}: missing frontmatter")
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        raise ValueError(f"Invalid agent definition format in {agent_path}")
    
    try:
        metadata = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML in {agent_path}: {e}")
    
    markdown_content = parts[2].strip()
    
    return {
        'metadata': metadata,
        'content': markdown_content,
        'path': agent_path
    }


def display_agent_info(metadata: Dict[str, Any]) -> None:
    """Display agent information to the user."""
    print("\n" + "=" * 70)
    print(f"Agent: {metadata.get('name', 'Unknown')}")
    print(f"ID: {metadata.get('id', 'N/A')}")
    print(f"Version: {metadata.get('version', '1.0.0')}")
    print(f"Category: {metadata.get('category', 'N/A')}")
    print(f"Execution: {metadata.get('execution', 'N/A')}")
    print("=" * 70)


def validate_paths(
    input_path: Path | None = None,
    output_path: Path | None = None
) -> bool:
    """
    Validate that required paths exist or can be created.
    
    Args:
        input_path: Path to input file or directory
        output_path: Path to output directory
        
    Returns:
        True if validation passes
        
    Raises:
        FileNotFoundError: If input path does not exist
        PermissionError: If output path is not writable
    """
    if input_path and not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")
    
    if output_path:
        if output_path.exists() and not output_path.is_dir():
            raise ValueError(f"Output path must be a directory: {output_path}")
        if not output_path.exists():
            try:
                output_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created output directory: {output_path}")
            except PermissionError as e:
                raise PermissionError(f"Cannot write to output path: {output_path}") from e
    
    return True


def log_placeholder_execution(agent_name: str, input_path: str | None, output_path: str | None) -> None:
    """Log placeholder execution message."""
    logger.info(f"\n--- Placeholder Execution ---")
    logger.info(f"Agent: {agent_name}")
    if input_path:
        logger.info(f"Input: {input_path}")
    if output_path:
        logger.info(f"Output: {output_path}")
    logger.info(f"Status: Ready for GitHub Copilot Agent Mode integration")
    logger.info(f"--- End Placeholder ---\n")


def _hash_file(file_path: Path) -> str:
    """Return SHA-256 hash for a file."""
    hasher = hashlib.sha256()
    with file_path.open('rb') as file_handle:
        while True:
            chunk = file_handle.read(8192)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def _hash_directory(directory_path: Path) -> str:
    """Return deterministic SHA-256 hash for directory contents."""
    hasher = hashlib.sha256()
    for path in sorted(p for p in directory_path.rglob('*') if p.is_file()):
        relative_path = path.relative_to(directory_path).as_posix()
        hasher.update(relative_path.encode('utf-8'))
        hasher.update(_hash_file(path).encode('utf-8'))
    return hasher.hexdigest()


def _hash_selected_paths(base_dir: Path, include_paths: Sequence[str]) -> str:
    """Return deterministic SHA-256 hash for selected files/directories under a base directory."""
    hasher = hashlib.sha256()
    for relative in sorted(set(include_paths)):
        target = (base_dir / relative).resolve()
        try:
            normalized_relative = target.relative_to(base_dir.resolve()).as_posix()
        except ValueError:
            normalized_relative = relative.replace('\\', '/')

        if not target.exists():
            hasher.update(f"missing:{normalized_relative}".encode('utf-8'))
            continue

        if target.is_file():
            hasher.update(f"file:{normalized_relative}".encode('utf-8'))
            hasher.update(_hash_file(target).encode('utf-8'))
            continue

        for path in sorted(p for p in target.rglob('*') if p.is_file()):
            rel = path.relative_to(base_dir).as_posix()
            hasher.update(f"dir-file:{rel}".encode('utf-8'))
            hasher.update(_hash_file(path).encode('utf-8'))

    return hasher.hexdigest()


def _hash_referenced_paths(workspace_root: Path, relative_paths: Sequence[str]) -> str:
    """Return deterministic hash for a set of referenced files under the workspace."""
    hasher = hashlib.sha256()
    for relative_path in sorted(set(relative_paths)):
        normalized = relative_path.replace('\\', '/').strip()
        if not normalized:
            continue
        target = workspace_root / normalized
        hasher.update(normalized.encode('utf-8'))
        if target.exists() and target.is_file():
            hasher.update(_hash_file(target).encode('utf-8'))
        else:
            hasher.update(b'missing')
    return hasher.hexdigest()


def _hash_skill_references(workspace_root: Path, skill_names: Sequence[str]) -> str:
    """Return deterministic hash for referenced skills and resolved skill definition files."""
    hasher = hashlib.sha256()
    skills_dir = workspace_root / 'ai' / 'skills'
    skill_files = sorted(skills_dir.glob('*.md')) if skills_dir.exists() else []

    for skill_name in sorted(set(skill_names)):
        normalized_name = skill_name.strip()
        if not normalized_name:
            continue
        hasher.update(f"skill:{normalized_name}".encode('utf-8'))

        matched_files: list[Path] = []
        pattern = re.compile(rf"^##\s+Skill:\s+{re.escape(normalized_name)}\s*$", re.IGNORECASE | re.MULTILINE)
        for skill_file in skill_files:
            content = skill_file.read_text(encoding='utf-8')
            if pattern.search(content):
                matched_files.append(skill_file)

        if not matched_files:
            hasher.update(b'unresolved')
            continue

        for matched in matched_files:
            relative = matched.relative_to(workspace_root).as_posix()
            hasher.update(relative.encode('utf-8'))
            hasher.update(_hash_file(matched).encode('utf-8'))

    return hasher.hexdigest()


def _extract_markdown_section_list(markdown_content: str, section_name: str) -> list[str]:
    """Extract bullet list items from a top-level markdown section."""
    section_header = f"## {section_name}".lower()
    lines = markdown_content.splitlines()
    in_section = False
    items: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('## '):
            if in_section:
                break
            in_section = stripped.lower() == section_header
            continue

        if not in_section:
            continue

        if stripped.startswith('- '):
            items.append(stripped[2:].strip())

    return items


def _load_agent_definition_by_id(agent_id: str) -> Optional[Dict[str, Any]]:
    """Resolve and load an agent definition using the agent id."""
    workspace_root = Path(__file__).parent.parent
    agents_dir = workspace_root / 'ai' / 'agents'
    if not agents_dir.exists():
        return None

    for agent_file in sorted(agents_dir.glob('*.md')):
        try:
            loaded = load_agent_definition(agent_file.name)
        except Exception:
            continue
        metadata = loaded.get('metadata') or {}
        if metadata.get('id') == agent_id:
            return loaded

    return None


def _resolve_owned_artifact_paths(
    output_path: Optional[Path],
    metadata: Dict[str, Any],
    markdown_content: str,
) -> list[Path]:
    """Return concrete output artifact paths owned by the agent for existence checks."""
    if output_path is None:
        return []

    workspace_root = Path(__file__).parent.parent
    resolved_output = output_path.resolve()
    category = str(metadata.get('category', '')).strip().lower()

    section_outputs = _extract_markdown_section_list(markdown_content, 'Outputs')
    metadata_outputs = metadata.get('produces') or []
    output_entries = section_outputs or list(metadata_outputs)

    artifact_base = resolved_output
    if category and resolved_output.name.lower() != category:
        if resolved_output.name.lower() == 'artifacts' or (resolved_output / category).exists():
            artifact_base = resolved_output / category

    resolved_paths: list[Path] = []
    for entry in output_entries:
        normalized = str(entry).strip().replace('\\', '/')
        if not normalized:
            continue

        if normalized.startswith('artifacts/'):
            resolved_paths.append((workspace_root / normalized).resolve())
            continue

        if '/' in normalized:
            resolved_paths.append((resolved_output / normalized).resolve())
            continue

        filename = normalized if normalized.endswith('.md') else f"{normalized}.md"
        resolved_paths.append((artifact_base / filename).resolve())

    # Preserve stable order while removing duplicates.
    unique_paths: list[Path] = []
    seen: set[str] = set()
    for candidate in resolved_paths:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        unique_paths.append(candidate)

    return unique_paths


def _build_execution_fingerprint(
    agent_id: str,
    input_signature: str,
    output_path: Optional[Path],
) -> tuple[str, Dict[str, str], list[Path]]:
    """Build execution fingerprint components and return missing owned artifacts."""
    workspace_root = Path(__file__).parent.parent
    loaded_agent = _load_agent_definition_by_id(agent_id)

    components: Dict[str, str] = {
        'input_signature': input_signature,
        'agent_definition': 'unresolved',
        'templates': 'none',
        'skills': 'none',
        'shared_instructions': 'none',
    }
    missing_owned_artifacts: list[Path] = []

    if loaded_agent is not None:
        metadata = loaded_agent.get('metadata') or {}
        markdown_content = loaded_agent.get('content', '')
        agent_path = loaded_agent.get('path')
        if isinstance(agent_path, Path) and agent_path.exists():
            components['agent_definition'] = _hash_file(agent_path)

        templates = _extract_markdown_section_list(markdown_content, 'Templates')
        if templates:
            components['templates'] = _hash_referenced_paths(workspace_root, templates)

        skills = _extract_markdown_section_list(markdown_content, 'Skills Used')
        if skills:
            components['skills'] = _hash_skill_references(workspace_root, skills)

        shared_instructions = _extract_markdown_section_list(markdown_content, 'Shared Instructions')
        if shared_instructions:
            components['shared_instructions'] = _hash_referenced_paths(workspace_root, shared_instructions)

        owned_artifacts = _resolve_owned_artifact_paths(output_path, metadata, markdown_content)
        missing_owned_artifacts = [path for path in owned_artifacts if not path.exists()]

    hasher = hashlib.sha256()
    for key in sorted(components):
        hasher.update(f"{key}:{components[key]}".encode('utf-8'))

    return hasher.hexdigest(), components, missing_owned_artifacts


def compute_input_signature(
    input_path: Optional[Path],
    include_paths: Optional[Sequence[str]] = None,
) -> str:
    """Compute a stable signature for the current input path."""
    if input_path is None:
        return 'no-input'

    resolved = input_path.resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Input path does not exist: {resolved}")

    if resolved.is_file():
        return f"file:{_hash_file(resolved)}"

    if include_paths:
        return f"dir:selected:{_hash_selected_paths(resolved, include_paths)}"

    return f"dir:{_hash_directory(resolved)}"


def validate_required_inputs(
    input_path: Optional[Path],
    required_paths: Optional[Sequence[str]],
) -> list[str]:
    """Return required relative paths that are missing under the input path."""
    if not required_paths or input_path is None or input_path.is_file():
        return []

    base_dir = input_path.resolve()
    return [
        rel for rel in required_paths
        if not (base_dir / rel).exists()
    ]


def _execution_state_path(output_path: Optional[Path], agent_id: str) -> Optional[Path]:
    """Return path to persisted execution state for an agent and output target."""
    if output_path is None:
        return None

    state_dir = output_path / '.agent_state'
    return state_dir / f"{agent_id}.json"


def should_skip_retry(
    agent_id: str,
    input_path: Optional[Path],
    output_path: Optional[Path],
    include_paths: Optional[Sequence[str]] = None,
) -> tuple[bool, str, str]:
    """
    Decide whether a retry should be skipped.

    Returns:
        Tuple of (should_skip, current_input_signature, reason)
    """
    signature = compute_input_signature(input_path, include_paths=include_paths)
    execution_fingerprint, fingerprint_components, missing_owned_artifacts = _build_execution_fingerprint(
        agent_id=agent_id,
        input_signature=signature,
        output_path=output_path,
    )

    if missing_owned_artifacts:
        missing_list = ', '.join(path.name for path in missing_owned_artifacts)
        return False, execution_fingerprint, f'Missing owned artifacts: {missing_list}.'

    state_path = _execution_state_path(output_path, agent_id)

    if state_path is None:
        return False, execution_fingerprint, 'Output path not provided; cannot compare prior state.'

    if not state_path.exists():
        return False, execution_fingerprint, 'No prior execution state found for this output.'

    try:
        state_data = json.loads(state_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return False, execution_fingerprint, 'Execution state is invalid; running update to recover state.'

    last_signature = state_data.get('input_signature')
    if last_signature == execution_fingerprint:
        return True, execution_fingerprint, 'All owned artifacts exist and execution fingerprint is unchanged.'

    last_components = state_data.get('fingerprint_components')
    if isinstance(last_components, dict):
        changed = [
            name for name in (
                'input_signature',
                'agent_definition',
                'templates',
                'skills',
                'shared_instructions',
            )
            if last_components.get(name) != fingerprint_components.get(name)
        ]
        if changed:
            readable_names = {
                'input_signature': 'consumed inputs',
                'agent_definition': 'agent definition',
                'templates': 'referenced templates',
                'skills': 'referenced skills',
                'shared_instructions': 'shared instructions',
            }
            changed_labels = ', '.join(readable_names[item] for item in changed)
            return False, execution_fingerprint, f'Execution fingerprint changed: {changed_labels}.'

    return False, execution_fingerprint, 'Execution fingerprint changed since last successful run.'


def record_execution_state(
    agent_id: str,
    input_signature: str,
    input_path: Optional[Path],
    output_path: Optional[Path],
) -> None:
    """Persist execution state after successful run."""
    state_path = _execution_state_path(output_path, agent_id)
    if state_path is None:
        return

    fingerprint_components: Optional[Dict[str, str]] = None
    if output_path is not None:
        _, fingerprint_components, _ = _build_execution_fingerprint(
            agent_id=agent_id,
            input_signature=input_signature,
            output_path=output_path,
        )

    state_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        'agent_id': agent_id,
        'input_signature': input_signature,
        'fingerprint_components': fingerprint_components,
        'input_path': str(input_path) if input_path else None,
        'output_path': str(output_path) if output_path else None,
        'updated_at': datetime.utcnow().isoformat(timespec='seconds') + 'Z',
    }
    state_path.write_text(json.dumps(payload, indent=2), encoding='utf-8')


def assess_execution_status(
    agent_id: str,
    input_path: Optional[Path],
    output_path: Optional[Path],
    include_paths: Optional[Sequence[str]] = None,
) -> tuple[str, str, str]:
    """
    Assess incremental execution status for a stage.

    Returns:
        Tuple of (status, input_signature, reason), where status is one of
        SKIPPED, UPDATED, or CREATED.
    """
    state_path = _execution_state_path(output_path, agent_id)
    state_exists = bool(state_path and state_path.exists())

    should_skip, input_signature, reason = should_skip_retry(
        agent_id=agent_id,
        input_path=input_path,
        output_path=output_path,
        include_paths=include_paths,
    )
    if should_skip:
        return 'SKIPPED', input_signature, reason

    if state_exists:
        return 'UPDATED', input_signature, reason

    return 'CREATED', input_signature, reason


class AgentBase:
    """Shared base class for lightweight agent script orchestration."""

    def __init__(self, name: str, agent_file: str):
        self.name = name
        self.agent_file = agent_file
        self.workspace_root = Path(__file__).parent.parent
        self.logger = setup_logging(name.lower().replace(' ', '_'))

    def load_artifact(self, relative_path: str) -> Optional[str]:
        """Load a repository artifact by relative path."""
        artifact_path = self.workspace_root / relative_path
        if not artifact_path.exists():
            return None
        return artifact_path.read_text(encoding='utf-8')

    def get_execution_status(
        self,
        agent_id: str,
        input_path: Optional[Path],
        output_path: Optional[Path],
        include_paths: Optional[Sequence[str]] = None,
    ) -> tuple[str, str, str]:
        """Return stage execution status using shared fingerprint state logic."""
        return assess_execution_status(
            agent_id=agent_id,
            input_path=input_path,
            output_path=output_path,
            include_paths=include_paths,
        )
