from pathlib import Path

from orchestration.workflow.executor import ExecutionEngine


def test_business_analyst_outputs_resolve_to_project_artifact_paths(tmp_path):
    agent_dir = tmp_path / "ai" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "01-business-analyst.md").write_text(
        "---\nname: Business Analyst\n---\n## Inputs\n- specification.md\n## Outputs\n- requirements_spec.md\n- user_stories.md\n",
        encoding="utf-8",
    )

    engine = ExecutionEngine(project_root=tmp_path)
    config = engine.get_stage_config("business-analyst")
    assert config is not None

    requirements_path = tmp_path / "artifacts" / "requirements" / "requirements_spec.md"
    requirements_path.parent.mkdir(parents=True, exist_ok=True)
    requirements_path.write_text("# req", encoding="utf-8")

    artifacts = engine._extract_artifacts("", "business-analyst", config)

    assert "requirements_spec" in artifacts


def test_execute_stage_fails_fast_when_required_inputs_missing(tmp_path):
    agent_dir = tmp_path / "ai" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "01-business-analyst.md").write_text(
        "---\nname: Business Analyst\n---\n"
        "## Inputs\n"
        "- artifacts/requirements/requirements_spec.md\n"
        "## Outputs\n"
        "- artifacts/requirements/user_stories.md\n",
        encoding="utf-8",
    )

    engine = ExecutionEngine(project_root=tmp_path)

    result = engine.execute_stage(
        stage_name="business-analyst",
        input_artifacts={},
        specification="# spec",
    )

    assert result.success is False
    assert result.error is not None
    assert "Missing required input artifacts" in result.error
    assert "fail-fast input policy" in result.error


def test_execute_stage_runs_when_required_inputs_available(tmp_path):
    agent_dir = tmp_path / "ai" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "01-business-analyst.md").write_text(
        "---\nname: Business Analyst\n---\n"
        "## Inputs\n"
        "- artifacts/requirements/requirements_spec.md\n"
        "## Outputs\n"
        "- artifacts/requirements/user_stories.md\n",
        encoding="utf-8",
    )

    output_path = tmp_path / "artifacts" / "requirements" / "user_stories.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("# stories", encoding="utf-8")

    engine = ExecutionEngine(project_root=tmp_path)

    result = engine.execute_stage(
        stage_name="business-analyst",
        input_artifacts={"requirements/requirements_spec": "# requirements"},
        specification="# spec",
    )

    assert result.success is True
