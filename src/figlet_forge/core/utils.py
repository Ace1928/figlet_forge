import subprocess
import sys
from typing import Any, Optional, Tuple

# Define unicode_string for Python 2/3 compatibility
# Instead of importing unicode package, define based on Python version
if sys.version_info[0] >= 3:
    unicode_string = str
else:
    unicode_string = unicode  # type: ignore # noqa


# Import needed for circular imports in a clean way
def lazy_import() -> Tuple[str, str, Any]:
    """Import Figlet-related components lazily to avoid circular imports.

    Returns:
        Tuple containing DEFAULT_FONT, RESET_COLORS, and Figlet class
    """
    from ..figlet import Figlet
    from ..version import DEFAULT_FONT, RESET_COLORS

    return DEFAULT_FONT, RESET_COLORS, Figlet


def figlet_format(text: str, font: Optional[str] = None, **kwargs: Any) -> str:
    """Format text in figlet style.

    Args:
        text: The text to render in figlet style
        font: Name of the figlet font to use
        **kwargs: Additional parameters passed to Figlet

    Returns:
        FigletString containing the rendered ASCII art
    """
    DEFAULT_FONT, _, Figlet = lazy_import()
    fig = Figlet(font=font or DEFAULT_FONT, **kwargs)
    return fig.renderText(text)


def print_figlet(
    text: str, font: Optional[str] = None, colors: str = ":", **kwargs: Any
) -> None:
    """Print figlet-formatted text to stdout with optional colors.

    This is a convenience function that creates a Figlet instance,
    renders the text, and prints it with specified colors.

    Args:
        text: The text to render in figlet style
        font: Name of the figlet font to use
        colors: Color specification string in "foreground:background" format
        **kwargs: Additional parameters passed to Figlet
    """
    DEFAULT_FONT, RESET_COLORS, _ = lazy_import()

    # Generate the figlet text
    result = figlet_format(text, font=font, **kwargs)

    # Apply colors if specified
    ansi_colors = None
    if colors and colors != ":":
        try:
            from ..color import parse_color

            ansi_colors = parse_color(colors)
            if ansi_colors:
                sys.stdout.write(ansi_colors)
        except ImportError:
            # Graceful fallback if color module not available
            pass

    # Print the result
    print(result)

    # Reset colors if needed
    if ansi_colors:
        sys.stdout.write(RESET_COLORS)
        sys.stdout.flush()


# Function to check if system unicode command is available
def has_unicode_command() -> bool:
    """Check if the system unicode command is available.

    Returns:
        True if the unicode command is available, False otherwise
    """
    try:
        result = subprocess.run(
            ["unicode", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.SubprocessError):
        return False
