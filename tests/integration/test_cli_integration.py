"""
Integration tests for the Figlet Forge CLI.

These tests verify that the CLI functions correctly as a whole,
handling arguments, input/output, and integration with the core library.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import pytest

# Get the path to the CLI script
CLI_SCRIPT = str(Path(__file__).parent.parent.parent / "tools" / "figlet_forge")
if not os.path.exists(CLI_SCRIPT):
    CLI_SCRIPT = "figlet_forge"  # Fall back to installed command


def run_cli(args: List[str], input_text: Optional[str] = None) -> Tuple[str, str, int]:
    """
    Run the figlet_forge CLI with given arguments and input.

    Args:
        args: Command line arguments
        input_text: Optional text to pass via stdin

    Returns:
        Tuple of (stdout, stderr, return_code)
    """
    # Prepare the command
    cmd = [sys.executable, "-m", "figlet_forge.cli.main"] + args

    # Set up the process
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Send input if provided
    if input_text is not None:
        stdout, stderr = proc.communicate(input_text)
    else:
        stdout, stderr = proc.communicate()

    return stdout, stderr, proc.returncode


@pytest.mark.parametrize(
    "args,expected_success,expected_output_contains",
    [
        (["test"], True, "test"),  # Basic text rendering
        (["--font=standard", "A"], True, "A"),  # Font option
        (["--width=40", "test"], True, ""),  # Width option
        (["--color=RED", "test"], True, "\033["),  # Color option
        (["--list-fonts"], True, "standard"),  # List fonts
        (["--invalid-option"], False, "error"),  # Invalid option
    ],
)
def test_cli_arguments(
    args: List[str], expected_success: bool, expected_output_contains: str
) -> None:
    """
    Test CLI argument handling.

    Args:
        args: Arguments to pass to CLI
        expected_success: Whether command should succeed
        expected_output_contains: String expected in output
    """
    stdout, stderr, return_code = run_cli(args)

    # Check return code
    if expected_success:
        assert return_code == 0, f"CLI failed with: {stderr}"
    else:
        assert return_code != 0, "CLI unexpectedly succeeded"

    # Check output
    if expected_output_contains:
        combined_output = stdout + stderr
        assert expected_output_contains in combined_output


def test_stdin_input() -> None:
    """Test reading input from stdin."""
    test_input = "from stdin"
    stdout, _, return_code = run_cli([], input_text=test_input)

    assert return_code == 0, "CLI failed"
    assert stdout.strip(), "No output generated"
    # Input should be reflected in output somehow
    flatten_output = "".join(stdout.replace(" ", "").replace("\n", "").lower())
    assert "stdin" in flatten_output


def test_output_to_file(tmp_path: Path) -> None:
    """
    Test writing output to a file.

    Args:
        tmp_path: Pytest's built-in temporary directory fixture
    """
    output_file = tmp_path / "output.txt"
    stdout, stderr, return_code = run_cli(["--output", str(output_file), "test output"])

    # Command should succeed
    assert return_code == 0, f"CLI failed with: {stderr}"

    # Output file should exist and contain content
    assert output_file.exists(), "Output file was not created"
    content = output_file.read_text()
    assert content.strip(), "Output file is empty"


def test_color_options() -> None:
    """Test various color options."""
    # Test with named color
    stdout, _, _ = run_cli(["--color=BLUE", "C"])
    assert "\033[" in stdout, "ANSI color codes not found in output"

    # Test with RGB color
    stdout, _, _ = run_cli(["--color=255;0;0", "C"])
    assert "\033[38;2;" in stdout, "RGB color codes not found in output"

    # Test with foreground:background format
    stdout, _, _ = run_cli(["--color=RED:BLUE", "C"])
    assert "\033[" in stdout, "ANSI color codes not found in output"


def test_transform_options() -> None:
    """Test text transformation options."""
    # Get baseline output
    base_stdout, _, _ = run_cli(["AB"])

    # Test with reverse option
    rev_stdout, _, _ = run_cli(["--reverse", "AB"])
    assert rev_stdout != base_stdout, "Reverse had no effect"

    # Test with flip option
    flip_stdout, _, _ = run_cli(["--flip", "AB"])
    assert flip_stdout != base_stdout, "Flip had no effect"

    # Test combined transforms
    combined_stdout, _, _ = run_cli(["--reverse", "--flip", "AB"])
    assert combined_stdout != base_stdout, "Combined transforms had no effect"
    assert combined_stdout != rev_stdout, "Combined transforms same as just reverse"
    assert combined_stdout != flip_stdout, "Combined transforms same as just flip"


def test_help_option() -> None:
    """Test help option displays usage information."""
    stdout, _, return_code = run_cli(["--help"])

    assert return_code == 0, "Help command failed"
    assert "usage:" in stdout.lower(), "Help output missing usage section"
    assert "options:" in stdout.lower(), "Help output missing options section"


def test_version_option() -> None:
    """Test version option displays version."""
    stdout, _, return_code = run_cli(["--version"])

    assert return_code == 0, "Version command failed"
    assert "version" in stdout.lower(), "Version info not displayed"
