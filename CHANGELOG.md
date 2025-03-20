# Changelog

All notable changes to Figlet Forge will be documented in this file.

## [1.0.2] - 2025-05-01

### Added

- RGB color support with 24-bit color capabilities
- Advanced color effects module with gradients, highlights, and animations
- Optimized Unicode rendering for East Asian scripts
- Comprehensive documentation with examples

### Fixed

- Resolved issues with right-to-left text rendering
- Fixed compatibility issues with certain font formats
- Improved error handling for font loading failures

### Changed

- Restructured codebase following Eidosian principles
- Optimized rendering engine for better performance
- Enhanced compatibility layer for seamless pyfiglet integration

## [1.0.1] - 2025-01-15

### Added

- Basic ANSI color support
- Unicode character rendering
- Compatibility with original pyfiglet
- Command-line interface enhancements

### Fixed

- Font parsing issues
- Character encoding problems
- Layout bugs in certain terminal environments

## [1.0.0] - 2024-11-01

### Added

- Initial release of Figlet Forge
- Core rendering functionality
- Support for FIGlet and TOIlet font formats
- Command-line interface
- Python API

## 2023-12-15 0.1.0

This release introduces figlet_forge, an Eidosian reimplementation extending the original pyfiglet package:

- Full colorized ANSI code support for vibrant text art
- Unicode character rendering with comprehensive mapping
- Expanded font ecosystem with careful attention to licensing
- Intelligent fallbacks for compatibility with older systems
- Significant performance optimizations without sacrificing quality
- Enhanced maintainability through modern Python practices
- Comprehensive documentation for all use cases
- Full backward compatibility with pyfiglet
- Integrated with the Eidosian Forge ecosystem as a core typography tool
- Modern project structure with pyproject.toml replacing setup.py

  Technical improvements:

- Type annotations throughout codebase (mypy, pyright integration)
- Modular architecture for better extensibility
- Unit tests covering all functionality (pytest)
- Code quality enforced via pre-commit hooks
- Documentation built with Sphinx and ReadTheDocs integration

## 2023-09-13 1.0.2

This release fixes a leaked file descriptor.

## 2023-09-10 1.0.1

This release adds a python_requires >= 3.9 to setup.py to prevent old python
versions from picking up the newly incompatible version.

## 2023-09-10 1.0.0

This release was yanked, because it introduced incompatibilities with old
versions of python but did not specify a python_requires line.

- Support for Python 2 was dropped
- Support for compressed fonts
- Support for more fonts
- Various fixes for corner cases of font rendering
- Drop use of pkg_resources in favour of importlib.resources
- Add pyproject.toml
- Many small fixes

## 2018-12-06 0.8.0

- #62 Change LICENSE to MIT
- #61 Provide font installation option (-L) and remove
  unlicenced fonts from the distribution

## 2018-10-17 0.7.6

- #57 Implement colored print
- #53 Allow fonts to be specified by path

## 2016-06-12 0.7.5

- #46 Add 100+ fonts from java.de figlet fonts collection v4.0
- #48 Include python3 in testing

## 2015-05-27 0.7.4

- #43 Don't leak file handles

## 2015-04-14 0.7.3

- #41 Add newline and text wrapping support

## 2014-09-14 0.7.2

- #35 Add this CHANGELOG
- #36 Bug fix for #34 (broken --reverse and --flip)
  (reported "character mapping must return integer, None or unicode")

## 2014-07-27 0.7.1

- #29 Fix for UTF8 regression
- #31 Add **main** entry point
- #32 Pep8 the code and minor refactoring
- #33 Trove classifiers update

## 2014-06-02 0.7

- #9 Add --list_fonts and --info_font
- #10 Add tools/pyfiglet_example for listing all fonts
- #11 Fix the pyfiglet command (had bad python path)
- #12 Pyflakes fixes
- #13 Configure Travis Continuous Integration
- #17 Documentation usage sample fix
- #19 Enable pyfiglet to use extended ASCII chars
- #20 Add two cyrillic fonts
- #21 Python 3 support
- #27 Code improvements
- #28 Human readable font list (-l)
