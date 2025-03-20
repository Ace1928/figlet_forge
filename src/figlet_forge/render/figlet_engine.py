class FigletRenderingEngine:
    """
    This class handles the rendering of a FigletFont,
    including smushing/kerning/justification/direction
    """

    def __init__(self, base=None):
        self.base = base

    def render(self, text):
        """
        Render an ASCII text string in figlet
        """
        builder = FigletBuilder(
            text,
            self.base.Font,
            self.base.direction,
            self.base.width,
            self.base.justify,
        )

        while builder.isNotFinished():
            builder.addCharToProduct()
            builder.goToNextChar()

        return builder.returnProduct()
