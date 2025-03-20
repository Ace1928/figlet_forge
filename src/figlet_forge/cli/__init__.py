"""
Figlet Forge Command Line Interface

This module provides the command-line interface for Figlet Forge,
enabling users to generate ASCII art text from the terminal with
support for colors, unicode characters, and various layout options.

The CLI maintains backward compatibility with the original pyfiglet
while adding enhanced features such as ANSI color support and improved
Unicode rendering.
"""

import sys
from typing import List, Optional, Union

# Import the main CLI function from main.py
from .main import main

__all__ = ["main"]

# Provide direct execution capability
if __name__ == "__main__":
    sys.exit(main())
