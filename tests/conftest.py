# tests/conftest.py
"""
Shared test fixtures and configuration for Figlet Forge tests.
"""
import os
import sys
from typing import Any, Dict, List

import pytest

# Ensure we use the local version for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def sample_text() -> str:
    """Sample text for testing."""
    return "Hello World"


@pytest.fixture
def standard_fonts() -> List[str]:
    """List of standard fonts we expect to work consistently."""
    return ["standard", "slant", "small", "big"]


@pytest.fixture
def default_params() -> Dict[str, Any]:
    """Default rendering parameters."""
    return {"width": 80, "justify": "auto", "direction": "auto"}
