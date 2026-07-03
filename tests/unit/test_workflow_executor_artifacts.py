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
    user_stories_path = tmp_path / "artifacts" / "requirements" / "user_stories.md"
    requirements_path.parent.mkdir(parents=True, exist_ok=True)
    requirements_path.write_text("# req", encoding="utf-8")
    user_stories_path.write_text("# stories", encoding="utf-8")

    artifacts, missing = engine._extract_artifacts("", "business-analyst", config)

    assert "requirements_spec" in artifacts
    assert missing == []


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


def test_execute_stage_treats_reference_inputs_as_optional_and_parses_comma_separated_inputs(
    tmp_path,
):
    agent_dir = tmp_path / ".github" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "03-ui-ux-developer.agent.md").write_text(
        "---\nname: UI/UX Developer\n---\n"
        "## Inputs\n"
        "- artifacts/requirements/requirements_spec.md\n"
        "- artifacts/requirements/requirements_spec.md, user_stories.md, acceptance_criteria.md,\n"
        "  non_functional_requirements.md, personas.md, business_process_flows.md\n"
        "## Outputs\n"
        "- artifacts/frontend/quality-report.md\n",
        encoding="utf-8",
    )

    for relative_path in [
        "artifacts/requirements/requirements_spec.md",
        "artifacts/requirements/user_stories.md",
        "artifacts/requirements/acceptance_criteria.md",
        "artifacts/requirements/non_functional_requirements.md",
        "artifacts/requirements/personas.md",
        "artifacts/requirements/business_process_flows.md",
    ]:
        path = tmp_path / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# content", encoding="utf-8")

    output_path = tmp_path / "artifacts" / "frontend" / "quality-report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("# quality report", encoding="utf-8")

    engine = ExecutionEngine(project_root=tmp_path)

    result = engine.execute_stage(
        stage_name="ui-ux-developer",
        input_artifacts={"requirements/requirements_spec": "# requirements"},
        specification="# spec",
    )

    assert result.success is True, result.error


def test_extract_artifacts_accepts_existing_directory_outputs(tmp_path):
    agent_dir = tmp_path / ".github" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "06-qa-engineer.agent.md").write_text(
        "---\nname: QA Engineer\n---\n"
        "## Outputs\n"
        "- artifacts/tests/unit/\n"
        "- artifacts/tests/coverage-matrix.md\n",
        encoding="utf-8",
    )

    directory_path = tmp_path / "artifacts" / "tests" / "unit"
    directory_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "artifacts" / "tests" / "coverage-matrix.md").parent.mkdir(
        parents=True, exist_ok=True
    )
    (tmp_path / "artifacts" / "tests" / "coverage-matrix.md").write_text(
        "# coverage", encoding="utf-8"
    )

    engine = ExecutionEngine(project_root=tmp_path)
    config = engine.get_stage_config("qa-engineer")
    assert config is not None

    artifacts, missing = engine._extract_artifacts("", "qa-engineer", config)

    assert "tests/unit" in artifacts
    assert missing == []


def test_execute_stage_fails_when_required_directory_output_is_missing(tmp_path):
    agent_dir = tmp_path / ".github" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "03-ui-ux-developer.agent.md").write_text(
        "---\nname: UI/UX Developer\n---\n"
        "## Inputs\n"
        "- artifacts/requirements/requirements_spec.md\n"
        "## Outputs\n"
        "- apps/frontend/src/pages\n",
        encoding="utf-8",
    )

    engine = ExecutionEngine(project_root=tmp_path)
    result = engine.execute_stage(
        stage_name="ui-ux-developer",
        input_artifacts={"requirements/requirements_spec": "# requirements"},
        specification="Design a task management dashboard view for the app.",
    )

    assert result.success is False
    assert "No output artifacts materialized" in result.error


