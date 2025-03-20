"""
Core FIGlet rendering functionality for Figlet Forge.

This module implements the main Figlet class which handles font loading and
text rendering, along with the print_figlet convenience function.
"""

import sys
from typing import List

from .core.figlet_font import FigletFont
from .core.figlet_string import FigletString
from .render.figlet_engine import FigletRenderingEngine
from .version import DEFAULT_FONT, RESET_COLORS


class Figlet:
    """
    Main FIGlet rendering class that handles font loading and text rendering.

    This class provides full backwards compatibility with the original pyfiglet
    while adding enhanced features for color support and Unicode rendering.
    """

    def __init__(
        self,
        font: str = DEFAULT_FONT,
        direction: str = "auto",
        justify: str = "auto",
        width: int = 80,
        unicode_aware: bool = False,
    ):
        """
        Initialize the Figlet object with specified parameters.

        Args:
            font: The name of the font to use or path to a .flf font file
            direction: The direction of the output text ('auto', 'left-to-right', 'right-to-left')
            justify: The justification of the output text ('auto', 'left', 'center', 'right')
            width: The maximum width of the output
            unicode_aware: Whether to enable Unicode character support
        """
        self.font = font
        self.direction = direction
        self.justify = justify
        self.width = width
        self.unicode_aware = unicode_aware

        # Initialize the font
        self.Font = None
        self.engine = None
        self.setFont(font)

    def setFont(self, font: str) -> None:
        """
        Set the current font to use for rendering.

        Args:
            font: The name of the font to use or path to a .flf font file
        """
        self.font = font
        self.Font = FigletFont(font)

        # Setup the rendering direction
        if self.direction == "auto":
            direction_value = getattr(self.Font, "printDirection", 0)
            if direction_value == 0:
                self.direction = "left-to-right"
            elif direction_value == 1:
                self.direction = "right-to-left"
            else:
                self.direction = "left-to-right"  # Default if undefined

        # Set up the rendering engine
        self.engine = FigletRenderingEngine(self)

    def getDirection(self) -> str:
        """
        Get the current direction setting.

        Returns:
            The direction ('left-to-right' or 'right-to-left')
        """
        return self.direction

    def getJustify(self) -> str:
        """
        Get the current justification setting.

        Returns:
            The justification ('auto', 'left', 'center', 'right')
        """
        if self.justify == "auto":
            if self.direction == "left-to-right":
                return "left"
            else:
                return "right"
        else:
            return self.justify

    @classmethod
    def getFonts(cls) -> List[str]:
        """
        Get a list of available fonts.

        Returns:
            A sorted list of available font names
        """
        return sorted(FigletFont.getFonts())

    @classmethod
    def infoFont(cls, font: str, short: bool = False) -> str:
        """
        Get information about a specific font.

        Args:
            font: The name of the font
            short: Whether to return only the first line of information

        Returns:
            Font information string
        """
        return FigletFont.infoFont(font, short)

    def renderText(self, text: str) -> FigletString:
        """
        Render input text with the current font.

        Args:
            text: The text to render

        Returns:
            A FigletString containing the rendered ASCII art
        """
        if self.engine is None:
            self.setFont(self.font)

        # Handle Unicode if enabled
        if self.unicode_aware and isinstance(text, str):
            try:
                # Ensure full Unicode handling
                pass  # Actual implementation would be here
            except UnicodeEncodeError:
                # Fall back to ASCII only if needed
                text = str(text.encode("ascii", "replace").decode("ascii"))

        # Render the text
        return self.engine.render(text)


def print_figlet(
    text: str, font: str = DEFAULT_FONT, colors: str = ":", **kwargs
) -> None:
    """
    Print ASCII art text using the selected FIGlet font with optional colors.

    This is a convenience function that creates a Figlet instance, renders
    the text, and prints it with the specified colors.

    Args:
        text: The text to print
        font: The FIGlet font to use
        colors: The colors to use (format: "foreground:background")
        **kwargs: Additional parameters to pass to the Figlet constructor
    """
    from .color import parse_color

    # Generate the figlet text
    fig = Figlet(font=font, **kwargs)
    result = fig.renderText(text)

    # Apply colors if specified
    ansi_colors = parse_color(colors) if colors else ""
    if ansi_colors:
        sys.stdout.write(ansi_colors)

    # Print the result
    print(result)

    # Reset colors if needed
    if ansi_colors:
        sys.stdout.write(RESET_COLORS)
        sys.stdout.flush()
