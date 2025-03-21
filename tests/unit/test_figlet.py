"""
Unit tests for core Figlet functionality.

These tests verify the correct operation of the Figlet class,
font loading, text rendering, and various transformation operations.
"""

import unittest

import pytest

from figlet_forge import Figlet
from figlet_forge.core.exceptions import FigletError, FontNotFound
from figlet_forge.core.figlet_string import FigletString


class TestFigletCore(unittest.TestCase):
    """Test core Figlet functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.test_text = "Test"
        self.default_font = "standard"

    def test_basic_initialization(self) -> None:
        """Test basic Figlet initialization."""
        fig = Figlet()
        self.assertIsNotNone(fig)
        self.assertEqual(fig.font, "standard")

    def test_custom_font_initialization(self) -> None:
        """Test Figlet initialization with custom font."""
        fig = Figlet(font="slant")
        self.assertEqual(fig.font, "slant")

    def test_invalid_font_fallback(self) -> None:
        """Test fallback behavior with invalid font."""
        # With invalid font, should fall back to standard
        fig = Figlet(font="non_existent_font", width=80)
        self.assertEqual(fig.font, "standard")

    def test_render_text(self) -> None:
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

    def test_width_constraint(self) -> None:
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

    def test_direction_setting(self) -> None:
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

    def test_justify_setting(self) -> None:
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

    def test_empty_text(self) -> None:
        """Test rendering empty text."""
        fig = Figlet(font=self.default_font)
        result = fig.renderText("")
        self.assertEqual(result, "")

    def test_font_list(self) -> None:
        """Test retrieving font list."""
        fig = Figlet()
        fonts = fig.getFonts()
        self.assertIsInstance(fonts, list)
        self.assertGreater(len(fonts), 0)
        self.assertIn(self.default_font, fonts)

    def test_newline_handling(self) -> None:
        """Test handling of newline characters in input text."""
        fig = Figlet(font=self.default_font)
        multi_line_text = "Line1\nLine2"
        result = fig.renderText(multi_line_text)

        # Result should contain multiple sections separated by newlines
        lines = result.splitlines()
        self.assertGreater(len(lines), 2)

    def test_error_handling(self) -> None:
        """Test error handling during rendering."""
        fig = Figlet(font=self.default_font)

        # Test handling of problematic input
        try:
            result = fig.renderText("\x00\x01")  # Control characters
            # If no exception, should still return something
            self.assertIsInstance(result, FigletString)
        except FigletError:
            # If exception raised, that's also acceptable
            pass


@pytest.mark.parametrize(
    "font_name,expected_success",
    [
        ("standard", True),  # Standard font should always succeed
        ("slant", True),  # Common font should succeed
        ("nonexistent", False),  # Non-existent font should fail
    ],
)
def test_font_loading(font_name: str, expected_success: bool) -> None:
    """
    Test font loading with pytest parametrization.

    Args:
        font_name: Name of font to test
        expected_success: Whether loading should succeed
    """
    if expected_success:
        # Should successfully load the font
        fig = Figlet(font=font_name)
        assert fig.font == font_name
    else:
        # Should fall back to standard font
        fig = Figlet(font=font_name)
        assert fig.font == "standard"


@pytest.mark.parametrize(
    "text,font,width,expected_width",
    [
        ("A", "standard", 80, 5),  # Single character
        ("AA", "standard", 80, 9),  # Two characters
        ("A", "small", 80, 3),  # Smaller font
    ],
)
def test_text_dimensions(text: str, font: str, width: int, expected_width: int) -> None:
    """
    Test rendered text dimensions.

    Args:
        text: Input text
        font: Font to use
        width: Width parameter
        expected_width: Expected output width
    """
    try:
        fig = Figlet(font=font, width=width)
        result = fig.renderText(text)

        # Check dimensions
        rendered_width = max(len(line) for line in result.splitlines())
        assert rendered_width == expected_width
    except FontNotFound:
        # Skip test if font isn't available
        pytest.skip(f"Font {font} not available")


class TestFigletString(unittest.TestCase):
    """Test FigletString functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.simple_text = "ABC\nDEF"
        self.figlet_string = FigletString(self.simple_text)

    def test_reverse(self) -> None:
        """Test string reversal."""
        reversed_string = self.figlet_string.reverse()
        self.assertEqual(reversed_string, "CBA\nFED")

    def test_flip(self) -> None:
        """Test vertical flipping."""
        flipped_string = self.figlet_string.flip()
        self.assertEqual(flipped_string, "DEF\nABC")

    def test_border(self) -> None:
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

    def test_center(self) -> None:
        """Test text centering."""
        width = 10
        centered = self.figlet_string.center(width)
        lines = centered.splitlines()
        for line in lines:
            self.assertEqual(len(line), width)
            self.assertTrue(line.strip().center(width).startswith(line))

    def test_strip_surrounding_newlines(self) -> None:
        """Test stripping surrounding newlines."""
        padded = FigletString("\n\nABC\nDEF\n\n")
        stripped = padded.strip_surrounding_newlines()
        self.assertEqual(stripped, "ABC\nDEF")

    def test_dimensions(self) -> None:
        """Test getting dimensions."""
        width, height = self.figlet_string.dimensions
        self.assertEqual(width, 3)  # "ABC" is 3 characters wide
        self.assertEqual(height, 2)  # Two lines: "ABC" and "DEF"

    def test_overlay(self) -> None:
        """Test overlay functionality."""
        base = FigletString("XXXXX\nXXXXX\nXXXXX")
        overlay = FigletString("AB\nCD")

        # Test overlay with default positioning (0, 0)
        result = base.overlay(overlay)
        self.assertEqual(result.splitlines()[0], "ABXXX")
        self.assertEqual(result.splitlines()[1], "CDXXX")

        # Test overlay with offset
        result = base.overlay(overlay, x_offset=2, y_offset=1)
        self.assertEqual(result.splitlines()[0], "XXXXX")
        self.assertEqual(result.splitlines()[1], "XXABX")
        self.assertEqual(result.splitlines()[2], "XXCDX")

        # Test overlay with transparency disabled
        result = base.overlay(overlay, transparent=False)
        self.assertEqual(result.splitlines()[0], "ABXXX")

    def test_rotate_90(self) -> None:
        """Test 90-degree rotation methods."""
        original = FigletString("AB\nCD")

        # Clockwise rotation
        rotated_cw = original.rotate_90_clockwise()
        self.assertEqual(rotated_cw.splitlines()[0], "CA")
        self.assertEqual(rotated_cw.splitlines()[1], "DB")

        # Counter-clockwise rotation
        rotated_ccw = original.rotate_90_counterclockwise()
        self.assertEqual(rotated_ccw.splitlines()[0], "BD")
        self.assertEqual(rotated_ccw.splitlines()[1], "AC")

    def test_shadow(self) -> None:
        """Test shadow effect."""
        original = FigletString("AB\nCD")
        shadowed = original.shadow()

        lines = shadowed.splitlines()
        self.assertGreater(len(lines), 2)
        # Shadow should appear offset
        self.assertEqual(lines[1], " B")


def test_with_fixtures(figlet_factory, test_text: str) -> None:
    """
    Test using pytest fixtures.

    Args:
        figlet_factory: Factory fixture to create Figlet instances
        test_text: Standard test text fixture
    """
    # Create Figlet with custom parameters
    fig = figlet_factory(width=60, justify="center")
    result = fig.renderText(test_text)

    # Result should be centered
    lines = result.splitlines()
    for line in lines:
        if line.strip():
            # Centered lines should have spaces on both sides
            assert line[0] == " " and line[-1] == " "


if __name__ == "__main__":
    unittest.main()
