#!/usr/bin/env python
"""
Command line interface for Figlet Forge.

This module provides the CLI entry point and command processing
functionality for the Figlet Forge package.
"""

import argparse
import sys
import textwrap
from typing import List, Optional

from ..color import colored_format, get_coloring_functions
from ..core.utils import get_terminal_size
from ..figlet import Figlet, FigletError
from ..version import __version__
from .showcase import generate_showcase

# Default values
DEFAULT_WIDTH = 80


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Figlet Forge - ASCII art text generator with advanced features",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Examples:
              figlet_forge "Hello World"
              figlet_forge --font=slant "Hello World"
              figlet_forge --color=rainbow "Hello World"
              figlet_forge --color=red:blue --border=double "Hello World"
              figlet_forge --flip --reverse "Hello World"
              figlet_forge --version
            """
        ),
    )

    text_input = parser.add_argument_group("Text Input")
    text_input.add_argument(
        "text", nargs="*", help="Text to convert (reads from STDIN if not provided)"
    )

    font_options = parser.add_argument_group("Font Options")
    font_options.add_argument("--font", "-f", help="Font to use (default: standard)")
    font_options.add_argument(
        "--list-fonts", "-l", action="store_true", help="List available fonts"
    )

    layout_options = parser.add_argument_group("Layout Options")
    layout_options.add_argument(
        "--width",
        "-w",
        type=int,
        help="Width of output (default: terminal width or 80)",
    )
    layout_options.add_argument(
        "--justify",
        "-j",
        choices=["left", "right", "center", "auto"],
        help="Text justification (default: auto)",
    )
    layout_options.add_argument(
        "--direction",
        "-d",
        choices=["auto", "left-to-right", "right-to-left"],
        help="Text direction (default: auto)",
    )

    transform_options = parser.add_argument_group("Transformation Options")
    transform_options.add_argument(
        "--reverse", "-r", action="store_true", help="Reverse the text direction"
    )
    transform_options.add_argument(
        "--flip", action="store_true", help="Flip the text vertically"
    )
    transform_options.add_argument(
        "--border",
        choices=["single", "double", "rounded", "bold", "shadow", "ascii"],
        help="Add border around the text",
    )
    transform_options.add_argument(
        "--shade", action="store_true", help="Add shading/shadow effect"
    )

    color_options = parser.add_argument_group("Color Options")
    color_options.add_argument(
        "--color",
        "-c",
        help="Color specification (NAME, NAME:BG, rgb;g;b, or rainbow/gradient)",
    )
    color_options.add_argument(
        "--color-list",
        action="store_true",
        help="List available colors",
    )

    display_options = parser.add_argument_group("Display Options")
    display_options.add_argument(
        "--unicode", "-u", action="store_true", help="Enable Unicode character support"
    )
    display_options.add_argument(
        "--output", "-o", help="File to write output to (default: STDOUT)"
    )

    showcase_options = parser.add_argument_group("Showcase Options")
    showcase_options.add_argument(
        "--showcase",
        "--sample",
        action="store_true",
        help="Show fonts and styles showcase",
    )
    showcase_options.add_argument(
        "--sample-text", default="hello", help="Text to use in showcase"
    )
    showcase_options.add_argument("--sample-color", help="Color to use in showcase")
    showcase_options.add_argument(
        "--sample-fonts", help="Comma-separated list of fonts to include in showcase"
    )

    info_options = parser.add_argument_group("Information")
    info_options.add_argument(
        "--version", "-v", action="store_true", help="Show version information"
    )

    return parser.parse_args(args)


def read_input() -> str:
    """
    Read text from STDIN.

    Returns:
        Text read from STDIN
    """
    # Check if input is coming from a pipe or redirection
    if not sys.stdin.isatty():
        return sys.stdin.read().rstrip()
    return ""


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.

    Args:
        argv: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    args = parse_args(argv)

    try:
        # Show version information
        if args.version:
            print(f"Figlet Forge v{__version__}")
            return 0

        # List available fonts
        if args.list_fonts:
            fig = Figlet()
            fonts = fig.getFonts()
            print("Available fonts:")
            for i, font in enumerate(sorted(fonts)):
                print(f"  {font}", end="\n" if (i + 1) % 4 == 0 else "\t")
            if len(fonts) % 4 != 0:
                print()  # Ensure a newline at the end
            return 0

        # List available colors
        if args.color_list:
            list_colors()
            return 0

        # Show showcase
        if args.showcase:
            sample_fonts = None
            if args.sample_fonts:
                sample_fonts = args.sample_fonts.split(",")
            generate_showcase(
                sample_text=args.sample_text,
                fonts=sample_fonts,
                color=args.sample_color,
            )
            return 0

        # Get text from arguments or STDIN
        text = " ".join(args.text) if args.text else read_input()
        if not text:
            print("No input provided. Use 'figlet_forge --help' for usage information.")
            return 1

        # Set up Figlet
        width = args.width
        if not width:
            term_width, _ = get_terminal_size()
            width = term_width

        fig = Figlet(
            font=args.font,
            width=width,
            justify=args.justify,
            direction=args.direction,
        )

        # Render text
        result = fig.renderText(text)

        # Apply transformations
        if args.reverse:
            result = result.reverse()
        if args.flip:
            result = result.flip()
        if args.border:
            result = result.border(style=args.border)
        if args.shade:
            result = result.shadow()

        # Apply colors
        if args.color:
            color_value = args.color.lower()
            if color_value == "rainbow":
                result = get_coloring_functions()["rainbow"](str(result))
            elif "_to_" in color_value:
                try:
                    start, end = color_value.split("_to_")
                    result = get_coloring_functions()["gradient"](
                        str(result), start, end
                    )
                except ValueError:
                    result = colored_format(str(result), color_value)
            else:
                result = colored_format(str(result), color_value)

        # Output result
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(str(result))
                f.write("\n")
        else:
            sys.stdout.write(str(result))
            sys.stdout.write("\n")

        return 0

    except FigletError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Operation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
