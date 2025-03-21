"""
Sample generation functionality for Figlet Forge.

This module provides utilities for generating and displaying samples of
fonts and color combinations, following Eidosian principles of clarity,
elegance, and comprehensive exploration.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..color.effects import gradient_colorize, rainbow_colorize
from ..color.figlet_color import COLOR_CODES
from ..core.figlet_font import FigletFont
from ..figlet import Figlet
from ..version import __version__

# Default sample text with meaningful structure
DEFAULT_SAMPLE_TEXT = "Welcome\nTo The\nEidosian\nFiglet\nForge!"

# Limit for number of fonts to sample in one go (prevent overwhelming output)
MAX_FONTS_SAMPLE = 100

# Cache directory for samples
CACHE_DIR = Path.home() / ".figlet_forge" / "cache"

# Font usage hints - short descriptions of when to use specific fonts
FONT_USAGE_HINTS = {
    "standard": "The classic figlet font, perfect for general use",
    "slant": "Adds a dynamic, forward-leaning style to text",
    "small": "Compact representation when space is limited",
    "big": "Bold, attention-grabbing display for headlines",
    "mini": "Ultra-compact font for constrained spaces",
    "block": "Solid, impactful lettering for emphasis",
    "script": "Elegant, cursive-like appearance for a sophisticated look",
    "bubble": "Rounded, friendly letters for approachable messaging",
    "digital": "Technical, LCD-like display for a technological feel",
    "shadow": "Dimensional text with drop shadows for depth",
}

# Color combination descriptions with standardized snake_case naming
COLOR_COMBINATIONS = [
    ("RED", "BLUE", "red_to_blue", "Vibrant transition from warm to cool"),
    ("YELLOW", "GREEN", "yellow_to_green", "Nature-inspired sunny to leafy gradient"),
    ("MAGENTA", "CYAN", "magenta_to_cyan", "Striking contrast with high visibility"),
    ("WHITE", "BLUE", "white_to_blue", "Clean fade to cool blue depths"),
]

# Foreground/background pairs with standardized snake_case naming
FG_BG_PAIRS = [
    ("RED", "BLACK", "red_on_black", "Classic high-contrast combination"),
    ("GREEN", "BLACK", "green_on_black", "Terminal/matrix style"),
    ("YELLOW", "BLUE", "yellow_on_blue", "High visibility warning style"),
    ("WHITE", "RED", "white_on_red", "Bold alert messaging"),
    ("BLACK", "WHITE", "black_on_white", "Traditional print style"),
    ("CYAN", "BLACK", "cyan_on_black", "Retro computer terminal look"),
]


def ensure_cache_dir() -> Path:
    """Ensure the cache directory exists and return its path."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR


def get_cache_path(sample_type: str, text: str) -> Path:
    """
    Get the cache file path for a specific sample type and text.

    Args:
        sample_type: Type of sample ('font' or 'color')
        text: The text used in the sample

    Returns:
        Path to the cache file
    """
    # Create a deterministic filename based on content
    text_hash = str(hash(text))[:10]  # Use part of hash for filename
    return ensure_cache_dir() / f"sample_{sample_type}_{text_hash}.json"


def load_from_cache(sample_type: str, text: str) -> Optional[Dict]:
    """
    Try to load sample data from cache.

    Args:
        sample_type: Type of sample ('font' or 'color')
        text: The text used in the sample

    Returns:
        Cached sample data or None if not available/valid
    """
    cache_path = get_cache_path(sample_type, text)

    if not cache_path.exists():
        return None

    try:
        # Check if cache is recent (less than 1 day old)
        if time.time() - cache_path.stat().st_mtime > 86400:
            return None

        with open(cache_path) as f:
            data = json.load(f)

        # Validate cache structure
        if not isinstance(data, dict) or "samples" not in data:
            return None

        return data
    except (json.JSONDecodeError, OSError):
        # Invalid cache, ignore it
        return None


