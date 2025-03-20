"""
Figlet Forge version information and constants.

An Eidosian reimplementation and extension of pyfiglet (which itself is a
pure Python port of FIGlet) with the following enhancements:
- Full colorized ANSI code support for vibrant text art
- Unicode character rendering with comprehensive mapping
- Expanded font ecosystem with careful attention to licensing
- Intelligent fallbacks for compatibility with older systems
- Significant performance optimizations without sacrificing quality
- Enhanced maintainability through modern Python practices
- Comprehensive documentation for all use cases
"""

__version__ = "1.0.2"
__package_name__ = "figlet_forge"
__author__ = "Lloyd Handyside"
__author_email__ = "ace1928@gmail.com"
__description__ = (
    "Enhanced Figlet System with colorized ANSI support and Unicode rendering"
)
__github_url__ = "https://github.com/Ace1928/figlet_forge"
__docs_url__ = "https://figlet-forge.readthedocs.io/"
__original_project__ = "https://github.com/pwaller/pyfiglet"

# Default figlet font - the foundation of all rendering operations
DEFAULT_FONT = "standard"

# Terminal color specification dictionary - precise ANSI color encoding
COLOR_CODES = {
    "BLACK": 30,
    "RED": 31,
    "GREEN": 32,
    "YELLOW": 33,
    "BLUE": 34,
    "MAGENTA": 35,
    "CYAN": 36,
    "LIGHT_GRAY": 37,
    "DEFAULT": 39,
    "DARK_GRAY": 90,
    "LIGHT_RED": 91,
    "LIGHT_GREEN": 92,
    "LIGHT_YELLOW": 93,
    "LIGHT_BLUE": 94,
    "LIGHT_MAGENTA": 95,
    "LIGHT_CYAN": 96,
    "WHITE": 97,
    "RESET": 0,
}

# Terminal escape sequence for resetting colors to default state
RESET_COLORS = "\033[0m"

# Platform-specific shared directory for font storage
import os
import sys

if sys.platform == "win32":
    SHARED_DIRECTORY = os.path.join(os.environ.get("APPDATA", ""), "pyfiglet")
else:
    SHARED_DIRECTORY = "/usr/local/share/pyfiglet/"
