class FigletString(unicode_string):
    """
    Rendered figlet font
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
        out = []
        for row in self.splitlines():
            out.append(row.translate(self.__reverse_map__)[::-1])

        return self.newFromList(out)

    def flip(self):
        out = []
        for row in self.splitlines()[::-1]:
            out.append(row.translate(self.__flip_map__))

        return self.newFromList(out)

    # doesn't do self.strip() because it could remove leading whitespace on first line of the font
    # doesn't do row.strip() because it could remove empty lines within the font character
    def strip_surrounding_newlines(self):
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
        return "\n" + self.strip_surrounding_newlines() + "\n"

    def newFromList(self, list):
        return FigletString("\n".join(list) + "\n")