def save_to_cache(sample_type: str, text: str, data: Dict) -> bool:
    """
    Save sample data to cache.

    Args:
        sample_type: Type of sample ('font' or 'color')
        text: The text used in the sample
        data: The sample data to cache

    Returns:
        True if saved successfully, False otherwise
    """
    cache_path = get_cache_path(sample_type, text)

    try:
        with open(cache_path, "w") as f:
            json.dump(data, f)
        return True
    except (OSError, TypeError):
        return False


def generate_font_samples(
    text: str = DEFAULT_SAMPLE_TEXT,
    max_fonts: int = MAX_FONTS_SAMPLE,
    fonts: Optional[List[str]] = None,
    width: int = 80,
) -> Tuple[Dict[str, str], List[str]]:
    """
    Generate text samples in all available fonts.

    Args:
        text: Text to render in different fonts
        max_fonts: Maximum number of fonts to sample
        fonts: Optional list of specific fonts to sample
        width: Width for rendering

    Returns:
        Tuple of (dictionary mapping font names to rendered samples, list of failed fonts)
    """
    # Try to load from cache first
    cache = load_from_cache("font", text)
    if cache:
        return cache["samples"], cache.get("failed_fonts", [])

    # Get available fonts
    available_fonts = fonts or FigletFont.getFonts()

    # Limit number of fonts to prevent overwhelming output
    if len(available_fonts) > max_fonts:
        available_fonts = available_fonts[:max_fonts]

    samples = {}
    failed_fonts = []

    # Generate samples for each font
    for font_name in available_fonts:
        try:
            fig = Figlet(font=font_name, width=width)
            rendered = fig.renderText(text)
            samples[font_name] = rendered
            # Print success message for debugging
            print(f"✓ Loaded font: {font_name}")
        except Exception as e:
            # Record fonts that failed to load
            failed_fonts.append(font_name)
            print(f"✗ Failed to load font: {font_name} - {str(e)}")
            continue

    # Cache the results
    save_to_cache("font", text, {"samples": samples, "failed_fonts": failed_fonts})

    return samples, failed_fonts


def generate_color_matrix(
    text: str = "Figlet",
    font: str = "standard",
    width: int = 80,
) -> Dict[str, str]:
    """
    Generate a matrix of color combinations for the given text.

    Args:
        text: Text to render with colors
        font: Font to use for rendering
        width: Width for rendering

    Returns:
        Dictionary mapping color descriptions to colored samples
    """
    # Try to load from cache first
    cache_key = f"{text}_{font}"
    cache = load_from_cache("color", cache_key)
    if cache:
        return cache["samples"]

    # Generate colored samples
    try:
        fig = Figlet(font=font, width=width)
        plain_text = fig.renderText(text)

        samples = {}

        # Add rainbow sample
        samples["rainbow"] = rainbow_colorize(plain_text)

        # Add gradient samples with standardized names
        for start_color, end_color, name, _ in COLOR_COMBINATIONS:
            samples[name] = gradient_colorize(plain_text, start_color, end_color)

        # Add foreground/background combinations
        for fg, bg, name, _ in FG_BG_PAIRS:
            # Create ANSI color codes
            fg_code = f"\033[{COLOR_CODES[fg]}m" if fg in COLOR_CODES else ""
            bg_code = f"\033[{int(COLOR_CODES[bg]) + 10}m" if bg in COLOR_CODES else ""
            reset_code = "\033[0m"

            # Apply colors
            samples[name] = f"{fg_code}{bg_code}{plain_text}{reset_code}"

        # Cache the results
        save_to_cache("color", cache_key, {"samples": samples})

        return samples

    except Exception as e:
        print(f"Error generating color matrix: {str(e)}")
        # Return an empty dict if we can't generate colors
        return {}


