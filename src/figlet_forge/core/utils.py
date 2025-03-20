def figlet_format(text, font=DEFAULT_FONT, **kwargs):
    fig = Figlet(font, **kwargs)
    return fig.renderText(text)


def print_figlet(text, font=DEFAULT_FONT, colors=":", **kwargs):
    ansiColors = parse_color(colors)
    if ansiColors:
        sys.stdout.write(ansiColors)

    print(figlet_format(text, font, **kwargs))

    if ansiColors:
        sys.stdout.write(RESET_COLORS.decode("UTF-8", "replace"))
        sys.stdout.flush()
