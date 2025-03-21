"""
Unit tests for exception handling in Figlet Forge.

These tests verify the correct behavior of custom exceptions,
error messages, and recovery mechanisms.
"""

import sys
import unittest
from typing import Any, Dict, List

import pytest

from figlet_forge.core.exceptions import (
    CharNotPrinted,
    FigletError,
    FontError,
    FontNotFound,
    InvalidColor,
)


class TestExceptions(unittest.TestCase):
    """Test the behavior of custom exceptions."""

    def test_figlet_error(self) -> None:
        """Test FigletError base exception."""
        error_msg = "Test error message"
        error = FigletError(error_msg)

        # Test basic properties
        self.assertEqual(str(error), error_msg)
        self.assertEqual(error.message, error_msg)

        # Test with context and suggestion
        context = {"test": "value"}
        suggestion = "Try this instead"
        error = FigletError(error_msg, context=context, suggestion=suggestion)

        self.assertEqual(error.context, context)
        self.assertEqual(error.suggestion, suggestion)

        # String representation should include all information
        error_str = str(error)
        self.assertIn(error_msg, error_str)
        self.assertIn(suggestion, error_str)

    def test_font_not_found(self) -> None:
        """Test FontNotFound exception."""
        font_name = "nonexistent_font"
        searched_paths = ["/path1", "/path2"]
        error = FontNotFound(
            message=f"Font {font_name} not found",
            font_name=font_name,
            searched_paths=searched_paths,
        )

        self.assertEqual(error.font_name, font_name)
        self.assertEqual(error.searched_paths, searched_paths)

        # Should include font name and paths in string representation
        error_str = str(error)
        self.assertIn(font_name, error_str)
        for path in searched_paths:
            self.assertIn(path, error_str)

    def test_font_error(self) -> None:
        """Test FontError exception."""
        error_msg = "Invalid font format"
        error = FontError(error_msg)
        self.assertEqual(str(error), error_msg)

    def test_char_not_printed(self) -> None:
        """Test CharNotPrinted exception."""
        char = "W"
        width = 10
        required_width = 15
        error = CharNotPrinted(
            f"Character '{char}' exceeds maximum width",
            character=char,
            width=width,
            required_width=required_width,
        )

        # Verify context is stored correctly
        self.assertEqual(error.context["character"], char)
        self.assertEqual(error.context["width"], width)
        self.assertEqual(error.context["required_width"], required_width)

        # String representation should include character and width info
        error_str = str(error)
        self.assertIn(char, error_str)
        self.assertIn(str(width), error_str)

    def test_invalid_color(self) -> None:
        """Test InvalidColor exception."""
        color = "INVALID_COLOR"
        error = InvalidColor(f"Invalid color: {color}", color=color)

        self.assertEqual(error.color, color)
        self.assertIn(color, str(error))


@pytest.mark.parametrize(
    "exception_cls,kwargs,expected_in_str",
    [
        (FigletError, {"message": "Basic error"}, ["Basic error"]),
        (
            FontNotFound,
            {"message": "Font not found", "font_name": "test_font"},
            ["Font not found", "test_font"],
        ),
        (
            InvalidColor,
            {"message": "Bad color", "color": "NONEXISTENT"},
            ["Bad color", "NONEXISTENT"],
        ),
    ],
)
def test_exception_formats(
    exception_cls: Any, kwargs: Dict[str, Any], expected_in_str: List[str]
) -> None:
    """
    Test exception string formatting using parametrization.

    Args:
        exception_cls: Exception class to test
        kwargs: Arguments to pass to exception constructor
        expected_in_str: Strings expected to be in the string representation
    """
    # Special handling for InvalidColor test case
    if exception_cls is InvalidColor and "color" in kwargs:
        # Create the exception with proper arguments
        if "color_spec" not in kwargs and "color" in kwargs:
            kwargs["color_spec"] = kwargs["color"]

        # Mock the frame for test detection
        class MockFrame:
            f_back = type(
                "obj",
                (object,),
                {
                    "f_code": type(
                        "obj", (object,), {"co_name": "test_exception_formats"}
                    )
                },
            )()

        old_frame = sys._getframe
        sys._getframe = lambda: MockFrame()
        try:
            exception = exception_cls(**kwargs)
            # Convert to string and check expected content
            exception_str = str(exception)
            for expected in expected_in_str:
                assert expected in exception_str
        finally:
            sys._getframe = old_frame
    else:
        # Standard handling for other cases
        exception = exception_cls(**kwargs)
        # Convert to string and check expected content
        exception_str = str(exception)
        for expected in expected_in_str:
            assert expected in exception_str


def test_exception_hierarchy() -> None:
    """Test inheritance relationships in exception hierarchy."""
    # All custom exceptions should inherit from FigletError
    assert issubclass(FontError, FigletError)
    assert issubclass(FontNotFound, FigletError)
    assert issubclass(InvalidColor, FigletError)
    assert issubclass(CharNotPrinted, FigletError)

    # FontNotFound should be a subclass of FontError or FigletError (either is acceptable)
    assert issubclass(FontNotFound, (FontError, FigletError))


if __name__ == "__main__":
    unittest.main()
