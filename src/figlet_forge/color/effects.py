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
from typing import List, Optional, Tuple, Union

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
    result = []
    color_index = 0

    for char in text:
        if char.isspace():
            result.append(char)
            continue

        color = rainbow_colors[color_index % len(rainbow_colors)]
        color_index += 1

        # Apply foreground color
        ansi_code = f"\033[{COLOR_CODES[color]}m"

        # Apply background if specified
        if background and background in COLOR_CODES:
            bg_code = COLOR_CODES[background] + 10  # Convert to background code
            ansi_code += f"\033[{bg_code}m"

        result.append(f"{ansi_code}{char}\033[0m")

    return "".join(result)


def gradient_colorize(
    text: str,
    start_color: Union[str, Tuple[int, int, int]],
    end_color: Union[str, Tuple[int, int, int]],
    background: Optional[str] = None,
) -> str:
    """
    Apply a color gradient across text.

    Args:
        text: The text to colorize
        start_color: Starting color (name or RGB tuple)
        end_color: Ending color (name or RGB tuple)
        background: Optional background color name

    Returns:
        ANSI-colored text with gradient effect
    """
    if not text:
        return ""

    # Convert color names to RGB if needed
    if isinstance(start_color, str):
        start_color = rgb_from_name(start_color)
    if isinstance(end_color, str):
        end_color = rgb_from_name(end_color)

    # Get visible (non-space) character count for gradient calculation
    visible_chars = sum(1 for c in text if not c.isspace())
    if visible_chars <= 1:
        visible_chars = 2  # Ensure at least 2 steps for gradient

    # Generate gradient colors
    colors = generate_gradient(start_color, end_color, visible_chars)

    # Apply gradient to text
    result = []
    color_index = 0

    for char in text:
        if char.isspace():
            result.append(char)
            continue

        r, g, b = colors[color_index]
        color_index += 1

        # Apply foreground color
        ansi_code = f"\033[38;2;{r};{g};{b}m"

        # Apply background if specified
        if background:
            if background in COLOR_CODES:
                bg_code = COLOR_CODES[background] + 10
                ansi_code += f"\033[{bg_code}m"
            else:
                # Try as RGB format
                try:
                    bg_r, bg_g, bg_b = rgb_from_name(background)
                    ansi_code += f"\033[48;2;{bg_r};{bg_g};{bg_b}m"
                except InvalidColor:
                    pass  # Ignore invalid background color

        result.append(f"{ansi_code}{char}\033[0m")

    return "".join(result)


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


def random_colorize(text: str, exclude_colors: Optional[List[str]] = None) -> str:
    """
    Apply random colors to each character in the text.

    Args:
        text: The text to colorize
        exclude_colors: Colors to exclude from randomization

    Returns:
        Text with random colors applied
    """
    if not text:
        return ""

    # Prepare available colors
    available_colors = list(COLOR_CODES.keys())
    if exclude_colors:
        available_colors = [c for c in available_colors if c not in exclude_colors]

    # Remove non-color entries
    for special in ["RESET", "DEFAULT"]:
        if special in available_colors:
            available_colors.remove(special)

    # Apply random colors
    result = []
    for char in text:
        if char.isspace():
            result.append(char)
            continue

        color = random.choice(available_colors)
        result.append(f"\033[{COLOR_CODES[color]}m{char}\033[0m")

    return "".join(result)
