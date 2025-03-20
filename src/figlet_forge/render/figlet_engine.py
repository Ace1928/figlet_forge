"""
Figlet rendering engine that orchestrates the transformation of text into ASCII art.

This module follows Eidosian principles:
- Flow Like Water, Strike Like Lightning: Operations chain seamlessly
- Exhaustive But Concise: Handling all edge cases with elegant code
- Structure as Control: Architecture prevents errors by design
"""

from typing import Any

from ..core.exceptions import CharNotPrinted, FontError
from ..core.figlet_builder import FigletBuilder
from ..core.figlet_string import FigletString


class FigletRenderingEngine:
    """
    Core rendering engine for Figlet Forge that transforms text into FIGlet output.

    This class handles the transformation of input text into ASCII art using
    the specified font, with support for different directions, justifications,
    and Unicode characters.
    """

    def __init__(self, figlet_instance: Any):
        """
        Initialize the rendering engine.

        Args:
            figlet_instance: The Figlet instance that contains configuration
        """
        self.figlet = figlet_instance
        self.font = figlet_instance.Font
        self.direction = figlet_instance.direction
        self.width = figlet_instance.width
        self.justify = figlet_instance.getJustify()
        self.unicode_aware = figlet_instance.unicode_aware

    def render(self, text: str) -> FigletString:
        """
        Render text using the current font and settings.

        Args:
            text: The text to render

        Returns:
            A FigletString containing the rendered ASCII art

        Raises:
            CharNotPrinted: If a character couldn't be rendered
            FontError: If there are issues with the font during rendering
        """
        if not text:
            return FigletString("")

        # Handle newlines in text - split and render separately
        if "\n" in text:
            return self._renderMultiline(text)

        # Determine direction for rendering
        if self.direction == "right-to-left":
            text = text[::-1]  # Reverse the text for right-to-left rendering

        # Prepare the text for rendering
        normalized_text = self._prepareText(text)

        # Create a builder for the rendering process
        builder = FigletBuilder(
            text=normalized_text,
            font=self.font,
            direction=self.direction,
            width=self.width,
            justify=self.justify,
        )

        # Perform the rendering
        try:
            # Process all characters in the text
            while builder.isNotFinished():
                builder.addCharToProduct()
                builder.goToNextChar()

            # Get the final rendered output
            result = builder.returnProduct()

            # For right-to-left, we reverse the output lines
            if self.direction == "right-to-left":
                result = result.reverse()

            return result

        except Exception as e:
            # Convert any unexpected exceptions to our defined error types
            if "width too small" in str(e).lower():
                raise CharNotPrinted(f"Character couldn't be printed: {str(e)}")
            else:
                raise FontError(f"Font rendering error: {str(e)}")

    def _renderMultiline(self, text: str) -> FigletString:
        """
        Handle multi-line text rendering.

        Args:
            text: Text containing newlines

        Returns:
            A FigletString combining all rendered lines
        """
        result = []
        lines = text.split("\n")

        for i, line in enumerate(lines):
            if line:
                # Render each non-empty line
                rendered = self.render(line)
                result.append(rendered)
            elif i < len(lines) - 1 or lines[-1]:
                # For empty lines (except potentially the last one), add empty FigletString
                result.append(FigletString(""))

        # Combine all rendered lines with newlines between them
        return FigletString("\n").join(result)

    def _prepareText(self, text: str) -> str:
        """
        Prepare text for rendering by handling Unicode and special characters.

        Args:
            text: The input text

        Returns:
            Normalized text ready for rendering
        """
        if not self.unicode_aware:
            # Without Unicode awareness, convert to ASCII with fallbacks
            try:
                return str(text.encode("ascii", "replace").decode("ascii"))
            except (UnicodeEncodeError, UnicodeDecodeError):
                # Fallback to basic representation
                return str(text.encode("ascii", "ignore").decode("ascii"))

        # With Unicode awareness, handle special characters and normalization
        try:
            import unicodedata

            # Normalize Unicode to ensure consistent rendering
            text = unicodedata.normalize("NFC", text)
            return text
        except (ImportError, Exception):
            # If unicodedata is not available or fails, return as is
            return text

    def adjust_width(self, new_width: int) -> None:
        """
        Adjust the output width for rendering.

        Args:
            new_width: The new width to use
        """
        self.width = new_width

    def adjust_direction(self, new_direction: str) -> None:
        """
        Change the text direction.

        Args:
            new_direction: New direction ('left-to-right' or 'right-to-left')
        """
        if new_direction in ("left-to-right", "right-to-left"):
            self.direction = new_direction

    def adjust_justify(self, new_justify: str) -> None:
        """
        Change the text justification.

        Args:
            new_justify: New justification ('left', 'center', 'right')
        """
        if new_justify in ("left", "center", "right"):
            self.justify = new_justify
