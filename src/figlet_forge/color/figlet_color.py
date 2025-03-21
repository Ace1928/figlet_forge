"""
Color support for Figlet Forge.

This module provides color parsing and processing functionality for
creating colorized ASCII art output with ANSI escape sequences.
"""

import random
import re
from typing import Optional, Tuple

from ..core.exceptions import InvalidColor
from ..version import COLOR_CODES, RESET_COLORS


class ColorMode:
    """
    Enum-like class for color modes.

    Attributes:
        NONE: No coloring
        FOREGROUND: Foreground coloring only
        BACKGROUND: Background coloring only
        FULL: Both foreground and background coloring
    """

    NONE = 0
    FOREGROUND = 1
    BACKGROUND = 2
    FULL = 3


class ColorScheme:
    """
    Represents a color scheme with foreground and background.

    This class encapsulates a color combination and provides methods
    to apply it to text.

    Attributes:
        foreground: ANSI escape sequence for foreground color
        background: ANSI escape sequence for background color
        name: Optional name for the color scheme
    """

    def __init__(
        self, foreground: str = "", background: str = "", name: Optional[str] = None
    ):
        """
        Initialize a ColorScheme.

        Args:
            foreground: ANSI escape sequence or color name for foreground
            background: ANSI escape sequence or color name for background
            name: Optional name for the color scheme
        """
        self.foreground = foreground
        self.background = background
        self.name = name
        self._mode = self._determine_mode()

    def _determine_mode(self) -> int:
        """
        Determine the color mode based on foreground and background.

        Returns:
            ColorMode value
        """
        if self.foreground and self.background:
            return ColorMode.FULL
        elif self.foreground:
            return ColorMode.FOREGROUND
        elif self.background:
            return ColorMode.BACKGROUND
        else:
            return ColorMode.NONE

    def apply(self, text: str) -> str:
        """
        Apply the color scheme to text.

        Args:
            text: Text to colorize

        Returns:
            Colorized text with ANSI escape sequences
        """
        if self._mode == ColorMode.NONE:
            return text

        # Apply colors and reset at the end
        return f"{self.foreground}{self.background}{text}{RESET_COLORS}"

    @classmethod
    def from_string(cls, color_spec: str) -> "ColorScheme":
        """
        Create a ColorScheme from a color specification string.

        Args:
            color_spec: Color specification (e.g., "RED:BLUE", "RED", "255;0;0:0;0;255")

        Returns:
            ColorScheme instance

        Raises:
            InvalidColor: If the color specification is invalid
        """
        fg, bg = parse_color(color_spec)
        return cls(fg, bg, name=color_spec)


def parse_color(color_spec: str) -> Tuple[str, str]:
    """
    Parse a color specification string into foreground and background ANSI codes.

    Args:
        color_spec: Color specification (e.g., "RED:BLUE", "RED", "255;0;0:0;0;255")

    Returns:
        Tuple of (foreground_ansi_code, background_ansi_code)

    Raises:
        InvalidColor: If the color specification is invalid
    """
    if not color_spec or color_spec == ":":
        return "", ""

    # Special case for random colors
    if color_spec.upper() == "RANDOM":
        fg_color = random.choice(list(COLOR_CODES.keys()))
        bg_color = ""
        return f"\033[{COLOR_CODES[fg_color]}m", ""

    # Special case for rainbow (handled differently in effects module)
    if color_spec.upper() == "RAINBOW":
        return "RAINBOW", ""

    # Check if we have a gradient specification
    if color_spec.upper().startswith("GRADIENT:"):
        # This will be handled by the effects module
        return color_spec.upper(), ""

    # Split into foreground and background
    parts = color_spec.split(":", 1)
    fg_part = parts[0]
    bg_part = parts[1] if len(parts) > 1 else ""

    # Process foreground color
    fg_code = ""
    if fg_part:
        fg_code = _process_color_part(fg_part, is_background=False)

    # Process background color
    bg_code = ""
    if bg_part:
        bg_code = _process_color_part(bg_part, is_background=True)

    return fg_code, bg_code