def display_font_sample(
    font_name: str, sample: str, with_color: bool = False, interactive: bool = False
) -> None:
    """
    Display a font sample with formatting.

    Args:
        font_name: Name of the font
        sample: Rendered text sample
        with_color: Whether to add color to the header
        interactive: Whether to wait for user input between samples
    """
    # Create a visually distinctive header
    header_width = min(
        80, max(len(font_name) + 10, len(sample.splitlines()[0]) if sample else 20)
    )

    # Add color to header if requested
    header_start = "\033[1;36m" if with_color else ""  # Bright cyan, bold
    header_end = "\033[0m" if with_color else ""

    # Get usage hint if available
    usage_hint = FONT_USAGE_HINTS.get(font_name, "")

    # Print the header with standardized format
    print(f"\n{header_start}{'═' * header_width}")
    print(f" FONT: {font_name}")
    if usage_hint:
        print(f" INFO: {usage_hint}")
    print(f"{'═' * header_width}{header_end}\n")

    # Print the sample
    print(sample)

    # In interactive mode, wait for user to press Enter
    if interactive:
        input("Press Enter for next font...")


def display_color_sample(
    color_name: str, sample: str, description: str = "", interactive: bool = False
) -> None:
    """
    Display a color sample with formatting.

    Args:
        color_name: Description of the color
        sample: Colored text sample
        description: Additional description of the color style
        interactive: Whether to wait for user input between samples
    """
    # Print header and sample with standardized format
    print(f"\n\033[1;35m{'═' * 40}")  # Magenta header
    print(f" COLOR STYLE: {color_name}")
    if description:
        print(f" INFO: {description}")
    print(f"{'═' * 40}\033[0m\n")

    # Print the colored sample
    print(sample)

    # In interactive mode, wait for user to press Enter
    if interactive:
        input("Press Enter for next color style...")


def display_usage_guide(
    font_samples: Dict[str, str], color_samples: Dict[str, str]
) -> None:
    """
    Display a usage guide for the user.

    Args:
        font_samples: Dictionary of font samples that were displayed
        color_samples: Dictionary of color samples that were displayed
    """
    print("\n\033[1;32m═══ FIGLET FORGE USAGE GUIDE ═══\033[0m")
    print("Use the following commands to create your own ASCII art:")

    # Basic usage
    print("\n\033[1mBasic Usage:\033[0m")
    print("  figlet_forge 'Your Text Here'")

    # Font examples
    if font_samples:
        print("\n\033[1mUsing Specific Fonts:\033[0m")
        print("  figlet_forge --font=<font_name> 'Your Text'")
        print("\n\033[1mAvailable Fonts:\033[0m")
        # Show a sample of fonts (up to 10)
        font_list = list(font_samples.keys())[:10]
        for font in font_list:
            print(f"  figlet_forge --font={font} 'Your Text'")
        if len(font_samples) > 10:
            print(f"  ... and {len(font_samples) - 10} more fonts")

    # Color examples
    if color_samples:
        print("\n\033[1mAdding Colors:\033[0m")
        print("  figlet_forge --color=<color_style> 'Your Text'")
        print("\n\033[1mAvailable Color Styles:\033[0m")
        # Show color styles
        for color in list(color_samples.keys())[:5]:
            print(f"  figlet_forge --color={color} 'Your Text'")
        if len(color_samples) > 5:
            print(f"  ... and {len(color_samples) - 5} more color styles")

    # Combined example
    if font_samples and color_samples:
        font = next(iter(font_samples))
        color = next(iter(color_samples))
        print("\n\033[1mCombining Fonts and Colors:\033[0m")
        print(f"  figlet_forge --font={font} --color={color} 'Your Text'")

    # Additional options
    print("\n\033[1mOther Useful Options:\033[0m")
    print("  --width=<columns>     # Set output width")
    print("  --reverse             # Mirror text horizontally")
    print("  --flip                # Flip text vertically")
    print("  --unicode             # Enable Unicode character support")

    # Help and examples
    print("\n\033[1mFor More Help:\033[0m")
    print("  figlet_forge --help   # Show all available options")
    print("  figlet_forge --sample # View more font examples")

    # Version info
    print(f"\n\033[1mFiglet Forge v{__version__}\033[0m - Eidosian Typography Engine")


