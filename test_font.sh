#!/usr/bin/env bash
#===============================================================================
# test_font.sh - Compare figlet and pyfiglet rendering of the same text
#===============================================================================
# DESCRIPTION:
#   This script renders the same text with both figlet and pyfiglet using
#   a specified font, then compares the outputs side-by-side with vimdiff.
#   Useful for finding differences in text rendering between implementations.
#
# USAGE:
#   ./test_font.sh "text_to_render" "font_name"
#
# ARGUMENTS:
#   $1 - Text to render with ASCII art
#   $2 - Font name to use for rendering
#
# DEPENDENCIES:
#   - figlet
#   - pyfiglet
#   - vimdiff
#===============================================================================

# Enable strict mode
set -euo pipefail
IFS=$'\n\t'

#-------------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------------
TEMP_DIR="/tmp"
FIGLET_OUTPUT="${TEMP_DIR}/figlet_output.txt"
PYFIGLET_OUTPUT="${TEMP_DIR}/pyfiglet_output.txt"
FIGLET_FONTS_DIR="pyfiglet/fonts"

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
function check_dependencies() {
  local missing_deps=0

  for cmd in figlet pyfiglet vimdiff; do
    if ! command -v "$cmd" &>/dev/null; then
      echo "Error: Required command '$cmd' not found" >&2
      missing_deps=1
    fi
  done

  if [[ $missing_deps -eq 1 ]]; then
    echo "Please install missing dependencies and try again." >&2
    exit 1
  fi
}

function validate_arguments() {
  if [[ $# -ne 2 ]]; then
    echo "Error: Incorrect number of arguments" >&2
    echo "Usage: $0 \"text_to_render\" \"font_name\"" >&2
    exit 1
  fi

  # Ensure font directory exists
  if [[ ! -d "$FIGLET_FONTS_DIR" ]]; then
    echo "Error: Font directory not found: $FIGLET_FONTS_DIR" >&2
    exit 1
  fi
}

function render_ascii_art() {
  local text="$1"
  local font="$2"

  echo "Rendering \"$text\" with font \"$font\"..."

  # Generate output with pyfiglet
  pyfiglet -f "$font" "$text" > "$PYFIGLET_OUTPUT"

  # Generate output with figlet
  figlet -d "$FIGLET_FONTS_DIR" -f "$font" "$text" > "$FIGLET_OUTPUT"
}

function compare_outputs() {
  echo "Comparing outputs with vimdiff..."
  vimdiff "$FIGLET_OUTPUT" "$PYFIGLET_OUTPUT"
}

function cleanup() {
  echo "Cleaning up temporary files..."
  rm -f "$FIGLET_OUTPUT" "$PYFIGLET_OUTPUT"
}

#-------------------------------------------------------------------------------
# Main script
#-------------------------------------------------------------------------------
function main() {
  check_dependencies
  validate_arguments "$@"

  local text_to_render="$1"
  local font_name="$2"

  render_ascii_art "$text_to_render" "$font_name"
  compare_outputs

  # Register cleanup to happen on exit
  trap cleanup EXIT
}

# Execute the script
main "$@"

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
