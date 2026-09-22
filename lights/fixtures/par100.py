from .base import Fixture


class PAR100(Fixture):
    """
    AVSL PAR-100.
    """

    def __init__(self, address=1, mode=7):
        super().__init__(address, mode)

    def set_brightness(self, value=255):
        self.set_channel(1, value)

    def set_red(self, value=255):
        self.set_channel(2, value)

    def set_green(self, value=255):
        self.set_channel(3, value)

    def set_blue(self, value=255):
        self.set_channel(4, value)


    def set_rgb(self, red: int, green: int, blue: int) -> None:
        for channel, value in ((2, red), (3, green), (4, blue)):
            self.set_channel(channel, value)
   
    def set_color(self, color: str, brightness: int = 255):
        colors = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "white": (255, 255, 255),
            "yellow": (255, 255, 0),
            "cyan": (0, 255, 255),
            "magenta": (255, 0, 255),
            "off": (0, 0, 0),
        }
        try:
            r, g, b = colors[color.lower()]
        except KeyError as exc:
            raise ValueError(f"Unsupported PAR100 colour: {color}") from exc

        self.set_red(r)
        self.set_green(g)
        self.set_blue(b)
        self.set_brightness(brightness)

