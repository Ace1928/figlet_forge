"""
╭────────────────────────────────────────────────────────────────╮
│   COLOR MANAGEMENT SYSTEM - FIGLET FORGE CHROMATIC ENGINE      │
╰────────────────────────────────────────────────────────────────╯

Precision color handling for Figlet Forge, providing elegant ANSI color
control with both named colors and RGB support.

This module follows Eidosian principles:
- Exhaustive but concise: complete color support with minimal complexity
- Structure as control: type-safe color representation prevents errors
- Precision as style: colors are represented with mathematical accuracy
"""

from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, Union

from ..core.exceptions import InvalidColor
from .figlet_color import color_to_ansi, parse_color

# Standard ANSI color names are exposed at the module level for convenience
ANSI_COLORS = [
    "BLACK",
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "MAGENTA",
    "CYAN",
    "LIGHT_GRAY",
    "DARK_GRAY",
    "LIGHT_RED",
    "LIGHT_GREEN",
    "LIGHT_YELLOW",
    "LIGHT_BLUE",
    "LIGHT_MAGENTA",
    "LIGHT_CYAN",
    "WHITE",
    "DEFAULT",
    "RESET",
]


# Color modes define how colors should be applied and processed
class ColorMode(Enum):
    """Color application modes for figlet text rendering."""

    NONE = auto()  # No color applied
    SOLID = auto()  # Solid foreground/background colors
    RAINBOW = auto()  # Rainbow gradient across characters
    GRADIENT = auto()  # Custom gradient with specific color stops
    RANDOM = auto()  # Random color for each character
    ANIMATE = auto()  # Color animation (when supported by terminal)


class ColorScheme:
    """
    Represents a complete color definition with foreground, background,
    styling options and application strategy.

    This class provides a structured way to define and apply color to
    figlet text, following the Eidosian principle of "Structure as Control".
    """

    def __init__(
        self,
        foreground: Optional[Union[str, Tuple[int, int, int]]] = None,
        background: Optional[Union[str, Tuple[int, int, int]]] = None,
        mode: ColorMode = ColorMode.SOLID,
        bold: bool = False,
        italic: bool = False,
    ):
        """
        Initialize a color scheme with foreground, background and style settings.

        Args:
            foreground: Color name or RGB tuple for text color
            background: Color name or RGB tuple for background color
            mode: How colors should be applied (solid, rainbow, etc.)
            bold: Whether text should be bold
            italic: Whether text should be italicized
        """
        self.foreground = foreground
        self.background = background
        self.mode = mode
        self.bold = bold
        self.italic = italic
        self._validate()

    def _validate(self) -> None:
        """Validate the color scheme configuration."""
        # Foreground validation
        if self.foreground is not None:
            if isinstance(self.foreground, str):
                if (
                    self.foreground.upper() not in ANSI_COLORS
                    and ";" not in self.foreground
                ):
                    raise InvalidColor(f"Invalid foreground color: {self.foreground}")
            elif not (isinstance(self.foreground, tuple) and len(self.foreground) == 3):
                raise InvalidColor("RGB colors must be tuples of 3 integers")

        # Background validation
        if self.background is not None:
            if isinstance(self.background, str):
                if (
                    self.background.upper() not in ANSI_COLORS
                    and ";" not in self.background
                ):
                    raise InvalidColor(f"Invalid background color: {self.background}")
            elif not (isinstance(self.background, tuple) and len(self.background) == 3):
                raise InvalidColor("RGB colors must be tuples of 3 integers")

    @classmethod
    def from_string(cls, color_spec: str) -> "ColorScheme":
        """
        Create a ColorScheme from a color specification string.

        Format: "foreground:background"
        Example: "RED:BLUE", "255;0;0:0;0;255", "GREEN:"

        Args:
            color_spec: String representation of colors

        Returns:
            A ColorScheme instance
        """
        foreground, _, background = color_spec.partition(":")
        fg = foreground if foreground else None
        bg = background if background else None
        return cls(foreground=fg, background=bg)

    def to_ansi(self) -> str:
        """
        Convert the color scheme to ANSI escape sequence.

        Returns:
            ANSI color escape sequence
        """
        components = []

        # Add styling
        if self.bold:
            components.append("\033[1m")
        if self.italic:
            components.append("\033[3m")

        # Add colors
        if self.foreground is not None:
            if isinstance(self.foreground, tuple):
                r, g, b = self.foreground
                components.append(f"\033[38;2;{r};{g};{b}m")
            else:
                components.append(color_to_ansi(self.foreground, False))

        if self.background is not None:
            if isinstance(self.background, tuple):
                r, g, b = self.background
                components.append(f"\033[48;2;{r};{g};{b}m")
            else:
                components.append(color_to_ansi(self.background, True))

        return "".join(components)

    def __str__(self) -> str:
        """String representation of the color scheme."""
        fg = self.foreground if self.foreground is not None else ""
        bg = self.background if self.background is not None else ""
        return f"{fg}:{bg}"


def colored_format(text: str, colors: Union[str, ColorScheme]) -> str:
    """
    Format text with ANSI color codes.

    Args:
        text: The text to colorize
        colors: Color specification as string or ColorScheme

    Returns:
        Colored text with ANSI escape codes
    """
    if not text:
        return ""

    # Convert string colors to ColorScheme if needed
    color_scheme = (
        colors if isinstance(colors, ColorScheme) else ColorScheme.from_string(colors)
    )

    # Apply colors based on mode
    if color_scheme.mode == ColorMode.SOLID:
        return f"{color_scheme.to_ansi()}{text}\033[0m"

    # Handle other color modes (rainbow, gradient, etc.)
    elif color_scheme.mode == ColorMode.RAINBOW:
        # Rainbow implementation
        result = []
        rainbow_colors = ["RED", "YELLOW", "GREEN", "CYAN", "BLUE", "MAGENTA"]
        for i, char in enumerate(text):
            if char.isspace():
                result.append(char)
            else:
                color = rainbow_colors[i % len(rainbow_colors)]
                temp_scheme = ColorScheme(
                    foreground=color, background=color_scheme.background
                )
                result.append(f"{temp_scheme.to_ansi()}{char}\033[0m")
        return "".join(result)

    # Default to solid coloring for other modes (can be expanded)
    else:
        return f"{color_scheme.to_ansi()}{text}\033[0m"


# Export the public API
__all__ = [
    "ANSI_COLORS",
    "ColorMode",
    "ColorScheme",
    "colored_format",
    "color_to_ansi",
    "parse_color",
    "InvalidColor",
]
