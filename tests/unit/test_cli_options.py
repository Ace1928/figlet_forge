import unittest
from unittest.mock import patch

from figlet_forge.cli.main import main


class TestCLIOptions(unittest.TestCase):
    """Test CLI options and flags."""

    def test_sample_flag(self):
        """Test that --sample works as a flag without requiring value."""
        with patch("figlet_forge.cli.main.generate_showcase") as mock_showcase:
            # Test with just --sample flag
            main(["--sample"])
            mock_showcase.assert_called_with(
                sample_text="hello", fonts=None, color=None
            )

            # Reset mock
            mock_showcase.reset_mock()

            # Test with --sample and --sample-text
            main(["--sample", "--sample-text=Test"])
            mock_showcase.assert_called_with(sample_text="Test", fonts=None, color=None)

    def test_sample_with_color_and_fonts(self):
        """Test that --sample works with color and font options."""
        with patch("figlet_forge.cli.main.generate_showcase") as mock_showcase:
            main(["--sample", "--sample-color=RED", "--sample-fonts=slant,small"])
            mock_showcase.assert_called_with(
                sample_text="hello", fonts=["slant", "small"], color="RED"
            )

    def test_showcase_equivalent_to_sample(self):
        """Test that --showcase is equivalent to --sample."""
        with patch("figlet_forge.cli.main.generate_showcase") as mock_showcase:
            # Test --showcase
            main(["--showcase"])
            mock_showcase.assert_called_with(
                sample_text="hello", fonts=None, color=None
            )

            # Reset mock
            mock_showcase.reset_mock()

            # Test --sample
            main(["--sample"])
            mock_showcase.assert_called_with(
                sample_text="hello", fonts=None, color=None
            )


if __name__ == "__main__":
    unittest.main()
