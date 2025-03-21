"""
Tests for color functionality in Figlet Forge.

This module tests the color parsing, application, and effect features.
"""

import unittest

from figlet_forge.color import ColorMode, ColorScheme
from figlet_forge.color.effects import (
    gradient_colorize,
    highlight_pattern,
    pulse_colorize,
    rainbow_colorize,
    random_colorize,
)
from figlet_forge.color.figlet_color import (
    color_to_ansi,
    parse_color,
)
from figlet_forge.core.exceptions import InvalidColor


class TestColorFunctions(unittest.TestCase):
    """Test color handling functions."""

    def test_parse_color(self):
        """Test parsing various color specifications."""
        # Test named colors
        fg, bg = parse_color("RED")
        self.assertTrue(fg.startswith("\033["))
        self.assertEqual(bg, "")

        # Test foreground:background format
        fg, bg = parse_color("RED:BLUE")
        self.assertTrue(fg.startswith("\033["))
        self.assertTrue(bg.startswith("\033["))

        # Test RGB format
        fg, bg = parse_color("255;0;0")
        self.assertTrue(fg.startswith("\033[38;2;"))

        # Test RGB foreground:background format
        fg, bg = parse_color("255;0;0:0;0;255")
        self.assertTrue(fg.startswith("\033[38;2;"))
        self.assertTrue(bg.startswith("\033[48;2;"))

        # Test empty string
        fg, bg = parse_color("")
        self.assertEqual(fg, "")
        self.assertEqual(bg, "")

        # Test invalid color
        with self.assertRaises(InvalidColor):
            parse_color("NONEXISTENT")

        # Test invalid RGB format
        with self.assertRaises(InvalidColor):
            parse_color("256;0;0")  # Value too large

    def test_color_to_ansi(self):
        """Test conversion of colors to ANSI codes."""
        # Test named colors
        ansi_red = color_to_ansi("RED")
        self.assertTrue(ansi_red.startswith("\033["))

        # Test RGB values
        ansi_rgb = color_to_ansi("255;0;0")
        self.assertTrue(ansi_rgb.startswith("\033[38;2;"))

        # Test background colors
        ansi_bg = color_to_ansi("BLUE", is_background=True)
        self.assertTrue(ansi_bg.startswith("\033[4"))

        # Test invalid color
        with self.assertRaises(InvalidColor):
            color_to_ansi("NONEXISTENT")

        # Test invalid RGB format
        with self.assertRaises(InvalidColor):
            color_to_ansi("300;0;0")  # Value too large


class TestColorEffects(unittest.TestCase):
    """Test color effect functions."""

    def setUp(self):
        """Set up test data."""
        self.test_text = "Test\nText"

    def test_rainbow_colorize(self):
        """Test rainbow colorization effect."""
        result = rainbow_colorize(self.test_text)
        self.assertIsInstance(result, str)
        self.assertTrue("\033[" in result)  # Should contain ANSI codes

        # Test with background color
        result_with_bg = rainbow_colorize(self.test_text, "BLACK")
        self.assertIsInstance(result_with_bg, str)
        self.assertNotEqual(result, result_with_bg)

        # Test with empty string
        result_empty = rainbow_colorize("")
        self.assertEqual(result_empty, "")

    def test_gradient_colorize(self):
        """Test gradient colorization effect."""
        result = gradient_colorize(self.test_text, "RED", "BLUE")
        self.assertIsInstance(result, str)
        self.assertTrue("\033[" in result)  # Should contain ANSI codes

        # Test with RGB colors
        result_rgb = gradient_colorize(self.test_text, (255, 0, 0), (0, 0, 255))
        self.assertIsInstance(result_rgb, str)
        self.assertTrue("\033[" in result_rgb)

        # Test with background color
        result_with_bg = gradient_colorize(self.test_text, "RED", "BLUE", "BLACK")
        self.assertIsInstance(result_with_bg, str)

        # Test with empty string
        result_empty = gradient_colorize("")
        self.assertEqual(result_empty, "")

    def test_random_colorize(self):
        """Test random colorization effect."""
        result = random_colorize(self.test_text)
        self.assertIsInstance(result, str)
        self.assertTrue("\033[" in result)  # Should contain ANSI codes

        # Test with background color
        result_with_bg = random_colorize(self.test_text, "BLACK")
        self.assertIsInstance(result_with_bg, str)

        # Test with empty string
        result_empty = random_colorize("")
        self.assertEqual(result_empty, "")

    def test_highlight_pattern(self):
        """Test pattern highlighting functionality."""
        text = "The quick brown fox jumps over the lazy dog"
        result = highlight_pattern(text, "fox", "RED", "BLUE")
        self.assertIsInstance(result, str)
        self.assertTrue("\033[" in result)

        # Test case sensitivity
        result_case = highlight_pattern(
            text, "FOX", "RED", "BLUE", case_sensitive=False
        )
        self.assertIsInstance(result_case, str)
        self.assertTrue("\033[" in result_case)

        # Test empty pattern
        result_empty = highlight_pattern(text, "", "RED", "BLUE")
        self.assertEqual(result_empty, text)

    def test_pulse_colorize(self):
        """Test pulse colorization effect."""
        result = pulse_colorize(self.test_text, "BLUE")
        self.assertIsInstance(result, str)
        self.assertTrue("\033[" in result)

        # Test with RGB color
        result_rgb = pulse_colorize(self.test_text, (0, 0, 255))
        self.assertIsInstance(result_rgb, str)
        self.assertTrue("\033[" in result_rgb)

        # Test with empty string
        result_empty = pulse_colorize("")
        self.assertEqual(result_empty, "")


