"""
Core color processing for Figlet Forge.

This module provides precision color handling with ANSI escape sequence
generation, RGB color support, and color parsing utilities.

Design follows Eidosian principles:
- Function is form: each utility does exactly one thing perfectly
- Exhaustive but concise: complete color processing with minimal complexity
- Error prevention through design: strict type checking and validation
"""

import re
from typing import Dict, List, Tuple

from ..core.exceptions import InvalidColor

# Mapping of color names to ANSI color codes for foreground colors
COLOR_CODES: Dict[str, int] = {
    "BLACK": 30,
    "RED": 31,
    "GREEN": 32,
    "YELLOW": 33,
    "BLUE": 34,
    "MAGENTA": 35,
    "CYAN": 36,
    "LIGHT_GRAY": 37,
    "DEFAULT": 39,
    "DARK_GRAY": 90,
    "LIGHT_RED": 91,
    "LIGHT_GREEN": 92,
    "LIGHT_YELLOW": 93,
    "LIGHT_BLUE": 94,
    "LIGHT_MAGENTA": 95,
    "LIGHT_CYAN": 96,
    "WHITE": 97,
    "RESET": 0,
}

# RGB pattern for validation
RGB_PATTERN = re.compile(r"^(\d{1,3});(\d{1,3});(\d{1,3})$")


def color_to_ansi(color: str, isBackground: bool) -> str:
    """
    Convert a color name or RGB specification to an ANSI escape sequence.

    Args:
        color: Color name from COLOR_CODES or RGB values as "R;G;B"
        isBackground: Whether this is a background color

    Returns:
        ANSI escape sequence for the specified color

    Raises:
        InvalidColor: If the specified color is not valid
    """
    if not color:
        return ""

    color = color.upper()

    # Handle RGB color format (e.g., "255;0;0" for red)
    rgb_match = RGB_PATTERN.match(color)
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        if any(c < 0 or c > 255 for c in (r, g, b)):
            raise InvalidColor(f"RGB values must be between 0 and 255: {color}")
        # Use 24-bit color escape sequence
        color_type = 48 if isBackground else 38
        return f"\033[{color_type};2;{r};{g};{b}m"

    # Handle named colors
    if color in COLOR_CODES:
        ansiCode = COLOR_CODES[color]
        if isBackground and color != "RESET":
            ansiCode += 10  # Convert foreground code to background code
        return f"\033[{ansiCode}m"

    # Invalid color
    raise InvalidColor(f"Specified color '{color}' not found in ANSI COLOR_CODES list")


def parse_color(color: str) -> str:
    """
    Parse a color specification string into ANSI escape sequences.

    Format: "foreground:background" where either part can be empty

    Args:
        color: Color specification string (e.g., "RED:BLUE", "GREEN:", ":YELLOW")

    Returns:
        ANSI escape sequence for the specified colors

    Raises:
        InvalidColor: If any specified color is invalid
    """
    if not color or color == ":":
        return ""

    foreground, _, background = color.partition(":")

    # Generate ANSI sequences for foreground and background
    try:
        ansiForeground = color_to_ansi(foreground, False) if foreground else ""
        ansiBackground = color_to_ansi(background, True) if background else ""
        return ansiForeground + ansiBackground
    except InvalidColor as e:
        # Re-raise with more context
        raise InvalidColor(f"Invalid color in '{color}': {str(e)}")


def generate_gradient(
    start_color: Tuple[int, int, int], end_color: Tuple[int, int, int], steps: int
) -> List[Tuple[int, int, int]]:
    """
    Generate a gradient between two RGB colors.

    Args:
        start_color: Starting RGB color as (r, g, b)
        end_color: Ending RGB color as (r, g, b)
        steps: Number of colors to generate in the gradient

    Returns:
        List of RGB color tuples representing the gradient
    """
    if steps < 2:
        return [start_color]

    r1, g1, b1 = start_color
    r2, g2, b2 = end_color

    r_step = (r2 - r1) / (steps - 1)
    g_step = (g2 - g1) / (steps - 1)
    b_step = (b2 - b1) / (steps - 1)

    gradient = []
    for i in range(steps):
        r = int(r1 + r_step * i)
        g = int(g1 + g_step * i)
        b = int(b1 + b_step * i)
        gradient.append((r, g, b))

    return gradient


def rgb_from_name(color_name: str) -> Tuple[int, int, int]:
    """
    Convert a color name to RGB values.

    Args:
        color_name: Named color from COLOR_CODES

    Returns:
        RGB tuple (r, g, b)

    Raises:
        InvalidColor: If the color name is not recognized
    """
    # Common RGB values for standard ANSI colors
    rgb_map = {
        "BLACK": (0, 0, 0),
        "RED": (255, 0, 0),
        "GREEN": (0, 255, 0),
        "YELLOW": (255, 255, 0),
        "BLUE": (0, 0, 255),
        "MAGENTA": (255, 0, 255),
        "CYAN": (0, 255, 255),
        "WHITE": (255, 255, 255),
        "LIGHT_GRAY": (192, 192, 192),
        "DARK_GRAY": (128, 128, 128),
        "LIGHT_RED": (255, 128, 128),
        "LIGHT_GREEN": (128, 255, 128),
        "LIGHT_YELLOW": (255, 255, 128),
        "LIGHT_BLUE": (128, 128, 255),
        "LIGHT_MAGENTA": (255, 128, 255),
        "LIGHT_CYAN": (128, 255, 255),
        "DEFAULT": (192, 192, 192),  # Default to light gray
    }

    color_name = color_name.upper()
    if color_name in rgb_map:
        return rgb_map[color_name]

    raise InvalidColor(f"Unknown color name: {color_name}")
