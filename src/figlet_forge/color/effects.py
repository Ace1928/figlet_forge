"""
Advanced color effects for Figlet Forge typography.

This module provides specialized color transformation and effect functions
that can be applied to figlet text output, creating visually striking results
while maintaining typographic integrity.

Design follows Eidosian principles:
- Flow like water, strike like lightning: effects chain seamlessly
- Structure as control: type safety ensures predictable outcomes
- Exhaustive but concise: rich capabilities with minimal complexity
"""

import random
from typing import Optional, Tuple

from ..core.exceptions import InvalidColor
from .figlet_color import COLOR_CODES, generate_gradient, rgb_from_name


def rainbow_colorize(text: str, background: Optional[str] = None) -> str:
    """
    Apply rainbow coloration to text characters.

    Args:
        text: The text to colorize
        background: Optional background color name

    Returns:
        ANSI-colored text with rainbow effect
    """
    if not text:
        return ""

    rainbow_colors = ["RED", "YELLOW", "GREEN", "CYAN", "BLUE", "MAGENTA"]
    bg_code = ""

    # Set background color if provided
    if background:
        try:
            bg_value = COLOR_CODES.get(background.upper())
            if bg_value:
                bg_code = f"\033[{int(bg_value) + 10}m"
        except (KeyError, ValueError):
            # Silently fail on invalid background
            pass

    # Process the text line by line to maintain structure
    result = []
    lines = text.splitlines()

    for line in lines:
        colored_line = []
        color_index = 0

        for char in line:
            if char.strip():  # Only colorize non-whitespace
                color = rainbow_colors[color_index % len(rainbow_colors)]
                fg_code = f"\033[{COLOR_CODES[color]}m"
                colored_line.append(f"{fg_code}{bg_code}{char}\033[0m")
                color_index += 1
            else:
                # Preserve whitespace without color
                colored_line.append(char)

        result.append("".join(colored_line))

    return "\n".join(result)


def gradient_colorize(
    text: str, start_color: str, end_color: str, background: Optional[str] = None
) -> str:
    """
    Apply a smooth gradient between two colors across the text.

    Args:
        text: The text to colorize
        start_color: Starting color name or RGB tuple
        end_color: Ending color name or RGB tuple
        background: Optional background color name

    Returns:
        ANSI-colored text with gradient effect

    Raises:
        InvalidColor: If provided colors are invalid
    """
    if not text:
        return ""

    lines = text.splitlines()
    if not lines:
        return ""

    # Get RGB values from color names
    try:
        start_rgb = (
            rgb_from_name(start_color) if isinstance(start_color, str) else start_color
        )
        end_rgb = rgb_from_name(end_color) if isinstance(end_color, str) else end_color
    except InvalidColor as e:
        # Graceful fallback with error message
        return f"\033[31mError: {str(e)}\033[0m\n{text}"

    # Set background if provided
    bg_code = ""
    if background:
        try:
            bg_value = COLOR_CODES.get(background.upper())
            if bg_value:
                bg_code = f"\033[{int(bg_value) + 10}m"
        except (KeyError, ValueError):
            pass

    # Count visible characters for gradient calculation
    visible_chars = sum(sum(1 for c in line if c.strip()) for line in lines)
    if visible_chars < 2:
        # Not enough visible characters for gradient
        return text

    # Generate gradient colors
    gradient = generate_gradient(start_rgb, end_rgb, visible_chars)

    # Apply gradient to text
    result = []
    char_count = 0

    for line in lines:
        colored_line = []
        for char in line:
            if char.strip():  # Only colorize non-whitespace
                r, g, b = gradient[char_count]
                fg_code = f"\033[38;2;{r};{g};{b}m"
                colored_line.append(f"{fg_code}{bg_code}{char}\033[0m")
                char_count += 1
            else:
                colored_line.append(char)
        result.append("".join(colored_line))

    return "\n".join(result)


def highlight_pattern(
    text: str,
    pattern: str,
    highlight_color: str = "YELLOW",
    base_color: str = "DEFAULT",
    case_sensitive: bool = False,
) -> str:
    """
    Highlight specific patterns in text with a different color.

    Args:
        text: The text to process
        pattern: The pattern to highlight
        highlight_color: Color for highlighted sections
        base_color: Color for non-highlighted sections
        case_sensitive: Whether pattern matching is case-sensitive

    Returns:
        Colored text with highlighted patterns
    """
    if not text or not pattern:
        return text

    # Prepare for case-insensitive search if needed
    search_text = text
    search_pattern = pattern

    if not case_sensitive:
        search_text = text.lower()
        search_pattern = pattern.lower()

    result = []
    last_end = 0

    # Find all occurrences of the pattern
    start = search_text.find(search_pattern)
    while start >= 0:
        # Add text before match with base color
        if start > last_end:
            prefix = text[last_end:start]
            result.append(f"\033[{COLOR_CODES[base_color]}m{prefix}")

        # Add the match with highlight color
        end = start + len(pattern)
        match = text[start:end]
        result.append(f"\033[{COLOR_CODES[highlight_color]}m{match}")

        # Update position and find next match
        last_end = end
        start = search_text.find(search_pattern, end)

    # Add any remaining text
    if last_end < len(text):
        suffix = text[last_end:]
        result.append(f"\033[{COLOR_CODES[base_color]}m{suffix}")

    # Add reset code at the end
    result.append("\033[0m")

    return "".join(result)


