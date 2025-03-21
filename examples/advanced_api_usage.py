#!/usr/bin/env python3
"""
Advanced API Usage Examples for Figlet Forge.

This module demonstrates sophisticated usage patterns of the
Figlet Forge library, showcasing its capabilities in a practical context.
"""

import sys
import time
from pathlib import Path

# Add the package to path when running directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from figlet_forge import Figlet
from figlet_forge.color.effects import (
    gradient_colorize,
    pulse_colorize,
    rainbow_colorize,
)
from figlet_forge.core.figlet_string import FigletString


def create_title_banner(title: str, subtitle: str = None) -> str:
    """
    Create a professional-looking title banner with optional subtitle.

    Args:
        title: Main title text
        subtitle: Optional subtitle text

    Returns:
        Formatted banner text with decorative elements
    """
    # Create the main title
    fig = Figlet(font="slant", width=80, justify="center")
    title_text = fig.renderText(title)

    # Apply gradient coloring
    colored_title = gradient_colorize(title_text, "CYAN", "BLUE")

    # Create banner structure
    banner = FigletString("═" * 80)
    result = banner + "\n" + colored_title

    # Add subtitle if provided
    if subtitle:
        small_fig = Figlet(font="small", width=80, justify="center")
        subtitle_text = small_fig.renderText(subtitle)
        colored_subtitle = pulse_colorize(subtitle_text, "LIGHT_CYAN")
        result += "\n" + colored_subtitle

    # Add bottom border
    result += "\n" + banner

    return result


def create_notice_box(text: str, style: str = "info") -> str:
    """
    Create a notice box with specified style.

    Args:
        text: The text to display
        style: Box style ('info', 'warning', 'error', 'success')

    Returns:
        Text in a decorated box
    """
    # Define style parameters
    styles = {
        "info": ("BLUE", "─ INFO ─"),
        "warning": ("YELLOW", "─ WARNING ─"),
        "error": ("RED", "─ ERROR ─"),
        "success": ("GREEN", "─ SUCCESS ─"),
    }

    color, title = styles.get(style.lower(), styles["info"])

    # Create the notice text
    fig = Figlet(font="small", width=70)
    text_art = fig.renderText(text).strip_surrounding_newlines()

    # Create the box
    box = text_art.border()

    # Apply color based on style
    return pulse_colorize(box, color)


def create_animated_text(text: str, frames: int = 10) -> list:
    """
    Create frames for animated text.

    Args:
        text: Text to animate
        frames: Number of animation frames

    Returns:
        List of frames for animation
    """
    fig = Figlet(font="standard", width=80, justify="center")
    base_text = fig.renderText(text)

    # Generate animation frames
    animation_frames = []

    # Create different color effects for each frame
    rainbow_frame = rainbow_colorize(base_text)
    animation_frames.append(rainbow_frame)

    # Create gradient frames with different color combinations
    color_pairs = [
        ("RED", "YELLOW"),
        ("YELLOW", "GREEN"),
        ("GREEN", "CYAN"),
        ("CYAN", "BLUE"),
        ("BLUE", "MAGENTA"),
        ("MAGENTA", "RED"),
    ]

    for start, end in color_pairs:
        gradient_frame = gradient_colorize(base_text, start, end)
        animation_frames.append(gradient_frame)

    # Add flipped and reversed variations
    flipped = base_text.flip()
    reversed_text = base_text.reverse()

    animation_frames.append(rainbow_colorize(flipped))
    animation_frames.append(rainbow_colorize(reversed_text))

    return animation_frames


def demonstrate_usage():
    """Run a demonstration of advanced API usage."""
    print("\n=== FIGLET FORGE ADVANCED API DEMONSTRATION ===\n")

    # Create and display a title banner
    banner = create_title_banner("Figlet Forge", "Advanced Typography Engine")
    print(banner)
    print()

    # Create and display notice boxes
    info_box = create_notice_box("This is an informational message", "info")
    print(info_box)
    print()

    warning_box = create_notice_box("Warning: Proceed with caution!", "warning")
    print(warning_box)
    print()

    # Demonstrate text animation
    print("Text Animation Demo:")
    frames = create_animated_text("Animate!")

    # Show animation frames (when running in terminal)
    if sys.stdout.isatty():
        try:
            for frame in frames * 2:  # Repeat animation twice
                # Clear previous frame
                print("\033[H\033[J")  # Clear screen
                # Print new frame
                print(frame)
                # Wait briefly
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nAnimation stopped.")
    else:
        # Just show one frame if not in a terminal
        print(frames[0])

    print("\n=== END OF DEMONSTRATION ===\n")


if __name__ == "__main__":
    demonstrate_usage()
