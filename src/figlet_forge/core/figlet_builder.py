from typing import Any, Dict, List

from .figlet_string import FigletString


class FigletProduct:
    """
    This class stores the internal build part of
    the ascii output string using an elegant buffers-as-transformation pattern.

    Buffer management follows recursive optimization principles—each
    operation improves rather than overwriting the previous state.
    """

    def __init__(self):
        self.queue: List[str] = []  # Character buffer sequence
        self.buffer_string: str = ""  # Accumulated output
        self._meta: Dict[str, Any] = {
            "transformations": [],  # Track transformation history recursively
            "metrics": {"chars": 0, "width": 0, "height": 0},  # Performance telemetry
        }

    def append(self, buffer: str) -> None:
        """
        Append a buffer to the product queue with transformation tracking.
        Each append operation is logged to enable recursive analysis and optimization.
        """
        self.queue.append(buffer)
        self._meta["metrics"]["chars"] += 1
        self._meta["transformations"].append({"type": "append", "size": len(buffer)})

    def getString(self) -> str:
        """
        Generate the final string output from accumulated buffers.

        Returns:
            The fully constructed FIGlet text as a string
        """
        # Join all buffers in the queue to form the complete output
        self.buffer_string = "".join(self.queue)

        # Update metrics with final width and height
        lines = self.buffer_string.split("\n")
        self._meta["metrics"]["height"] = len(lines)
        self._meta["metrics"]["width"] = max((len(line) for line in lines), default=0)

        # Return the complete string
        return self.buffer_string

    def reset(self) -> None:
        """Reset the product state while preserving transformation metrics."""
        self.queue = []
        self.buffer_string = ""
        # Preserve metrics for optimization analysis
        self._meta["transformations"].append({"type": "reset", "reason": "explicit"})

    def get_metrics(self) -> Dict[str, Any]:
        """Get telemetry about the product's construction process."""
        self._meta["metrics"]["width"] = max(
            (len(line) for line in self.getString().split("\n")), default=0
        )
        self._meta["metrics"]["height"] = self.getString().count("\n") + 1
        return self._meta["metrics"]

    def to_figlet_string(self) -> FigletString:
        """Convert the product to a FigletString for client consumption."""
        return FigletString(self.getString())


class FigletBuilder:
    """
    FigletBuilder orchestrates the construction of FIGlet ASCII art text.

    This class handles the character-by-character transformation process,
    managing the flow of rendering each character according to the specified
    font and layout parameters.
    """

    def __init__(
        self,
        text: str,
        font: Any,
        direction: str = "auto",
        width: int = 80,
        justify: str = "auto",
    ):
        """
        Initialize the FigletBuilder with rendering parameters.

        Args:
            text: The text to render
            font: The FigletFont to use for rendering
            direction: Text direction ('auto', 'left-to-right', 'right-to-left')
            width: Maximum width for the output
            justify: Justification ('auto', 'left', 'center', 'right')
        """
        self.text = text
        self.font = font
        self.direction = direction
        self.width = width
        self.justify = justify

        # State variables for rendering
        self.product = FigletProduct()
        self.current_char_index = 0
        self.lines: List[List[str]] = [[] for _ in range(self.font.height)]
        self.current_line_width = 0

        # Initialize the rendering metrics
        self._meta = {"char_count": len(text), "processed": 0, "transformations": []}

    def isNotFinished(self) -> bool:
        """
        Check if there are more characters to process.

        Returns:
            True if there are more characters to render, False otherwise
        """
        return self.current_char_index < len(self.text)

    def addCharToProduct(self) -> None:
        """
        Add the current character to the FigletProduct.

        This method processes the current character, renders it using the
        font, and adds it to the lines buffer while respecting width constraints.

        Raises:
            CharNotPrinted: If the character cannot fit within width constraints
        """
        from .exceptions import CharNotPrinted

        # Get the current character
        char = self.text[self.current_char_index]

        # Handle newline character specially
        if char == "\n":
            # Finalize current lines and add to product
            self._flushLinesToProduct()
            # Add the newline to product
            self.product.append("\n")
            return

        # Get the character's FIGlet representation from the font
        char_lines = self.font.getCharacter(char)
        char_width = self.font.getWidth(char)

        # Check if adding this character would exceed width
        if self.current_line_width + char_width > self.width:
            # For word wrapping, we would need to check if we're mid-word
            # and decide whether to wrap the whole word or split it
            # For now, simply force the character onto a new line
            self._flushLinesToProduct()

            # If the character itself is wider than allowed width, that's an error
            if char_width > self.width:
                raise CharNotPrinted(
                    f"Character '{char}' exceeds maximum width",
                    width=self.width,
                    char=char,
                    required_width=char_width,
                )

        # Add the character's lines to our buffer
        for i, line in enumerate(char_lines):
            self.lines[i].append(line)

        # Update current line width
        self.current_line_width += char_width

        # Update metrics
        self._meta["processed"] += 1
        self._meta["transformations"].append({"char": char, "width": char_width})

    def _flushLinesToProduct(self) -> None:
        """
        Combine the current lines buffer and add to the product.

        This method is called when a line is complete, when a newline is
        encountered, or when the width limit would be exceeded.
        """
        if not any(self.lines):  # Skip if lines buffer is empty
            return

        # Apply justification
        if self.justify == "center":
            padding = (self.width - self.current_line_width) // 2
            justified_lines = [" " * padding + "".join(line) for line in self.lines]
        elif self.justify == "right":
            justified_lines = [
                " " * (self.width - self.current_line_width) + "".join(line)
                for line in self.lines
            ]
        else:  # left or auto
            justified_lines = ["".join(line) for line in self.lines]

        # Add lines to product with newlines
        for line in justified_lines:
            self.product.append(line + "\n")

        # Reset lines buffer for next set of characters
        self.lines = [[] for _ in range(self.font.height)]
        self.current_line_width = 0

    def goToNextChar(self) -> None:
        """
        Advance to the next character in the text.
        """
        self.current_char_index += 1

    def returnProduct(self) -> FigletString:
        """
        Complete the rendering process and return the final product.

        Returns:
            A FigletString containing the rendered ASCII art
        """
        # Flush any remaining lines
        self._flushLinesToProduct()

        # Get the completed string
        result = self.product.getString()

        # Wrap in FigletString for additional operations
        return FigletString(result)