def animate_prepare(
    text: str,
    animation_type: str = "blink",
    fg_color: str = "DEFAULT",
    bg_color: Optional[str] = None,
) -> str:
    """
    Prepare text with ANSI animation codes.

    Note: Animation support depends on the terminal emulator.

    Args:
        text: The text to animate
        animation_type: Type of animation ("blink", "bold", etc.)
        fg_color: Foreground color
        bg_color: Background color

    Returns:
        Text with appropriate ANSI animation codes
    """
    if not text:
        return ""

    # Define animation ANSI codes
    animation_codes = {
        "blink": "\033[5m",
        "bold": "\033[1m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "reverse": "\033[7m",  # Inverts fg and bg colors
    }

    # Get animation code
    anim_code = animation_codes.get(animation_type.lower(), "")

    # Build color codes
    color_code = ""
    if fg_color in COLOR_CODES:
        color_code += f"\033[{COLOR_CODES[fg_color]}m"

    if bg_color and bg_color in COLOR_CODES:
        bg_value = COLOR_CODES[bg_color] + 10
        color_code += f"\033[{bg_value}m"

    # Apply codes
    return f"{color_code}{anim_code}{text}\033[0m"


def random_colorize(text: str, background: Optional[str] = None) -> str:
    """
    Apply random coloration to each character in the text.

    Args:
        text: The text to colorize
        background: Optional background color name

    Returns:
        ANSI-colored text with random colors
    """
    if not text:
        return ""

    color_names = [c for c in COLOR_CODES.keys() if c != "RESET"]
    bg_code = ""

    # Set background if provided
    if background:
        try:
            bg_value = COLOR_CODES.get(background.upper())
            if bg_value:
                bg_code = f"\033[{int(bg_value) + 10}m"
        except (KeyError, ValueError):
            pass

    # Process text line by line
    result = []
    lines = text.splitlines()

    for line in lines:
        colored_line = []
        for char in line:
            if char.strip():  # Only colorize non-whitespace
                color = random.choice(color_names)
                fg_code = f"\033[{COLOR_CODES[color]}m"
                colored_line.append(f"{fg_code}{bg_code}{char}\033[0m")
            else:
                colored_line.append(char)

        result.append("".join(colored_line))

    return "\n".join(result)


def pulse_colorize(
    text: str, color: str, intensity_range: Tuple[float, float] = (0.4, 1.0)
) -> str:
    """
    Create a pulsing effect by varying the intensity of a color.

    Args:
        text: The text to colorize
        color: Base color name
        intensity_range: Tuple of (min, max) intensity values (0.0-1.0)

    Returns:
        ANSI-colored text with pulsing effect

    Raises:
        InvalidColor: If provided color is invalid
    """
    if not text:
        return ""

    # Get base RGB values
    try:
        base_rgb = rgb_from_name(color) if isinstance(color, str) else color
    except InvalidColor as e:
        return f"\033[31mError: {str(e)}\033[0m\n{text}"

    r, g, b = base_rgb
    min_intensity, max_intensity = intensity_range

    # Count visible characters
    lines = text.splitlines()
    visible_chars = sum(sum(1 for c in line if c.strip()) for line in lines)

    # Generate intensity values in a sine-wave pattern
    intensities = []
    import math

    for i in range(visible_chars):
        # Create sine wave between min and max intensity
        ratio = (math.sin(i * 0.5) + 1) / 2  # Value between 0 and 1
        intensity = min_intensity + ratio * (max_intensity - min_intensity)
        intensities.append(intensity)

    # Apply pulsing effect
    result = []
    char_count = 0

    for line in lines:
        colored_line = []
        for char in line:
            if char.strip():
                intensity = intensities[char_count % len(intensities)]
                # Scale RGB values by intensity
                pulse_r = int(r * intensity)
                pulse_g = int(g * intensity)
                pulse_b = int(b * intensity)
                fg_code = f"\033[38;2;{pulse_r};{pulse_g};{pulse_b}m"
                colored_line.append(f"{fg_code}{char}\033[0m")
                char_count += 1
            else:
                colored_line.append(char)

        result.append("".join(colored_line))

    return "\n".join(result)
