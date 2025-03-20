#!/usr/bin/env python3

"""
Test script to verify figlet_forge compatibility with pyfiglet.

This script ensures that the figlet_forge compatibility layer works
identically to the original pyfiglet package by running equivalent
operations using both APIs.
"""


try:
    import pyfiglet

    PYFIGLET_AVAILABLE = True
except ImportError:
    print("Original pyfiglet not available for comparison.")
    PYFIGLET_AVAILABLE = False

# Import figlet_forge compatibility layer
import figlet_forge.compat as ff_compat

# Colors for output formatting
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"
BOLD = "\033[1m"


def test_api_signatures() -> None:
    """Test that all expected API functions and classes are available."""
    print(f"\n{BOLD}Testing API signatures...{RESET}")

    expected_attributes = [
        "Figlet",
        "FigletFont",
        "FigletString",
        "figlet_format",
        "print_figlet",
    ]

    missing = []
    for attr in expected_attributes:
        if not hasattr(ff_compat, attr):
            missing.append(attr)
            print(f"{RED}Missing: {attr}{RESET}")
        else:
            print(f"{GREEN}Found: {attr}{RESET}")

    if missing:
        print(f"\n{RED}Missing {len(missing)} API elements!{RESET}")
    else:
        print(f"\n{GREEN}All expected API elements are present.{RESET}")


def test_figlet_format() -> None:
    """Test the figlet_format function for compatibility."""
    print(f"\n{BOLD}Testing figlet_format function...{RESET}")

    test_text = "Hello"
    test_fonts = ["small", "standard", "slant"]

    for font in test_fonts:
        print(f"\nRendering with font '{font}':")

        # Render with figlet_forge compatibility layer
        ff_result = ff_compat.figlet_format(test_text, font=font)
        print(f"{GREEN}figlet_forge result:{RESET}")
        print(ff_result)

        # Compare with pyfiglet if available
        if PYFIGLET_AVAILABLE:
            py_result = pyfiglet.figlet_format(test_text, font=font)
            print(f"{GREEN}pyfiglet result:{RESET}")
            print(py_result)

            if ff_result == py_result:
                print(f"{GREEN}✓ Results match!{RESET}")
            else:
                print(f"{RED}✗ Results differ!{RESET}")


def test_figlet_class() -> None:
    """Test the Figlet class for compatibility."""
    print(f"\n{BOLD}Testing Figlet class...{RESET}")

    # Test font listing
    ff_fonts = set(ff_compat.Figlet().getFonts())
    print(f"figlet_forge fonts available: {len(ff_fonts)}")

    if PYFIGLET_AVAILABLE:
        py_fonts = set(pyfiglet.Figlet().getFonts())
        print(f"pyfiglet fonts available: {len(py_fonts)}")

        common_fonts = ff_fonts.intersection(py_fonts)
        print(f"Common fonts: {len(common_fonts)}")

        if common_fonts:
            # Test rendering with a common font
            test_font = next(iter(common_fonts))
            test_text = "Test"

            ff_fig = ff_compat.Figlet(font=test_font)
            ff_result = ff_fig.renderText(test_text)

            py_fig = pyfiglet.Figlet(font=test_font)
            py_result = py_fig.renderText(test_text)

            if ff_result == py_result:
                print(f"{GREEN}✓ Rendering with font '{test_font}' matches!{RESET}")
            else:
                print(f"{RED}✗ Rendering with font '{test_font}' differs!{RESET}")


def test_figletstring_operations() -> None:
    """Test FigletString operations for compatibility."""
    print(f"\n{BOLD}Testing FigletString operations...{RESET}")

    ff_fig = ff_compat.Figlet(font="small")
    ff_text = ff_fig.renderText("Flip")

    # Test flip operation
    print("Original:")
    print(ff_text)

    print("\nFlipped:")
    flipped = ff_text.flip()
    print(flipped)

    print("\nReversed:")
    reversed_text = ff_text.reverse()
    print(reversed_text)

    if PYFIGLET_AVAILABLE:
        py_fig = pyfiglet.Figlet(font="small")
        py_text = py_fig.renderText("Flip")

        py_flipped = py_text.flip()
        py_reversed = py_text.reverse()

        if ff_text.flip() == py_flipped:
            print(f"{GREEN}✓ Flip operation matches pyfiglet!{RESET}")
        else:
            print(f"{RED}✗ Flip operation differs from pyfiglet!{RESET}")

        if ff_text.reverse() == py_reversed:
            print(f"{GREEN}✓ Reverse operation matches pyfiglet!{RESET}")
        else:
            print(f"{RED}✗ Reverse operation differs from pyfiglet!{RESET}")


def main() -> None:
    """Run all compatibility tests."""
    print(f"{BOLD}FIGLET FORGE COMPATIBILITY TEST{RESET}")
    print("-" * 40)

    if PYFIGLET_AVAILABLE:
        print(f"Testing against pyfiglet version: {pyfiglet.__version__}")

    print(f"figlet_forge.compat version: {ff_compat.__version__}")
    print("-" * 40)

    # Run tests
    test_api_signatures()
    test_figlet_format()
    test_figlet_class()
    test_figletstring_operations()

    print(f"\n{BOLD}Compatibility test complete!{RESET}")


if __name__ == "__main__":
    main()
