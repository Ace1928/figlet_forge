# tests/conftest.py
"""
Shared test configuration and fixtures for Figlet Forge.

This module provides fixtures and utilities that can be reused across
all test suites, following Eidosian principles of recursive optimization
and structural integrity.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Generator, List, Tuple

import pytest

# Ensure package can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import constants only after path setup

# Test data constants
TEST_TEXT = "Hello, Figlet!"
TEST_UNICODE_TEXT = "Hello 世界"
STANDARD_FONTS = ["standard", "slant", "small", "big", "mini"]
TEST_COLORS = ["RED", "GREEN", "BLUE", "YELLOW", "CYAN", "MAGENTA"]


@pytest.fixture
def test_text() -> str:
    """Provide standard test text."""
    return TEST_TEXT


@pytest.fixture
def test_unicode_text() -> str:
    """Provide Unicode test text."""
    return TEST_UNICODE_TEXT


@pytest.fixture
def standard_fonts() -> List[str]:
    """Provide a list of standard fonts that should be available."""
    return STANDARD_FONTS


@pytest.fixture
def temp_file_path(tmp_path: Path) -> Generator[Path, None, None]:
    """
    Provide a temporary file path for testing file operations.

    Args:
        tmp_path: Pytest's built-in temporary directory fixture

    Yields:
        A Path object pointing to a temporary file
    """
    temp_file = tmp_path / "test_output.txt"
    yield temp_file
    # Cleanup if file exists
    if temp_file.exists():
        temp_file.unlink()


@pytest.fixture
def captured_output() -> Generator[Tuple[List[str], List[str]], None, None]:
    """
    Capture stdout and stderr for testing.

    Yields:
        Tuple containing lists of captured stdout and stderr lines
    """
    import io
    from contextlib import redirect_stderr, redirect_stdout

    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
        yield stdout_capture, stderr_capture


@pytest.fixture
def figlet_factory():
    """
    Provide a factory function to create Figlet instances with specified parameters.

    Returns:
        Function that creates Figlet instances
    """
    from figlet_forge import Figlet

    def _create_figlet(**kwargs):
        """Create a Figlet instance with specified parameters."""
        return Figlet(**kwargs)

    return _create_figlet


@pytest.fixture
def mock_env_vars() -> Generator[Dict[str, str], None, None]:
    """
    Temporarily modify environment variables for testing.

    Yields:
        Dictionary to store original environment variables
    """
    original_vars = {}

    # Save any environment variables we'll modify
    for var in ["COLUMNS", "LINES"]:
        if var in os.environ:
            original_vars[var] = os.environ[var]

    try:
        yield original_vars
    finally:
        # Restore original environment variables
        for var, value in original_vars.items():
            os.environ[var] = value

        # Remove any variables we added but weren't there originally
        for var in ["COLUMNS", "LINES"]:
            if var not in original_vars and var in os.environ:
                del os.environ[var]


@pytest.fixture
def sample_figlet_string():
    """Provide a sample FigletString for testing transformations."""
    from figlet_forge.core.figlet_string import FigletString

    ascii_art = """
  ___ ___ ___
 | _ \_ _/ __|
 |  _/| | (_ |
 |_| |___\___|
"""
    return FigletString(ascii_art.strip())
