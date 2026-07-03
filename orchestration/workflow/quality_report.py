"""Helpers for rendering quality reports from runtime metadata."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Dict, Optional

DEFAULT_METADATA = {
    "workflow_id": "WF-unknown",
    "correlation_id": "CORR-unknown",
    "agent_name": "unknown",
    "stage_name": "unknown",
    "session_id": "N/A",
    "start_time": "N/A",
    "end_time": "N/A",
    "duration": "N/A",
    "input_tokens": "N/A",
    "output_tokens": "N/A",
    "total_tokens": "N/A",
    "estimated_cost": "$0.00",
    "retry_count": 0,
    "status": "unknown",
    "blocking_reason": "None",
}


def _coerce_value(raw_value: Any) -> str:
    if raw_value is None:
        return "N/A"
    if isinstance(raw_value, (int, float)):
        return str(raw_value)
    if isinstance(raw_value, datetime):
        return raw_value.isoformat()
    return str(raw_value)


def _build_fallback_metadata() -> Dict[str, Any]:
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        **DEFAULT_METADATA,
        "start_time": now,
        "end_time": now,
        "duration": "0 seconds",
        "workflow_id": "WF-unknown",
        "correlation_id": "CORR-unknown",
    }


def render_quality_report_template(
    template_text: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """Replace placeholder tokens in a quality report template with runtime data."""
    effective_metadata = _build_fallback_metadata()
    if metadata:
        effective_metadata.update(metadata)

    replacements = {
        "workflow_id": effective_metadata.get("workflow_id", DEFAULT_METADATA["workflow_id"]),
        "correlation_id": effective_metadata.get("correlation_id", DEFAULT_METADATA["correlation_id"]),
        "agent_name": effective_metadata.get("agent_name", DEFAULT_METADATA["agent_name"]),
        "stage_name": effective_metadata.get("stage_name", DEFAULT_METADATA["stage_name"]),
        "session_id": effective_metadata.get("session_id", DEFAULT_METADATA["session_id"]),
        "start_time": effective_metadata.get("start_time", DEFAULT_METADATA["start_time"]),
        "end_time": effective_metadata.get("end_time", DEFAULT_METADATA["end_time"]),
        "duration": effective_metadata.get("duration", DEFAULT_METADATA["duration"]),
        "input_tokens": effective_metadata.get("input_tokens", DEFAULT_METADATA["input_tokens"]),
        "output_tokens": effective_metadata.get("output_tokens", DEFAULT_METADATA["output_tokens"]),
        "total_tokens": effective_metadata.get("total_tokens", DEFAULT_METADATA["total_tokens"]),
        "estimated_cost": effective_metadata.get("estimated_cost", DEFAULT_METADATA["estimated_cost"]),
        "retry_count": effective_metadata.get("retry_count", DEFAULT_METADATA["retry_count"]),
        "status": effective_metadata.get("status", DEFAULT_METADATA["status"]),
        "blocking_reason": effective_metadata.get("blocking_reason", DEFAULT_METADATA["blocking_reason"]),
    }

    rendered = template_text
    for key, value in replacements.items():
        rendered = rendered.replace(f"[{key}]", _coerce_value(value))
        rendered = rendered.replace(f"[{key} or N/A]", _coerce_value(value))
        rendered = rendered.replace(f"[{key} or reason]", _coerce_value(value))
        rendered = rendered.replace(f"[completed | failed | blocked | partial]", _coerce_value(replacements["status"]))
        rendered = rendered.replace(f"[none or reason]", _coerce_value(replacements["blocking_reason"]))

    rendered = re.sub(r"\[.*?\]", "N/A", rendered)
    return rendered
