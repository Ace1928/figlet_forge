"""
FigletString handling for Figlet Forge.

This module implements the FigletString class which represents a rendered
figlet text output with various transformation capabilities.
"""


class FigletString(str):
    """
    Represents rendered figlet font output as a string with
    additional transformation methods.

    FigletString extends the built-in str type to provide operations
    specific to figlet output like flipping or reversing the ASCII art.
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
        Reverse the figlet text (horizontal mirror).

        Returns:
            A new FigletString with characters reversed and appropriate
            character substitutions for mirror symmetry.
        """
        out = []
        for row in self.splitlines():
            out.append(row.translate(self.__reverse_map__)[::-1])

        return self.newFromList(out)

    def flip(self):
        """
        Flip the figlet text upside down (vertical mirror).

        Returns:
            A new FigletString with rows reversed and appropriate character
            substitutions for vertical symmetry.
        """
        out = []
        for row in self.splitlines()[::-1]:
            out.append(row.translate(self.__flip_map__))

        return self.newFromList(out)

    def strip_surrounding_newlines(self):
        """
        Strip empty lines from the beginning and end of the figlet text.

        Returns:
            A new FigletString without leading or trailing empty lines
        """
        out = []
        chars_seen = False
        for row in self.splitlines():
            # if the row isn't empty or if we're in the middle of the font character, add the line.
            if row.strip() != "" or chars_seen:
                chars_seen = True
                out.append(row)

        # rstrip to get rid of the trailing newlines
        return self.newFromList(out).rstrip()

    def normalize_surrounding_newlines(self):
        """
        Normalize to exactly one surrounding newline before and after.

        Returns:
            A new FigletString with exactly one newline before and after
        """
        return "\n" + self.strip_surrounding_newlines() + "\n"

    def newFromList(self, list_of_rows):
        """
        Create a new FigletString from a list of rows.

        Args:
            list_of_rows: List of strings, each representing one row

        Returns:
            A new FigletString instance
        """
        return FigletString("\n".join(list_of_rows) + "\n")

    def apply_color(self, color_spec):
        """
        Apply ANSI color to the figlet text.

        This is an enhancement not present in the original pyfiglet,
        but implemented in a way that preserves compatibility.

        Args:
            color_spec: Color specification string ("foreground:background")

        Returns:
            A new FigletString with color applied
        """
        from .color import colored_format

        return FigletString(colored_format(self, color_spec))
