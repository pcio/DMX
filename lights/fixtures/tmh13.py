from .base import Fixture


class TMH13(Fixture):
    """11-channel moving head.

    The channel mapping is deliberately isolated here. Extend this class as
    the exact fixture manual/channel map is added.
    """

    def __init__(self, address=1, mode=11):
        super().__init__(address, mode)

    def set_channel(self, channel: int, value: int) -> None:
        super().set_channel(channel, value)
        
    def set_color(self, color: str, brightness: int = 255):
        colors = {
            "white": 0,
            "red": 10,
            "green": 20,
            "blue": 30,
            "yellow": 40,
            "cyan": 50,
            "orange": 60,
            "magenta": 70,
            "magentaorange": 80,
            "orangemagenta": 80,
            "orangecyan": 90,
            "cyanorange": 90,
            "cyanyellow": 100,
            "yellowcyan": 100,
            "yellowblue": 110,		
			"blueyellow": 110,
            "greenblue": 120,
            "bluegreen": 120,
            "greenred": 130,
			"redgreen": 130,
        }
        if color.lower() not in colors:
            raise ValueError(f"Unsupported TMH13 colour: {color}")
        self.set_channel(1, colors[color.lower()])
        self.set_brightness(brightness)
		
    def set_rainbow(self, speed: int = 0, brightness: int = 255):
        value = 140 + int(speed)
        if value > 255:
            raise ValueError(f"Speed must be less than 116: {speed}")
        self.set_channel(5, value)
        self.set_brightness(brightness)
	
    def pan(self, value: int):
        self.set_channel(1, value)

    def tilt(self, value: int):
        self.set_channel(3, value)

    def sweep(self, speed: int | str = 128) -> None:
        speeds = {"slow": 40, "medium": 128, "fast": 220}
        value = speeds.get(str(speed).lower(), speed)
        self.set_channel(5, int(value))

    def set_brightness(self, brightness: int = 255):
        self.set_channel(8, brightness)