def color_to_ansi(color_part: str, is_background: bool = False) -> str:
    """
    Convert a color name or RGB value to an ANSI escape code.

    Args:
        color_part: Color specification (e.g., "RED", "255;0;0")
        is_background: Whether this is for background color

    Returns:
        ANSI escape code for the specified color

    Raises:
        InvalidColor: If the color specification is invalid
    """
    # Use the existing _process_color_part function
    return _process_color_part(color_part, is_background)


def _process_color_part(color_part: str, is_background: bool = False) -> str:
    """
    Process a color specification part into an ANSI escape code.

    Args:
        color_part: Color specification part (e.g., "RED", "255;0;0")
        is_background: Whether this is for background color

    Returns:
        ANSI escape code

    Raises:
        InvalidColor: If the color specification is invalid
    """
    # Empty part
    if not color_part:
        return ""

    # Base code for foreground or background
    base = "4" if is_background else "3"
    bright_base = "10" if is_background else "9"

    # Named color
    upper_color = color_part.upper()
    if upper_color in COLOR_CODES:
        code = COLOR_CODES[upper_color]
        # If the code starts with 9, it's a bright color
        if code.startswith("9") and is_background:
            # Convert bright foreground to bright background
            code = "10" + code[1:]
        return f"\033[{code}m"

    # Check if it's a bright color variant
    if upper_color.startswith("BRIGHT_") and upper_color[7:] in COLOR_CODES:
        base_color = upper_color[7:]
        if base_color in COLOR_CODES:
            # Get the non-bright code and convert it to bright
            code = COLOR_CODES[base_color]
            if code.startswith("3"):  # Regular foreground
                code = "9" + code[1:]  # Convert to bright
            elif code.startswith("4"):  # Regular background
                code = "10" + code[1:]  # Convert to bright
            return f"\033[{code}m"

    # Check for RGB format (255;255;255)
    rgb_match = re.match(r"^(\d{1,3});(\d{1,3});(\d{1,3})$", color_part)
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            # Use 24-bit color escape sequence
            code = "48" if is_background else "38"
            return f"\033[{code};2;{r};{g};{b}m"

    # If we get here, the color specification is invalid
    raise InvalidColor(
        f"Invalid color specification: '{color_part}'",
        color_part,
        "Use named colors (RED, GREEN, etc.) or RGB format (255;0;0).",
    )


def colored_format(
    text: str, fg_color: Optional[str] = None, bg_color: Optional[str] = None
) -> str:
    """
    Format text with ANSI color codes.

    Args:
        text: Text to format
        fg_color: Foreground color name or ANSI code
        bg_color: Background color name or ANSI code

    Returns:
        Formatted text with color codes
    """
    # Get foreground and background color codes
    fg_code = ""
    bg_code = ""

    if fg_color:
        try:
            fg_code, _ = parse_color(fg_color)
        except InvalidColor:
            # Fall back to direct code if provided
            if fg_color.startswith("\033["):
                fg_code = fg_color

    if bg_color:
        try:
            _, bg_code = parse_color(bg_color)
        except InvalidColor:
            # Fall back to direct code if provided
            if bg_color.startswith("\033["):
                bg_code = bg_color

    if fg_code or bg_code:
        return f"{fg_code}{bg_code}{text}{RESET_COLORS}"
    else:
        return text


def get_coloring_functions():
    """
    Get available coloring functions.

    Returns:
        dict: Mapping of color function names to their implementations
    """
    from .effects import (
        gradient_colorize,
        pulse_colorize,
        rainbow_colorize,
        random_colorize,
    )

    return {
        "rainbow": rainbow_colorize,
        "gradient": gradient_colorize,
        "random": random_colorize,
        "pulse": pulse_colorize,
    }
