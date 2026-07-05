from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any, Dict, Iterable


def _format_status(value: str | None) -> str:
    status = (value or "unknown").strip().lower()
    if status in {"passed", "pass", "success", "ok"}:
        return "PASSED"
    if status in {"failed", "fail", "error", "broken"}:
        return "FAILED"
    if status in {"skipped", "skip", "not_run", "not_tested"}:
        return "SKIPPED"
    return status.upper() if status else "UNKNOWN"


def _render_test_cases(test_cases: Iterable[Dict[str, Any]]) -> str:
    rows = []
    for case in test_cases:
        name = escape(str(case.get("name", "Unnamed test")))
        status = _format_status(case.get("status"))
        details = escape(str(case.get("details", "")))
        rows.append(f"<tr><td>{name}</td><td>{status}</td><td>{details}</td></tr>")
    return "".join(rows) or "<tr><td colspan=3>No test cases recorded.</td></tr>"


def save_html_report(
    results: Dict[str, Any], output_path: str | Path | None = None
) -> Path:
    """Create a standalone HTML summary from structured test results."""
    if output_path is None:
        output_path = Path("artifacts/tests/qa-report.html")
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    summary_rows = []
    total = 0
    passed = 0
    failed = 0
    skipped = 0

    for suite_name, suite_result in results.items():
        total += 1
        status = _format_status(suite_result.get("status"))
        if status == "PASSED":
            passed += 1
        elif status == "FAILED":
            failed += 1
        elif status == "SKIPPED":
            skipped += 1

        suite_label = escape(str(suite_name))
        command = escape(str(suite_result.get("command", "")))
        exit_code = escape(str(suite_result.get("exit_code", "")))
        duration = escape(str(suite_result.get("duration_sec", "")))
        summary_rows.append(
            "<tr>"
            f"<td>{suite_label}</td><td>{status}</td><td>{command}</td>"
            f"<td>{exit_code}</td><td>{duration}</td>"
            "</tr>"
        )

    html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>QA Test Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; color: #1f2937; }}
    h1, h2 {{ color: #111827; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; }}
    th, td {{ border: 1px solid #d1d5db; padding: 0.6rem; text-align: left; }}
    th {{ background: #f3f4f6; }}
    .summary {{ display: flex; gap: 1rem; flex-wrap: wrap; margin: 1rem 0; }}
    .card {{ border: 1px solid #d1d5db; border-radius: 6px; padding: 0.75rem 1rem; min-width: 140px; }}
  </style>
</head>
<body>
  <h1>QA Test Report</h1>
  <p>Generated: {generated_at}</p>
  <div class=\"summary\">
    <div class=\"card\"><strong>Total Suites:</strong> {total}</div>
    <div class=\"card\"><strong>Passed:</strong> {passed}</div>
    <div class=\"card\"><strong>Failed:</strong> {failed}</div>
    <div class=\"card\"><strong>Skipped:</strong> {skipped}</div>
  </div>

  <h2>Suite Summary</h2>
  <table>
    <thead>
      <tr><th>Suite</th><th>Status</th><th>Command</th><th>Exit Code</th><th>Duration (s)</th></tr>
    </thead>
    <tbody>
      {''.join(summary_rows)}
    </tbody>
  </table>

  <h2>Detailed Test Cases</h2>
  <table>
    <thead>
      <tr><th>Test Case</th><th>Status</th><th>Details</th></tr>
    </thead>
    <tbody>
      {''.join(_render_test_cases(_collect_test_cases(results)))}
    </tbody>
  </table>
</body>
</html>
"""
    output_path.write_text(html, encoding="utf-8")
    return output_path


def _collect_test_cases(results: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    collected = []
    for suite_result in results.values():
        test_cases = suite_result.get("test_cases") or []
        if isinstance(test_cases, list):
            collected.extend(test_cases)
    return collected
