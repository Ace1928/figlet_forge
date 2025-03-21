#!/usr/bin/env python3
"""
ASCII to SVG Conversion Example.

This script demonstrates how to convert ASCII art text to SVG format
using Figlet Forge's rendering capabilities.
"""

import sys
from pathlib import Path

# Add the package to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from figlet_forge import Figlet
from figlet_forge.render.figlet_engine import RenderEngine


def main():
    """Demonstrate ASCII to SVG conversion."""
    # Get text from command line or use default
    text = sys.argv[1] if len(sys.argv) > 1 else "SVG Art!"

    # Create Figlet instance with a nice font
    fig = Figlet(font="slant", width=100, justify="center")

    # Render the text to ASCII art
    ascii_art = fig.renderText(text)

    # Add a border for better visual appearance
    bordered_art = ascii_art.border()

    # Print the ASCII art to console
    print("ASCII Art:")
    print(bordered_art)

    # Convert to SVG
    svg_options = {
        "font_family": "monospace, 'Courier New', Courier",
        "font_size": 16,
        "fg_color": "#333",
        "bg_color": "#f8f8f8",
        "padding": 20,
    }
    svg_content = RenderEngine.to_svg(str(bordered_art), svg_options)

    # Save to file
    output_file = "figlet_svg_output.svg"
    with open(output_file, "w") as f:
        f.write(svg_content)

    print(f"\nSVG version saved to '{output_file}'")
    print("You can open it in a web browser or SVG editor.")


if __name__ == "__main__":
    main()
