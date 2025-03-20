def color_to_ansi(color, isBackground):
    if not color:
        return ""
    color = color.upper()
    if color.count(";") > 0 and color.count(";") != 2:
        raise InvalidColor("Specified color '{}' not a valid color in R;G;B format")
    elif color.count(";") == 0 and color not in COLOR_CODES:
        raise InvalidColor(
            f"Specified color '{color}' not found in ANSI COLOR_CODES list"
        )

    if color in COLOR_CODES:
        ansiCode = COLOR_CODES[color]
        if isBackground:
            ansiCode += 10
    else:
        ansiCode = 48 if isBackground else 38
        ansiCode = f"{ansiCode};2;{color}"

    return f"\033[{ansiCode}m"


def parse_color(color):
    foreground, _, background = color.partition(":")
    ansiForeground = color_to_ansi(foreground, isBackground=False)
    ansiBackground = color_to_ansi(background, isBackground=True)
    return ansiForeground + ansiBackground