class TestColorScheme(unittest.TestCase):
    """Test ColorScheme class."""

    def test_color_scheme_creation(self):
        """Test creating ColorScheme objects."""
        # Test with color names
        scheme = ColorScheme(foreground="RED", background="BLUE")
        self.assertEqual(scheme.foreground, "RED")
        self.assertEqual(scheme.background, "BLUE")

        # Test with RGB tuples
        rgb_scheme = ColorScheme(foreground=(255, 0, 0), background=(0, 0, 255))
        self.assertEqual(rgb_scheme.foreground, (255, 0, 0))
        self.assertEqual(rgb_scheme.background, (0, 0, 255))

        # Test with mode
        mode_scheme = ColorScheme(foreground="GREEN", mode=ColorMode.RAINBOW)
        self.assertEqual(mode_scheme.mode, ColorMode.RAINBOW)

        # Test invalid color
        with self.assertRaises(InvalidColor):
            ColorScheme(foreground="NOT_A_COLOR")

    def test_from_string(self):
        """Test creating ColorScheme from string specification."""
        # Test with foreground only
        scheme1 = ColorScheme.from_string("RED")
        self.assertEqual(scheme1.foreground, "RED")
        self.assertIsNone(scheme1.background)

        # Test with foreground and background
        scheme2 = ColorScheme.from_string("GREEN:BLUE")
        self.assertEqual(scheme2.foreground, "GREEN")
        self.assertEqual(scheme2.background, "BLUE")

        # Test with empty parts
        scheme3 = ColorScheme.from_string(":")
        self.assertIsNone(scheme3.foreground)
        self.assertIsNone(scheme3.background)

    def test_to_ansi(self):
        """Test conversion to ANSI escape sequences."""
        # Basic scheme
        scheme = ColorScheme(foreground="RED")
        ansi = scheme.to_ansi()
        self.assertTrue(ansi.startswith("\033["))

        # Scheme with styling
        styled = ColorScheme(
            foreground="BLUE", background="WHITE", bold=True, italic=True
        )
        ansi_styled = styled.to_ansi()
        self.assertIn("\033[1m", ansi_styled)  # Bold
        self.assertIn("\033[3m", ansi_styled)  # Italic


class TestColorFunctionality(unittest.TestCase):
    """Test overall color functionality."""

    def test_colored_format(self):
        """Test the colored_format function."""
        from figlet_forge.color import colored_format

        text = "Hello World"
        # Test with string color spec
        result1 = colored_format(text, "RED")
        self.assertTrue("\033[" in result1)

        # Test with ColorScheme object
        scheme = ColorScheme(foreground="BLUE", background="BLACK")
        result2 = colored_format(text, scheme)
        self.assertTrue("\033[" in result2)

        # Test with empty text
        empty = colored_format("", "RED")
        self.assertEqual(empty, "")


if __name__ == "__main__":
    unittest.main()
