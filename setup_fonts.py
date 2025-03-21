#!/usr/bin/env python3

"""
Setup script to install standard fonts for Figlet Forge.

This script ensures that the essential fonts are available
for the package to function correctly.
"""

import os
import shutil
import sys
from pathlib import Path

# Define essential fonts - minimum set required for compatibility
ESSENTIAL_FONTS = ["standard", "slant", "small", "big", "mini"]


def main():
    """Set up the fonts directory with essential fonts."""
    package_root = Path(__file__).parent
    fonts_dir = package_root / "src" / "figlet_forge" / "fonts"

    # Create fonts directory if needed
    fonts_dir.mkdir(parents=True, exist_ok=True)

    print(f"Setting up fonts directory: {fonts_dir}")

    # Check system font directories
    system_font_dirs = [
        Path("/usr/share/figlet"),
        Path("/usr/local/share/figlet"),
    ]

    # Add any OS-specific directories
    if sys.platform == "win32":
        # Windows font locations
        system_font_dirs.append(
            Path(os.environ.get("APPDATA", "")) / "figlet" / "fonts"
        )
    elif sys.platform == "darwin":
        # macOS font locations
        system_font_dirs.append(Path("/opt/local/share/figlet"))
        system_font_dirs.append(
            Path.home() / "Library" / "Application Support" / "figlet"
        )

    # Track fonts we've copied
    copied_fonts = []
    missing_fonts = list(ESSENTIAL_FONTS)  # Start with all fonts as missing

    # Look in system directories
    for directory in system_font_dirs:
        if not directory.exists():
            print(f"Directory doesn't exist: {directory}")
            continue

        print(f"Checking font directory: {directory}")
        for font_name in list(
            missing_fonts
        ):  # Use a copy to safely modify during iteration
            font_path = directory / f"{font_name}.flf"
            if font_path.exists():
                try:
                    dest_path = fonts_dir / f"{font_name}.flf"
                    shutil.copy2(font_path, dest_path)
                    print(f"Copied font: {font_name}")
                    copied_fonts.append(font_name)
                    missing_fonts.remove(font_name)
                except Exception as e:
                    print(f"Error copying {font_name}: {e}")

    # Report results
    if not copied_fonts:
        print("\nNo fonts could be found or copied.")
        print("Please run get_figlet_fonts.py to download the required fonts.")
        return 1

    print(
        f"\n✅ Successfully copied {len(copied_fonts)} fonts: {', '.join(copied_fonts)}"
    )

    if missing_fonts:
        print(f"\n⚠️ Some essential fonts are still missing: {', '.join(missing_fonts)}")
        print("Please run get_figlet_fonts.py to download all required fonts.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
