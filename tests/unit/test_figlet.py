# tests/unit/test_figlet.py
"""
Unit tests for the core Figlet functionality.
"""
import pytest

from figlet_forge import Figlet, FigletString


def test_figlet_init():
    """Test Figlet initialization with default parameters."""
    fig = Figlet()
    assert fig.font == "standard"
    assert fig.width == 80


def test_figlet_with_font():
    """Test Figlet initialization with specific font."""
    fig = Figlet(font="slant")
    assert fig.font == "slant"


def test_render_simple_text(sample_text):
    """Test rendering simple text."""
    fig = Figlet()
    result = fig.renderText(sample_text)
    assert isinstance(result, FigletString)
    assert len(result) > 0


def test_get_fonts():
    """Test retrieving available fonts."""
    fig = Figlet()
    fonts = fig.getFonts()
    assert isinstance(fonts, list)
    assert "standard" in fonts


def test_set_font():
    """Test changing font after initialization."""
    fig = Figlet(font="standard")
    fig.setFont(font="slant")
    assert fig.font == "slant"


@pytest.mark.fonts
def test_standard_fonts(standard_fonts, sample_text):
    """Test all standard fonts render without errors."""
    fig = Figlet()
    for font in standard_fonts:
        fig.setFont(font=font)
        result = fig.renderText(sample_text)
        assert isinstance(result, FigletString)
        assert len(result) > 0
