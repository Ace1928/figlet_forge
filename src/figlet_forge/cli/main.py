def main():
    parser = OptionParser(version=__version__, usage="%prog [options] [text..]")
    parser.add_option(
        "-f",
        "--font",
        default=DEFAULT_FONT,
        help="font to render with (default: %default)",
        metavar="FONT",
    )
    parser.add_option(
        "-D",
        "--direction",
        type="choice",
        choices=("auto", "left-to-right", "right-to-left"),
        default="auto",
        metavar="DIRECTION",
        help="set direction text will be formatted in " "(default: %default)",
    )
    parser.add_option(
        "-j",
        "--justify",
        type="choice",
        choices=("auto", "left", "center", "right"),
        default="auto",
        metavar="SIDE",
        help="set justification, defaults to print direction",
    )
    parser.add_option(
        "-w",
        "--width",
        type="int",
        default=80,
        metavar="COLS",
        help="set terminal width for wrapping/justification " "(default: %default)",
    )
    parser.add_option(
        "-r",
        "--reverse",
        action="store_true",
        default=False,
        help="shows mirror image of output text",
    )
    parser.add_option(
        "-n",
        "--normalize-surrounding-newlines",
        action="store_true",
        default=False,
        help="output has one empty line before and after",
    )
    parser.add_option(
        "-s",
        "--strip-surrounding-newlines",
        action="store_true",
        default=False,
        help="removes empty leading and trailing lines",
    )
    parser.add_option(
        "-F",
        "--flip",
        action="store_true",
        default=False,
        help="flips rendered output text over",
    )
    parser.add_option(
        "-l",
        "--list_fonts",
        action="store_true",
        default=False,
        help="show installed fonts list",
    )
    parser.add_option(
        "-i",
        "--info_font",
        action="store_true",
        default=False,
        help="show font's information, use with -f FONT",
    )
    parser.add_option(
        "-L",
        "--load",
        default=None,
        help="load and install the specified font definition",
    )
    parser.add_option(
        "-c",
        "--color",
        default=":",
        help="""prints text with passed foreground color,
                            --color=foreground:background
                            --color=:background\t\t\t # only background
                            --color=foreground | foreground:\t # only foreground
                            --color=list\t\t\t # list all colors
                            COLOR = list[COLOR] | [0-255];[0-255];[0-255] (RGB)""",
    )
    opts, args = parser.parse_args()

    if opts.list_fonts:
        print("\n".join(sorted(FigletFont.getFonts())))
        exit(0)

    if opts.color == "list":
        print("[0-255];[0-255];[0-255] # RGB\n" + "\n".join(sorted(COLOR_CODES.keys())))
        exit(0)

    if opts.info_font:
        print(FigletFont.infoFont(opts.font))
        exit(0)

    if opts.load:
        FigletFont.installFonts(opts.load)
        exit(0)

    if len(args) == 0:
        parser.print_help()
        return 1

    if sys.version_info < (3,):
        args = [arg.decode("UTF-8") for arg in args]

    text = " ".join(args)

    try:
        f = Figlet(
            font=opts.font,
            direction=opts.direction,
            justify=opts.justify,
            width=opts.width,
        )
    except FontNotFound:
        print(f"pyfiglet error: requested font {opts.font!r} not found.")
        return 1

    r = f.renderText(text)
    if opts.reverse:
        r = r.reverse()
    if opts.flip:
        r = r.flip()
    if opts.strip_surrounding_newlines:
        r = r.strip_surrounding_newlines()
    elif opts.normalize_surrounding_newlines:
        r = r.normalize_surrounding_newlines()

    if sys.version_info > (3,):
        # Set stdout to binary mode
        sys.stdout = sys.stdout.detach()

    ansiColors = parse_color(opts.color)
    if ansiColors:
        sys.stdout.write(ansiColors.encode("UTF-8"))

    sys.stdout.write(r.encode("UTF-8"))
    sys.stdout.write(b"\n")

    if ansiColors:
        sys.stdout.write(RESET_COLORS)

    return 0


if __name__ == "__main__":
    sys.exit(main())
