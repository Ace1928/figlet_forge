from typing import Any, Dict, Optional


class FigletError(Exception):
    """
    Base exception class for all Figlet Forge errors.

    Provides structured error representation with optional
    context and suggestions for error recovery. Follows the
    Eidosian principle that errors should be as informative
    as the operations they interrupt.
    """

    def __init__(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        suggestion: Optional[str] = None,
        error_code: Optional[str] = None,
    ):
        self.message = message
        self.context = context or {}
        self.suggestion = suggestion
        self.error_code = error_code
        super().__init__(self.message)

    def __str__(self) -> str:
        """Format the error message with context if available."""
        result = self.message

        if self.suggestion:
            result += f" — {self.suggestion}"

        if self.context and len(self.context) > 0:
            ctx_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            result += f" [{ctx_str}]"

        return result


class CharNotPrinted(FigletError):
    """
    Raised when the width is not sufficient to print a character.

    This occurs when attempting to render text within a width
    constraint that cannot accommodate one or more characters
    in the selected font.
    """

    def __init__(
        self,
        message: str = "Character couldn't be printed due to width constraints",
        width: Optional[int] = None,
        char: Optional[str] = None,
        required_width: Optional[int] = None,
    ):
        context = {}
        if width is not None:
            context["current_width"] = width
        if char is not None:
            context["character"] = char
        if required_width is not None:
            context["required_width"] = required_width

        suggestion = "Try increasing the width or using a narrower font"
        super().__init__(message, context, suggestion, "WIDTH_CONSTRAINT")


class FontNotFound(FigletError):
    """
    Raised when a font can't be located in any of the font directories.

    This exception provides details about the search process to help
    diagnose why a font wasn't found and how to resolve the issue.
    """

    def __init__(
        self,
        message: str = "Font not found",
        font_name: Optional[str] = None,
        searched_paths: Optional[list] = None,
    ):
        context = {}
        if font_name is not None:
            context["font"] = font_name
        if searched_paths is not None:
            context["searched_paths"] = searched_paths

        suggestion = "Check font name or install the font using the --load option"
        super().__init__(message, context, suggestion, "FONT_NOT_FOUND")


class FontError(FigletError):
    """
    Raised when there is a problem parsing a font file.

    This can occur due to invalid font format, corrupted files,
    or incompatible font specifications.
    """

    def __init__(
        self,
        message: str = "Error parsing font file",
        font_name: Optional[str] = None,
        line_number: Optional[int] = None,
        error_detail: Optional[str] = None,
    ):
        context = {}
        if font_name is not None:
            context["font"] = font_name
        if line_number is not None:
            context["line"] = line_number
        if error_detail is not None:
            context["detail"] = error_detail

        suggestion = "Check if the font file is valid and in the correct format"
        super().__init__(message, context, suggestion, "FONT_PARSE_ERROR")


class InvalidColor(FigletError):
    """
    Raised when the color passed is invalid.

    This can occur if the color name is not recognized, the RGB
    values are out of range, or the color specification format
    is incorrect.
    """

    def __init__(
        self,
        message: str = "Invalid color specification",
        color_spec: Optional[str] = None,
        available_colors: Optional[list] = None,
    ):
        context = {}
        if color_spec is not None:
            context["specified_color"] = color_spec
        if available_colors is not None:
            context["available_colors"] = available_colors

        suggestion = "Use a valid color name or RGB format (e.g., RED or 255;0;0)"
        super().__init__(message, context, suggestion, "INVALID_COLOR")
