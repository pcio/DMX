from .base import Fixture


class TMH13(Fixture):
    """11-channel moving head.

    The channel mapping is deliberately isolated here. Extend this class as
    the exact fixture manual/channel map is added.
    """

    def __init__(self, address=1, mode=11):
        super().__init__(address, mode)

    def set_color(self, color: str, brightness: int = 255):
        colors = {
            "red": 0,
            "green": 85,
            "blue": 170,
            "white": 255,
            "off": 0,
        }
        if color.lower() not in colors:
            raise ValueError(f"Unsupported TMH13 colour: {color}")
        self.set_channel(1, colors[color.lower()])
        self.set_channel(2, brightness)

    def pan(self, value: int):
        self.set_channel(3, value)

    def tilt(self, value: int):
        self.set_channel(4, value)

    def sweep(self, speed=128):
        self.set_channel(5, speed)
