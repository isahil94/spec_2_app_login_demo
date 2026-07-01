"""
Artifact Management

Manages storage and retrieval of artifacts throughout the workflow:
- Requirements
- Architecture
- UI/UX Designs
- Backend Code
- Database Schema
- Test Plans
- Documentation
- Deployment Plans

Artifacts are stored in artifacts/ directory organized by stage.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ArtifactManager:
    """Manages workflow artifacts"""

    def __init__(self, artifacts_root: Path = None):
        """Initialize artifact manager"""
        self.artifacts_root = artifacts_root or Path("artifacts")
        self.artifacts_root.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for each stage
        self.stage_dirs = {
            "requirements": self.artifacts_root / "requirements",
            "planning": self.artifacts_root / "planning",
            "architecture": self.artifacts_root / "architecture",
            "design": self.artifacts_root / "design",
            "frontend": self.artifacts_root / "frontend",
            "backend": self.artifacts_root / "backend",
            "database": self.artifacts_root / "database",
            "tests": self.artifacts_root / "tests",
            "documentation": self.artifacts_root / "documentation",
            "deployment": self.artifacts_root / "deployment",
        }

        for dir_path in self.stage_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)

    def save_artifact(
        self,
        stage: str,
        artifact_name: str,
        content: str,
        artifact_type: str = "md"
    ) -> Path:
        """
        Save artifact to appropriate directory

        Args:
            stage: Stage name (requirements, architecture, etc.)
            artifact_name: Name of artifact (e.g., business-requirements)
            content: Artifact content
            artifact_type: File type (md, json, py, sql, etc.)

        Returns:
            Path to saved artifact
        """
        if stage not in self.stage_dirs:
            raise ValueError(f"Unknown stage: {stage}")

        artifact_path = self.stage_dirs[stage] / f"{artifact_name}.{artifact_type}"

        # Create parent directories if needed
        artifact_path.parent.mkdir(parents=True, exist_ok=True)

        # Write artifact
        with open(artifact_path, "w") as f:
            f.write(content)

        return artifact_path

    def load_artifact(
        self,
        stage: str,
        artifact_name: str,
        artifact_type: str = "md"
    ) -> Optional[str]:
        """
        Load artifact from storage

        Args:
            stage: Stage name
            artifact_name: Name of artifact
            artifact_type: File type

        Returns:
            Artifact content or None if not found
        """
        if stage not in self.stage_dirs:
            return None

        artifact_path = self.stage_dirs[stage] / f"{artifact_name}.{artifact_type}"

        if not artifact_path.exists():
            return None

        with open(artifact_path, "r") as f:
            return f.read()

    def save_json_artifact(
        self,
        stage: str,
        artifact_name: str,
        data: Dict[str, Any]
    ) -> Path:
        """Save artifact as JSON"""
        if stage not in self.stage_dirs:
            raise ValueError(f"Unknown stage: {stage}")

        artifact_path = self.stage_dirs[stage] / f"{artifact_name}.json"
        artifact_path.parent.mkdir(parents=True, exist_ok=True)

        with open(artifact_path, "w") as f:
            json.dump(data, f, indent=2)

        return artifact_path

    def load_json_artifact(
        self,
        stage: str,
        artifact_name: str
    ) -> Optional[Dict[str, Any]]:
        """Load artifact as JSON"""
        if stage not in self.stage_dirs:
            return None

        artifact_path = self.stage_dirs[stage] / f"{artifact_name}.json"

        if not artifact_path.exists():
            return None

        with open(artifact_path, "r") as f:
            return json.load(f)

    def list_artifacts(self, stage: str) -> List[Path]:
        """List all artifacts in a stage"""
        if stage not in self.stage_dirs:
            return []

        stage_dir = self.stage_dirs[stage]
        if not stage_dir.exists():
            return []

        return sorted(stage_dir.iterdir())

    def get_artifact_metadata(self, stage: str, artifact_name: str) -> Optional[Dict[str, Any]]:
        """Get metadata about an artifact"""
        if stage not in self.stage_dirs:
            return None

        # Try common extensions
        for ext in ["md", "json", "py", "sql", "txt"]:
            artifact_path = self.stage_dirs[stage] / f"{artifact_name}.{ext}"
            if artifact_path.exists():
                stat = artifact_path.stat()
                return {
                    "name": artifact_name,
                    "stage": stage,
                    "extension": ext,
                    "path": str(artifact_path),
                    "size_bytes": stat.st_size,
                    "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }

        return None

    def stage_requires_artifacts(self, stage: str) -> List[str]:
        """Get required input artifacts for a stage"""
        requirements_map = {
            "requirements": ["specification"],
            "planning": ["business-requirements"],
            "architecture": ["business-requirements", "acceptance-criteria"],
            "design": ["architecture"],
            "frontend": ["ui-spec", "architecture"],
            "backend": ["api-spec", "architecture"],
            "database": ["database-design", "architecture"],
            "tests": ["test-plan", "api-spec", "ui-spec"],
            "documentation": [
                "architecture",
                "api-spec",
                "ui-spec",
                "deployment-plan",
            ],
            "deployment": ["deployment-plan", "release-notes"],
        }
        return requirements_map.get(stage, [])

    def stage_produces_artifacts(self, stage: str) -> List[str]:
        """Get expected output artifacts from a stage"""
        produces_map = {
            "requirements": ["business-requirements", "stakeholder-analysis"],
            "planning": ["acceptance-criteria", "user-story", "implementation-plan"],
            "architecture": [
                "architecture",
                "api-spec",
                "database-design",
                "deployment-plan",
            ],
            "design": ["ui-spec"],
            "frontend": ["ui-code", "ui-tests"],
            "backend": ["backend-code", "api-tests"],
            "database": ["database-schema", "database-tests"],
            "tests": ["test-report", "quality-report"],
            "documentation": [
                "user-guide",
                "developer-guide",
                "api-documentation",
            ],
            "deployment": ["release-notes", "deployment-guide"],
        }
        return produces_map.get(stage, [])

    def verify_stage_inputs(self, stage: str) -> tuple[bool, List[str]]:
        """
        Verify that required input artifacts exist

        Returns:
            (is_valid, missing_artifacts)
        """
        required = self.stage_requires_artifacts(stage)
        missing = []

        for artifact_name in required:
            # Try to find artifact in any format
            found = False
            for ext in ["md", "json", "py", "sql", "txt"]:
                for prev_stage in self.stage_dirs:
                    path = self.stage_dirs[prev_stage] / f"{artifact_name}.{ext}"
                    if path.exists():
                        found = True
                        break
                if found:
                    break

            if not found:
                missing.append(artifact_name)

        return len(missing) == 0, missing

    def get_stage_summary(self, stage: str) -> Dict[str, Any]:
        """Get summary of artifacts for a stage"""
        artifacts = self.list_artifacts(stage)
        return {
            "stage": stage,
            "artifact_count": len(artifacts),
            "artifacts": [
                {
                    "name": artifact.name,
                    "size_bytes": artifact.stat().st_size,
                    "path": str(artifact.relative_to(self.artifacts_root)),
                }
                for artifact in artifacts
            ],
            "required_inputs": self.stage_requires_artifacts(stage),
            "expected_outputs": self.stage_produces_artifacts(stage),
        }

    def get_all_artifacts_summary(self) -> Dict[str, Any]:
        """Get summary of all artifacts"""
        return {
            "artifacts_root": str(self.artifacts_root),
            "created_at": datetime.now().isoformat(),
            "stages": {
                stage: self.get_stage_summary(stage)
                for stage in self.stage_dirs
            },
        }
