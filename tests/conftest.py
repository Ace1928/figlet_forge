# tests/conftest.py
"""
Pytest configuration for Figlet Forge tests.

This module provides fixtures and configuration for pytest-based testing,
enabling more advanced test scenarios and better test organization.
"""

import os
import random
import string
import tempfile
from pathlib import Path

import pytest

from figlet_forge import Figlet

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


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def temp_font_file(temp_dir):
    """Create a simple valid FIGlet font file for testing."""
    # Minimal valid .flf file content
    font_content = (
        "flf2a$ 5 4 8 -1 14 0 0 0\n"  # Header
        "Font Author\n"  # Comment line
        "Minimal test font for Figlet Forge\n"  # Comment line
        "@\n"  # Comment line
        "@\n"  # Comment line
        "@\n"  # Comment line
        "@\n"  # Comment line
        "@\n"  # Comment line
        "@\n"  # Comment line
        "@\n"  # Comment line
        "@\n"  # Comment line
        "@\n"  # Comment line
        "@\n"  # Comment line
        "@\n"  # Comment line
        "@\n"  # Comment line
        "@\n"  # Comment line
        "@\n"  # Comment line
        " $@\n"  # Space (32)
        "!$@\n"  # ! (33)
        '"$@\n'  # " (34)
        "#$@\n"  # # (35)
    )

    # Complete the font with basic characters
    for i in range(36, 127):
        char = chr(i)
        font_content += f"{char}$@\n"  # Each character with end marker

    # Write the font to a file
    font_path = temp_dir / "test_font.flf"
    with open(font_path, "w") as f:
        f.write(font_content)

    return font_path


@pytest.fixture
def figlet_instance():
    """Create a Figlet instance with standard font."""
    return Figlet(font="standard")


@pytest.fixture
def random_text():
    """Generate random text for testing."""
    length = random.randint(5, 20)
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


@pytest.fixture
def capture_output(monkeypatch):
    """Capture stdout output for testing CLI functions."""
    from io import StringIO

    output = StringIO()
    monkeypatch.setattr("sys.stdout", output)
    return output
