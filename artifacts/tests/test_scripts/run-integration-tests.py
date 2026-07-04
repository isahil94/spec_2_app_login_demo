#!/usr/bin/env python3
"""Setup script for integration testing."""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_status(message: str, status: str = "info"):
    """Print colored status message."""
    if status == "success":
        print(f"{GREEN}✓ {message}{RESET}")
    elif status == "error":
        print(f"{RED}✗ {message}{RESET}")
    elif status == "warning":
        print(f"{YELLOW}⚠ {message}{RESET}")
    else:
        print(f"{BLUE}ℹ {message}{RESET}")


def check_backend(url: str = "http://localhost:8001/health", timeout: int = 10) -> bool:
    """Check if backend is running and healthy."""
    print_status(f"Checking backend at {url}...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    print_status("Backend is healthy", "success")
                    return True
        except requests.exceptions.RequestException:
            pass

        time.sleep(1)

    print_status("Backend is not responding. Please start the backend first.", "error")
    return False


def check_database(db_path: str = "apps/data/task_management.db") -> bool:
    """Check if database exists."""
    db_file = Path(db_path)
    if db_file.exists():
        size_mb = db_file.stat().st_size / (1024 * 1024)
        print_status(f"Database exists ({size_mb:.1f} MB)", "success")
        return True
    else:
        print_status(
            "Database does not exist yet (will be created on backend startup)",
            "warning",
        )
        return False


def seed_database() -> bool:
    """Seed the database with test data."""
    print_status("Seeding database with test data...")

    try:
        result = subprocess.run(
            [sys.executable, "artifacts/tests/test_scripts/seed_data.py"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            print_status("Database seeded successfully", "success")
            # Print credentials
            lines = result.stdout.split("\n")
            for line in lines:
                if "Email:" in line or "Password:" in line or "Role:" in line:
                    print(f"  {line}")
            return True
        else:
            print_status(f"Failed to seed database: {result.stderr}", "warning")
            return False
    except subprocess.TimeoutExpired:
        print_status("Database seeding timed out", "warning")
        return False
    except Exception as e:
        print_status(f"Error seeding database: {e}", "warning")
        return False


def check_frontend_setup(frontend_dir: str = "apps/frontend") -> bool:
    """Check if frontend dependencies are installed."""
    print_status("Checking frontend setup...")

    node_modules = Path(frontend_dir) / "node_modules"
    if node_modules.exists():
        print_status("Frontend dependencies are installed", "success")
        return True
    else:
        print_status("Frontend dependencies not installed", "warning")
        print_status("Install dependencies with: cd apps/frontend && npm install")
        return False


def run_tests(
    test_file: str = "persistence-integration.spec.ts",
    frontend_dir: str = "apps/frontend",
) -> bool:
    """Run the integration tests."""
    print_status(f"Running integration tests: {test_file}...")

    try:
        result = subprocess.run(
            ["npm", "test", "--", test_file],
            cwd=frontend_dir,
            timeout=300,  # 5 minute timeout
        )

        if result.returncode == 0:
            print_status("All tests passed!", "success")
            return True
        else:
            print_status("Some tests failed. Check output above.", "error")
            return False
    except subprocess.TimeoutExpired:
        print_status("Tests timed out", "error")
        return False
    except Exception as e:
        print_status(f"Error running tests: {e}", "error")
        return False


def main():
    """Main setup and test execution flow."""
    print(f"\n{BLUE}{'=' * 60}")
    print("Integration Testing Setup & Execution")
    print(f"{'=' * 60}{RESET}\n")

    # Step 1: Check backend
    print_status("Step 1: Checking backend...", "info")
    if not check_backend():
        print_status("\nPlease start the backend with:", "error")
        print("  cd apps/backend")
        print(
            "  .venv\\Scripts\\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8001"
        )
        return False

    # Step 2: Check/create database
    print_status("\nStep 2: Checking database...", "info")
    check_database()

    # Step 3: Optionally seed database
    print_status("\nStep 3: Database seeding", "info")
    try:
        response = requests.get("http://localhost:8001/api/v1/health")
        # Try to check if we have test data
        user_count = 0
        try:
            # This is a simple check - we'll assume if DB is empty, we should seed
            import sqlite3

            db_path = Path("apps/data/task_management.db")
            if db_path.exists():
                conn = sqlite3.connect(str(db_path))
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM users")
                user_count = cur.fetchone()[0]
                conn.close()
        except:
            user_count = 0

        if user_count == 0:
            print_status("No test data found. Seeding database...", "warning")
            seed_database()
        else:
            print_status(
                f"Database contains {user_count} users. Skipping seeding.", "success"
            )
    except:
        print_status("Could not check database state", "warning")

    # Step 4: Check frontend setup
    print_status("\nStep 4: Checking frontend setup...", "info")
    if not check_frontend_setup():
        print_status("Please install frontend dependencies:", "error")
        print("  cd apps/frontend && npm install")
        return False

    # Step 5: Run tests
    print(f"\n{BLUE}{'=' * 60}")
    print("Running Integration Tests")
    print(f"{'=' * 60}{RESET}\n")

    test_file = "persistence-integration.spec.ts"
    success = run_tests(test_file)

    # Summary
    print(f"\n{BLUE}{'=' * 60}")
    if success:
        print_status("Integration testing completed successfully!", "success")
    else:
        print_status("Integration testing had failures. See output above.", "error")
    print(f"{'=' * 60}{RESET}\n")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
