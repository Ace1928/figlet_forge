"""
Core FIGlet rendering functionality for Figlet Forge.

This module implements the main Figlet class which handles font loading and
text rendering, along with the print_figlet convenience function.
"""

from typing import Any, List, Union

from .color.figlet_color import parse_color
from .core.exceptions import FigletError, FontNotFound
from .core.figlet_font import FigletFont
from .core.figlet_string import FigletString
from .render.figlet_engine import FigletRenderingEngine
from .version import DEFAULT_FONT, RESET_COLORS


class Figlet:
    """
    Main FIGlet interface for rendering ASCII art text with various options.

    This class handles font loading, text formatting, layout control, and
    rendering of ASCII art text using FIGlet fonts. It follows the Eidosian
    principles of flow, precision, and context-awareness.

    Attributes:
        font (str): Name of the loaded font
        direction (str): Text direction ('auto', 'left-to-right', 'right-to-left')
        justify (str): Text justification ('auto', 'left', 'center', 'right')
        width (int): Maximum width of rendered output
        unicode_aware (bool): Whether to handle Unicode characters
        Font (FigletFont): Font instance used for rendering

    Examples:
        >>> from figlet_forge import Figlet
        >>> fig = Figlet(font='standard')
        >>> result = fig.renderText("Hello")
        >>> print(result)
          _   _          _   _
         | | | |   ___  | | | |   ___
         | |_| |  / _ \ | | | |  / _ \
         |  _  | |  __/ | | | | | (_) |
         |_| |_|  \___| |_| |_|  \___/
    """

    def __init__(
        self,
        font: Union[str, FigletFont] = DEFAULT_FONT,
        direction: str = "auto",
        justify: str = "auto",
        width: int = 80,
        unicode_aware: bool = False,
    ):
        """
        Initialize the Figlet renderer with specified options.

        Args:
            font: Name of font to use or a FigletFont instance
            direction: Text direction ('auto', 'left-to-right', 'right-to-left')
            justify: Text justification ('auto', 'left', 'center', 'right')
            width: Maximum width of rendered output
            unicode_aware: Whether to handle Unicode characters
        """
        self.font = font if isinstance(font, str) else "custom"
        self.direction = direction
        self.justify = justify
        self.width = width
        self.unicode_aware = unicode_aware
        self._engine = None
        self._load_font(font)

    def _load_font(self, font: Union[str, FigletFont]) -> None:
        """
        Load the specified font.

        Args:
            font: Name of font or FigletFont instance to use

        Raises:
            FontNotFound: If the font cannot be located
        """
        if isinstance(font, FigletFont):
            self.Font = font
        else:
            try:
                self.Font = FigletFont(font)
            except FontNotFound as e:
                # Try to fall back to standard font if possible
                if font.lower() != DEFAULT_FONT.lower():
                    try:
                        self.Font = FigletFont(DEFAULT_FONT)
                        self.font = DEFAULT_FONT  # Update font name
                    except Exception:
                        # Propagate the original error if fallback fails
                        raise e
                else:
                    raise

    def getJustify(self) -> str:
        """
        Get the effective justification value.

        Returns:
            Resolved justification value ('left', 'center', or 'right')
        """
        if self.justify == "auto":
            if self.direction == "right-to-left":
                return "right"
            return "left"
        return self.justify

    def renderText(self, text: str) -> FigletString:
        """
        Render text using the current font and settings.

        This is the main method for converting input text to ASCII art.

        Args:
            text: The text to render

        Returns:
            A FigletString containing the rendered ASCII art

        Raises:
            FigletError: If there are issues during rendering
        """
        if not text:
            return FigletString("")

        try:
            # Initialize the rendering engine if not already done
            if not self._engine:
                self._engine = FigletRenderingEngine(self)

            # Render the text
            return self._engine.render(text)
        except Exception as e:
            if not isinstance(e, FigletError):
                # Wrap unexpected errors
                raise FigletError(
                    f"Error rendering text: {str(e)}",
                    suggestion="Check input text and font compatibility",
                ) from e
            raise

    def setFont(self, font: Union[str, FigletFont] = DEFAULT_FONT) -> None:
        """
        Change the font used for rendering.

        Args:
            font: Name of font to use or a FigletFont instance

        Raises:
            FontNotFound: If the font cannot be located
        """
        self.font = font if isinstance(font, str) else "custom"
        self._load_font(font)
        self._engine = None  # Reset engine to use new font

    def getFonts(self) -> List[str]:
        """
        Get a list of available font names.

        Returns:
            List of available font names
        """
        return FigletFont.getFonts()

    def getDirection(self) -> str:
        """
        Get the current text direction.

        Returns:
            Text direction ('left-to-right' or 'right-to-left')
        """
        if self.direction == "auto":
            return "left-to-right"
        return self.direction

    def setDirection(self, direction: str) -> None:
        """
        Set the text direction.

        Args:
            direction: Text direction ('auto', 'left-to-right', 'right-to-left')
        """
        if direction in ("auto", "left-to-right", "right-to-left"):
            self.direction = direction
            if self._engine:
                self._engine.adjust_direction(self.getDirection())

    def setJustify(self, justify: str) -> None:
        """
        Set the text justification.

        Args:
            justify: Text justification ('auto', 'left', 'center', 'right')
        """
        if justify in ("auto", "left", "center", "right"):
            self.justify = justify
            if self._engine:
                self._engine.adjust_justify(self.getJustify())

    def setWidth(self, width: int) -> None:
        """
        Set the output width.

        Args:
            width: Maximum width of rendered output
        """
        if width > 0:
            self.width = width
            if self._engine:
                self._engine.adjust_width(width)


def print_figlet(
    text: str,
    font: str = DEFAULT_FONT,
    colors: str = "",
    width: int = 80,
    justify: str = "auto",
    direction: str = "auto",
    **kwargs: Any,
) -> None:
    """
    Render and print FIGlet text to console with optional coloring.

    A convenient function that combines rendering and output in one step.

    Args:
        text: Text to render
        font: Name of font to use
        colors: Color specification (format: "fg:bg", "RED", "RED:BLUE", etc.)
        width: Maximum width of rendered output
        justify: Text justification ('auto', 'left', 'center', 'right')
        direction: Text direction ('auto', 'left-to-right', 'right-to-left')
        **kwargs: Additional parameters passed to Figlet constructor

    Examples:
        >>> print_figlet("Hello", font="slant", colors="RED:BLACK")
        # Prints "Hello" in slant font with red text on black background
    """
    import sys

    # Create a Figlet instance with specified options
    fig = Figlet(font=font, width=width, justify=justify, direction=direction, **kwargs)

    # Render the text
    result = fig.renderText(text)

    # Apply colors if specified
    if colors:
        try:
            foreground, background = parse_color(colors)
            if foreground or background:
                sys.stdout.write(foreground + background)
        except Exception as e:
            sys.stderr.write(f"Warning: Color error - {str(e)}\n")

    # Print the result
    sys.stdout.write(str(result))

    # Ensure output ends with newline
    if not str(result).endswith("\n"):
        sys.stdout.write("\n")

    # Reset colors if needed
    if colors:
        sys.stdout.write(RESET_COLORS)
        sys.stdout.flush()
