from .base import Fixture


class Tetra(Fixture):
    def __init__(self, address=1, mode=11):
        super().__init__(address, mode)

    def set_channel(self, channel, value):
        super().set_channel(channel, value)

    def water(self, value=128): self.set_channel(1, value)
    def white(self, value=255): self.set_channel(2, value)

    def fireball(self, colour):
        values = {"off": 0, "red": 25, "green": 60, "blue": 95,
                  "redgreen": 130, "greenblue": 165, "redblue": 200, "all": 235}
        try:
            self.set_channel(3, values[colour.lower()])
        except KeyError as exc:
            raise ValueError(f"Unsupported Tetra fireball colour: {colour}") from exc

    def laser(self, colour):
        values = {"off": 0, "red": 50, "green": 150, "redgreen": 225}
        try:
            self.set_channel(4, values[colour.lower()])
        except KeyError as exc:
            raise ValueError(f"Unsupported Tetra laser colour: {colour}") from exc

    def uv(self, value=255): self.set_channel(5, value)
    def effects(self, value=0): self.set_channel(6, value)
    def strobe(self, value=0): self.set_channel(7, value)
    def water_speed(self, value=0): self.set_channel(8, value)
    def fireball_speed(self, value=0): self.set_channel(9, value)
    def laser_rotation(self, value=0): self.set_channel(10, value)
    def manual(self): self.set_channel(11, 0)
    def auto1(self): self.set_channel(11, 100)
    def auto2(self): self.set_channel(11, 175)
    def sound1(self): self.set_channel(11, 225)
    def sound2(self): self.set_channel(11, 255)
