from __future__ import annotations


class Fixture:
    """Base class for a DMX fixture.

    Fixture classes translate friendly operations (colour, pan, etc.) into
    DMX channel values. The engine never needs to know the channel layout.
    """

    def __init__(self, address: int, mode: int):
        if address < 1 or address > 512:
            raise ValueError("DMX address must be between 1 and 512")
        if mode < 1 or address + mode - 1 > 512:
            raise ValueError(f"Invalid DMX mode/address combination: {mode}/{address}")

        self.address = int(address)
        self.mode = int(mode)
        self.channels = [0] * self.mode

    def set_channel(self, channel: int, value: int) -> None:
        if not 1 <= channel <= self.mode:
            raise ValueError(f"{self.__class__.__name__}: invalid channel {channel}")
        self.channels[channel - 1] = max(0, min(255, int(value)))

    def get_channels(self) -> list[int]:
        return self.channels.copy()

    def blackout(self) -> None:
        self.channels = [0] * self.mode

    def channel_values(self) -> tuple[int, ...]:
        return tuple(self.channels)
