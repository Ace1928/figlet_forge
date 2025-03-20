import re
import shutil
import zipfile
from importlib import resources
from pathlib import Path
from typing import Dict, List, Union

from .exceptions import FontError, FontNotFound
from .utils import unicode_string

unicode_string = type("".encode("ascii").decode("ascii"))


class FigletFont:
    """
    FigletFont represents a font loaded from a .flf file.

    This class handles font loading, parsing, and character extraction
    with comprehensive Unicode support and robust error handling.
    """

    def __init__(self, font: Union[str, Path] = "standard"):
        """
        Initialize the FigletFont.

        Args:
            font: Name of the font or a Path object pointing to a font file

        Raises:
            FontNotFound: If the specified font cannot be located
            FontError: If there are issues parsing the font file
        """
        self.font = font
        self.font_name = ""
        self.comment = ""
        self.chars: Dict[int, List[str]] = {}  # Map of character codes to figlet lines
        self.width = {}
        self.data = None
        self.reMagicNumber = re.compile(r"^flf2.")
        self.reEndMarker = re.compile(r"(.)\s*$")
        self.base_dir = None  # Will be determined during loading

        self.height = 0  # Height of every character
        self.hardblank = ""  # Hard blank character
        self.max_length = 0  # Maximum line length
        self.old_layout = 0  # Layout settings
        self.comment_count = 0  # Number of comment lines
        self.print_direction = 0  # Print direction
        self.full_layout = 0  # Full layout settings
        self.codetag_count = 0  # Number of code-tagged characters

        # German special chars - required for backward compatibility
        self.deutsch = {
            ord("Ä"): 0x8E,
            ord("Ö"): 0x99,
            ord("Ü"): 0x9A,
            ord("ä"): 0x84,
            ord("ö"): 0x94,
            ord("ü"): 0x81,
            ord("ß"): 0xE1,
        }

        self.loadFont()

    def loadFont(self) -> None:
        """
        Load the font data from the specified source.

        Raises:
            FontNotFound: If the font file cannot be located
        """
        # Priority of font search:
        # 1. Direct file path
        # 2. Package resources in figlet_forge/fonts/
        # 3. Standard font directories

        # If the font is a direct path
        if isinstance(self.font, Path) or (
            isinstance(self.font, str) and ("/" in self.font or "\\" in self.font)
        ):
            font_path = Path(self.font)
            if not font_path.exists():
                raise FontNotFound(f"Font file not found: {font_path}")

            with open(font_path, "rb") as f:
                self.data = f.read().decode("latin-1", "replace")
            self.base_dir = font_path.parent
            return

        # Check package resources
        try:
            with resources.open_text("figlet_forge.fonts", f"{self.font}.flf") as f:
                self.data = f.read()
                return
        except (ModuleNotFoundError, FileNotFoundError):
            pass  # Continue to next search method

        # Search in standard font directories
        from ..version import SHARED_DIRECTORY

        search_dirs = [
            Path(SHARED_DIRECTORY) / "fonts",
            Path(__file__).parent.parent.parent / "fonts",
            Path.home() / ".figlet_forge" / "fonts",
            Path("/usr/share/figlet"),
            Path("/usr/local/share/figlet"),
        ]

        for directory in search_dirs:
            if not directory.exists():
                continue

            # Look for exact match first
            font_path = directory / f"{self.font}.flf"
            if font_path.exists():
                with open(font_path, "rb") as f:
                    self.data = f.read().decode("latin-1", "replace")
                self.base_dir = directory
                return

            # Then look for case-insensitive match
            for file in directory.glob("*.flf"):
                if file.stem.lower() == self.font.lower():
                    with open(file, "rb") as f:
                        self.data = f.read().decode("latin-1", "replace")
                    self.base_dir = directory
                    return

        # Font not found
        raise FontNotFound(f"Font '{self.font}' not found after exhaustive search")

    def parseFont(self) -> None:
        """
        Parse the font data after loading.

        Raises:
            FontError: If there are issues parsing the font file
        """
        if not self.data:
            raise FontError("No font data loaded to parse")

        lines = self.data.splitlines()

        # Parse header line
        try:
            header = lines[0].split()

            if not self.reMagicNumber.search(header[0]):
                raise FontError("Not a valid FIGlet font file")

            self.hardblank = header[0][-1]
            self.height = int(header[1])
            self.max_length = int(header[3])
            self.old_layout = int(header[4])
            self.comment_count = int(header[5])

            if len(header) > 6:
                self.print_direction = int(header[6])
            if len(header) > 7:
                self.full_layout = int(header[7])
            if len(header) > 8:
                self.codetag_count = int(header[8])

        except (IndexError, ValueError) as e:
            raise FontError(f"Error parsing font header: {e}")

        # Skip comment lines
        try:
            line_no = self.comment_count + 1

            # Load ASCII standard character set (required)
            for i in range(32, 127):
                end = None
                width = 0

                for j in range(0, self.height):
                    if end:
                        line = lines[line_no + j][0:end]
                    else:
                        line = lines[line_no + j]

                    if j == 0:
                        match = self.reEndMarker.search(line)
                        if match:
                            end = match.start(1)
                            width = end
                        else:
                            width = len(line)

                    if i not in self.chars:
                        self.chars[i] = []

                    self.chars[i].append(line)

                self.width[i] = width
                line_no += self.height

            # Load additional characters (German, code-tagged, etc.)
            self.loadGerman(lines, line_no)
            self.loadCodetagged(lines, line_no)

        except Exception as e:
            raise FontError(f"Error parsing font data: {e}")

    def loadGerman(self, lines: List[str], line_no: int) -> None:
        """
        Load German character set for backward compatibility.

        Args:
            lines: Font file lines
            line_no: Current line number in parsing
        """
        # This method is specifically for compatibility with older FIGlet functionality
        # which required special handling of German characters
        deutsch_chars = [91, 92, 93, 123, 124, 125, 126]
        for i in deutsch_chars:
            try:
                end = None

                for j in range(0, self.height):
                    if end:
                        line = lines[line_no + j][0:end]
                    else:
                        line = lines[line_no + j]
                        match = self.reEndMarker.search(line)
                        if match:
                            end = match.start(1)

                    if i not in self.chars:
                        self.chars[i] = []
                    self.chars[i].append(line)

                line_no += self.height
            except IndexError:
                # If we hit an IndexError, we're beyond the end of the file
                # Create zero-width characters as fallback for German chars
                for j in range(0, self.height):
                    if i not in self.chars:
                        self.chars[i] = []
                    self.chars[i].append("")

    def loadCodetagged(self, lines: List[str], line_no: int) -> None:
        """
        Load code-tagged characters if available.

        Args:
            lines: Font file lines
            line_no: Current line number in parsing
        """
        if self.codetag_count:
            for i in range(0, self.codetag_count):
                try:
                    # Get the code from the first line of the character
                    line = lines[line_no]
                    match = re.search(r"0x([0-9A-Fa-f]+)", line)
                    if match:
                        code = int(match.group(1), 16)

                        # Skip header line
                        line_no += 1
                        end = None

                        # Parse each row of the character
                        for j in range(0, self.height):
                            if end:
                                line = lines[line_no + j][0:end]
                            else:
                                line = lines[line_no + j]
                                match = self.reEndMarker.search(line)
                                if match:
                                    end = match.start(1)

                            if code not in self.chars:
                                self.chars[code] = []
                            self.chars[code].append(line)

                        line_no += self.height

                except IndexError:
                    # If we hit an IndexError, we're beyond the end of the file
                    break

    def getCharacter(self, char: Union[str, int]) -> List[str]:
        """
        Get the lines of the specified character.

        Args:
            char: Character or character code to retrieve

        Returns:
            List of strings representing the character's FIGlet lines
        """
        c = ord(char) if isinstance(char, str) else char

        if c in self.chars:
            return self.chars[c]

        # Handle German characters for backward compatibility
        if c in self.deutsch:
            return self.chars[self.deutsch[c]]

        # Special handling for unknown characters
        # Default to space or "block" character if configured
        if 32 in self.chars:
            return self.chars[32]  # Space as fallback

        # Last resort - create blank character with the right height
        return ["" for _ in range(self.height)]

    def getWidth(self, char: Union[str, int]) -> int:
        """
        Get the width of the specified character.

        Args:
            char: Character or character code to measure

        Returns:
            Width of the character in columns
        """
        c = ord(char) if isinstance(char, str) else char

        if c in self.width:
            return self.width[c]

        if c in self.deutsch and self.deutsch[c] in self.width:
            return self.width[self.deutsch[c]]

        # Attempt to calculate width from character data
        if c in self.chars:
            return max(len(l) for l in self.chars[c])

        # Default to space width
        if 32 in self.width:
            return self.width[32]

        # Zero width as last resort
        return 0

    @classmethod
    def getFonts(cls) -> List[str]:
        """
        Get list of available FIGlet fonts.

        Returns:
            List of font names
        """
        fonts = set()

        # Look in package resources
        try:
            package_fonts = [
                f.name[:-4]
                for f in resources.files("figlet_forge.fonts").iterdir()
                if f.name.endswith(".flf")
            ]
            fonts.update(package_fonts)
        except (ModuleNotFoundError, FileNotFoundError, AttributeError):
            pass  # Continue to next search method

        # Check standard directories
        from ..version import SHARED_DIRECTORY

        search_dirs = [
            Path(SHARED_DIRECTORY) / "fonts",
            Path(__file__).parent.parent.parent / "fonts",
            Path.home() / ".figlet_forge" / "fonts",
            Path("/usr/share/figlet"),
            Path("/usr/local/share/figlet"),
        ]

        for directory in search_dirs:
            if directory.exists():
                try:
                    dir_fonts = [f.stem for f in directory.glob("*.flf")]
                    fonts.update(dir_fonts)
                except Exception:
                    continue

        return sorted(list(fonts))

    @classmethod
    def infoFont(cls, font: str, short: bool = False) -> str:
        """
        Get information about a specific font.

        Args:
            font: Name of the font
            short: Whether to return only the first line of information

        Returns:
            Font information string

        Raises:
            FontNotFound: If the specified font cannot be found
        """
        try:
            # Load font data
            figfont = cls(font)

            # Extract the comment section
            data = figfont.data.splitlines()

            # Extract header info
            header = data[0].split()

            if short:
                return f"{font}: {' '.join(header[1:])}"

            # Return full comment section
            comment_lines = data[1 : figfont.comment_count + 1]
            info = [f"Font: {font}", f"Header: {' '.join(header[1:])}"]
            info.extend([f"Comment: {line}" for line in comment_lines])

            return "\n".join(info)

        except FontNotFound:
            return f"Font '{font}' not found"
        except Exception as e:
            return f"Error retrieving font info for '{font}': {str(e)}"

    @classmethod
    def installFonts(cls, source_path: Union[str, Path]) -> bool:
        """
        Install fonts from a file or directory to the user's font directory.

        Args:
            source_path: Path to font file, directory, or zip containing fonts

        Returns:
            True if fonts were installed successfully, False otherwise
        """
        # Create user font directory if it doesn't exist
        user_font_dir = Path.home() / ".figlet_forge" / "fonts"
        user_font_dir.mkdir(parents=True, exist_ok=True)

        path = Path(source_path)

        # Handle different source types
        try:
            if not path.exists():
                print(f"Source does not exist: {path}")
                return False

            if path.is_file():
                if path.suffix == ".flf":
                    # Single font file
                    dest = user_font_dir / path.name
                    shutil.copy2(path, dest)
                    print(f"Installed font: {path.name}")
                    return True
                elif path.suffix == ".zip":
                    # Zip archive of fonts
                    installed = 0
                    with zipfile.ZipFile(path) as z:
                        for item in z.namelist():
                            if item.endswith(".flf"):
                                font_name = Path(item).name
                                z.extract(item, user_font_dir)
                                print(f"Installed font from archive: {font_name}")
                                installed += 1
                    return installed > 0
            elif path.is_dir():
                # Directory of fonts
                installed = 0
                for font_file in path.glob("*.flf"):
                    dest = user_font_dir / font_file.name
                    shutil.copy2(font_file, dest)
                    print(f"Installed font: {font_file.name}")
                    installed += 1
                return installed > 0

            return False

        except Exception as e:
            print(f"Error installing fonts: {e}")
            return False
