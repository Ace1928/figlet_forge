#!/usr/bin/env python
"""
Main CLI entry point for Figlet Forge.

This module provides the command-line interface for the Figlet Forge system,
allowing users to create ASCII text art with various styling options.
"""

import os
import sys
from optparse import OptionParser
from typing import List, Optional

from figlet_forge.color.figlet_color import (
    COLOR_CODES,
    RESET_COLORS,
    parse_color,
)
from figlet_forge.core.exceptions import FigletError, FontNotFound, InvalidColor

# Import the FigletFont class
from figlet_forge.core.figlet_font import FigletFont

# Import the Figlet class from the local package
from figlet_forge.figlet import Figlet

from ..version import __version__

# Default font for rendering
DEFAULT_FONT = "standard"


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the Figlet Forge CLI.

    Args:
        args: Command line arguments (uses sys.argv if None)

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = OptionParser(version=__version__, usage="%prog [options] [text..]")

    # Add debug option for troubleshooting
    parser.add_option(
        "--debug",
        action="store_true",
        default=False,
        help="enable debug output for troubleshooting",
    )
    parser.add_option(
        "-f",
        "--font",
        default=DEFAULT_FONT,
        help="font to render with (default: %default)",
        metavar="FONT",
    )
    parser.add_option(
        "-D",
        "--direction",
        type="choice",
        choices=("auto", "left-to-right", "right-to-left"),
        default="auto",
        metavar="DIRECTION",
        help="set direction text will be formatted in " "(default: %default)",
    )
    parser.add_option(
        "-j",
        "--justify",
        type="choice",
        choices=("auto", "left", "center", "right"),
        default="auto",
        metavar="SIDE",
        help="set justification, defaults to print direction",
    )
    parser.add_option(
        "-w",
        "--width",
        type="int",
        default=80,
        metavar="COLS",
        help="set terminal width for wrapping/justification " "(default: %default)",
    )
    parser.add_option(
        "-r",
        "--reverse",
        action="store_true",
        default=False,
        help="shows mirror image of output text",
    )
    parser.add_option(
        "-n",
        "--normalize-surrounding-newlines",
        action="store_true",
        default=False,
        help="output has one empty line before and after",
    )
    parser.add_option(
        "-s",
        "--strip-surrounding-newlines",
        action="store_true",
        default=False,
        help="removes empty leading and trailing lines",
    )
    parser.add_option(
        "-F",
        "--flip",
        action="store_true",
        default=False,
        help="flips rendered output text over",
    )
    parser.add_option(
        "-l",
        "--list-fonts",
        action="store_true",
        default=False,
        help="show installed fonts list",
    )
    parser.add_option(
        "-i",
        "--info-font",
        action="store_true",
        default=False,
        help="show font's information, use with -f FONT",
    )
    parser.add_option(
        "-L",
        "--load",
        default=None,
        help="load and install the specified font definition",
    )
    parser.add_option(
        "-c",
        "--color",
        default=None,  # Changed from ":" to None for clarity
        help="""prints text with passed foreground color,
                            --color=foreground:background
                            --color=:background\t\t\t # only background
                            --color=foreground | foreground:\t # only foreground
                            --color=list\t\t\t # list all colors
                            COLOR = list[COLOR] | [0-255];[0-255];[0-255] (RGB)""",
    )
    parser.add_option(
        "-u",
        "--unicode",
        action="store_true",
        default=False,
        help="enable Unicode character support for rendering",
    )

    # Sample options
    parser.add_option(
        "--sample",
        action="store_true",
        default=False,
        help="show text rendered in all available fonts",
    )
    parser.add_option(
        "--sample-color",
        action="store_true",
        default=False,
        help="show text with various color combinations",
    )
    parser.add_option(
        "--interactive",
        action="store_true",
        default=False,
        help="in sample mode, pause after each font for user input",
    )
    parser.add_option(
        "--max-samples",
        type="int",
        default=100,
        help="maximum number of fonts to sample (default: %default)",
    )

    if args is None:
        args = sys.argv[1:]

    opts, args = parser.parse_args(args)

    # Enable or disable debugging
    if opts.debug:
        import logging

        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debug logging enabled")

    # Handle samples mode - this takes precedence over other operations
    if opts.sample or opts.sample_color:
        from .sample import DEFAULT_SAMPLE_TEXT, run_samples

        # Get sample text either from args or use default
        sample_text = " ".join(args) if args else DEFAULT_SAMPLE_TEXT

        run_samples(
            text=sample_text,
            show_fonts=opts.sample,
            show_colors=opts.sample_color,
            interactive=opts.interactive,
            width=opts.width,
            max_fonts=opts.max_samples,
        )
        return 0

    if opts.list_fonts:
        print("\n".join(sorted(FigletFont.getFonts())))
        return 0

    if opts.color == "list":
        print("[0-255];[0-255];[0-255] # RGB\n" + "\n".join(sorted(COLOR_CODES.keys())))
        return 0

    if opts.info_font:
        print(FigletFont.infoFont(opts.font))
        return 0

    if opts.load:
        FigletFont.installFonts(opts.load)
        return 0  # Added return statement for consistency

    # Parse color option
    ansi_colors = ("", "")
    if opts.color:
        try:
            ansi_colors = parse_color(opts.color)
        except InvalidColor as e:
            sys.stderr.write(f"Error: {str(e)}\n")
            return 1

    # Get the text to render
    if len(args) == 0:
        if os.isatty(sys.stdin.fileno()):
            parser.print_help()
            return 0
        text = sys.stdin.read()
        if text == "":
            return 0
    else:
        text = " ".join(args)

    try:
        # Debug font list
        if opts.debug:
            print("Available fonts:")
            for font in sorted(FigletFont.getFonts()):
                print(f"  - {font}")
            print(f"Selected font: {opts.font}")

        fig_obj = Figlet(
            font=opts.font,
            direction=opts.direction,
            justify=opts.justify,
            width=opts.width,
            unicode_aware=opts.unicode,
        )

        rendered_text = fig_obj.renderText(text)

        # Apply text transformations
        if opts.reverse:
            rendered_text = rendered_text.reverse()

        if opts.flip:
            rendered_text = rendered_text.flip()

        if opts.normalize_surrounding_newlines:
            # Add one empty line before and after
            rendered_text = f"\n{rendered_text}\n"

        if opts.strip_surrounding_newlines:
            # Strip leading and trailing blank lines
            lines = rendered_text.split("\n")
            while lines and not lines[0].strip():
                lines.pop(0)
            while lines and not lines[-1].strip():
                lines.pop()
            rendered_text = "\n".join(lines)

        # Apply color if specified
        if opts.color and opts.color != ":":
            foreground, background = ansi_colors

            # Special handling for rainbow mode
            if foreground == "RAINBOW":
                from figlet_forge.color.effects import rainbow_colorize

                rendered_text = rainbow_colorize(rendered_text, background)
            else:
                # Regular color handling
                rendered_text = f"{foreground}{background}{rendered_text}{RESET_COLORS}"

        # Write the final text to stdout
        sys.stdout.write(rendered_text)

        # Ensure output ends with a newline if it doesn't already
        if not rendered_text.endswith("\n"):
            sys.stdout.write("\n")

        if opts.color and opts.color != ":":
            # Ensure colors are reset
            sys.stdout.write(RESET_COLORS)
            sys.stdout.flush()

        return 0

    except (FontNotFound, FigletError) as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        return 1
    except Exception as e:
        if opts.debug:
            import traceback

            traceback.print_exc()
        sys.stderr.write(f"Unexpected error: {str(e)}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
