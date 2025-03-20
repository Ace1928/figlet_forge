class FigletError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


class CharNotPrinted(FigletError):
    """
    Raised when the width is not sufficient to print a character
    """


class FontNotFound(FigletError):
    """
    Raised when a font can't be located
    """


class FontError(FigletError):
    """
    Raised when there is a problem parsing a font file
    """


class InvalidColor(FigletError):
    """
    Raised when the color passed is invalid
    """
