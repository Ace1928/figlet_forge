#!/usr/bin/env python3

"""
Tests compatibility between Figlet Forge and the original pyfiglet.

This standalone script verifies that Figlet Forge maintains
compatibility with the pyfiglet API and rendering behavior.
Following Eidosian principles, it provides detailed feedback about
compatibility status while maintaining elegance and precision.
"""

import sys
import unittest
from pathlib import Path

# Ensure we can import from the package
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestFigletCompatibility(unittest.TestCase):
    """Test suite for compatibility between Figlet Forge and pyfiglet."""

    def setUp(self):
        """Set up test environment."""
        # Try to import pyfiglet and figlet_forge
        try:
            import pyfiglet

            self.pyfiglet_available = True
            self.pyfiglet = pyfiglet
        except ImportError:
            print("Warning: Original pyfiglet not available, skipping comparison tests")
            self.pyfiglet_available = False
            self.pyfiglet = None

        try:
            import figlet_forge
            from figlet_forge.compat import Figlet as CompatFiglet

            self.figlet_forge_available = True
            self.figlet_forge = figlet_forge
            self.compat_figlet = CompatFiglet
        except ImportError:
            print("Error: Figlet Forge not available!")
            self.figlet_forge_available = False
            self.figlet_forge = None
            self.compat_figlet = None

    def test_api_compatibility(self):
        """Test that the API interfaces are compatible."""
        if not self.figlet_forge_available:
            self.skipTest("Figlet Forge not available")

        # Import from the compat module
        from figlet_forge.compat import (
            DEFAULT_FONT,
            VERSION,
            Figlet,
            FigletError,
            FontNotFound,
            figlet_format,
            renderText,
        )

        # Test the module attributes
        self.assertIsInstance(DEFAULT_FONT, str)
        self.assertEqual(figlet_format.__name__, "figlet_format")
        self.assertEqual(renderText.__name__, "figlet_format")  # Should be aliased

        # Ensure exceptions are defined
        self.assertTrue(issubclass(FigletError, Exception))
        self.assertTrue(issubclass(FontNotFound, FigletError))

        # Test version is available
        self.assertIsInstance(VERSION, str)

        # Test Figlet class
        fig = Figlet()
        self.assertEqual(fig.__class__.__name__, "Figlet")

        # Test methods exist
        self.assertTrue(hasattr(fig, "renderText"))
        self.assertTrue(hasattr(fig, "getFonts"))
        self.assertTrue(hasattr(fig, "getDirection"))
        self.assertTrue(hasattr(fig, "setFont"))

        # Test additional pyfiglet compatibility methods
        self.assertTrue(hasattr(fig, "getRenderWidth"))

        # Test figlet_format function
        result = figlet_format("Test")
        self.assertIsInstance(result, str)
        self.assertIn("Test", result.replace(" ", "").replace("\n", ""))

    def test_rendering_equivalence(self):
        """Test that rendering produces equivalent results."""
        if not self.pyfiglet_available or not self.figlet_forge_available:
            self.skipTest("Both pyfiglet and Figlet Forge required for comparison")

        test_strings = ["Hello", "World", "Testing", "123"]
        fonts = ["standard", "slant", "small"]

        for text in test_strings:
            for font in fonts:
                try:
                    pyfiglet_result = self.pyfiglet.figlet_format(text, font=font)
                    forge_result = self.figlet_forge.compat.figlet_format(
                        text, font=font
                    )

                    # Clean up strings for comparison
                    py_clean = self._normalize_output(pyfiglet_result)
                    forge_clean = self._normalize_output(forge_result)

                    # Compare the results
                    self.assertEqual(
                        py_clean,
                        forge_clean,
                        f"Output differs for font '{font}' and text '{text}'",
                    )
                except Exception as e:
                    self.fail(f"Error comparing outputs for font '{font}': {e}")

    def test_font_loading(self):
        """Test that font loading behaves consistently."""
        if not self.figlet_forge_available:
            self.skipTest("Figlet Forge not available")

        from figlet_forge.compat import Figlet

        # Test that default font loads
        fig = Figlet()
        self.assertIsNotNone(fig)

        # Test loading specific font
        fig = Figlet(font="slant")
        self.assertEqual(fig.font, "slant")

        # Test getFonts method
        fonts = fig.getFonts()
        self.assertIsInstance(fonts, list)
        self.assertTrue(len(fonts) > 0)
        self.assertIn("standard", fonts)

        # Test setting font after initialization
        fig.setFont("small")
        self.assertEqual(fig.font, "small")

    def test_justification_and_direction(self):
        """Test justification and direction settings."""
        if not self.figlet_forge_available:
            self.skipTest("Figlet Forge not available")

        from figlet_forge.compat import Figlet

        # Test justification
        fig = Figlet(justify="center")
        self.assertEqual(fig.justify, "center")
        fig.setJustify("right")
        self.assertEqual(fig.justify, "right")

        # Test direction
        fig = Figlet(direction="right-to-left")
        self.assertEqual(fig.direction, "right-to-left")
        fig.setDirection("left-to-right")
        self.assertEqual(fig.direction, "left-to-right")

    def test_get_render_width(self):
        """Test the getRenderWidth method."""
        if not self.figlet_forge_available:
            self.skipTest("Figlet Forge not available")

        from figlet_forge.compat import Figlet

        fig = Figlet(font="standard")
        width = fig.getRenderWidth("A")

        # Width should be greater than 0
        self.assertGreater(width, 0)

        # Width should match the maximum line length of rendered text
        rendered = fig.renderText("A")
        expected_width = max((len(line) for line in rendered.splitlines()), default=0)
        self.assertEqual(width, expected_width)

    def _normalize_output(self, text: str) -> str:
        """Normalize output for comparison by removing whitespace variations."""
        # Remove trailing whitespace from each line
        lines = [line.rstrip() for line in text.splitlines()]
        # Remove empty lines from beginning and end
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop(-1)
        return "\n".join(lines)


def main():
    """Run the compatibility tests."""
    unittest.main()


if __name__ == "__main__":
    main()
