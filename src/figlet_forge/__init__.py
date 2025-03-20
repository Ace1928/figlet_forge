#!/usr/bin/env python

"""
╔═══════════════════════════════════════════════════════════════════════════╗
║   ███████╗██╗ ██████╗ ██╗     ███████╗████████╗    ███████╗ ██████╗ ██████╗  ██████╗ ███████╗   ║
║   ██╔════╝██║██╔════╝ ██║     ██╔════╝╚══██╔══╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝   ║
║   █████╗  ██║██║  ███╗██║     █████╗     ██║       █████╗  ██║   ██║██████╔╝██║  ███╗█████╗     ║
║   ██╔══╝  ██║██║   ██║██║     ██╔══╝     ██║       ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝     ║
║   ██║     ██║╚██████╔╝███████╗███████╗   ██║       ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗   ║
║   ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝       ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ║
║                                                                                                   ║
║ ╭────────────────────────────────────────────────────────────────────────────────────────────╮   ║
║ │           TEXT CRYSTALLIZATION ENGINE - DIGITAL TYPOGRAPHY FORGE                           │   ║
║ ╰────────────────────────────────────────────────────────────────────────────────────────────╯   ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝

Figlet Forge: An Eidosian reimplementation extending pyfiglet with colorized ANSI support,
Unicode rendering and intelligent fallbacks while maintaining backward compatibility.
"""

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 📚 CORE IMPORTS & TYPE DEFINITIONS                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

import importlib.resources
import itertools
import logging
import os
import pathlib
import re
import shutil
import sys
import zipfile
from datetime import date
from optparse import OptionParser
from typing import Any, Dict, List, Literal, Optional, Tuple, TypedDict, Union

from .cli import main

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 🔧 PACKAGE METADATA                                                       ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

__version__ = "0.1.0"
__author__ = "Lloyd Handyside <ace1928@gmail.com>"
__org__ = "Neuroforge"
__copyright__ = """
The MIT License (MIT)
Copyright © 2007-2024
    Lloyd Handyside <ace1928@gmail.com>
    Peter Waller <p@pwaller.net>
    Christopher Jones <cjones@insub.org>
    Stefano Rivera <stefano@rivera.za.net>
    And various contributors (see git history).

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 🎛️ CONFIGURATION & CONSTANTS                                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

# Initialize logging with precise contextual formatting
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Default figlet font - the foundation of all rendering operations
DEFAULT_FONT: str = "standard"

# Terminal color specification dictionary - precise ANSI color encoding
COLOR_CODES: Dict[str, int] = {
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
RESET_COLORS: bytes = b"\033[0m"

# Platform-specific shared directory for font storage - environment aware
if sys.platform == "win32":
    SHARED_DIRECTORY: str = os.path.join(os.environ["APPDATA"], "pyfiglet")
else:
    SHARED_DIRECTORY: str = "/usr/local/share/pyfiglet/"

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 🔄 COMPONENT IMPORTS                                                      ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

# Core components - expose main classes at package level for backward compatibility
# Enhanced color support - extends the original capabilities with modern features
from .color import ColorMode, ColorScheme, colored_format
from .figlet import Figlet, print_figlet
from .figlet_string import FigletString

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 📦 PACKAGE EXPORTS                                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

__all__: List[str] = [
    "Figlet",
    "FigletString",
    "print_figlet",
    "colored_format",
    "ColorMode",
    "ColorScheme",
]

# Immediate execution context handler
if __name__ == "__main__":
    sys.exit(main())