def test_execute_stage_fails_when_required_file_output_is_missing(tmp_path):
    agent_dir = tmp_path / ".github" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "04-backend-developer.agent.md").write_text(
        "---\nname: Backend Developer\n---\n"
        "## Inputs\n"
        "- artifacts/requirements/requirements_spec.md\n"
        "## Outputs\n"
        "- artifacts/backend/backend-design.md\n",
        encoding="utf-8",
    )

    engine = ExecutionEngine(project_root=tmp_path)
    result = engine.execute_stage(
        stage_name="backend-developer",
        input_artifacts={"requirements/requirements_spec": "# requirements"},
        specification="Build a task management API for teams to create projects and assign work.",
    )

    assert result.success is False
    assert "No output artifacts materialized" in result.error


def test_execute_stage_preserves_existing_artifacts(tmp_path):
    agent_dir = tmp_path / ".github" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "01-business-analyst.agent.md").write_text(
        "---\nname: Business Analyst\n---\n"
        "## Inputs\n"
        "- artifacts/requirements/requirements_spec.md\n"
        "## Outputs\n"
        "- artifacts/requirements/user_stories.md\n",
        encoding="utf-8",
    )

    existing_path = tmp_path / "artifacts" / "requirements" / "user_stories.md"
    existing_path.parent.mkdir(parents=True, exist_ok=True)
    existing_path.write_text("# existing user stories\n", encoding="utf-8")

    engine = ExecutionEngine(project_root=tmp_path)
    result = engine.execute_stage(
        stage_name="business-analyst",
        input_artifacts={"requirements/requirements_spec": "# requirements"},
        specification="# spec",
    )

    assert result.success is True
    assert existing_path.exists()
    assert existing_path.read_text(encoding="utf-8") == "# existing user stories\n"


def test_build_stage_prompt_loads_prompt_template(tmp_path):
    agent_dir = tmp_path / "ai" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    prompt_dir = tmp_path / "ai" / "prompts" / "business-analyst"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    (prompt_dir / "v1.0.md").write_text(
        "# Prompt Content\n\nThis is the business analyst prompt template.\n",
        encoding="utf-8",
    )
    (agent_dir / "01-business-analyst.md").write_text(
        "---\nname: Business Analyst\nprompt_template: ai/prompts/business-analyst/v1.0.md\n---\n"
        "## Inputs\n- specification.md\n## Outputs\n- requirements_spec.md\n- user_stories.md\n",
        encoding="utf-8",
    )

    engine = ExecutionEngine(project_root=tmp_path)
    config = engine.get_stage_config("business-analyst")
    assert config is not None
    assert config.prompt_template == "ai/prompts/business-analyst/v1.0.md"

    prompt = engine._build_stage_prompt(
        stage_name="business-analyst",
        config=config,
        input_artifacts={"requirements/requirements_spec": "# requirements"},
        specification="# spec",
    )

    assert "# Prompt Content" in prompt
    assert "This is the business analyst prompt template." in prompt


def test_extract_section_bullets_ignores_unindented_text_after_list(tmp_path):
    agent_dir = tmp_path / "ai" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "01-business-analyst.md").write_text(
        "---\nname: Business Analyst\n---\n"
        "## Inputs\n"
        "- specification.md\n"
        "## Outputs\n"
        "- artifacts/requirements/quality_report.md\n"
        "- artifacts/requirements/handoff_contract.md\n"
        "- artifacts/requirements/openlog.md\n"
        "Do not create separate files for requirements fragments, use cases, business rules, or open questions — record those inside the artifacts above only. If no Figma/screenshots exist, keep `ui_observations.md` with concise business placeholders and no warnings.\n",
        encoding="utf-8",
    )

    engine = ExecutionEngine(project_root=tmp_path)
    config = engine.get_stage_config("business-analyst")
    assert config is not None
    assert "requirements/openlog" in config.output_artifacts
    assert all(
        not art.endswith(
            "openlog.md Do not create separate files for requirements fragments, use cases, business rules, or open questions — record those inside the artifacts above only. If no Figma/screenshots exist, keep `ui_observations.md` with concise business placeholders and no warnings."
        )
        for art in config.output_artifacts
    )
