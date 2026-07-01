"""Pytest configuration and fixtures."""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def temp_workspace(tmp_path):
    """Provide temporary workspace for tests."""
    return tmp_path


@pytest.fixture
def sample_specification():
    """Provide sample specification for testing."""
    return {
        "title": "Test Application",
        "description": "A test application for validation",
        "features": [
            "Authentication",
            "Dashboard",
            "Notifications"
        ]
    }


def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
