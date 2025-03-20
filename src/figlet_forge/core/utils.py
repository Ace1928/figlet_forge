import sys

# Define unicode_string for Python 2/3 compatibility
try:
    import unicode

    unicode_string = unicode
except NameError:  # Python 3
    unicode_string = str


# Import needed for circular imports in a clean way
def lazy_import():
    from ..figlet import Figlet
    from ..version import DEFAULT_FONT, RESET_COLORS

    return DEFAULT_FONT, RESET_COLORS, Figlet


def figlet_format(text, font=None, **kwargs):
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


def print_figlet(text, font=None, colors=":", **kwargs):
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
    if colors and colors != ":" and "parse_color" in locals():
        sys.stdout.write(RESET_COLORS)
        sys.stdout.flush()
