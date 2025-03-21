"""
Figlet Forge Font Resources

This package contains the default fonts for Figlet Forge, ensuring that
the package can render text even without external font files.

Font files are sourced from the original FIGlet distribution and maintain
their original licensing, which is embedded in each font file.
"""

import os
from pathlib import Path

# Get the directory containing font files
FONT_DIRECTORY = Path(__file__).parent
# Check if we're running from a zipped package
if not FONT_DIRECTORY.exists():
    # Alternative lookup for packaged environment
    import importlib.resources as pkg_resources

    try:
        # This works for Python 3.9+
        FONT_DIRECTORY = pkg_resources.files("figlet_forge.fonts")
    except (AttributeError, ImportError):
        # Fallback for older Python versions
        FONT_DIRECTORY = Path(pkg_resources.resource_filename("figlet_forge", "fonts"))


def get_font_path(font_name: str) -> Path:
    """
    Get the path to a specific font file.

    Args:
        font_name: Name of the font (without .flf extension)

    Returns:
        Path object pointing to the font file
    """
    return FONT_DIRECTORY / f"{font_name}.flf"


def list_fonts() -> list:
    """
    List all available fonts in the package.

    Returns:
        List of font names (without extensions)
    """
    try:
        return [f.stem for f in FONT_DIRECTORY.glob("*.flf")]
    except Exception:
        # Fallback for packaged environments
        import importlib.resources as pkg_resources

        try:
            # This works for Python 3.9+
            return [
                f.stem for f in pkg_resources.files("figlet_forge.fonts").glob("*.flf")
            ]
        except (AttributeError, ImportError):
            # Even more basic fallback
            return ["standard", "slant", "small", "big"]  # Minimum set
