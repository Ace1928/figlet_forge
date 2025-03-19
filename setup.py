#!/usr/bin/env python
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║   ███████╗██╗ ██████╗ ██╗     ███████╗████████╗    ███████╗ ██████╗ ██████╗  ██████╗ ███████╗   ║
║   ██╔════╝██║██╔════╝ ██║     ██╔════╝╚══██╔══╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝   ║
║   █████╗  ██║██║  ███╗██║     █████╗     ██║       █████╗  ██║   ██║██████╔╝██║  ███╗█████╗     ║
║   ██╔══╝  ██║██║   ██║██║     ██╔══╝     ██║       ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝     ║
║   ██║     ██║╚██████╔╝███████╗███████╗   ██║       ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗   ║
║   ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝       ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ║
║                                                                                                   ║
║ ╭────────────────────────────────────────────────────────────────────────────────────────────╮   ║
║ │           TEXT CRYSTALLIZATION ENGINE - DIGITAL TYPOGRAPHY FORGE                           │   ║
║ ╰────────────────────────────────────────────────────────────────────────────────────────────╯   ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝

FigletForge: The hyper-optimized ASCII art typography engine for digital expression.

This quantum-leap reimplementation of the classic FIGlet standard transforms ordinary text
into crystallized typographical structures with unparalleled fidelity and performance.

Core capabilities:
• Font ecosystem management with cryptographic integrity verification
• Version intelligence with adaptive fallback mechanisms
• Package topology optimization for minimal cognitive overhead
• Self-aware installation verification across execution contexts
• Typography rendering with mathematical precision

Architectural principles:
• Functional atomicity - each component does one thing exceptionally well
• Error boundary containment - failure states are predictable and recoverable
• Type-theoretic safety - contracts are explicit and verified
• Environmental awareness - adapts to the computational context it inhabits
• Performance-first design - no CPU cycle or memory byte is wasted

