"""
Tests for backward compatibility with pyfiglet.

This module verifies that Figlet Forge maintains API compatibility
with the original pyfiglet package, ensuring a smooth transition
for existing users.
"""

import unittest
from typing import Dict, Tuple

import pytest

# Import from compatibility layer
from figlet_forge.compat import DEFAULT_FONT, Figlet, figlet_format, renderText


class TestPyfigletCompatibility(unittest.TestCase):
    """Test suite for pyfiglet API compatibility."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.test_text = "Test"

    def test_figlet_class_compatibility(self) -> None:
        """Test that the Figlet class has compatible API."""
        # Check initialization with default parameters
        fig = Figlet()
        self.assertEqual(fig.font, DEFAULT_FONT)

        # Check initialization with custom parameters
        fig = Figlet(font="slant", direction="right-to-left", width=60)
        self.assertEqual(fig.font, "slant")
        self.assertEqual(fig.direction, "right-to-left")
        self.assertEqual(fig.width, 60)

        # Check that getFonts returns a list of available fonts
        fonts = fig.getFonts()
        self.assertIsInstance(fonts, list)
        self.assertGreater(len(fonts), 0)

        # Check renderText method
        result = fig.renderText(self.test_text)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), len(self.test_text))

    def test_figlet_format_compatibility(self) -> None:
        """Test that figlet_format function is compatible."""
        # Check with default parameters
        result = figlet_format(self.test_text)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), len(self.test_text))

        # Check with custom parameters
        result = figlet_format(
            self.test_text,
            font="slant",
            width=60,
            justify="center",
            direction="right-to-left",
        )
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), len(self.test_text))

    def test_rendertext_compatibility(self) -> None:
        """Test that renderText function (alias of figlet_format) is compatible."""
        # Check with default parameters
        result = renderText(self.test_text)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), len(self.test_text))

        # Check with custom parameters
        result = renderText(
            self.test_text,
            font="slant",
            width=60,
        )
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), len(self.test_text))


@pytest.mark.parametrize(
    "functions,args,expected_match",
    [
        # Test that figlet_format and renderText produce the same output
        ((figlet_format, renderText), {"text": "AB", "font": "standard"}, True),
        # Test with different parameters
        (
            (figlet_format, renderText),
            {"text": "AB", "font": "standard", "width": 60, "justify": "center"},
            True,
        ),
    ],
)
def test_function_equivalence(
    functions: Tuple[callable, callable],
    args: Dict[str, any],
    expected_match: bool,
) -> None:
    """
    Test that different functions produce equivalent results.

    Args:
        functions: Tuple of functions to compare
        args: Arguments to pass to both functions
        expected_match: Whether outputs should match
    """
    # Call both functions with the same arguments
    results = [func(**args) for func in functions]

    # Check if outputs match as expected
    if expected_match:
        assert results[0] == results[1], "Functions produced different outputs"
    else:
        assert results[0] != results[1], "Functions unexpectedly produced same output"


@pytest.mark.skipif(True, reason="Actual pyfiglet package may not be installed")
def test_against_real_pyfiglet() -> None:
    """
    Test compatibility against the actual pyfiglet package if installed.

    This test is skipped by default since it requires pyfiglet to be installed.
    """
    try:
        import pyfiglet

        test_text = "Compat"

        # Get output from pyfiglet
        pf_result = pyfiglet.figlet_format(test_text, font="standard")

        # Get output from figlet_forge compatibility layer
        ff_result = figlet_format(test_text, font="standard")

        # Compare outputs (ignoring whitespace at line ends)
        pf_normalized = "\n".join(line.rstrip() for line in pf_result.splitlines())
        ff_normalized = "\n".join(line.rstrip() for line in ff_result.splitlines())

        assert pf_normalized == ff_normalized, "Output differs from original pyfiglet"

    except ImportError:
        pytest.skip("Original pyfiglet package not installed")


def test_method_signatures() -> None:
    """Test that method signatures are compatible with pyfiglet."""
    fig = Figlet()

    # Check that all expected methods exist
    assert hasattr(fig, "renderText")
    assert hasattr(fig, "getFonts")
    assert hasattr(fig, "setFont")

    # Check method signatures by calling with expected arguments
    fig.renderText("Test")
    fig.getFonts()
    fig.setFont(font="slant")

    # Check that figlet_format accepts expected parameters
    figlet_format("Test", font="standard", width=80)


if __name__ == "__main__":
    unittest.main()
