#!/usr/bin/env python
"""
Main CLI entry point for Figlet Forge.

This module provides the command-line interface for the Figlet Forge system,
allowing users to create ASCII text art from the terminal with
support for colors, unicode characters, and various layout options.
"""

import os
import sys
from optparse import OptionGroup, OptionParser
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
    parser = OptionParser(
        version=f"Figlet Forge {__version__} - Eidosian Typography Engine",
        usage="%prog [options] [text..]",
        description=(
            "Transform text into ASCII art typography with advanced styling options. "
            "An Eidosian reimplementation extending the original pyfiglet."
        ),
    )

    # Core functionality options
    group_core = OptionGroup(parser, "Core Options", "Basic functionality options")
    group_core.add_option(
        "-f",
        "--font",
        default=DEFAULT_FONT,
        help="font to render with (default: %default)",
        metavar="FONT",
    )
    group_core.add_option(
        "-D",
        "--direction",
        type="choice",
        choices=("auto", "left-to-right", "right-to-left"),
        default="auto",
        metavar="DIR",
        help="set text direction: auto, left-to-right, right-to-left (default: %default)",
    )
    group_core.add_option(
        "-j",
        "--justify",
        type="choice",
        choices=("auto", "left", "center", "right"),
        default="auto",
        metavar="SIDE",
        help="set justification: auto, left, center, right (default: %default)",
    )
    group_core.add_option(
        "-w",
        "--width",
        type="int",
        default=80,
        metavar="COLS",
        help="set terminal width for wrapping/justification (default: %default)",
    )
    parser.add_option_group(group_core)

    # Transformation options
    group_transform = OptionGroup(
        parser, "Transformation Options", "Text transformation options"
    )
    group_transform.add_option(
        "-r",
        "--reverse",
        action="store_true",
        default=False,
        help="show mirror image of output text (horizontal flip)",
    )
    group_transform.add_option(
        "-F",
        "--flip",
        action="store_true",
        default=False,
        help="flip rendered output text vertically (upside down)",
    )
    group_transform.add_option(
        "-n",
        "--normalize-surrounding-newlines",
        action="store_true",
        default=False,
        help="output has one empty line before and after",
    )
    group_transform.add_option(
        "-s",
        "--strip-surrounding-newlines",
        action="store_true",
        default=False,
        help="removes empty leading and trailing lines",
    )
    parser.add_option_group(group_transform)

    # Color options
    group_color = OptionGroup(parser, "Color Options", "Text color and style options")
    group_color.add_option(
        "-c",
        "--color",
        default=None,
        metavar="SPEC",
        help=(
            "print text with colors (formats: COLOR, FG:BG, or 255;0;0:0;0;255). "
            "Special values: rainbow, gradient:<colors>, random. "
            "Use --color=list to see available named colors."
        ),
    )
    group_color.add_option(
        "--fg",
        dest="fg_color",
        default=None,
        metavar="COLOR",
        help="shorthand for setting foreground color only",
    )
    group_color.add_option(
        "--bg",
        dest="bg_color",
        default=None,
        metavar="COLOR",
        help="shorthand for setting background color only",
    )
    parser.add_option_group(group_color)

    # Font management options
    group_fonts = OptionGroup(
        parser, "Font Management", "Font listing and installation options"
    )
    group_fonts.add_option(
        "-l",
        "--list-fonts",
        action="store_true",
        default=False,
        help="show installed fonts list",
    )
    group_fonts.add_option(
        "-i",
        "--info-font",
        action="store_true",
        default=False,
        help="show font's information, use with -f FONT",
    )
    group_fonts.add_option(
        "-L",
        "--load",
        default=None,
        metavar="PATH",
        help="load and install font file (.flf) or directory of fonts",
    )
    parser.add_option_group(group_fonts)

    # Advanced options
    group_advanced = OptionGroup(
        parser, "Advanced Options", "Extra formatting and debugging options"
    )
    group_advanced.add_option(
        "-u",
        "--unicode",
        action="store_true",
        default=False,
        help="enable Unicode character support for rendering",
    )
    group_advanced.add_option(
        "--border",
        type="choice",
        choices=("none", "single", "double", "rounded", "bold", "ascii"),
        default="none",
        help="add a border around the output (none, single, double, rounded, bold, ascii)",
    )
    group_advanced.add_option(
        "--shade",
        action="store_true",
        default=False,
        help="add shadow effect to the output",
    )
    group_advanced.add_option(
        "--debug",
        action="store_true",
        default=False,
        help="enable debug output for troubleshooting",
    )
    parser.add_option_group(group_advanced)

    # Sample/demo options
    group_samples = OptionGroup(
        parser, "Sample Options", "Font and color showcase options"
    )
    group_samples.add_option(
        "--sample",
        action="store_true",
        default=False,
        help="show text rendered in all available fonts",
    )
    group_samples.add_option(
        "--sample-color",
        action="store_true",
        default=False,
        help="show text with various color combinations",
    )
    group_samples.add_option(
        "--interactive",
        action="store_true",
        default=False,
        help="in sample mode, pause after each font for user input",
    )
    group_samples.add_option(
        "--max-samples",
        type="int",
        default=100,
        help="maximum number of fonts to sample (default: %default)",
    )
    parser.add_option_group(group_samples)

    # Output options
    group_output = OptionGroup(
        parser, "Output Options", "Control output format and destination"
    )
    group_output.add_option(
        "-o",
        "--output",
        default=None,
        metavar="FILE",
        help="write output to file instead of stdout",
    )
    group_output.add_option(
        "--format",
        type="choice",
        choices=("plain", "ansi", "html", "svg"),
        default="plain",
        help="output format: plain, ansi, html, svg (default: plain, or ansi with colors)",
    )
    parser.add_option_group(group_output)

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
        print("Available color names:")
        print("\n".join(sorted(COLOR_CODES.keys())))
        print("\nColor formats:")
        print("  COLOR_NAME              # Named color (e.g., RED)")
        print("  FG:BG                   # Foreground:Background (e.g., GREEN:BLUE)")
        print("  R;G;B                   # RGB values (e.g., 255;0;0)")
        print("  R;G;B:R;G;B             # RGB foreground:background")
        print("  rainbow                 # Rainbow effect")
        print("  random                  # Random colors")
        return 0

    if opts.info_font:
        print(FigletFont.infoFont(opts.font))
        return 0

    if opts.load:
        success = FigletFont.installFonts(opts.load)
        if success:
            print(f"Successfully installed fonts from {opts.load}")
        else:
            print(f"Failed to install fonts from {opts.load}")
        return 0 if success else 1

    # Combine color options - direct --color takes precedence over --fg/--bg
    if not opts.color and (opts.fg_color or opts.bg_color):
        fg = opts.fg_color or ""
        bg = opts.bg_color or ""
        opts.color = f"{fg}:{bg}"

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
            rendered_text = rendered_text.normalize_surrounding_newlines()

        if opts.strip_surrounding_newlines:
            # Strip leading and trailing blank lines
            rendered_text = rendered_text.strip_surrounding_newlines()

        # Apply border if requested
        if opts.border != "none":
            rendered_text = rendered_text.border(style=opts.border)

        # Apply shadow if requested
        if opts.shade:
            rendered_text = rendered_text.shadow()

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

        # Output handling
        if opts.output:
            with open(opts.output, "w") as f:
                f.write(rendered_text)
        else:
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
