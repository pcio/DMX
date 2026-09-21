class DMXLayer:
    """Build a 512-channel DMX universe.

    Hardware output is intentionally separated from state generation. For now
    `send()` stores the latest universe, making the project testable without
    DMX hardware. A hardware backend can later consume `universe`.
    """

    UNIVERSE_SIZE = 512

    def __init__(self):
        self.universe = [0] * self.UNIVERSE_SIZE

    def build_universe(self, fixtures):
        universe = [0] * self.UNIVERSE_SIZE
        for fixture in fixtures:
            start = fixture.address - 1
            end = start + fixture.mode
            if end > self.UNIVERSE_SIZE:
                raise ValueError(f"Fixture at address {fixture.address} exceeds DMX universe")
            universe[start:end] = fixture.get_channels()
        return universe

    def send(self, fixtures):
        self.universe = self.build_universe(fixtures)
        return self.universe.copy()
