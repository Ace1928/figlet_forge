"""
Test package for figlet_forge.

This package contains unit, integration, and compatibility tests for the
figlet_forge system, ensuring full functionality and backward compatibility
with pyfiglet.
"""

import os
import sys
from pathlib import Path

# Add src directory to path for test imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Initialize test constants
TEST_SAMPLE_TEXT = "Hello, Figlet!"
TEST_FONTS = ["standard", "slant", "small"]
