"""
FigletString handling for Figlet Forge.

This module implements the FigletString class which represents a rendered
figlet text output with various transformation capabilities.
"""

from .core.figlet_string import FigletString

# Re-export the core FigletString class
__all__ = ["FigletString"]
