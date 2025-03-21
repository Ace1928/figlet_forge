"""
Unit tests for core Figlet functionality.

These tests verify the correct operation of the Figlet class,
font loading, text rendering, and various transformation operations.
"""

import unittest

from figlet_forge import Figlet, FigletString


class TestFigletCore(unittest.TestCase):
    """Test core Figlet functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_text = "Test"
        self.default_font = "standard"

    def test_basic_initialization(self):
        """Test basic Figlet initialization."""
        fig = Figlet()
        self.assertIsNotNone(fig)
        self.assertEqual(fig.font, "standard")

    def test_custom_font_initialization(self):
        """Test Figlet initialization with custom font."""
        fig = Figlet(font="slant")
        self.assertEqual(fig.font, "slant")

    def test_invalid_font_fallback(self):
        """Test fallback behavior with invalid font."""
        # With invalid font, should fall back to standard
        fig = Figlet(font="non_existent_font", width=80)
        self.assertEqual(fig.font, "standard")

    def test_render_text(self):
        """Test rendering text to ASCII art."""
        fig = Figlet(font=self.default_font)
        result = fig.renderText(self.test_text)

        # Result should be a FigletString
        self.assertIsInstance(result, FigletString)

        # Result should contain the test text (in some form)
        self.assertGreater(len(result), 0)

        # Test specific properties of the result
        lines = result.splitlines()
        self.assertGreater(len(lines), 1)  # Should be multi-line

    def test_width_constraint(self):
        """Test width constraint behavior."""
        # Test with very small width
        narrow_width = 10
        fig = Figlet(font=self.default_font, width=narrow_width)

        # Rendering should still work with narrow width
        result = fig.renderText("A")  # Single character should fit
        self.assertIsInstance(result, FigletString)

        # Each line should respect width constraint
        for line in result.splitlines():
            self.assertLessEqual(len(line), narrow_width)

    def test_direction_setting(self):
        """Test text direction settings."""
        fig = Figlet(font=self.default_font)

        # Test default direction
        self.assertEqual(fig.getDirection(), "left-to-right")

        # Test changing direction
        fig.setDirection("right-to-left")
        self.assertEqual(fig.getDirection(), "right-to-left")

        # Test auto direction
        fig.setDirection("auto")
        self.assertEqual(fig.getDirection(), "left-to-right")

    def test_justify_setting(self):
        """Test text justification settings."""
        fig = Figlet(font=self.default_font)

        # Test default justification (should be 'left' for LTR)
        self.assertEqual(fig.getJustify(), "left")

        # Test changing justification
        fig.setJustify("center")
        self.assertEqual(fig.getJustify(), "center")

        # Test auto justification with RTL
        fig.setDirection("right-to-left")
        fig.setJustify("auto")
        self.assertEqual(fig.getJustify(), "right")

    def test_empty_text(self):
        """Test rendering empty text."""
        fig = Figlet(font=self.default_font)
        result = fig.renderText("")
        self.assertEqual(result, "")

    def test_font_list(self):
        """Test retrieving font list."""
        fig = Figlet()
        fonts = fig.getFonts()
        self.assertIsInstance(fonts, list)
        self.assertGreater(len(fonts), 0)
        self.assertIn(self.default_font, fonts)


class TestFigletString(unittest.TestCase):
    """Test FigletString functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.simple_text = "ABC\nDEF"
        self.figlet_string = FigletString(self.simple_text)

    def test_reverse(self):
        """Test string reversal."""
        reversed_string = self.figlet_string.reverse()
        self.assertEqual(reversed_string, "CBA\nFED")

    def test_flip(self):
        """Test vertical flipping."""
        flipped_string = self.figlet_string.flip()
        self.assertEqual(flipped_string, "DEF\nABC")

    def test_border(self):
        """Test border addition."""
        bordered = self.figlet_string.border()
        lines = bordered.splitlines()
        self.assertTrue(lines[0].startswith("┌"))
        self.assertTrue(lines[0].endswith("┐"))
        self.assertTrue(lines[-1].startswith("└"))
        self.assertTrue(lines[-1].endswith("┘"))

        # Test with different border style
        double_bordered = self.figlet_string.border("double")
        lines = double_bordered.splitlines()
        self.assertTrue(lines[0].startswith("╔"))
        self.assertTrue(lines[-1].startswith("╚"))

    def test_center(self):
        """Test text centering."""
        width = 10
        centered = self.figlet_string.center(width)
        lines = centered.splitlines()
        for line in lines:
            self.assertEqual(len(line), width)
            self.assertTrue(line.strip().center(width).startswith(line))

    def test_strip_surrounding_newlines(self):
        """Test stripping surrounding newlines."""
        padded = FigletString("\n\nABC\nDEF\n\n")
        stripped = padded.strip_surrounding_newlines()
        self.assertEqual(stripped, "ABC\nDEF")

    def test_dimensions(self):
        """Test getting dimensions."""
        width, height = self.figlet_string.dimensions
        self.assertEqual(width, 3)  # "ABC" is 3 characters wide
        self.assertEqual(height, 2)  # Two lines: "ABC" and "DEF"


if __name__ == "__main__":
    unittest.main()
