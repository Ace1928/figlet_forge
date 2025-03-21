"""
Figlet Forge Font Resources

This package contains the default fonts for Figlet Forge, ensuring that
the package can render text even without external font files.

Font files are sourced from the original FIGlet distribution and maintain
their original licensing, which is embedded in each font file.
"""

import os
from pathlib import Path
from typing import List, Optional

# Get the directory containing font files
FONT_DIRECTORY = Path(__file__).parent
# Define subdirectories for font categories
STANDARD_DIRECTORY = FONT_DIRECTORY / "standard"
CONTRIB_DIRECTORY = FONT_DIRECTORY / "contrib"

# Check if we're running from a zipped package
if not FONT_DIRECTORY.exists():
    # Alternative lookup for packaged environment
    import importlib.resources as pkg_resources

    try:
        # This works for Python 3.9+
        FONT_DIRECTORY = pkg_resources.files("figlet_forge.fonts")
        STANDARD_DIRECTORY = pkg_resources.files("figlet_forge.fonts.standard")
        CONTRIB_DIRECTORY = pkg_resources.files("figlet_forge.fonts.contrib")
    except (AttributeError, ImportError):
        # Fallback for older Python versions
        FONT_DIRECTORY = Path(pkg_resources.resource_filename("figlet_forge", "fonts"))
        STANDARD_DIRECTORY = Path(
            pkg_resources.resource_filename("figlet_forge.fonts", "standard")
        )
        CONTRIB_DIRECTORY = Path(
            pkg_resources.resource_filename("figlet_forge.fonts", "contrib")
        )


def get_font_path(font_name: str) -> Path:
    """
    Get the path to a specific font file.

    Args:
        font_name: Name of the font (without .flf extension)

    Returns:
        Path object pointing to the font file
    """
    # Try to find the font file in various locations
    font_path = FONT_DIRECTORY / f"{font_name}.flf"
    if font_path.exists():
        return font_path

    # Check standard directory
    font_path = STANDARD_DIRECTORY / f"{font_name}.flf"
    if font_path.exists():
        return font_path

    # Check contrib directory
    font_path = CONTRIB_DIRECTORY / f"{font_name}.flf"
    if font_path.exists():
        return font_path

    # Default to the original behavior if not found
    return FONT_DIRECTORY / f"{font_name}.flf"


def list_fonts() -> List[str]:
    """
    List all available fonts in the package.

    Returns:
        List of font names (without extensions)
    """
    fonts = []

    try:
        # Get fonts from main directory
        fonts.extend([f.stem for f in FONT_DIRECTORY.glob("*.flf")])

        # Get fonts from standard directory
        if STANDARD_DIRECTORY.exists():
            fonts.extend([f.stem for f in STANDARD_DIRECTORY.glob("*.flf")])

        # Get fonts from contrib directory
        if CONTRIB_DIRECTORY.exists():
            fonts.extend([f.stem for f in CONTRIB_DIRECTORY.glob("*.flf")])

        return fonts
    except Exception:
        # Fallback for packaged environments
        import importlib.resources as pkg_resources

        try:
            # This works for Python 3.9+
            fonts = []
            fonts.extend(
                [
                    f.stem
                    for f in pkg_resources.files("figlet_forge.fonts").glob("*.flf")
                ]
            )
            try:
                fonts.extend(
                    [
                        f.stem
                        for f in pkg_resources.files(
                            "figlet_forge.fonts.standard"
                        ).glob("*.flf")
                    ]
                )
            except (ImportError, FileNotFoundError):
                pass
            try:
                fonts.extend(
                    [
                        f.stem
                        for f in pkg_resources.files("figlet_forge.fonts.contrib").glob(
                            "*.flf"
                        )
                    ]
                )
            except (ImportError, FileNotFoundError):
                pass
            return fonts
        except (AttributeError, ImportError):
            # Even more basic fallback
            return ["standard", "slant", "small", "big"]  # Minimum set
