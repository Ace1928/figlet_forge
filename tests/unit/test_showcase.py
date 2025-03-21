"""
Unit tests for the showcase module.

These tests verify the functionality of the showcase module,
including font and color demonstrations.
"""

import unittest
from io import StringIO
from unittest.mock import patch

import pytest

from figlet_forge.cli.showcase import ColorShowcase, generate_showcase


class TestShowcase(unittest.TestCase):
    """Test the showcase functionality."""

    def test_color_showcase_initialization(self):
        """Test initialization of ColorShowcase."""
        showcase = ColorShowcase(use_color=True)
        self.assertTrue(hasattr(showcase, "color_styles"))
        self.assertTrue(hasattr(showcase, "font_descriptions"))

    def test_print_methods(self):
        """Test print formatting methods."""
        showcase = ColorShowcase(use_color=False)  # No color for predictable output

        with patch("sys.stdout", new=StringIO()) as fake_out:
            showcase.print_header("Test Header")
            showcase.print_subheader("Test Subheader")
            showcase.print_success("Success Message")
            showcase.print_info("Info Message")

            output = fake_out.getvalue()
            self.assertIn("Test Header", output)
            self.assertIn("Test Subheader", output)
            self.assertIn("Success Message", output)
            self.assertIn("Info Message", output)

    def test_generate_font_showcase_with_color(self):
        """Test generating a font showcase with color."""
        showcase = ColorShowcase(use_color=False)

        # Mock the Figlet class and other functions to avoid actual rendering
        with patch("figlet_forge.cli.showcase.Figlet") as mock_figlet, patch(
            "figlet_forge.cli.showcase.rainbow_colorize",
            return_value="RAINBOW COLORED TEXT",
        ), patch("sys.stdout", new=StringIO()) as fake_out:

            mock_figlet_instance = mock_figlet.return_value
            mock_figlet_instance.renderText.return_value = "Rendered ASCII Art"

            # Test with rainbow color
            showcase.generate_font_showcase(
                fonts=["standard"], sample_text="hello", sample_color="rainbow"
            )

            output = fake_out.getvalue()
            mock_figlet.assert_called_with(font="standard")
            mock_figlet_instance.renderText.assert_called_with("hello")
            self.assertIn("RAINBOW COLORED TEXT", output)

    def test_generate_usage_guide(self):
        """Test generating the usage guide."""
        showcase = ColorShowcase(use_color=False)

        with patch("sys.stdout", new=StringIO()) as fake_out:
            showcase.generate_usage_guide()

            output = fake_out.getvalue()
            self.assertIn("FIGLET FORGE USAGE GUIDE", output)
            self.assertIn("CORE USAGE PATTERNS", output)
            self.assertIn("FONT METAMORPHOSIS", output)

    def test_generate_color_showcase(self):
        """Test generating color showcase."""
        showcase = ColorShowcase(use_color=False)

        # Mock the necessary functions
        with patch("figlet_forge.cli.showcase.Figlet") as mock_figlet, patch(
            "figlet_forge.cli.showcase.rainbow_colorize",
            return_value="RAINBOW EFFECT",
        ), patch(
            "figlet_forge.cli.showcase.gradient_colorize",
            return_value="GRADIENT EFFECT",
        ), patch(
            "figlet_forge.cli.showcase.color_style_apply",
            return_value="COLOR STYLE EFFECT",
        ), patch(
            "sys.stdout", new=StringIO()
        ) as fake_out:

            mock_figlet_instance = mock_figlet.return_value
            mock_figlet_instance.renderText.return_value = "Rendered ASCII Art"

            showcase.generate_color_showcase("standard", "hello")

            output = fake_out.getvalue()
            self.assertIn("COLOR SHOWCASE", output)
            self.assertIn("RAINBOW EFFECT", output)
            self.assertIn("GRADIENT EFFECT", output)
            self.assertIn("COLOR STYLE EFFECT", output)


@pytest.mark.parametrize(
    "sample_text,color,fonts",
    [
        ("hello", None, None),  # Default parameters
        ("test", "rainbow", None),  # With color
        ("example", None, ["slant", "mini"]),  # With specific fonts
        ("all", "red_to_blue", ["standard"]),  # With both color and font
    ],
)
def test_generate_showcase_parameters(sample_text, color, fonts):
    """
    Test showcase generation with different parameters.

    Args:
        sample_text: Sample text to use
        color: Color to apply
        fonts: Fonts to showcase
    """
    # Mock the ColorShowcase class to avoid actual rendering
    with patch("figlet_forge.cli.showcase.ColorShowcase") as mock_showcase_class:
        mock_showcase = mock_showcase_class.return_value

        generate_showcase(sample_text=sample_text, fonts=fonts, color=color)

        # Verify correct method calls
        mock_showcase.generate_font_showcase.assert_called_once_with(
            fonts, sample_text, color
        )
        mock_showcase.print_header.assert_called_with("END OF SHOWCASE")
        mock_showcase.generate_usage_guide.assert_called_once()


@pytest.mark.parametrize(
    "font_list,expected_count",
    [
        (None, 5),  # Default should use 5 curated fonts
        (["standard"], 1),  # Single font
        (["standard", "slant", "mini"], 3),  # Multiple fonts
        ([], 5),  # Empty list should fall back to default
    ],
)
def test_font_showcase_options(font_list, expected_count):
    """Test font showcase with different font options."""
    showcase = ColorShowcase(use_color=False)

    # Mock to avoid actual font loading and rendering
    with patch("figlet_forge.cli.showcase.Figlet") as mock_figlet, patch(
        "sys.stdout", new=StringIO()
    ):
        mock_instance = mock_figlet.return_value
        mock_instance.renderText.return_value = "Rendered Text"

        # Replace fonts with an empty list if None to count function calls
        fonts_to_use = [] if font_list is None else font_list

        with patch.object(showcase, "print_subheader") as mock_subheader:
            showcase.generate_font_showcase(fonts=font_list, sample_text="Test")

            # Check how many fonts were processed by counting subheader calls
            if not font_list:
                # Default set of fonts should be used
                assert mock_subheader.call_count >= 5
            else:
                assert mock_subheader.call_count == len(font_list)


if __name__ == "__main__":
    unittest.main()
