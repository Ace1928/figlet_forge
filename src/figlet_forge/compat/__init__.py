"""
Compatibility layer for pyfiglet.

This module provides backward compatibility with the pyfiglet library,
allowing Figlet Forge to be used as a drop-in replacement.

Following Eidosian principles, we maintain compatibility while adding
recursive optimization under the hood.
"""

import os
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

# Re-export our core functionality under pyfiglet-compatible names
from ..core.figlet_font import FigletFont
from ..figlet import Figlet as BaseFiglet  # Import our implementation as BaseFiglet
from ..version import DEFAULT_FONT, __version__

# Constants for compatibility
VERSION = __version__


class FigletError(Exception):
    """Compatibility class for pyfiglet's FigletError."""

    pass


class FontNotFound(FigletError):
    """Compatibility class for pyfiglet's FontNotFound."""

    pass


# Wrap our implementation in a compatibility class that mirrors pyfiglet's API
class Figlet(BaseFiglet):
    """
    Compatibility wrapper for the Figlet class.

    This class provides the same API as pyfiglet's Figlet class,
    while using Figlet Forge's implementation under the hood.
    """

    def __init__(
        self,
        font: Union[str, FigletFont] = DEFAULT_FONT,
        direction: str = "auto",
        justify: str = "auto",
        width: int = 80,
        **kwargs: Any,
    ) -> None:
        """
        Initialize with pyfiglet-compatible parameters.

        Args:
            font: Name of the font to use or a FigletFont instance
            direction: Text direction ('auto', 'left-to-right', 'right-to-left')
            justify: Text justification ('auto', 'left', 'center', 'right')
            width: Maximum width of the rendered output
            **kwargs: Additional parameters (for forward compatibility)
        """
        # Extract pyfiglet-specific parameters from kwargs
        unicode_aware = kwargs.pop("unicode_aware", False)

        # Initialize base Figlet implementation
        super().__init__(
            font=font,
            direction=direction,
            justify=justify,
            width=width,
            unicode_aware=unicode_aware,
        )

    # Alias for compatibility
    def renderText(self, text: str) -> str:
        """
        Render text in the current font (pyfiglet API compatibility).

        Args:
            text: The text to render

        Returns:
            ASCII art rendering of the text
        """
        # Convert FigletString to str for compatibility
        return str(super().renderText(text))

    # Additional pyfiglet-compatible methods
    def getRenderWidth(self, text: str) -> int:
        """
        Get the width of the rendered text (compatibility method).

        Args:
            text: The text to measure

        Returns:
            Width in characters
        """
        rendered = self.renderText(text)
        return max((len(line) for line in rendered.splitlines()), default=0)


def figlet_format(
    text: str,
    font: str = DEFAULT_FONT,
    width: int = 80,
    justify: str = "auto",
    direction: str = "auto",
    **kwargs: Any,
) -> str:
    """
    Render ASCII art text using the specified font and options.

    This is a compatibility function mirroring pyfiglet.figlet_format.

    Args:
        text: The text to render
        font: Name of the font to use
        width: Maximum width of the rendered output
        justify: Text justification ('auto', 'left', 'center', 'right')
        direction: Text direction ('auto', 'left-to-right', 'right-to-left')
        **kwargs: Additional parameters

    Returns:
        ASCII art rendering of the text
    """
    fig = Figlet(
        font=font,
        direction=direction,
        justify=justify,
        width=width,
        **kwargs,
    )
    return fig.renderText(text)


# Alias for backward compatibility
renderText = figlet_format


def print_figlet(
    text: str,
    font: str = DEFAULT_FONT,
    colors: str = "",
    width: int = 80,
    justify: str = "auto",
    **kwargs: Any,
) -> None:
    """
    Print ASCII art text with optional coloring (compatibility function).

    Args:
        text: The text to render
        font: Name of the font to use
        colors: Color specification (format: "fg:bg", "RED", "RED:BLUE", etc.)
        width: Maximum width of the rendered output
        justify: Text justification ('auto', 'left', 'center', 'right')
        **kwargs: Additional parameters
    """
    from ..figlet import print_figlet as core_print_figlet

    core_print_figlet(
        text=text,
        font=font,
        colors=colors,
        width=width,
        justify=justify,
        **kwargs,
    )
