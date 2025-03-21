"""
Tests for compatibility with the original pyfiglet.

This module verifies that Figlet Forge maintains backward compatibility
with the original pyfiglet package, following the Eidosian principle of
"Structure as Control" - ensuring that the architecture prevents errors.
"""

import unittest
from unittest.mock import patch

from figlet_forge.compat import Figlet, figlet_format


class TestPyfigletCompatibility(unittest.TestCase):
    """Test compatibility with the original pyfiglet API."""

    def test_figlet_format_compatibility(self):
        """Test the figlet_format function's compatibility."""
        # Test basic functionality
        result = figlet_format("Hello")
        self.assertIsInstance(result, str)
        self.assertIn("Hello", result.replace(" ", ""))

        # Test with font parameter
        result = figlet_format("Hello", font="slant")
        self.assertIsInstance(result, str)
        self.assertIn("Hello", result.replace(" ", ""))

        # Test with width parameter
        result = figlet_format("Hello", width=120)
        self.assertIsInstance(result, str)

        # Test with direction parameter
        result = figlet_format("Hello", direction="left-to-right")
        self.assertIsInstance(result, str)

        # Test with justify parameter
        result = figlet_format("Hello", justify="center")
        self.assertIsInstance(result, str)

    def test_figlet_class_compatibility(self):
        """Test the Figlet class's compatibility."""
        # Test initialization
        fig = Figlet()
        self.assertIsInstance(fig, Figlet)

        # Test with font parameter
        fig = Figlet(font="slant")
        self.assertEqual(fig.font, "slant")

        # Test with direction parameter
        fig = Figlet(direction="right-to-left")
        self.assertEqual(fig.direction, "right-to-left")

        # Test with justify parameter
        fig = Figlet(justify="center")
        self.assertEqual(fig.justify, "center")

        # Test with width parameter
        fig = Figlet(width=120)
        self.assertEqual(fig.width, 120)

        # Test renderText method
        result = fig.renderText("Hello")
        self.assertIsInstance(result, str)
        self.assertIn("Hello", result.replace(" ", ""))

        # Test getFonts method
        fonts = fig.getFonts()
        self.assertIsInstance(fonts, list)
        self.assertIn("standard", fonts)

        # Test getDirection method
        direction = fig.getDirection()
        self.assertIn(direction, ["left-to-right", "right-to-left"])

        # Test setFont method
        fig.setFont("standard")
        self.assertEqual(fig.font, "standard")

    def test_module_level_attributes(self):
        """Test that module-level attributes are available."""
        from figlet_forge.compat import DEFAULT_FONT, renderText

        self.assertIsInstance(DEFAULT_FONT, str)

        # Test the renderText alias
        result = renderText("Hello")
        self.assertIsInstance(result, str)
        self.assertIn("Hello", result.replace(" ", ""))

    @patch("sys.stdout")
    def test_print_figlet_compatibility(self, mock_stdout):
        """Test print_figlet function compatibility."""
        from figlet_forge.compat import print_figlet

        # Call the function
        print_figlet("Hello")

        # Verify that something was written to stdout
        mock_stdout.write.assert_called()


if __name__ == "__main__":
    unittest.main()
