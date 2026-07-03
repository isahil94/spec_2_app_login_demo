#!/usr/bin/env python
"""Debug stage config loading."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from orchestration.workflow.executor import ExecutionEngine

engine = ExecutionEngine(project_root=Path(__file__).parent)

print("=== Stage Configs ===")
for stage_name, config in engine._stage_configs.items():
    print(f"\nStage: {stage_name}")
    print(f"  Agent File: {config.agent_file}")
    print(f"  Chat Mode: {config.chat_mode}")
    print(f"  Input Artifacts: {config.input_artifacts}")
    print(f"  Optional Inputs: {config.optional_input_artifacts}")
    print(f"  Output Artifacts: {config.output_artifacts}")
    print(f"  Output Targets: {config.output_targets}")
