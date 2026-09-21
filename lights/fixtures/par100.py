from .base import Fixture


class PAR100(Fixture):
    """7-channel PAR100.

    Channel layout is kept here so the rest of the application does not need
    to know about DMX channel numbers.
    """

    def __init__(self, address=1, mode=7):
        super().__init__(address, mode)

    def set_red(self, value=255):
        self.set_channel(1, value)

    def set_green(self, value=255):
        self.set_channel(2, value)

    def set_blue(self, value=255):
        self.set_channel(3, value)

    def set_white(self, value=255):
        self.set_channel(4, value)

    def set_color(self, color: str, brightness: int = 255):
        colors = {
            "red": (255, 0, 0, 0),
            "green": (0, 255, 0, 0),
            "blue": (0, 0, 255, 0),
            "white": (0, 0, 0, 255),
            "yellow": (255, 255, 0, 0),
            "cyan": (0, 255, 255, 0),
            "magenta": (255, 0, 255, 0),
            "off": (0, 0, 0, 0),
        }
        try:
            r, g, b, w = colors[color.lower()]
        except KeyError as exc:
            raise ValueError(f"Unsupported PAR100 colour: {color}") from exc

        scale = max(0, min(255, int(brightness))) / 255
        self.set_red(round(r * scale))
        self.set_green(round(g * scale))
        self.set_blue(round(b * scale))
        self.set_white(round(w * scale))

    def set_brightness(self, value=255):
        # Channel 5 is assumed to be dimmer/master on this fixture.
        self.set_channel(5, value)
