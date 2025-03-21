"""
Integration tests for compatibility module.

These tests verify that the compatibility layer works correctly
with the rest of the Figlet Forge system.
"""

import unittest
from typing import Any, Dict, List

import pytest

from figlet_forge import Figlet as CoreFiglet
from figlet_forge.compat import (
    DEFAULT_FONT,
    FontNotFound,
    figlet_format,
    renderText,
)
from figlet_forge.compat import (
    Figlet as CompatFiglet,
)
from figlet_forge.core.figlet_string import FigletString


class TestCompatIntegration(unittest.TestCase):
    """Test integration between compat module and core functionality."""

    def test_compat_core_integration(self):
        """Test that compat layer integrates with core functionality."""
        # Create instances of both classes
        core_fig = CoreFiglet(font=DEFAULT_FONT)
        compat_fig = CompatFiglet(font=DEFAULT_FONT)

        # Render the same text with both
        test_text = "Hello"
        core_result = core_fig.renderText(test_text)
        compat_result = compat_fig.renderText(test_text)

        # Core result should be FigletString, compat result should be str
        self.assertIsInstance(core_result, FigletString)
        self.assertIsInstance(compat_result, str)

        # Despite different types, string content should match
        self.assertEqual(str(core_result), compat_result)

    def test_exception_compatibility(self):
        """Test that exceptions are properly translated."""
        # Try to load a non-existent font
        # Both should raise their respective exceptions
        with self.assertRaises(Exception) as core_ctx:
            try:
                CoreFiglet(font="nonexistent_font_xyz")
            except Exception as e:
                # Ensure it's a core exception
                self.assertNotIsInstance(e, FontNotFound)
                raise e

        with self.assertRaises(FontNotFound) as compat_ctx:
            CompatFiglet(font="nonexistent_font_xyz")

        # Both exceptions should carry similar information
        self.assertIn("font", str(core_ctx.exception).lower())
        self.assertIn("font", str(compat_ctx.exception).lower())

    def test_figlet_format_integration(self):
        """Test that figlet_format integrates with core functionality."""
        # Use figlet_format from compat
        result = figlet_format("Test")

        # Should get a valid string result
        self.assertIsInstance(result, str)
        self.assertIn("Test", result.replace(" ", "").replace("\n", ""))

        # Test with custom parameters
        result_custom = figlet_format("Test", font="small", width=60, justify="center")
        self.assertIsInstance(result_custom, str)
        self.assertNotEqual(result, result_custom)  # Results should differ

    def test_alias_functionality(self):
        """Test that renderText alias functions correctly."""
        # renderText should be an alias for figlet_format
        result1 = figlet_format("Alias")
        result2 = renderText("Alias")

        # Results should be identical
        self.assertEqual(result1, result2)


@pytest.mark.parametrize(
    "method_name,args,kwargs,return_type",
    [
        ("renderText", ["Hello"], {}, str),
        ("getFonts", [], {}, list),
        ("getDirection", [], {}, str),
        ("getJustify", [], {}, str),
        ("getRenderWidth", ["Test"], {}, int),
    ],
)
def test_compat_methods(
    method_name: str,
    args: List[Any],
    kwargs: Dict[str, Any],
    return_type: type,
):
    """
    Test that compat Figlet methods work correctly and return expected types.

    Args:
        method_name: Name of method to test
        args: Positional arguments for method
        kwargs: Keyword arguments for method
        return_type: Expected return type
    """
    # Create a compat Figlet instance
    fig = CompatFiglet()

    # Get and call the method
    method = getattr(fig, method_name)
    result = method(*args, **kwargs)

    # Verify result type
    assert isinstance(
        result, return_type
    ), f"Expected {return_type}, got {type(result)}"


def test_compat_consistency():
    """Test consistency of operations between different ways of using the compat layer."""
    # Different ways to render the same text
    text = "Test"

    # Method 1: Use Figlet class
    fig = CompatFiglet()
    result1 = fig.renderText(text)

    # Method 2: Use figlet_format function
    result2 = figlet_format(text)

    # Method 3: Use renderText alias
    result3 = renderText(text)

    # All results should match
    assert result1 == result2 == result3
