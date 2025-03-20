"""
Compatibility layer for pyfiglet.

This module provides perfect backward compatibility with the original pyfiglet package,
ensuring that any code written for pyfiglet will work seamlessly with figlet_forge.
It maintains identical API signatures while leveraging the enhanced features of
figlet_forge under the hood.

Example usage with original pyfiglet syntax:
    from figlet_forge.compat import Figlet
    fig = Figlet(font='slant')
    print(fig.renderText('Hello, world!'))

Usage as a drop-in replacement:
    # Original code
    import pyfiglet
    print(pyfiglet.figlet_format("Hello World"))

    # Replacement code (identical behavior)
    import figlet_forge.compat as pyfiglet
    print(pyfiglet.figlet_format("Hello World"))
"""

import sys
import warnings
from typing import Any, Dict, List, Optional, Tuple, Union

# Import the core figlet_forge components
from .. import (
    COLOR_CODES,
    DEFAULT_FONT,
    RESET_COLORS,
    Figlet,
    FigletFont,
    FigletString,
)

# Re-export all the original pyfiglet classes and functions
__all__ = [
    "Figlet",
    "FigletFont",
    "FigletString",
    "figlet_format",
    "print_figlet",
    "DEFAULT_FONT",
    "COLOR_CODES",
    "RESET_COLORS",
]

# Version information matching pyfiglet format
__version__ = "1.0.2"  # Match the current pyfiglet version for compatibility


def figlet_format(
    text: str,
    font: str = DEFAULT_FONT,
    width: int = 80,
    height: Optional[int] = None,  # Unused in original but kept for API compatibility
    justify: Optional[str] = None,
    direction: Optional[str] = None,
) -> str:
    """
    Return ASCII art text using the selected FIGlet font.

    This function maintains the exact API signature of the original pyfiglet.figlet_format
    while leveraging the enhanced figlet_forge rendering engine under the hood.

    Args:
        text: The text to render
        font: The FIGlet font to use
        width: The maximum width of the output
        height: Unused (kept for API compatibility)
        justify: The justification of the output text ('left', 'center', 'right')
        direction: The direction of the output text ('auto', 'left-to-right', 'right-to-left')

    Returns:
        A string containing the ASCII art
    """
    if height is not None:
        warnings.warn("The 'height' parameter is not supported and will be ignored.")

    fig = Figlet(font=font, width=width, justify=justify, direction=direction)
    return fig.renderText(text)


def print_figlet(
    text: str,
    font: str = DEFAULT_FONT,
    colors: str = ":",
    width: int = 80,
    justify: Optional[str] = None,
    direction: Optional[str] = None,
) -> None:
    """
    Print ASCII art text using the selected FIGlet font with optional colors.

    This provides the same interface as the original pyfiglet.print_figlet,
    with additional color support for compatibility with common pyfiglet extensions.

    Args:
        text: The text to print
        font: The FIGlet font to use
        colors: The colors to use (syntax: "foreground:background")
        width: The maximum width of the output
        justify: The justification of the output text ('left', 'center', 'right')
        direction: The direction of the output text ('auto', 'left-to-right', 'right-to-left')
    """
    from ..color import parse_color

    # Generate the figlet text
    fig = Figlet(font=font, width=width, justify=justify, direction=direction)
    result = fig.renderText(text)

    # Apply colors if specified
    ansi_colors = parse_color(colors)
    if ansi_colors:
        sys.stdout.write(ansi_colors)

    # Print the result
    print(result)

    # Reset colors if needed
    if ansi_colors:
        sys.stdout.write("\033[0m")
        sys.stdout.flush()


# Alias original functions to maintain compatibility with less common imports
renderText = figlet_format


# Create a module-level accessor to mimic pyfiglet's structure
class _PyfigletCompat:
    """
    Module-level accessor for pyfiglet-compatible functions.
    This enables importing and using figlet_forge.compat as a direct
    replacement for the pyfiglet module.
    """

    @staticmethod
    def figlet_format(*args, **kwargs):
        return figlet_format(*args, **kwargs)

    @staticmethod
    def print_figlet(*args, **kwargs):
        return print_figlet(*args, **kwargs)


# Expose the module-level accessor
sys.modules[__name__].__class__ = _PyfigletCompat


# Provide classic pyfiglet API namespace attributes
figlet_format = figlet_format
