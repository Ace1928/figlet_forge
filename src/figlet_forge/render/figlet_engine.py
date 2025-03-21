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

import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, Optional

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

            # Ensure text is always a string
            if not isinstance(text, str):
                text = str(text)

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

            # Enforce width constraint if needed
            if self.width > 0:
                lines = result.splitlines()
                trimmed_lines = []
                for line in lines:
                    if len(line) > self.width:
                        trimmed_lines.append(line[: self.width])
                    else:
                        trimmed_lines.append(line)
                result = FigletString("\n".join(trimmed_lines))

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


class RenderEngine:
    """
    Render engine for converting FigletString to different output formats.
    """

    @staticmethod
    def to_svg(text: str, options: Optional[Dict] = None) -> str:
        """
        Convert FigletString to SVG format.

        Args:
            text: The FigletString text to convert
            options: Options for SVG rendering including:
                - font_family: Font family for text (default: monospace)
                - font_size: Font size in pixels (default: 14)
                - line_height: Line height as multiplier of font_size (default: 1.2)
                - char_width: Character width in pixels (default: 8.4)
                - fg_color: Foreground color (default: black)
                - bg_color: Background color (default: transparent)
                - padding: Padding in pixels (default: 10)

        Returns:
            SVG representation of the FigletString
        """
        # Default options
        opts = {
            "font_family": "monospace",
            "font_size": 14,
            "line_height": 1.2,
            "char_width": 8.4,
            "fg_color": "black",
            "bg_color": "transparent",
            "padding": 10,
        }

        # Override with provided options
        if options:
            opts.update(options)

        # Split into lines and calculate dimensions
        lines = text.split("\n")
        max_line_length = max(len(line) for line in lines)

        # Calculate SVG dimensions
        text_width = max_line_length * opts["char_width"]
        text_height = len(lines) * (opts["font_size"] * opts["line_height"])
        total_width = text_width + (opts["padding"] * 2)
        total_height = text_height + (opts["padding"] * 2)

        # Create SVG root element
        root = ET.Element(
            "svg",
            {
                "xmlns": "http://www.w3.org/2000/svg",
                "width": str(total_width),
                "height": str(total_height),
                "viewBox": f"0 0 {total_width} {total_height}",
            },
        )

        # Add background if not transparent
        if opts["bg_color"] != "transparent":
            ET.SubElement(
                root,
                "rect",
                {"width": "100%", "height": "100%", "fill": opts["bg_color"]},
            )

        # Add text group
        text_group = ET.SubElement(
            root,
            "g",
            {
                "font-family": opts["font_family"],
                "font-size": str(opts["font_size"]),
                "fill": opts["fg_color"],
            },
        )

        # Extract ANSI color codes if present
        ansi_pattern = re.compile(r"\033\[[^m]*m")

        # Add each line of text
        for i, line in enumerate(lines):
            # Handle ANSI color codes
            if "\033[" in line:
                # This is a simplified approach - a full implementation would parse and
                # convert ANSI codes to SVG <tspan> elements with appropriate fill colors
                clean_line = ansi_pattern.sub("", line)
                y_pos = opts["padding"] + (i + 1) * (
                    opts["font_size"] * opts["line_height"]
                )

                text_elem = ET.SubElement(
                    text_group,
                    "text",
                    {
                        "x": str(opts["padding"]),
                        "y": str(y_pos),
                        "xml:space": "preserve",
                    },
                )
                text_elem.text = clean_line
            else:
                # Standard text without ANSI codes
                y_pos = opts["padding"] + (i + 1) * (
                    opts["font_size"] * opts["line_height"]
                )
                text_elem = ET.SubElement(
                    text_group,
                    "text",
                    {
                        "x": str(opts["padding"]),
                        "y": str(y_pos),
                        "xml:space": "preserve",
                    },
                )
                text_elem.text = line

        # Convert to string
        ET.register_namespace("", "http://www.w3.org/2000/svg")
        tree = ET.ElementTree(root)
        from io import BytesIO

        f = BytesIO()
        tree.write(f, encoding="utf-8", xml_declaration=True)
        return f.getvalue().decode("utf-8")

    @staticmethod
    def to_html(text: str, options: Optional[Dict] = None) -> str:
        """
        Convert FigletString to HTML format.

        Args:
            text: The FigletString text to convert
            options: Options for HTML rendering including:
                - css_class: CSS class for the pre element (default: figlet)
                - fg_color: Foreground color (default: inherit)
                - bg_color: Background color (default: transparent)

        Returns:
            HTML representation of the FigletString
        """
        # Default options
        opts = {"css_class": "figlet", "fg_color": "inherit", "bg_color": "transparent"}

        # Override with provided options
        if options:
            opts.update(options)

        # Escape HTML special characters
        from html import escape

        escaped_text = escape(text)

        # Handle ANSI codes if present - convert to span elements with CSS
        if "\033[" in text:
            # This is a placeholder - a full implementation would convert
            # ANSI codes to CSS/HTML color spans
            html = f'<pre class="{opts["css_class"]}" style="color: {opts["fg_color"]}; background-color: {opts["bg_color"]};">{escaped_text}</pre>'
        else:
            html = f'<pre class="{opts["css_class"]}" style="color: {opts["fg_color"]}; background-color: {opts["bg_color"]};">{escaped_text}</pre>'

        return html
