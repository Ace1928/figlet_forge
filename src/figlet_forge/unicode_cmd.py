"""
Unicode System Command Interface for Figlet Forge.

This module provides a comprehensive interface to the system unicode command,
enabling advanced character lookups, transformations, and information retrieval
according to Eidosian principles of clarity, functionality, and maintainability.
"""

import shutil
import subprocess
from enum import Enum
from typing import List, Optional, Union

# Define constants
DEFAULT_CHARSET = "UTF-8"
DEFAULT_MAX_COUNT = 10


class UnicodeInputMode(Enum):
    """Input modes for the unicode command."""

    AUTO = "auto"
    HEXADECIMAL = "hexadecimal"
    OCTAL = "octal"
    BINARY = "binary"
    DECIMAL = "decimal"
    REGEXP = "regexp"
    STRING = "string"


class UnicodeCommand:
    """
    Interface to the system unicode command with comprehensive option support.

    This class provides a Pythonic interface to all functionality of the system
    unicode command, supporting various input formats, display options, and
    output formatting capabilities.
    """

    def __init__(self):
        """Initialize the UnicodeCommand interface."""
        self._command_path = shutil.which("unicode")
        if self._command_path is None:
            raise FileNotFoundError(
                "Unicode command not found. Please ensure it is installed and in PATH."
            )

    def lookup(
        self,
        query: str,
        mode: Union[UnicodeInputMode, str] = UnicodeInputMode.AUTO,
        max_count: int = DEFAULT_MAX_COUNT,
        io_charset: str = DEFAULT_CHARSET,
        from_cp: Optional[str] = None,
        add_charset: Optional[str] = None,
        use_color: Optional[str] = None,
        verbose: bool = False,
        wikipedia: bool = False,
        wiktionary: bool = False,
        brief: bool = False,
        format_string: Optional[str] = None,
    ) -> str:
        """
        Look up Unicode information using the system unicode command.

        Args:
            query: The character, codepoint, or pattern to look up
            mode: Input interpretation mode (auto, hexadecimal, etc.)
            max_count: Maximum number of codepoints to display (0=unlimited)
            io_charset: I/O character set
            from_cp: Convert numerical arguments from this encoding
            add_charset: Show hexadecimal representation in additional charset
            use_color: Whether to use colors ('on', 'off', 'auto')
            verbose: Increase verbosity (reads Unihan properties)
            wikipedia: Query Wikipedia for the character
            wiktionary: Query Wiktionary for the character
            brief: Use brief output format
            format_string: Custom formatting string

        Returns:
            Output from the unicode command as a string

        Raises:
            subprocess.SubprocessError: If the unicode command fails
            FileNotFoundError: If the unicode command is not found
        """
        # Build command arguments
        args = [self._command_path]

        # Process mode
        if isinstance(mode, UnicodeInputMode):
            mode = mode.value

        if mode == UnicodeInputMode.HEXADECIMAL.value:
            args.append("--hexadecimal")
        elif mode == UnicodeInputMode.OCTAL.value:
            args.append("--octal")
        elif mode == UnicodeInputMode.BINARY.value:
            args.append("--binary")
        elif mode == UnicodeInputMode.DECIMAL.value:
            args.append("--decimal")
        elif mode == UnicodeInputMode.REGEXP.value:
            args.append("--regexp")
        elif mode == UnicodeInputMode.STRING.value:
            args.append("--string")
        elif mode == UnicodeInputMode.AUTO.value:
            args.append("--auto")

        # Add other options
        if max_count != DEFAULT_MAX_COUNT:
            args.extend(["--max", str(max_count)])

        if io_charset != DEFAULT_CHARSET:
            args.extend(["--io", io_charset])

        if from_cp:
            args.extend(["--fromcp", from_cp])

        if add_charset:
            args.extend(["--charset-add", add_charset])

        if use_color:
            args.extend(["--colour", use_color])

        if verbose:
            args.append("--verbose")

        if wikipedia:
            args.append("--wikipedia")

        if wiktionary:
            args.append("--wiktionary")

        if brief:
            args.append("--brief")

        if format_string:
            args.extend(["--format", format_string])

        # Add the query
        args.append(query)

        # Execute the command
        try:
            result = subprocess.run(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            if e.stderr:
                return f"Unicode command error: {e.stderr}"
            return f"Unicode command failed with code {e.returncode}"

    def list_encodings(self) -> List[str]:
        """
        List all known character encodings.

        Returns:
            List of available character encodings
        """
        try:
            result = subprocess.run(
                [self._command_path, "--list"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            # Parse the output to get the list of encodings
            return [line.strip() for line in result.stdout.splitlines() if line.strip()]
        except subprocess.CalledProcessError as e:
            if e.stderr:
                raise RuntimeError(f"Unicode command error: {e.stderr}")
            raise RuntimeError(f"Unicode command failed with code {e.returncode}")

    def display_ascii_table(self, brexit: bool = False) -> str:
        """
        Display ASCII table.

        Args:
            brexit: Whether to use the EU-UK Trade and Cooperation Agreement version

        Returns:
            ASCII table as a string
        """
        args = [self._command_path]

        if brexit:
            args.append("--brexit-ascii")
        else:
            args.append("--ascii")

        try:
            result = subprocess.run(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            if e.stderr:
                return f"Unicode command error: {e.stderr}"
            return f"Unicode command failed with code {e.returncode}"

    def download_unicode_data(self) -> bool:
        """
        Download UnicodeData.txt.

        Returns:
            True if successful, False otherwise
        """
        try:
            result = subprocess.run(
                [self._command_path, "--download"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            return "downloaded successfully" in result.stdout.lower()
        except subprocess.CalledProcessError:
            return False


def get_unicode_info(
    char: str, mode: UnicodeInputMode = UnicodeInputMode.STRING, verbose: bool = False
) -> str:
    """
    Get Unicode information for a character or codepoint.

    Convenience function for quick character lookups.

    Args:
        char: Character or codepoint to look up
        mode: Input interpretation mode
        verbose: Whether to show verbose information

    Returns:
        Unicode information as a string

    Raises:
        FileNotFoundError: If the unicode command is not available
    """
    try:
        cmd = UnicodeCommand()
        return cmd.lookup(char, mode=mode, verbose=verbose)
    except FileNotFoundError:
        return f"System unicode command not available. Character: {char}"


# Test if unicode command is available on the system
def is_available() -> bool:
    """
    Check if the system unicode command is available.

    Returns:
        True if the unicode command is available, False otherwise
    """
    return shutil.which("unicode") is not None
