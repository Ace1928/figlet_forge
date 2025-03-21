"""
Version information and constants for Figlet Forge.

This module provides version information, default settings, and constants
used throughout the Figlet Forge package.
"""

import os
import sys
from pathlib import Path

# Version information
__version__ = "0.1.0"
__package_name__ = "figlet-forge"
__author__ = "Lloyd Handyside"
__author_email__ = "ace1928@gmail.com"
__description__ = "Advanced FIGlet text rendering with color and Unicode support"
__github_url__ = "https://github.com/Ace1928/figlet_forge"
__docs_url__ = "https://github.com/Ace1928/figlet_forge/docs"

# Default settings
DEFAULT_FONT = "standard"

# Color constants
RESET_COLORS = "\033[0m"  # ANSI code to reset colors
COLOR_CODES = {
    "BLACK": "30",
    "RED": "31",
    "GREEN": "32",
    "YELLOW": "33",
    "BLUE": "34",
    "MAGENTA": "35",
    "CYAN": "36",
    "WHITE": "37",
    "LIGHT_GRAY": "37",
    "DARK_GRAY": "90",
    "LIGHT_RED": "91",
    "LIGHT_GREEN": "92",
    "LIGHT_YELLOW": "93",
    "LIGHT_BLUE": "94",
    "LIGHT_MAGENTA": "95",
    "LIGHT_CYAN": "96",
    "RESET": "0",
}

# Directory structure
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_DIR = os.path.dirname(SCRIPT_DIR)

# Detect installation environment
try:
    import site

    USER_SITE = site.getusersitepackages()
    SHARED_DIRECTORY = os.path.dirname(os.path.dirname(USER_SITE))
except (ImportError, AttributeError):
    # Fallback for when site module is not available
    USER_SITE = os.path.expanduser("~/.local/lib/python")
    SHARED_DIRECTORY = "/usr/share"

# Font-related settings
FONT_EXTENSIONS = [".flf", ".tlf"]
FONT_SEARCH_PATHS = [
    Path(__file__).parent / "fonts",  # Package fonts
    Path(SHARED_DIRECTORY) / "figlet" / "fonts",  # System fonts (Unix-like)
    Path(os.path.expanduser("~")) / ".figlet_forge" / "fonts",  # User fonts
]

# Add OS-specific paths
if sys.platform == "win32":
    FONT_SEARCH_PATHS.extend(
        [
            Path(os.environ.get("APPDATA", "")) / "figlet_forge" / "fonts",
            Path(os.environ.get("PROGRAMFILES", "")) / "Figlet" / "fonts",
        ]
    )
elif sys.platform == "darwin":
    FONT_SEARCH_PATHS.extend(
        [
            Path("/opt/local/share/figlet/fonts"),
            Path.home() / "Library" / "figlet" / "fonts",
        ]
    )
