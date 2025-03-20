class FigletProduct:
    """
    This class stores the internal build part of
    the ascii output string
    """

    def __init__(self):
        self.queue = list()
        self.buffer_string = ""

    def append(self, buffer):
        self.queue.append(buffer)

    def getString(self):
        return FigletString(self.buffer_string)


class FigletBuilder:
    """
    Represent the internals of the build process
    """

    def __init__(self, text, font, direction, width, justify):

        self.text = list(map(ord, list(text)))
        self.direction = direction
        self.width = width
        self.font = font
        self.justify = justify

        self.iterator = 0
        self.maxSmush = 0
        self.newBlankRegistered = False

        self.curCharWidth = 0
        self.prevCharWidth = 0
        self.currentTotalWidth = 0

        self.blankMarkers = list()
        self.product = FigletProduct()
        self.buffer = ["" for i in range(self.font.height)]

        # constants.. lifted from figlet222
        self.SM_EQUAL = 1  # smush equal chars (not hardblanks)
        self.SM_LOWLINE = 2  # smush _ with any char in hierarchy
        self.SM_HIERARCHY = 4  # hierarchy: |, /\, [], {}, (), <>
        self.SM_PAIR = 8  # hierarchy: [ + ] -> |, { + } -> |, ( + ) -> |
        self.SM_BIGX = 16  # / + \ -> X, > + < -> X
        self.SM_HARDBLANK = 32  # hardblank + hardblank -> hardblank
        self.SM_KERN = 64
        self.SM_SMUSH = 128

    # builder interface

    def addCharToProduct(self):
        curChar = self.getCurChar()

        # if the character is a newline, we flush the buffer
        if self.text[self.iterator] == ord("\n"):
            self.blankMarkers.append(([row for row in self.buffer], self.iterator))
            self.handleNewLine()
            return None

        if curChar is None:
            return
        if self.width < self.getCurWidth():
            raise CharNotPrinted("Width is not enough to print this character")
        self.curCharWidth = self.getCurWidth()
        self.maxSmush = self.currentSmushAmount(curChar)

        self.currentTotalWidth = len(self.buffer[0]) + self.curCharWidth - self.maxSmush

        if self.text[self.iterator] == ord(" "):
            self.blankMarkers.append(([row for row in self.buffer], self.iterator))

        if self.text[self.iterator] == ord("\n"):
            self.blankMarkers.append(([row for row in self.buffer], self.iterator))
            self.handleNewLine()

        if self.currentTotalWidth >= self.width:
            self.handleNewLine()
        else:
            for row in range(0, self.font.height):
                self.addCurCharRowToBufferRow(curChar, row)

        self.prevCharWidth = self.curCharWidth

    def goToNextChar(self):
        self.iterator += 1

    def returnProduct(self):
        """
        Returns the output string created by formatProduct
        """
        if self.buffer[0] != "":
            self.flushLastBuffer()
        self.formatProduct()
        return self.product.getString()

    def isNotFinished(self):
        ret = self.iterator < len(self.text)
        return ret

    # private

    def flushLastBuffer(self):
        self.product.append(self.buffer)

    def formatProduct(self):
        """
        This create the output string representation from
        the internal representation of the product
        """
        string_acc = ""
        for buffer in self.product.queue:
            buffer = self.justifyString(self.justify, buffer)
            string_acc += self.replaceHardblanks(buffer)
        self.product.buffer_string = string_acc

    def getCharAt(self, i):
        if i < 0 or i >= len(list(self.text)):
            return None
        c = self.text[i]

        if c not in self.font.chars:
            return None
        else:
            return self.font.chars[c]

    def getCharWidthAt(self, i):
        if i < 0 or i >= len(self.text):
            return None
        c = self.text[i]
        if c not in self.font.chars:
            return None
        else:
            return self.font.width[c]

    def getCurChar(self):
        return self.getCharAt(self.iterator)

    def getCurWidth(self):
        return self.getCharWidthAt(self.iterator)

    def getLeftSmushedChar(self, i, addLeft):
        idx = len(addLeft) - self.maxSmush + i
        if idx >= 0 and idx < len(addLeft):
            left = addLeft[idx]
        else:
            left = ""
        return left, idx

    def currentSmushAmount(self, curChar):
        return self.smushAmount(self.buffer, curChar)

    def updateSmushedCharInLeftBuffer(self, addLeft, idx, smushed):
        l = list(addLeft)
        if idx < 0 or idx > len(l):
            return addLeft
        l[idx] = smushed
        addLeft = "".join(l)
        return addLeft

    def smushRow(self, curChar, row):
        addLeft = self.buffer[row]
        addRight = curChar[row]

        if self.direction == "right-to-left":
            addLeft, addRight = addRight, addLeft

        for i in range(0, self.maxSmush):
            left, idx = self.getLeftSmushedChar(i, addLeft)
            right = addRight[i]
            smushed = self.smushChars(left=left, right=right)
            addLeft = self.updateSmushedCharInLeftBuffer(addLeft, idx, smushed)
        return addLeft, addRight

    def addCurCharRowToBufferRow(self, curChar, row):
        addLeft, addRight = self.smushRow(curChar, row)
        self.buffer[row] = addLeft + addRight[self.maxSmush :]

    def cutBufferCommon(self):
        self.currentTotalWidth = 0
        self.buffer = ["" for i in range(self.font.height)]
        self.blankMarkers = list()
        self.prevCharWidth = 0
        curChar = self.getCurChar()
        if curChar is None:
            return
        self.maxSmush = self.currentSmushAmount(curChar)

    def cutBufferAtLastBlank(self, saved_buffer, saved_iterator):
        self.product.append(saved_buffer)
        self.iterator = saved_iterator
        self.cutBufferCommon()

    def cutBufferAtLastChar(self):
        self.product.append(self.buffer)
        self.iterator -= 1
        self.cutBufferCommon()

    def blankExist(self, last_blank):
        return last_blank != -1

    def getLastBlank(self):
        try:
            saved_buffer, saved_iterator = self.blankMarkers.pop()
        except IndexError:
            return -1, -1
        return (saved_buffer, saved_iterator)

    def handleNewLine(self):
        saved_buffer, saved_iterator = self.getLastBlank()
        if self.blankExist(saved_iterator):
            self.cutBufferAtLastBlank(saved_buffer, saved_iterator)
        else:
            self.cutBufferAtLastChar()

    def justifyString(self, justify, buffer):
        if justify == "right":
            for row in range(0, self.font.height):
                buffer[row] = (" " * (self.width - len(buffer[row]) - 1)) + buffer[row]
        elif justify == "center":
            for row in range(0, self.font.height):
                buffer[row] = (" " * int((self.width - len(buffer[row])) / 2)) + buffer[
                    row
                ]
        return buffer

    def replaceHardblanks(self, buffer):
        string = "\n".join(buffer) + "\n"
        string = string.replace(self.font.hardBlank, " ")
        return string

    def smushAmount(self, buffer=[], curChar=[]):
        """
        Calculate the amount of smushing we can do between this char and the
        last If this is the first char it will throw a series of exceptions
        which are caught and cause appropriate values to be set for later.

        This differs from C figlet which will just get bogus values from
        memory and then discard them after.
        """
        if (self.font.smushMode & (self.SM_SMUSH | self.SM_KERN)) == 0:
            return 0

        maxSmush = self.curCharWidth
        for row in range(0, self.font.height):
            lineLeft = buffer[row]
            lineRight = curChar[row]
            if self.direction == "right-to-left":
                lineLeft, lineRight = lineRight, lineLeft

            # Only strip ascii space to match figlet exactly.
            linebd = len(lineLeft.rstrip(" ")) - 1
            if linebd < 0:
                linebd = 0

            if linebd < len(lineLeft):
                ch1 = lineLeft[linebd]
            else:
                linebd = 0
                ch1 = ""

            # Only strip ascii space to match figlet exactly.
            charbd = len(lineRight) - len(lineRight.lstrip(" "))
            if charbd < len(lineRight):
                ch2 = lineRight[charbd]
            else:
                charbd = len(lineRight)
                ch2 = ""

            amt = charbd + len(lineLeft) - 1 - linebd

            if ch1 == "" or ch1 == " ":
                amt += 1
            elif ch2 != "" and self.smushChars(left=ch1, right=ch2) is not None:
                amt += 1

            if amt < maxSmush:
                maxSmush = amt

        return maxSmush

    def smushChars(self, left="", right=""):
        """
        Given 2 characters which represent the edges rendered figlet
        fonts where they would touch, see if they can be smushed together.
        Returns None if this cannot or should not be done.
        """
        # Don't use isspace because this also matches unicode chars that figlet
        # treats as hard breaks
        if left == " ":
            return right
        if right == " ":
            return left

        # Disallows overlapping if previous or current char has a width of 1 or
        # zero
        if (self.prevCharWidth < 2) or (self.curCharWidth < 2):
            return

        # kerning only
        if (self.font.smushMode & self.SM_SMUSH) == 0:
            return

        # smushing by universal overlapping
        if (self.font.smushMode & 63) == 0:
            # Ensure preference to visiable characters.
            if left == self.font.hardBlank:
                return right
            if right == self.font.hardBlank:
                return left

            # Ensures that the dominant (foreground)
            # fig-character for overlapping is the latter in the
            # user's text, not necessarily the rightmost character.
            if self.direction == "right-to-left":
                return left
            else:
                return right

        if self.font.smushMode & self.SM_HARDBLANK:
            if left == self.font.hardBlank and right == self.font.hardBlank:
                return left

        if left == self.font.hardBlank or right == self.font.hardBlank:
            return

        if self.font.smushMode & self.SM_EQUAL:
            if left == right:
                return left

        smushes = ()

        if self.font.smushMode & self.SM_LOWLINE:
            smushes += (("_", r"|/\[]{}()<>"),)

        if self.font.smushMode & self.SM_HIERARCHY:
            smushes += (
                ("|", r"/\[]{}()<>"),
                (r"\/", "[]{}()<>"),
                ("[]", "{}()<>"),
                ("{}", "()<>"),
                ("()", "<>"),
            )

        for a, b in smushes:
            if left in a and right in b:
                return right
            if right in a and left in b:
                return left

        if self.font.smushMode & self.SM_PAIR:
            for pair in [left + right, right + left]:
                if pair in ["[]", "{}", "()"]:
                    return "|"

        if self.font.smushMode & self.SM_BIGX:
            if (left == "/") and (right == "\\"):
                return "|"
            if (right == "/") and (left == "\\"):
                return "Y"
            if (left == ">") and (right == "<"):
                return "X"
        return
