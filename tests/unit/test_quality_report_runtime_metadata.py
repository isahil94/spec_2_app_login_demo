from orchestration.workflow.quality_report import render_quality_report_template


def test_render_quality_report_template_uses_runtime_metadata():
    template = """
# Quality Report

## AI Usage Summary
| Field | Value |
|---|---|
| Workflow ID | [workflow_id] |
| Correlation ID | [correlation_id] |
| Agent Name | [agent_name] |
| Stage Name | [stage_name] |
| Session ID | [session_id or N/A] |
| Start Time | [start_time] |
| End Time | [end_time] |
| Duration | [duration] |
| Input Tokens | [input_tokens] |
| Output Tokens | [output_tokens] |
| Total Tokens | [total_tokens] |
| Estimated Cost | [estimated_cost] |
"""

    metadata = {
        "workflow_id": "WF-123",
        "correlation_id": "CORR-456",
        "agent_name": "Business Analyst",
        "stage_name": "Requirements Analysis",
        "session_id": "session-001",
        "start_time": "2026-07-02T10:00:00Z",
        "end_time": "2026-07-02T10:00:05Z",
        "duration": "5 seconds",
        "input_tokens": 120,
        "output_tokens": 80,
        "total_tokens": 200,
        "estimated_cost": "$0.02",
    }

    rendered = render_quality_report_template(template, metadata=metadata)

    assert "WF-123" in rendered
    assert "CORR-456" in rendered
    assert "Business Analyst" in rendered
    assert "Requirements Analysis" in rendered
    assert "session-001" in rendered
    assert "2026-07-02T10:00:00Z" in rendered
    assert "5 seconds" in rendered
    assert "120" in rendered
    assert "$0.02" in rendered


def test_render_quality_report_template_falls_back_without_workflow_metadata():
    template = """
| Workflow ID | [workflow_id] |
| Correlation ID | [correlation_id] |
| Session ID | [session_id or N/A] |
| Start Time | [start_time] |
| End Time | [end_time] |
| Duration | [duration] |
| Total Tokens | [total_tokens] |
| Estimated Cost | [estimated_cost] |
"""

    rendered = render_quality_report_template(template)

    assert "WF-" in rendered
    assert "CORR-" in rendered
    assert "N/A" in rendered
    assert "T" in rendered
    assert "seconds" in rendered
    assert "$0.00" in rendered
