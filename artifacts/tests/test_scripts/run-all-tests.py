#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Master test runner for all QA tests (unit, integration, E2E, backend)."""

import subprocess
import sys
from enum import Enum
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from artifacts.tests.generate_html_report import save_html_report

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


class TestType(Enum):
    """Test types available."""

    UNIT_BACKEND = "unit_backend"
    PERSISTENCE_E2E = "persistence_e2e"
    FRONTEND_E2E = "frontend_e2e"
    INTEGRATION = "integration"
    ALL = "all"


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}{text.center(70)}{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}\n")


def print_status(msg: str, status: str = "info"):
    """Print colored status."""
    if status == "success":
        print(f"{GREEN}✓ {msg}{RESET}")
    elif status == "error":
        print(f"{RED}✗ {msg}{RESET}")
    elif status == "warning":
        print(f"{YELLOW}⚠ {msg}{RESET}")
    else:
        print(f"{BLUE}ℹ {msg}{RESET}")


def run_backend_unit_tests():
    """Run Python backend unit tests."""
    print_header("Backend Unit Tests")

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "artifacts/tests/test_scripts/backend_tests/unit",
                "-v",
                "--tb=short",
            ],
            timeout=300,
        )
        if result.returncode == 0:
            print_status("Backend unit tests PASSED", "success")
            return True
        else:
            print_status("Backend unit tests FAILED", "error")
            return False
    except subprocess.TimeoutExpired:
        print_status("Backend unit tests TIMEOUT", "error")
        return False
    except Exception as e:
        print_status(f"Backend unit tests ERROR: {e}", "error")
        return False


def run_persistence_e2e_tests():
    """Run persistence E2E tests."""
    print_header("Persistence End-to-End Tests (Database Persistence)")

    try:
        # Check backend health first
        import requests

        try:
            response = requests.get("http://localhost:8001/health", timeout=5)
            if response.status_code != 200:
                print_status("Backend is not healthy", "error")
                return False
            print_status("Backend is healthy", "success")
        except:
            print_status("Backend is not responding", "error")
            return False

        # Run persistence integration tests from test_scripts directory
        result = subprocess.run(
            "npm test -- persistence-integration.spec.ts",
            cwd="artifacts/tests/test_scripts",
            shell=True,
            timeout=600,
        )

        # Print report location
        print_status(
            "HTML Chromium report saved to: artifacts/tests/test_scripts/test-results/html-report/index.html",
            "success",
        )

        if result.returncode == 0:
            print_status("Persistence E2E tests PASSED", "success")
            return True
        else:
            print_status("Persistence E2E tests FAILED", "error")
            return False
    except subprocess.TimeoutExpired:
        print_status("Persistence E2E tests TIMEOUT", "error")
        return False
    except Exception as e:
        print_status(f"Persistence E2E tests ERROR: {e}", "error")
        return False


def run_frontend_e2e_tests():
    """Run all frontend E2E tests (excluding persistence tests handled separately)."""
    print_header("Frontend End-to-End Tests")

    try:
        # Run all E2E tests - report is auto-saved with open: 'never' in config
        result = subprocess.run(
            "npm test",
            cwd="artifacts/tests/test_scripts",
            shell=True,
            timeout=600,
            capture_output=False,  # Show output but don't block on interactive server
        )

        # Print report location
        print_status(
            "HTML Chromium report saved to: artifacts/tests/test_scripts/test-results/html-report/index.html",
            "success",
        )

        if result.returncode == 0:
            print_status("Frontend E2E tests PASSED", "success")
            return True
        else:
            print_status("Frontend E2E tests FAILED (check output above)", "error")
            return False
    except subprocess.TimeoutExpired:
        print_status("Frontend E2E tests TIMEOUT", "error")
        return False
    except Exception as e:
        print_status(f"Frontend E2E tests ERROR: {e}", "error")
        return False


def run_all_tests():
    """Run all tests."""
    print_header("Running ALL Tests")

    results = {}

    # Backend unit tests
    print_status("Starting backend unit tests...", "info")
    results["backend_unit"] = run_backend_unit_tests()

    # Persistence E2E tests
    print_status("Starting persistence E2E tests...", "info")
    results["persistence_e2e"] = run_persistence_e2e_tests()

    # Frontend E2E tests
    print_status("Starting frontend E2E tests...", "info")
    results["frontend_e2e"] = run_frontend_e2e_tests()

    report_output = Path("artifacts/tests/qa-report.html")
    save_html_report(
        {
            suite_name: {
                "status": "passed" if result else "failed",
                "command": suite_name,
                "exit_code": 0 if result else 1,
                "duration_sec": None,
                "test_cases": [],
            }
            for suite_name, result in results.items()
        },
        report_output,
    )
    print_status(f"HTML report written to {report_output}", "success")

    return results


def print_summary(results):
    """Print test summary."""
    print_header("Test Execution Summary")

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed

    for test_name, result in results.items():
        status = "PASSED" if result else "FAILED"
        color = GREEN if result else RED
        print(f"  {color}{test_name.replace('_', ' ').title()}: {status}{RESET}")

    print()
    print(
        f"Total: {total} | {GREEN}Passed: {passed}{RESET} | {RED}Failed: {failed}{RESET}"
    )

    if failed == 0:
        print_status("All tests passed!", "success")
        return True
    else:
        print_status(f"{failed} test suite(s) failed", "error")
        return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Master test runner for all QA tests",
        epilog="Examples:\n"
        "  python run-all-tests.py --unit           # Backend unit tests only\n"
        "  python run-all-tests.py --persistence    # Persistence E2E tests only\n"
        "  python run-all-tests.py --frontend       # Frontend E2E tests only\n"
        "  python run-all-tests.py --all            # All tests\n"
        "  python run-all-tests.py                  # All tests (default)",
    )

    parser.add_argument("--unit", action="store_true", help="Run backend unit tests")
    parser.add_argument(
        "--persistence", action="store_true", help="Run persistence E2E tests"
    )
    parser.add_argument(
        "--frontend", action="store_true", help="Run frontend E2E tests"
    )
    parser.add_argument("--all", action="store_true", help="Run all tests")

    args = parser.parse_args()

    # Default to all if nothing specified
    if not any([args.unit, args.persistence, args.frontend, args.all]):
        args.all = True

    results = {}

    if args.all:
        results = run_all_tests()
    else:
        if args.unit:
            results["backend_unit"] = run_backend_unit_tests()
        if args.persistence:
            results["persistence_e2e"] = run_persistence_e2e_tests()
        if args.frontend:
            results["frontend_e2e"] = run_frontend_e2e_tests()

    success = print_summary(results)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
