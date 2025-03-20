#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ Figlet Forge - Font Tester                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
# This script tests fonts with various options to ensure everything works correctly

# Function to print section headers
print_header() {
    echo "═══════════════════════════════════════════════════════"
    echo "  $1"
    echo "═══════════════════════════════════════════════════════"
}

# Detect if we're in a terminal with color support
if [ -t 1 ] && [ -n "$TERM" ] && [ "$TERM" != "dumb" ]; then
    COLOR_SUPPORT=1
else
    COLOR_SUPPORT=0
fi

# Set up command depending on what's installed
if command -v figlet_forge > /dev/null 2>&1; then
    CMD="figlet_forge"
    echo "Using figlet_forge command"
elif command -v python -c "import figlet_forge" > /dev/null 2>&1; then
    CMD="python -m figlet_forge"
    echo "Using figlet_forge module"
else
    echo "Error: figlet_forge not found!"
    exit 1
fi

# First, let's list the available fonts
print_header "AVAILABLE FONTS"
$CMD -l | sort | head -n 15
echo "... (showing first 15 fonts only)"

# Test basic rendering
print_header "BASIC RENDERING (standard font)"
$CMD "FigletForge"

# Test with another font
print_header "ALTERNATE FONT (slant)"
$CMD -f slant "FigletForge"

# Test with another font
print_header "SMALL FONT (small)"
$CMD -f small "FigletForge"

# Test text direction right-to-left
print_header "RIGHT-TO-LEFT DIRECTION"
$CMD -D right-to-left "وَرْج تِلِجِف"

# Test text justification
print_header "CENTER JUSTIFICATION"
$CMD -w 60 -j center "Centered Text"

# Test color (if supported)
if [ "$COLOR_SUPPORT" -eq 1 ]; then
    print_header "COLOR TESTS"
    $CMD -f standard -c "RED:" "Red Text"
    $CMD -f standard -c ":BLUE" "Blue Background"
    $CMD -f standard -c "GREEN:YELLOW" "Green on Yellow"
fi

# Test transformations
print_header "TRANSFORMATIONS"
echo "Normal:"
$CMD -f small "Flip Me"
echo "Flipped:"
$CMD -f small -F "Flip Me"
echo "Reversed:"
$CMD -f small -r "Reverse Me"

# Test Unicode support
print_header "UNICODE SUPPORT"
$CMD -u "Hello 世界"

print_header "TEST COMPLETE"
echo "Font testing completed successfully!"
exit 0
