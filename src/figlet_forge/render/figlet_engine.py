"""
Figlet Rendering Engine - The core typographic processor.

This module implements the rendering engine for Figlet Forge, handling
the transformation of text into FIGlet ASCII art with comprehensive
options for formatting, layout, and character handling.

Following Eidosian principles:
- Flow Like Water: Operations chain seamlessly
- Structure as Control: Architecture prevents errors
- Recursive Refinement: Each rendering pass enhances the result
"""

from typing import Any, Dict

from ..core.exceptions import CharNotPrinted, FigletError
from ..core.figlet_builder import FigletBuilder
from ..core.figlet_string import FigletString


class FigletRenderingEngine:
    """
    Engine for rendering FIGlet ASCII art.

    This class handles the transformation of text into FIGlet ASCII art,
    providing comprehensive options for layout, direction, width control,
    and Unicode support.
    """

    def __init__(self, figlet_instance: Any):
        """
        Initialize the rendering engine with the parent Figlet instance.

        Args:
            figlet_instance: The parent Figlet object containing configuration
        """
        self.figlet = figlet_instance
        self.font = figlet_instance.Font
        self.direction = figlet_instance.getDirection()
        self.justify = figlet_instance.getJustify()
        self.width = figlet_instance.width
        self.unicode_aware = figlet_instance.unicode_aware

        # Metrics for recursive optimization
        self._metrics: Dict[str, Any] = {
            "renders": 0,
            "chars_processed": 0,
            "max_width_rendered": 0,
            "rendering_time_ms": 0,
        }

    def render(self, text: str) -> FigletString:
        """
        Render text using the current font and settings.

        This is the main rendering method that transforms input text to ASCII art.

        Args:
            text: The text to render

        Returns:
            A FigletString containing the rendered ASCII art

        Raises:
            FigletError: If there are issues during rendering
        """
        import time

        # Record start time for performance metrics
        start_time = time.time()

        # Update metrics
        self._metrics["renders"] += 1

        try:
            # Handle empty text
            if not text:
                return FigletString("")

            # Preprocess text for Unicode handling if needed
            processed_text = self._preprocess_text(text)

            # Apply text direction (RTL or LTR)
            oriented_text = self._apply_direction(processed_text)

            # Create builder for text transformation
            builder = FigletBuilder(
                oriented_text,
                self.font,
                direction=self.direction,
                width=self.width,
                justify=self.justify,
            )

            # Process text character by character
            while builder.isNotFinished():
                builder.addCharToProduct()
                builder.goToNextChar()

            # Generate the final FigletString
            result = builder.returnProduct()

            # Update metrics
            self._metrics["chars_processed"] += len(text)
            self._metrics["max_width_rendered"] = max(
                self._metrics["max_width_rendered"],
                result.dimensions[0] if result else 0,
            )
            self._metrics["rendering_time_ms"] += (time.time() - start_time) * 1000

            return result

        except CharNotPrinted as e:
            # Convert specific exceptions to general FigletError with context
            raise FigletError(
                f"Character rendering failed: {e}",
                context={"char": e.context.get("character"), "width": self.width},
                suggestion="Try increasing width or using a narrower font",
            )
        except Exception as e:
            # Wrap unexpected errors with clear context
            if not isinstance(e, FigletError):
                raise FigletError(
                    f"Rendering error: {str(e)}",
                    suggestion="Check input text and font compatibility",
                ) from e
            raise
        finally:
            # Record total rendering time
            self._metrics["rendering_time_ms"] += (time.time() - start_time) * 1000

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text before rendering.

        Handles unicode normalization and other text transformations.

        Args:
            text: The text to preprocess

        Returns:
            Preprocessed text ready for rendering
        """
        # Apply Unicode handling if enabled
        if self.unicode_aware:
            import unicodedata

            # Normalize to composed form (NFC)
            text = unicodedata.normalize("NFC", text)

        return text

    def _apply_direction(self, text: str) -> str:
        """
        Apply text direction (RTL or LTR).

        Args:
            text: The text to process

        Returns:
            Text with correct directional orientation
        """
        if self.direction == "right-to-left":
            # Reverse each line for RTL
            lines = text.split("\n")
            return "\n".join(line[::-1] for line in lines)
        return text

    def adjust_width(self, width: int) -> None:
        """
        Update the output width.

        Args:
            width: New width value
        """
        self.width = width

    def adjust_justify(self, justify: str) -> None:
        """
        Update the justification method.

        Args:
            justify: New justification ('left', 'center', 'right')
        """
        self.justify = justify

    def adjust_direction(self, direction: str) -> None:
        """
        Update the text direction.

        Args:
            direction: New direction ('left-to-right', 'right-to-left')
        """
        self.direction = direction

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get rendering metrics for optimization analysis.

        Returns:
            Dictionary of performance metrics
        """
        return self._metrics
