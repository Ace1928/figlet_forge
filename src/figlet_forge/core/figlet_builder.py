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
        # Return cached result if available for performance
        if self.buffer_string:
            return self.buffer_string

        # Otherwise join the fragments
        self.buffer_string = "".join(self.queue)
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
    Represents the internals of the build process following the Builder pattern.

    This implementation follows Eidosian principles:
    - Flow Like Water: Operations chain seamlessly through fluent methods
    - Structure as Control: Type safety prevents errors by design
    - Recursive Refinement: Continuously optimizes output through feedback loops
    """

    def __init__(self, text: str, font: Any, direction: str, width: int, justify: str):
        """
        Initialize the FigletBuilder with rendering parameters.

        Args:
            text: Text to render
            font: FigletFont to use for rendering
            direction: Text direction (left-to-right or right-to-left)
            width: Maximum width for rendering
            justify: Text justification (left, center, right)
        """
        self.font = font
        self.direction = direction
        self.width = width
        self.justify = justify
        self.text = text

        # Internal state management
        self.iterator = 0  # Current position in text
        self.buffer = []  # Current character buffer
        self.product = FigletProduct()  # Final product under construction

        # Performance optimization - precompute character width lookup
        self.width_lookup = {}

        # State tracking for recursive optimization
        self._state = {
            "last_smushed": 0,  # Track last smushing amount for optimization
            "overflow_count": 0,  # Track overflow incidents for adaptive width
            "last_blank": -1,  # Position of last blank for word wrapping
            "forced_breaks": 0,  # Count of forced line breaks for analysis
        }

    # ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
    # Builder interface - External API for rendering process
    # ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔

    def addCharToProduct(self) -> None:
        """
        Add current character to product, handling smooshing and layout.
        Uses recursive optimization to determine optimal character placement.
        """
        if not self.buffer:
            # First character or after newline
            curChar = self.getCurChar()
            if curChar:
                self.buffer = curChar.copy()  # Start fresh buffer
            return

        # Get current character
        curChar = self.getCurChar()

        # Check for newline handling
        if curChar is None:
            # End of string or unprintable character
            return
        elif curChar == ["\n"]:
            # Explicit newline - handle specially
            self.handleNewLine()
            return

        # Calculate amount to smush (0 means none)
        smushAmount = self.currentSmushAmount(curChar)

        # Update optimization metrics
        self._state["last_smushed"] = smushAmount

        # Process each row in the character
        for row in range(self.font.height):
            # Check for buffer overflow based on terminal width
            if len(self.buffer[row]) + len(curChar[row]) - smushAmount > self.width:
                self._state["overflow_count"] += 1
                # Handle overflow by cutting at last break opportunity
                if self.blankExist(self._state["last_blank"]):
                    self.cutBufferAtLastBlank(self.buffer.copy(), self.iterator)
                else:
                    # Force cut at current position if no good break point
                    self.cutBufferAtLastChar()

                # Reset buffer and restart with current character
                self.buffer = curChar.copy()
                return

            # Add current character to buffer row, handling smushing
            self.addCurCharRowToBufferRow(curChar, row, smushAmount)

        # Track position of last blank for word wrapping
        if self.text[self.iterator] == " ":
            self._state["last_blank"] = self.iterator

    def goToNextChar(self) -> None:
        """Advance to the next character in the input text."""
        self.iterator += 1

    def returnProduct(self) -> FigletString:
        """
        Return the completed FigletString product after final processing.
        Performs finishing touches like justification and hardblank replacement.

        Returns:
            A FigletString containing the rendered ASCII art
        """
        # Flush any remaining content in the buffer
        self.flushLastBuffer()

        # Get raw output and apply post-processing
        output = self.product.getString()

        # Apply justification if needed
        if self.justify != "left":
            output = self.justifyString(self.justify, output)

        # Replace hardblanks with spaces
        output = self.replaceHardblanks(output)

        # Return as FigletString for client transformations
        return FigletString(output)

    def isNotFinished(self) -> bool:
        """
        Check if processing is complete.

        Returns:
            True if there are more characters to process, False otherwise
        """
        return self.iterator < len(self.text)

    # ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
    # Private implementation - Internal rendering mechanisms
    # ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▁▁▁

    def flushLastBuffer(self) -> None:
        """
        Flush the buffer to the product queue with optimal formatting.
        Called at end of text or when buffer needs to be cleared.
        """
        if not self.buffer:
            return

        # Format buffer for output
        formattedBuffer = self.formatProduct()

        # Add to final product
        self.product.append(formattedBuffer)

        # Reset buffer for next operation
        self.buffer = []
        self._state["last_blank"] = -1

    def formatProduct(self) -> str:
        """
        Format the current buffer into a string with newlines.

        Returns:
            Formatted buffer as a string
        """
        return "\n".join(self.buffer)

    def getCharAt(self, i: int) -> List[str]:
        """
        Get the FIGlet character at a specific text position.

        Args:
            i: Index in the text

        Returns:
            List of strings representing the FIGcharacter's rows
        """
        if i >= len(self.text):
            return []

        c = self.text[i]

        # Handle special case for newlines
        if c == "\n":
            return ["\n"]

        # Get character rows from font
        return self.font.getCharacter(c)

    def getCharWidthAt(self, i: int) -> int:
        """
        Get the width of the FIGlet character at a specific position.
        Implements caching for performance optimization.

        Args:
            i: Index in the text

        Returns:
            Width of the character
        """
        # Return from cache if available
        if i in self.width_lookup:
            return self.width_lookup[i]

        if i >= len(self.text):
            return 0

        c = self.text[i]

        # Special case for newlines (zero width)
        if c == "\n":
            return 0

        # Calculate width from font
        width = self.font.getWidth(c)

        # Cache for future lookups
        self.width_lookup[i] = width
        return width

    def getCurChar(self) -> List[str]:
        """
        Get the FIGlet character at the current position.

        Returns:
            List of strings representing the current character's rows
        """
        return self.getCharAt(self.iterator)

    def getCurWidth(self) -> int:
        """
        Get the width of the current FIGlet character.

        Returns:
            Width of the current character
        """
        return self.getCharWidthAt(self.iterator)

    def getLeftSmushedChar(self, i: int, addLeft: int) -> str:
        """
        Get the left-smushed character from a buffer row.

        Args:
            i: Row index
            addLeft: Number of characters to add from the left

        Returns:
            The character from the buffer after smushing
        """
        if addLeft < 0:
            return ""

        idx = len(self.buffer[i]) - addLeft - 1

        if idx < 0:
            return ""

        return self.buffer[i][idx]

    def currentSmushAmount(self, curChar: List[str]) -> int:
        """
        Calculate the amount to smush the current character.

        Args:
            curChar: Current character rows

        Returns:
            Amount of horizontal space to smush
        """
        if self.font.old_layout > -1:
            return self.smushAmount(self.buffer, curChar)
        return 0

    def updateSmushedCharInLeftBuffer(
        self, addLeft: int, idx: int, smushed: str
    ) -> None:
        """
        Update the left buffer with a smushed character.

        Args:
            addLeft: Number of characters to add from the left
            idx: Row index
            smushed: The resulting smushed character
        """
        if addLeft < 0:
            return

        bufIdx = len(self.buffer[idx]) - addLeft - 1

        if bufIdx < 0:
            return

        # Replace character at position with smushed result
        self.buffer[idx] = (
            self.buffer[idx][:bufIdx] + smushed + self.buffer[idx][bufIdx + 1 :]
        )

    def smushRow(self, curChar: List[str], row: int, smushAmount: int) -> None:
        """
        Smush a row of the current character with the buffer.

        Args:
            curChar: Current character rows
            row: Row index
            smushAmount: Amount of horizontal space to smush
        """
        if smushAmount <= 0 or len(curChar[row]) <= 0:
            return

        # Calculate the overlap positions
        for i in range(min(smushAmount, len(curChar[row]))):
            addLeft = i

            # Get characters to smush
            charLeft = self.getLeftSmushedChar(row, addLeft)
            charRight = curChar[row][i] if i < len(curChar[row]) else ""

            # Skip if either character is empty
            if not charLeft or not charRight:
                continue  # No smushing possible with empty characters

            # Apply smushing rules
            smushed = self.smushChars(charLeft, charRight)

            # Update the buffer with the smushed character
            self.updateSmushedCharInLeftBuffer(addLeft, row, smushed)

    def addCurCharRowToBufferRow(
        self, curChar: List[str], row: int, smushAmount: int = 0
    ) -> None:
        """
        Add a row of the current character to the buffer, handling smushing.

        Args:
            curChar: Current character rows
            row: Row index
            smushAmount: Amount of horizontal space to smush
        """
        # Handle smushing if needed
        if smushAmount > 0:
            self.smushRow(
                curChar, row, smushAmount
            )  # Apply smushing rules to overlapping segments

        # Calculate new content to add (skip smushed portion)
        addString = (
            curChar[row][smushAmount:] if smushAmount < len(curChar[row]) else ""
        )

        # Add to buffer row
        self.buffer[row] += addString

    def cutBufferCommon(self) -> None:
        """Common processing after cutting the buffer."""
        # Format the cut buffer for output
        formattedBuffer = self.formatProduct()

        # Add to product
        self.product.append(formattedBuffer)
        self.product.append("\n")  # Add newline after cut

    def cutBufferAtLastBlank(
        self, saved_buffer: List[str], saved_iterator: int
    ) -> None:
        """
        Cut the buffer at the last blank for word wrapping.

        Args:
            saved_buffer: Buffer state before overflow
            saved_iterator: Iterator position before overflow
        """
        # Determine optimal cut position
        lastBlank = self._state["last_blank"]

        # Process text up to the last blank
        self.buffer = []  # Clear current buffer
        saved_iterator = self.iterator  # Save current position

        # Reset and process up to last blank
        self.iterator = 0
        self._state["last_blank"] = -1

        # Process characters up to last blank
        while self.iterator < lastBlank:
            self.addCharToProduct()
            self.goToNextChar()

        # Flush buffer and handle common post-cutting tasks
        self.flushLastBuffer()

        # Jump ahead to character after blank
        self.iterator = lastBlank + 1
        self._state["last_blank"] = -1

        # Record this wrap for metrics
        self._state["forced_breaks"] += 1

    def cutBufferAtLastChar(self) -> None:
        """
        Cut the buffer at the current character position.
        Used when no suitable word break is found and width is exceeded.
        """
        # Simply flush the current buffer and continue
        self.flushLastBuffer()

        # Record this break for metrics
        self._state["forced_breaks"] += 1

    def blankExist(self, last_blank: int) -> bool:
        """
        Check if a valid blank space exists for word wrapping.

        Args:
            last_blank: Position of the last blank

        Returns:
            True if a usable blank exists, False otherwise
        """
        return last_blank > -1

    def getLastBlank(self) -> int:
        """
        Get the position of the last blank space for word wrapping.

        Returns:
            Position of the last blank, or -1 if none
        """
        return self._state["last_blank"]

    def handleNewLine(self) -> None:
        """Handle an explicit newline in the input text."""
        # Flush the current buffer
        self.flushLastBuffer()

        # Add a newline to the product
        self.product.append("\n")

        # Reset tracking state
        self._state["last_blank"] = -1

    def justifyString(self, justify: str, buffer: str) -> str:
        """
        Apply justification to the output text.

        Args:
            justify: Justification mode ('left', 'center', 'right')
            buffer: Text to justify

        Returns:
            Justified text
        """
        if justify == "left":
            return buffer  # Already left-justified

        lines = buffer.split("\n")
        result = []

        # Calculate the maximum line length
        maxLength = max((len(line) for line in lines), default=0)

        for line in lines:
            if not line:  # Skip empty lines
                result.append("")
                continue

            lineLen = len(line)

            if justify == "center":
                # Center text with even padding
                padding = (self.width - lineLen) // 2
                padding = max(0, padding)  # Ensure non-negative
                result.append(" " * padding + line)

            elif justify == "right":
                # Right-align text
                padding = self.width - lineLen
                padding = max(0, padding)  # Ensure non-negative
                result.append(" " * padding + line)

        return "\n".join(result)

    def replaceHardblanks(self, buffer: str) -> str:
        """
        Replace hardblanks with regular spaces.

        Args:
            buffer: Text containing hardblanks

        Returns:
            Text with hardblanks replaced by spaces
        """
        if not buffer:
            return buffer

        return buffer.replace(self.font.hardblank, " ")

    def smushAmount(self, buffer: List[str] = None, curChar: List[str] = None) -> int:
        """
        Calculate the amount of smushing possible between two characters.

        Args:
            buffer: Current buffer (defaults to self.buffer)
            curChar: Current character (defaults to current character)

        Returns:
            Amount of horizontal space to smush (0 means no smushing)
        """
        if buffer is None:
            buffer = self.buffer

        if curChar is None:
            curChar = self.getCurChar()

        if not buffer or not curChar:
            return 0

        # Determine max possible smushing amount
        maxSmush = 0

        for row in range(self.font.height):
            # Skip if either row is empty
            if row >= len(buffer) or row >= len(curChar):
                continue

            lineLeft = buffer[row].rstrip("\0")
            lineRight = curChar[row].rstrip("\0")

            if not lineLeft or not lineRight:
                continue

            # Find the rightmost non-space in left line
            rightMostChar = len(lineLeft) - 1
            while rightMostChar >= 0 and lineLeft[rightMostChar] == " ":
                rightMostChar -= 1

            # Find the leftmost non-space in right line
            leftMostChar = 0
            while leftMostChar < len(lineRight) and lineRight[leftMostChar] == " ":
                leftMostChar += 1

            # Determine overlap
            overlapAmount = rightMostChar + leftMostChar - len(lineLeft) + 2

            # Update max smushing amount
            if overlapAmount > maxSmush:
                maxSmush = overlapAmount

        # Ensure non-negative result
        return max(0, maxSmush)

    def smushChars(self, left: str = "", right: str = "") -> str:
        """
        Smush two characters according to the font's smushing rules.

        Args:
            left: Left character
            right: Right character

        Returns:
            Result of smushing the two characters
        """
        if left == " ":
            return right
        elif right == " ":
            return left

        # Universal smushing - later character wins
        if self.font.old_layout == -1:
            return right

        # Apply smushing rules based on font settings
        if self.font.old_layout & 1:  # Rule 1: Equal character smushing
            if left == right:
                return left

        if self.font.old_layout & 2:  # Rule 2: Underscore smushing
            if left == "_" and right in "|/\\[]{}()<>":
                return right
            if right == "_" and left in "|/\\[]{}()<>":
                return left

        if self.font.old_layout & 4:  # Rule 3: Hierarchy smushing
            classes = "| /\\ [] {} () <>"
            leftClass = classes.find(left)
            rightClass = classes.find(right)

            if leftClass != -1 and rightClass != -1:
                if leftClass > rightClass:
                    return left
                else:
                    return right

        if self.font.old_layout & 8:  # Rule 4: Opposite pair smushing
            pairs = {"[": "]", "]": "[", "{": "}", "}": "{", "(": ")", ")": "("}

            if left in pairs and right == pairs[left]:
                return "|"

        if self.font.old_layout & 16:  # Rule 5: Big X smushing
            if left == "/" and right == "\\":
                return "|"
            if left == "\\" and right == "/":
                return "Y"
            if left == ">" and right == "<":
                return "X"

        if self.font.old_layout & 32:  # Rule 6: Hardblank smushing
            if left == self.font.hardblank and right == self.font.hardblank:
                return self.font.hardblank

        # No applicable rules, so default to first character
        return left
