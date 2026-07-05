import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from artifacts.tests.generate_html_report import save_html_report


def test_save_html_report_writes_summary_and_case_details(tmp_path):
    results = {
        "backend_unit": {
            "status": "passed",
            "command": "pytest -q",
            "exit_code": 0,
            "duration_sec": 12.5,
            "test_cases": [{"name": "test_login", "status": "passed"}],
        }
    }

    report_path = tmp_path / "qa-report.html"
    generated_path = save_html_report(results, report_path)

    assert generated_path == report_path
    html_text = report_path.read_text(encoding="utf-8")
    assert "QA Test Report" in html_text
    assert "backend_unit" in html_text
    assert "test_login" in html_text
    assert "PASSED" in html_text
