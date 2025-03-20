from .utils import unicode_string


class FigletString(unicode_string):
    """
    Rendered figlet font

    A specialized string class for ASCII art text that provides
    transformation operations specifically designed for FIGlet output.
    Maintains the structural integrity of ASCII art during manipulation.
    """

    # translation map for reversing ascii art / -> \, etc.
    __reverse_map__ = (
        "\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f"
        "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
        " !\"#$%&')(*+,-.\\"
        "0123456789:;>=<?"
        "@ABCDEFGHIJKLMNO"
        "PQRSTUVWXYZ]/[^_"
        "`abcdefghijklmno"
        "pqrstuvwxyz}|{~\x7f"
        "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f"
        "\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
        "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf"
        "\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
        "\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf"
        "\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
        "\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
        "\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
    )

    # translation map for flipping ascii art ^ -> v, etc.
    __flip_map__ = (
        "\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f"
        "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
        " !\"#$%&'()*+,-.\\"
        "0123456789:;<=>?"
        "@VBCDEFGHIJKLWNO"
        "bQbSTUAMXYZ[/]v-"
        "`aPcdefghijklwno"
        "pqrstu^mxyz{|}~\x7f"
        "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f"
        "\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
        "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf"
        "\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
        "\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf"
        "\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
        "\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
        "\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
    )

    def reverse(self):
        """
        Reverse the FIGlet text horizontally (mirror image).

        Returns:
            A new FigletString with reversed content

        Example:
            /\  becomes  /\
            \/           \/
        """
        if not self:
            return self

        # Split the string into lines, reverse each line and translate special chars
        result = []
        for line in self.splitlines():
            line = line.translate(self.__reverse_map__)
            result.append(line[::-1])

        # Join lines back together and return as a new FigletString
        return self.__class__("\n".join(result))

    def flip(self):
        """
        Flip the FIGlet text vertically (upside down).

        Returns:
            A new FigletString with flipped content

        Example:
            /\  becomes  \/
            \/           /\
        """
        if not self:
            return self

        # Process the text line by line and apply character translations
        result = []
        for line in self.splitlines():
            line = line.translate(self.__flip_map__)
            result.append(line)

        # Reverse the order of lines and return as a new FigletString
        return self.__class__("\n".join(result[::-1]))

    def strip_surrounding_newlines(self):
        """
        Remove empty lines from the beginning and end of the FIGlet text.

        Returns:
            A new FigletString with extra lines removed
        """
        return self.__class__(self.strip("\n"))

    def normalize_surrounding_newlines(self):
        """
        Ensure exactly one empty line at the beginning and end of the FIGlet text.

        Returns:
            A new FigletString with normalized line spacing
        """
        # Strip all surrounding newlines first
        text = self.strip("\n")
        # Add exactly one newline at beginning and end
        return self.__class__(f"\n{text}\n")

    def center(self, width=None):
        """
        Center each line of the FIGlet text within the specified width.

        Args:
            width: Width to center within (default: use widest line)

        Returns:
            A new FigletString with centered content
        """
        if not self:
            return self

        lines = self.splitlines()

        # Calculate width if not provided
        if width is None:
            width = max(len(line) for line in lines)

        # Center each line
        result = []
        for line in lines:
            padding = (width - len(line)) // 2
            result.append(" " * padding + line)

        return self.__class__("\n".join(result))

    def join(self, iterable):
        """
        Join FigletStrings vertically, with self as separator.

        Args:
            iterable: Collection of FigletStrings to join

        Returns:
            A new FigletString with joined content
        """
        return self.__class__(super(FigletString, self).join(iterable))

    def overlay(self, other, x_offset=0, y_offset=0, transparent=True):
        """
        Overlay another FigletString on top of this one.

        Args:
            other: FigletString to overlay
            x_offset: Horizontal offset
            y_offset: Vertical offset
            transparent: Whether spaces in other should be transparent

        Returns:
            A new FigletString with the overlay applied
        """
        if not other:
            return self.__class__(self)

        self_lines = self.splitlines()
        other_lines = other.splitlines()
        result_lines = list(self_lines)  # Create a copy

        # Handle empty base
        if not self_lines:
            return self.__class__(other)

        # Apply overlay
        for i, other_line in enumerate(other_lines):
            if i + y_offset < 0 or i + y_offset >= len(result_lines):
                continue

            base_line = result_lines[i + y_offset]

            # Create new line with overlay
            new_line = list(base_line)
            for j, char in enumerate(other_line):
                if j + x_offset < 0:
                    continue
                if j + x_offset >= len(new_line):
                    # Extend line if needed
                    new_line.extend(" " * (j + x_offset - len(new_line) + 1))

                # Apply character from overlay if not transparent or not space
                if not transparent or char != " ":
                    new_line[j + x_offset] = char

            result_lines[i + y_offset] = "".join(new_line)

        return self.__class__("\n".join(result_lines))

    def __add__(self, other):
        """
        Concatenate this FigletString with another string.

        Args:
            other: String to append

        Returns:
            A new FigletString with combined content
        """
        return self.__class__(super(FigletString, self).__add__(other))
