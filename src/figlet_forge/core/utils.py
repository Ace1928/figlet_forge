"""
Utility functions for Figlet Forge.

This module provides common utility functions shared across the codebase,
following the Eidosian principle of "Structure as Control" to prevent errors
through architecture.
"""

import os
import subprocess
import sys
from typing import Any, Dict, Optional, Tuple


def unicode_string(input_str: str) -> str:
    """
    Ensure proper handling of Unicode strings across Python versions.

    Args:
        input_str: Input string to process

    Returns:
        Properly encoded Unicode string
    """
    return str(input_str)


def safe_read_file(filepath: str) -> str:
    """
    Safely read a file with proper error handling.

    Args:
        filepath: Path to the file to read

    Returns:
        File contents as string

    Raises:
        FileNotFoundError: If the file does not exist
        PermissionError: If the file cannot be read
        UnicodeDecodeError: If the file cannot be decoded
    """
    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            return f.read()
    except UnicodeDecodeError:
        # Try again with latin-1 which can decode any byte sequence
        with open(filepath, encoding="latin-1") as f:
            return f.read()


def get_terminal_size() -> Tuple[int, int]:
    """
    Get the current terminal size with fallbacks for various environments.

    Returns:
        Tuple of (width, height) in characters
    """
    # Default fallback values
    default_size = (80, 24)

    # Try using shutil.get_terminal_size (Python 3.3+)
    try:
        import shutil

        size = shutil.get_terminal_size()
        return size.columns, size.lines
    except (ImportError, AttributeError):
        pass

    # Try environment variables
    try:
        return (
            int(os.environ.get("COLUMNS", default_size[0])),
            int(os.environ.get("LINES", default_size[1])),
        )
    except (ValueError, TypeError):
        pass

    # Final fallback
    return default_size


def normalize_path(path: str) -> str:
    """
    Normalize a file path for consistent handling across platforms.

    Args:
        path: File path to normalize

    Returns:
        Normalized path with consistent separators
    """
    return os.path.normpath(path)


def strip_ansi_codes(text: str) -> str:
    """
    Remove ANSI escape codes from a string.

    Useful for getting the plain text version of colored output.

    Args:
        text: String with possible ANSI codes

    Returns:
        String with all ANSI codes removed
    """
    import re

    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two dictionaries with dict2 values taking precedence.

    Args:
        dict1: Base dictionary
        dict2: Dictionary with override values

    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    result.update(dict2)
    return result


# Import needed for circular imports in a clean way
def lazy_import() -> Tuple[str, str, Any]:
    """Import Figlet-related components lazily to avoid circular imports.

    Returns:
        Tuple containing DEFAULT_FONT, RESET_COLORS, and Figlet class
    """
    from ..figlet import Figlet
    from ..version import DEFAULT_FONT, RESET_COLORS

    return DEFAULT_FONT, RESET_COLORS, Figlet


def figlet_format(text: str, font: Optional[str] = None, **kwargs: Any) -> str:
    """Format text in figlet style.

    Args:
        text: The text to render in figlet style
        font: Name of the figlet font to use
        **kwargs: Additional parameters passed to Figlet

    Returns:
        FigletString containing the rendered ASCII art
    """
    DEFAULT_FONT, _, Figlet = lazy_import()
    fig = Figlet(font=font or DEFAULT_FONT, **kwargs)
    return fig.renderText(text)


def print_figlet(
    text: str, font: Optional[str] = None, colors: str = ":", **kwargs: Any
) -> None:
    """Print figlet-formatted text to stdout with optional colors.

    This is a convenience function that creates a Figlet instance,
    renders the text, and prints it with specified colors.

    Args:
        text: The text to render in figlet style
        font: Name of the figlet font to use
        colors: Color specification string in "foreground:background" format
        **kwargs: Additional parameters passed to Figlet
    """
    DEFAULT_FONT, RESET_COLORS, _ = lazy_import()

    # Generate the figlet text
    result = figlet_format(text, font=font, **kwargs)

    # Apply colors if specified
    ansi_colors = None
    if colors and colors != ":":
        try:
            from ..color import parse_color

            ansi_colors = parse_color(colors)
            if ansi_colors:
                sys.stdout.write(ansi_colors)
        except ImportError:
            # Graceful fallback if color module not available
            pass

    # Print the result
    print(result)

    # Reset colors if needed
    if ansi_colors:
        sys.stdout.write(RESET_COLORS)
        sys.stdout.flush()


# Function to check if system unicode command is available
def has_unicode_command() -> bool:
    """Check if the system unicode command is available.

    Returns:
        True if the unicode command is available, False otherwise
    """
    try:
        result = subprocess.run(
            ["unicode", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.SubprocessError):
        return False