def run_samples(
    text: str = DEFAULT_SAMPLE_TEXT,
    show_fonts: bool = True,
    show_colors: bool = False,
    interactive: bool = False,
    width: int = 80,
    max_fonts: int = MAX_FONTS_SAMPLE,
) -> None:
    """
    Run the sample display process.

    Args:
        text: Text to render in samples
        show_fonts: Whether to show font samples
        show_colors: Whether to show color samples
        interactive: Whether to wait for user input between samples
        width: Width for rendering
        max_fonts: Maximum number of fonts to sample
    """
    # Show welcome message
    print("\n\033[1;32m═══ FIGLET FORGE SAMPLE SHOWCASE ═══\033[0m")
    print("Exploring the typographic possibilities with Figlet Forge...")

    font_samples = {}
    color_samples = {}
    displayed_fonts = []
    displayed_colors = []
    failed_fonts = []

    # Generate font samples if requested
    if show_fonts:
        font_samples, failed_fonts = generate_font_samples(
            text, max_fonts=max_fonts, width=width
        )

        # Show summary
        total_fonts = len(font_samples)
        total_failed = len(failed_fonts)

        print("\n\033[1;32m=== FONT SHOWCASE SUMMARY ===\033[0m")
        print(f"✓ Successfully loaded {total_fonts} fonts")
        if failed_fonts:
            print(
                f"✗ Failed to load {total_failed} fonts: {', '.join(failed_fonts[:5])}"
            )
            if len(failed_fonts) > 5:
                print(f"  ... and {len(failed_fonts) - 5} more")

        # Show each font sample
        for font_name, sample in font_samples.items():
            displayed_fonts.append(font_name)

            # If showing both fonts and colors, generate color samples for each font
            if show_colors:
                # Show the plain font first
                display_font_sample(
                    font_name, sample, with_color=True, interactive=False
                )

                # Then show color variants
                try:
                    color_matrix = generate_color_matrix(
                        text=(
                            text.splitlines()[0] if "\n" in text else text
                        ),  # Use first line for color samples
                        font=font_name,
                        width=width,
                    )

                    for idx, (_, _, name, description) in enumerate(COLOR_COMBINATIONS):
                        if name in color_matrix:
                            displayed_colors.append(name)
                            display_color_sample(
                                f"{font_name} - {name}",
                                color_matrix[name],
                                description=description,
                                interactive=False,
                            )

                    for idx, (_, _, name, description) in enumerate(FG_BG_PAIRS):
                        if name in color_matrix:
                            displayed_colors.append(name)
                            display_color_sample(
                                f"{font_name} - {name}",
                                color_matrix[name],
                                description=description,
                                interactive=False,
                            )

                    # Wait after all color variants are shown for this font
                    if interactive:
                        input("\nPress Enter for next font with colors...")
                except Exception as e:
                    print(
                        f"\n\033[1;31mError generating color samples for {font_name}: {e}\033[0m"
                    )
            else:
                # Just show the font without colors
                display_font_sample(
                    font_name, sample, with_color=True, interactive=interactive
                )

    elif show_colors:
        # If only showing colors without font samples, use standard font
        try:
            color_samples = generate_color_matrix(
                text=text, font="standard", width=width
            )

            # Rainbow effect
            if "rainbow" in color_samples:
                displayed_colors.append("rainbow")
                display_color_sample(
                    "rainbow",
                    color_samples["rainbow"],
                    description="Dynamic multi-color effect",
                    interactive=interactive,
                )

            # Gradients
            for start_color, end_color, name, description in COLOR_COMBINATIONS:
                if name in color_samples:
                    displayed_colors.append(name)
                    display_color_sample(
                        name,
                        color_samples[name],
                        description=description,
                        interactive=interactive,
                    )

            # FG/BG combinations
            for fg, bg, name, description in FG_BG_PAIRS:
                if name in color_samples:
                    displayed_colors.append(name)
                    display_color_sample(
                        name,
                        color_samples[name],
                        description=description,
                        interactive=interactive,
                    )
        except Exception as e:
            print(f"\n\033[1;31mError generating color samples: {e}\033[0m")

    # Show closing message
    print("\n\033[1;32m═══ END OF SHOWCASE ═══\033[0m")

    # Display usage guide
    display_usage_guide(font_samples, color_samples)
