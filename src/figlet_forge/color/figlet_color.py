"""
Color handling for Figlet Forge.

Provides utilities for ANSI color processing and application to FIGlet output.
Supports standard ANSI colors, 256-color mode, and true color (24-bit) terminals.
"""

import re
from typing import Dict, List, Tuple

from figlet_forge.core.exceptions import InvalidColor

# Define colors as strings rather than bytes for compatibility with sys.stdout.write()
COLOR_CODES: Dict[str, str] = {
    "BLACK": "30",
    "RED": "31",
    "GREEN": "32",
    "YELLOW": "33",
    "BLUE": "34",
    "MAGENTA": "35",
    "CYAN": "36",
    "WHITE": "37",
    "LIGHT_GRAY": "37",
    "DARK_GRAY": "90",
    "LIGHT_RED": "91",
    "LIGHT_GREEN": "92",
    "LIGHT_YELLOW": "93",
    "LIGHT_BLUE": "94",
    "LIGHT_MAGENTA": "95",
    "LIGHT_CYAN": "96",
    "RESET": "0",
}

# Reset sequence as a string, not bytes
RESET_COLORS: str = "\033[0m"

# RGB pattern for validation
RGB_PATTERN = re.compile(r"^(\d{1,3});(\d{1,3});(\d{1,3})$")


def color_to_ansi(color: str, is_background: bool = False) -> str:
    """Convert a color name or RGB value to ANSI color code.

    Args:
        color: Color name (e.g., 'RED') or RGB format (e.g., '255;0;0')
        is_background: If True, returns background color code

    Returns:
        ANSI color code as a string

    Raises:
        InvalidColor: If the specified color is not valid
    """
    # Special case for rainbow - handle it separately
    if color.upper() == "RAINBOW":
        return "RAINBOW"

    # Handle RGB format (e.g., '255;0;0')
    if ";" in color:
        match = RGB_PATTERN.match(color)
        if not match:
            raise InvalidColor(
                f"Invalid RGB format: '{color}' - use format 'R;G;B' with values 0-255"
            )

        try:
            r, g, b = map(int, color.split(";"))
            if not all(0 <= val <= 255 for val in (r, g, b)):
                raise InvalidColor(f"RGB values must be between 0-255: '{color}'")

            code_prefix = "48;2;" if is_background else "38;2;"
            return f"\033[{code_prefix}{r};{g};{b}m"
        except ValueError as e:
            raise InvalidColor(
                f"Invalid RGB format: '{color}' - use format 'R;G;B' with values 0-255"
            ) from e

    # Handle named colors
    color_upper = color.upper()
    if color_upper in COLOR_CODES:
        base = "4" if is_background else "3"
        return f"\033[{base}{COLOR_CODES[color_upper]}m"

    raise InvalidColor(
        f"Specified color '{color}' not found in ANSI COLOR_CODES list — "
        f"Use a valid color name or RGB format (e.g., RED or 255;0;0)"
    )


def parse_color(color: str) -> Tuple[str, str]:
    """Parse color specification string into foreground and background ANSI color codes.

    Args:
        color: Color specification string in format "foreground:background"

    Returns:
        Tuple of (foreground_code, background_code)

    Raises:
        InvalidColor: If the specified color is invalid
    """
    if not color:
        return ("", "")

    try:
        if color.lower() == "list":
            available_colors = ", ".join(sorted(COLOR_CODES.keys()))
            print(f"Available colors: {available_colors}")
            print("You can also use RGB values in format: R;G;B (e.g., 255;0;0)")
            print("Special value: RAINBOW - Creates rainbow-colored text")
            return ("", "")

        # Split foreground and background
        if ":" in color:
            foreground, background = color.split(":", 1)
        else:
            foreground, background = color, ""

        ansi_foreground = color_to_ansi(foreground, False) if foreground else ""
        ansi_background = color_to_ansi(background, True) if background else ""
        return (ansi_foreground, ansi_background)

    except InvalidColor as e:
        raise InvalidColor(f"Invalid color in '{color}': {str(e)}") from e
    except Exception as e:
        raise InvalidColor(f"Error parsing color '{color}': {str(e)}") from e


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

    gradient: List[Tuple[int, int, int]] = []
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
