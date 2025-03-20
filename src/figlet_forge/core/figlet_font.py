class FigletFont:
    """
    This class represents the currently loaded font, including
    meta-data about how it should be displayed by default
    """

    reMagicNumber = re.compile(r"^[tf]lf2.")
    reEndMarker = re.compile(r"(.)\s*$")

    def __init__(self, font=DEFAULT_FONT):
        self.font = font

        self.comment = ""
        self.chars = {}
        self.width = {}
        self.data = self.preloadFont(font)
        self.loadFont()

    @classmethod
    def preloadFont(cls, font):
        """
        Load font data if exist
        """
        # Find a plausible looking font file.
        data = None
        font_path = None
        for extension in ("tlf", "flf"):
            fn = "%s.%s" % (font, extension)
            path = importlib.resources.files("pyfiglet.fonts").joinpath(fn)
            if path.exists():
                font_path = path
                break
            else:
                for location in ("./", SHARED_DIRECTORY):
                    full_name = os.path.join(location, fn)
                    if os.path.isfile(full_name):
                        font_path = pathlib.Path(full_name)
                        break

        # Unzip the first file if this file/stream looks like a ZIP file.
        if font_path:
            with font_path.open("rb") as f:
                if zipfile.is_zipfile(f):
                    with zipfile.ZipFile(f) as zip_file:
                        zip_font = zip_file.open(zip_file.namelist()[0])
                        data = zip_font.read()
                else:
                    # ZIP file check moves the current file pointer - reset to start of file.
                    f.seek(0)
                    data = f.read()

        # Return the decoded data (if any).
        if data:
            return data.decode("UTF-8", "replace")
        else:
            raise FontNotFound(font)

    @classmethod
    def isValidFont(cls, font):
        if not font.endswith((".flf", ".tlf")):
            return False
        f = None
        full_file = os.path.join(SHARED_DIRECTORY, font)
        if os.path.isfile(font):
            f = open(font, "rb")
        elif os.path.isfile(full_file):
            f = open(full_file, "rb")
        else:
            f = importlib.resources.files("pyfiglet.fonts").joinpath(font).open("rb")

        if zipfile.is_zipfile(f):
            # If we have a match, the ZIP file spec says we should just read the first file in the ZIP.
            with zipfile.ZipFile(f) as zip_file:
                zip_font = zip_file.open(zip_file.namelist()[0])
                header = zip_font.readline().decode("UTF-8", "replace")
        else:
            # ZIP file check moves the current file pointer - reset to start of file.
            f.seek(0)
            header = f.readline().decode("UTF-8", "replace")

        f.close()

        return cls.reMagicNumber.search(header)

    @classmethod
    def getFonts(cls):
        all_files = importlib.resources.files("pyfiglet.fonts").iterdir()
        if os.path.isdir(SHARED_DIRECTORY):
            all_files = itertools.chain(
                all_files, pathlib.Path(SHARED_DIRECTORY).iterdir()
            )
        return [
            font.name.split(".", 2)[0]
            for font in all_files
            if font.is_file() and cls.isValidFont(font.name)
        ]

    @classmethod
    def infoFont(cls, font, short=False):
        """
        Get information of font
        """
        data = FigletFont.preloadFont(font)
        infos = []
        reStartMarker = re.compile(
            r"""
            ^(FONT|COMMENT|FONTNAME_REGISTRY|FAMILY_NAME|FOUNDRY|WEIGHT_NAME|
              SETWIDTH_NAME|SLANT|ADD_STYLE_NAME|PIXEL_SIZE|POINT_SIZE|
              RESOLUTION_X|RESOLUTION_Y|SPACING|AVERAGE_WIDTH|
              FONT_DESCENT|FONT_ASCENT|CAP_HEIGHT|X_HEIGHT|FACE_NAME|FULL_NAME|
              COPYRIGHT|_DEC_|DEFAULT_CHAR|NOTICE|RELATIVE_).*""",
            re.VERBOSE,
        )
        reEndMarker = re.compile(r"^.*[@#$]$")
        for line in data.splitlines()[0:100]:
            if (
                cls.reMagicNumber.search(line) is None
                and reStartMarker.search(line) is None
                and reEndMarker.search(line) is None
            ):
                infos.append(line)
        return "\n".join(infos) if not short else infos[0]

    @staticmethod
    def installFonts(file_name):
        """
        Install the specified font file to this system.
        """
        if hasattr(importlib.resources.files("pyfiglet"), "resolve"):
            # Figlet looks like a standard directory - so lets use that to install new fonts.
            location = str(importlib.resources.files("pyfiglet.fonts"))
        else:
            # Figlet is installed using a zipped resource - don't try to upload to it.
            location = SHARED_DIRECTORY

        print(f"Installing {file_name} to {location}")

        # Make sure the required destination directory exists
        if not os.path.exists(location):
            os.makedirs(location)

        # Copy the font definitions - unpacking any zip files as needed.
        if os.path.splitext(file_name)[1].lower() == ".zip":
            # Ignore any structure inside the ZIP file.
            with zipfile.ZipFile(file_name) as zip_file:
                for font in zip_file.namelist():
                    font_file = os.path.basename(font)
                    if not font_file:
                        continue
                    with zip_file.open(font) as src:
                        with open(os.path.join(location, font_file), "wb") as dest:
                            shutil.copyfileobj(src, dest)
        else:
            shutil.copy(file_name, location)

    def loadFont(self):
        """
        Parse loaded font data for the rendering engine to consume
        """
        try:
            # Remove any unicode line splitting characters other
            # than CRLF - to match figlet line parsing
            data = re.sub(r"[\u0085\u2028\u2029]", " ", self.data)

            # Parse first line of file, the header
            data = data.splitlines()

            header = data.pop(0)
            if self.reMagicNumber.search(header) is None:
                raise FontError("%s is not a valid figlet font" % self.font)

            header = self.reMagicNumber.sub("", header)
            header = header.split()

            if len(header) < 6:
                raise FontError("malformed header for %s" % self.font)

            hardBlank = header[0]
            height, baseLine, maxLength, oldLayout, commentLines = map(int, header[1:6])
            printDirection = fullLayout = None

            # these are all optional for backwards compat
            if len(header) > 6:
                printDirection = int(header[6])
            if len(header) > 7:
                fullLayout = int(header[7])

            # if the new layout style isn't available,
            # convert old layout style. backwards compatibility
            if fullLayout is None:
                if oldLayout == 0:
                    fullLayout = 64
                elif oldLayout < 0:
                    fullLayout = 0
                else:
                    fullLayout = (oldLayout & 31) | 128

            # Some header information is stored for later, the rendering
            # engine needs to know this stuff.
            self.height = height
            self.hardBlank = hardBlank
            self.printDirection = printDirection
            self.smushMode = fullLayout

            # Strip out comment lines
            for i in range(0, commentLines):
                self.comment += data.pop(0)

            def __char(data):
                """
                Function loads one character in the internal array from font
                file content
                """
                end = None
                width = 0
                chars = []
                for j in range(0, height):
                    line = data.pop(0)
                    if end is None:
                        end = self.reEndMarker.search(line).group(1)
                        end = re.compile(re.escape(end) + r"{1,2}\s*$")

                    line = end.sub("", line)

                    if len(line) > width:
                        width = len(line)
                    chars.append(line)
                return width, chars

            # Load ASCII standard character set (32 - 127).
            # Don't skip space definition as later rendering pipeline will
            # ignore all missing chars and space is critical for the line
            # breaking logic.
            for i in range(32, 127):
                width, letter = __char(data)
                if i == 32 or "".join(letter) != "":
                    self.chars[i] = letter
                    self.width[i] = width

            # Load German Umlaute - the follow directly after standard character 127
            if data:
                for i in "ÄÖÜäöüß":
                    width, letter = __char(data)
                    if "".join(letter) != "":
                        self.chars[ord(i)] = letter
                        self.width[ord(i)] = width

            # Load ASCII extended character set
            while data:
                line = data.pop(0).strip()
                i = line.split(" ", 1)[0]
                if i == "":
                    continue
                hex_match = re.search("^0x", i, re.IGNORECASE)
                if hex_match is not None:
                    i = int(i, 16)
                    width, letter = __char(data)
                    if "".join(letter) != "":
                        self.chars[i] = letter
                        self.width[i] = width

        except Exception as e:
            raise FontError("problem parsing %s font: %s" % (self.font, e))

    def __str__(self):
        return "<FigletFont object: %s>" % self.font


unicode_string = type("".encode("ascii").decode("ascii"))
