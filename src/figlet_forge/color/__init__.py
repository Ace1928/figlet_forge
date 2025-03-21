"""
Color utilities for Figlet text.

This module provides functions and classes to add color to ASCII art text.
"""

# Define the color formats dict for the CLI
color_formats = {
    "rainbow": "Apply rainbow colors to text",
    "gradient": "Apply gradient colors (requires start/end colors)",
    "random": "Apply random colors to text",
    "pulse": "Apply pulsing effect with a single color",
    "red_on_black": "Red text on black background",
    "green_on_black": "Green text on black background",
    "yellow_on_blue": "Yellow text on blue background",
    "white_on_red": "White text on red background",
    "cyan_on_black": "Cyan text on black background",
}

from .effects import (
    color_style_apply,
    gradient_colorize,
    highlight_pattern,
    pulse_colorize,
    rainbow_colorize,
    random_colorize,
)
from .figlet_color import (
    ColorMode,
    ColorScheme,
    color_to_ansi,
    colored_format,
    get_coloring_functions,
    parse_color,
)

__all__ = [
    "color_to_ansi",
    "parse_color",
    "colored_format",
    "ColorScheme",
    "ColorMode",
    "rainbow_colorize",
    "gradient_colorize",
    "random_colorize",
    "pulse_colorize",
    "highlight_pattern",
    "color_style_apply",
    "color_formats",
    "get_coloring_functions",
]
