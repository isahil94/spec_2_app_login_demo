"""
Artifact Manager

Manages artifact discovery, validation, and summary generation for the SDLC workflow.
"""

from pathlib import Path
from typing import Dict, List


class ArtifactManager:
    """Tracks artifacts generated during workflow execution."""

    def __init__(self, artifacts_dir: Path):
        self.artifacts_dir = artifacts_dir
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def get_all_artifacts_summary(self) -> Dict[str, object]:
        """Return a summary of all artifacts under the artifacts directory."""
        artifacts = []
        for path in sorted(self.artifacts_dir.rglob("*")):
            if path.is_file():
                artifacts.append({
                    "path": str(path.relative_to(self.artifacts_dir)),
                    "size_bytes": path.stat().st_size,
                })

        return {
            "artifact_root": str(self.artifacts_dir),
            "artifact_count": len(artifacts),
            "artifacts": artifacts,
        }

    def artifact_exists(self, relative_path: str) -> bool:
        """Check if an artifact exists under the artifacts directory."""
        candidate = self.artifacts_dir / relative_path
        return candidate.exists() and candidate.is_file()

    def resolve_artifact_path(self, relative_path: str) -> Path:
        """Resolve an artifact path under the artifacts directory."""
        return (self.artifacts_dir / relative_path).resolve()