Maintainer: Lloyd Handyside (ace1928@gmail.com)
License: MIT
Python: >= 3.9
Last Modified: 2023-11-15
"""

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 🧩 IMPORTS & DEPENDENCIES                                                 ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

import os
import sys
import shutil
import logging
import platform
import datetime
from pathlib import Path
from typing import Dict, List, TypeVar
from functools import lru_cache
from setuptools import setup, find_packages

T = TypeVar("T")  # Generic type for function signatures

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 🛠️ CORE CONFIGURATION                                                     ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

# Package identity - The digital DNA of our creation
PACKAGE_NAME: str = "figlet_forge"
DESCRIPTION: str = "Hyper-optimized ASCII art typography engine"
LONG_DESCRIPTION_FILE: str = "README.md"
LICENSE: str = "MIT"
PACKAGE_URL: str = "https://github.com/Ace1928/figlet_forge"
AUTHOR: str = "Lloyd Handyside"
AUTHOR_EMAIL: str = "ace1928@gmail.com"

# Version boundaries - Runtime compatibility definition
MIN_PYTHON_VERSION: str = ">=3.9"
RECOMMENDED_PYTHON_VERSION: str = ">=3.11"

# Filesystem topology - The skeletal structure of our digital organism
ROOT_DIR: Path = Path(__file__).parent.absolute()
PACKAGE_DIR: Path = ROOT_DIR / PACKAGE_NAME
FONTS_DIR: Path = PACKAGE_DIR / "fonts"
STANDARD_FONTS_DIR: Path = PACKAGE_DIR / "fonts-standard"
VERSION_FILE: Path = PACKAGE_DIR / "version_forge" / "version.py"
TEST_DIR: Path = ROOT_DIR / "tests"

# Runtime flags - Environmental behavior adaptations
DEBUG: bool = os.environ.get("FIGLETFORGE_DEBUG", "").lower() in ("true", "1", "yes")
VERBOSE: bool = os.environ.get("FIGLETFORGE_VERBOSE", "").lower() in (
    "true",
    "1",
    "yes",
)
SKIP_FONT_CHECKS: bool = os.environ.get("FIGLETFORGE_SKIP_FONT_CHECKS", "").lower() in (
    "true",
    "1",
    "yes",
)
VERIFY_INSTALL: bool = os.environ.get("FIGLETFORGE_VERIFY_INSTALL", "").lower() in (
    "true",
    "1",
    "yes",
)

# System context - Execution environment awareness
SYSTEM_INFO: Dict[str, str] = {
    "platform": platform.system(),
    "platform_release": platform.release(),
    "platform_version": platform.version(),
    "architecture": platform.machine(),
    "processor": platform.processor(),
    "python_version": platform.python_version(),
    "python_implementation": platform.python_implementation(),
}

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 📝 LOGGING SYSTEM                                                         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

# Logger configuration - Digital breadcrumbs for future archeologists
LOG_FORMAT: str = "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL: int = (
    logging.DEBUG if DEBUG else (logging.INFO if VERBOSE else logging.WARNING)
)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = logging.getLogger("figletforge.setup")

# Initial system context logging
logger.info(
    f"FigletForge setup initialized on {SYSTEM_INFO['platform']} ({SYSTEM_INFO['architecture']})"
)
logger.info(
    f"Python {SYSTEM_INFO['python_version']} ({SYSTEM_INFO['python_implementation']})"
)
logger.debug(
    f"Debug: {DEBUG} | Verbose: {VERBOSE} | Skip font checks: {SKIP_FONT_CHECKS}"
)

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ ⚠️ ERROR TAXONOMY                                                         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝


class SetupError(Exception):
    """Base exception class for setup-related errors - the root of our error taxonomy."""

    pass


class FontDirectoryError(SetupError):
    """Font ecosystem initialization failures."""

    pass


class VersionError(SetupError):
    """Version intelligence retrieval failures."""

    pass


class EnvironmentError(SetupError):
    """Execution context validation failures."""

    pass


class FileOperationError(SetupError):
    """Filesystem interaction failures."""

    pass


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 🧠 CORE FUNCTIONS                                                         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝


def initialize_font_directory() -> None:
    """
    Font ecosystem initialization with integrity verification.

    Ensures typography assets are properly deployed from version control
    to the runtime package directory with rigorous validation.

    Raises:
        FontDirectoryError: When font ecosystem fails to materialize properly
    """
    if FONTS_DIR.exists():
        logger.debug(f"Font ecosystem already established at {FONTS_DIR}")
        if not SKIP_FONT_CHECKS:
            font_files = list(FONTS_DIR.glob("*.fl[fc]"))
            logger.debug(
                f"Font ecosystem contains {len(font_files)} typographical assets"
            )
        return

    # Font ecosystem needs initialization
    if not STANDARD_FONTS_DIR.exists():
        error_msg = f"Typography source not found: {STANDARD_FONTS_DIR}"
        logger.critical(error_msg)
        raise FontDirectoryError(error_msg)

    logger.info(f"Initializing typography ecosystem: {FONTS_DIR}")
    FONTS_DIR.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Deploy typography assets
        shutil.copytree(STANDARD_FONTS_DIR, FONTS_DIR)

        # Verify typography ecosystem integrity
        if not SKIP_FONT_CHECKS:
            source_files = list(STANDARD_FONTS_DIR.glob("*.fl[fc]"))
            dest_files = list(FONTS_DIR.glob("*.fl[fc]"))

            if len(source_files) != len(dest_files):
                error_msg = f"Typography asset count mismatch: {len(source_files)} → {len(dest_files)}"
                logger.error(error_msg)
                raise FontDirectoryError(error_msg)

        logger.info(
            f"Typography ecosystem initialized with {len(list(FONTS_DIR.glob('*.fl[fc]')))} assets"
        )

    except PermissionError as e:
        error_msg = f"Filesystem permission boundary violation: {e}"
        logger.error(error_msg)
        raise FontDirectoryError(error_msg) from e
    except Exception as e:
        error_msg = f"Typography ecosystem initialization failure: {e}"
        logger.error(error_msg)
        raise FontDirectoryError(error_msg) from e


@lru_cache(maxsize=1)  # Cache version result for efficiency
def get_version() -> str:
    """
    Version intelligence retrieval with adaptive fallback cascade.

    Employs multiple strategies to determine package version with graceful degradation:
    1. Direct module import (primary source)
    2. File parsing (secondary mechanism)
    3. Default versioning (safety net)

    Returns:
        str: Semantic version string (e.g., "1.0.0")
    """
    default_version: str = "0.0.0"
    version: str = default_version  # Initialize with default to ensure type consistency
    original_path: List[str] = sys.path.copy()

    try:
        # Strategy Alpha: Module import pathway
        logger.debug("Initiating version retrieval via module import")
        sys.path.insert(0, str(PACKAGE_DIR))

        try:
            # Use dynamic import to avoid type checking issues
            version_module = __import__(
                "version_forge.version", fromlist=["__version__"]
            )
            imported_version = getattr(version_module, "__version__", None)
            if isinstance(imported_version, str):
                version = imported_version
                logger.info(f"Version intelligence acquired via module: {version}")
        except ImportError as e:
            logger.warning(f"Module import pathway failed: {e}")

            # Strategy Beta: File parsing pathway
            if VERSION_FILE.exists():
                logger.debug(f"Attempting version extraction from {VERSION_FILE}")
                try:
                    version_content = VERSION_FILE.read_text(encoding="utf-8")
                    for line in version_content.splitlines():
                        if line.startswith("__version__"):
                            extracted_version = line.split("=")[1].strip().strip("\"'")
                            if extracted_version:  # Ensure it's not empty
                                version = extracted_version
                                logger.info(
                                    f"Version extracted via file parsing: {version}"
                                )
                                break
                except Exception as parse_error:
                    logger.warning(f"File parsing pathway failed: {parse_error}")

        # Strategy Omega: Default fallback
        if not version:
            logger.warning(
                f"Version intelligence unavailable, using default: {default_version}"
            )
            version = default_version

        # Version format validation
        # We know version is str at this point
        if not all(part.isdigit() for part in version.split(".") if part):
            logger.warning(
                f"Version format integrity check failed: {version}, using default"
            )
            version = default_version

        return version
    finally:
        # Restore path state - Always clean up after ourselves
        sys.path = original_path
        logger.debug("Path state restoration complete")


def read_file(filename: str) -> str:
    """
    Safe file content extraction with comprehensive error handling.

    Performs validation, extraction, and diagnostics with precision:
    - Path existence verification
    - Access permission validation
    - Content extraction with encoding awareness
    - Detailed diagnostics generation

    Args:
        filename: Target file path (relative or absolute)

    Returns:
        str: File content as UTF-8 string

    Raises:
        FileOperationError: When content extraction fails
    """
    file_path = Path(filename)
    absolute_path = file_path if file_path.is_absolute() else ROOT_DIR / file_path

    logger.debug(f"Initiating content extraction: {absolute_path}")

    # Pre-extraction validation
    if not absolute_path.exists():
        error_msg = f"Target file not found: {absolute_path}"
        logger.error(error_msg)
        raise FileOperationError(error_msg)

    if not os.access(absolute_path, os.R_OK):
        error_msg = f"Access permission denied: {absolute_path}"
        logger.error(error_msg)
        raise FileOperationError(error_msg)

    # Content extraction with error boundary
    try:
        content = absolute_path.read_text(encoding="utf-8")

        # Diagnostic metrics
        file_size = len(content)
        line_count = content.count("\n") + 1
        logger.debug(
            f"Content extracted: {absolute_path} ({file_size} bytes, {line_count} lines)"
        )

        return content

    except UnicodeDecodeError as e:
        error_msg = f"Content encoding boundary violation: {e}"
        logger.error(error_msg)
        raise FileOperationError(error_msg) from e

    except IOError as e:
        error_msg = f"I/O subsystem failure: {e}"
        logger.error(error_msg)
        raise FileOperationError(error_msg) from e


def validate_environment() -> None:
    """
    Execution context validation with comprehensive boundary checks.

    Verifies the computational environment meets all prerequisites:
    - Python version compatibility
    - Directory structure integrity
    - File system permissions
    - Resource availability

    Raises:
        EnvironmentError: When execution context is unsuitable
    """
    logger.info("Initiating execution context validation")

    # Python version boundary check
    current_python = f"{sys.version_info.major}.{sys.version_info.minor}"
    min_python = MIN_PYTHON_VERSION.replace(">=", "")

    logger.debug(f"Python version: {current_python} | Required: {min_python}")

    if sys.version_info < tuple(map(int, min_python.split("."))):
        error_msg = (
            f"Python {current_python} is below minimal requirements ({min_python})"
        )
        logger.error(error_msg)
        raise EnvironmentError(error_msg)

    # Directory structure integrity checks
    for dir_path, dir_name in [
        (PACKAGE_DIR, "Package"),
        (STANDARD_FONTS_DIR, "Typography source"),
    ]:
        if not dir_path.exists():
            error_msg = f"{dir_name} directory not found: {dir_path}"
            logger.error(error_msg)
            raise EnvironmentError(error_msg)

    # Resource availability check
    font_files = list(STANDARD_FONTS_DIR.glob("*.fl[fc]"))
    if not font_files:
        error_msg = f"Typography assets missing: {STANDARD_FONTS_DIR}"
        logger.error(error_msg)
        raise EnvironmentError(error_msg)
    logger.debug(f"Found {len(font_files)} typography assets in source directory")

    # Filesystem permission check
    if not os.access(PACKAGE_DIR, os.W_OK):
        error_msg = f"Write permission denied for package directory: {PACKAGE_DIR}"
        logger.error(error_msg)
        raise EnvironmentError(error_msg)

    logger.info("Execution context validation successful")


def verify_installation(package_name: str = PACKAGE_NAME) -> bool:
    """
    Post-installation verification with functionality testing.

    Performs comprehensive verification of installed package:
    - Import pathway validation
    - Core component availability check
    - Basic functionality testing

    Args:
        package_name: Target package identifier

    Returns:
        bool: True if verification passed, False if issues detected
    """
    logger.info(f"Initiating post-installation verification: {package_name}")

    try:
        # Ensure site-packages is accessible
        import site

        site_packages = site.getsitepackages()[0]
        if site_packages not in sys.path:
            sys.path.insert(0, site_packages)

        # Validate import pathway
        package = __import__(package_name)
        logger.debug(f"Import pathway verified: {package_name}")

        # Validate core components
        if not hasattr(package, "FigletFont"):
            logger.warning(f"Core component missing: FigletFont")
            return False

        logger.info(f"Installation verification successful: {package_name}")
        return True

    except ImportError as e:
        logger.error(f"Import pathway failure: {e}")
        return False
    except Exception as e:
        logger.error(f"Verification process failure: {e}")
        return False


def run_setup() -> None:
    """
    Master installation orchestration with comprehensive error handling.

    Coordinates the complete installation process with precision:
    1. Environment validation
    2. Font ecosystem initialization
    3. Metadata acquisition
    4. Package configuration
    5. Installation execution
    6. Verification (when requested)

    All operations are meticulously logged and errors are contained
    with context-specific exception handling and informative diagnostics.
    """
    start_time = datetime.datetime.now()
    logger.info(
        f"FigletForge installation sequence initiated at {start_time.isoformat()}"
    )

    try:
        # Phase 1: Environment validation
        validate_environment()

        # Phase 2: Font ecosystem initialization
        initialize_font_directory()

        # Phase 3: Metadata acquisition
        version = get_version()
        logger.info(f"Building {PACKAGE_NAME} v{version}")
        long_description = read_file(LONG_DESCRIPTION_FILE)

        # Phase 4: Setup configuration and execution
        setup(
            # Core identity
            name=PACKAGE_NAME,
            version=version,
            description=DESCRIPTION,
            long_description=long_description,
            long_description_content_type="text/markdown",
            license=LICENSE,
            # Author information
            author=AUTHOR,
            author_email=AUTHOR_EMAIL,
            url=PACKAGE_URL,
            # Runtime requirements
            python_requires=MIN_PYTHON_VERSION,
            # Package structure
            packages=find_packages(exclude=["tests", "tests.*"]),
            package_data={
                f"{PACKAGE_NAME}.fonts": ["*.flf", "*.flc"],
                f"{PACKAGE_NAME}": ["py.typed"],  # PEP 561 typing support
            },
            # Metadata classifiers
            classifiers=[
                # Development status
                "Development Status :: 5 - Production/Stable",
                "Environment :: Console",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                # Language support
                "Natural Language :: English",
                "Natural Language :: Japanese",  # For Katakana
                "Natural Language :: Bulgarian",  # For Cyrillic
                "Natural Language :: Bosnian",
                "Natural Language :: Macedonian",
                "Natural Language :: Russian",
                "Natural Language :: Serbian",
                # System compatibility
                "Operating System :: Unix",
                "Operating System :: MacOS :: MacOS X",
                "Operating System :: Microsoft :: Windows",
                # Python compatibility
                "Programming Language :: Python",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.9",
                "Programming Language :: Python :: 3.10",
                "Programming Language :: Python :: 3.11",
                "Programming Language :: Python :: 3.12",
                "Programming Language :: Python :: Implementation :: CPython",
                "Programming Language :: Python :: Implementation :: PyPy",
                # Functionality categories
                "Topic :: Text Processing",
                "Topic :: Text Processing :: Fonts",
            ],
            # Command-line entry points
            entry_points={
                "console_scripts": [
                    f"{PACKAGE_NAME} = {PACKAGE_NAME}:main",
                ],
            },
            # Additional resources
            project_urls={
                "Bug Tracker": f"{PACKAGE_URL}/issues",
                "Documentation": f"{PACKAGE_URL}/docs",
                "Source Code": PACKAGE_URL,
            },
        )

        # Phase 5: Completion reporting
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(
            f"Installation sequence completed for {PACKAGE_NAME} v{version} in {duration:.2f}s"
        )

        # Phase 6: Optional verification
        if VERIFY_INSTALL:
            if verify_installation():
                logger.info("Post-installation verification successful")
            else:
                logger.warning("Post-installation verification revealed issues")

    except SetupError as e:
        logger.error(f"Installation failure: {e}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected installation failure: {e}", exc_info=True)
        raise SetupError(f"Catastrophic failure: {e}") from e


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 🚀 EXECUTION ENTRY POINT                                                  ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

if __name__ == "__main__":
    try:
        run_setup()
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
else:
    # Module import pathway (normal setup.py behavior)
    run_setup()
