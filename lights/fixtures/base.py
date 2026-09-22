from __future__ import annotations


class Fixture:
    """Base class for a DMX fixture.

    Fixture classes translate friendly operations (colour, pan, etc.) into
    DMX channel values. The engine never needs to know the channel layout.
    """

    def __init__(self, address: int = 1, mode: int = 1):
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

    def get_channel(self, channel: int) -> int:
        if not 1 <= channel <= self.mode:
            raise ValueError(f"Channel must be 1..{self.mode}")
        return self.channels[channel - 1]
    
    def get_channels(self) -> list[int]:
        return self.channels.copy()

    def blackout(self) -> None:
        self.channels = [0] * self.mode

    def channel_values(self) -> tuple[int, ...]:
        return tuple(self.channels)

    def apply_to(self, dmx) -> None:
        dmx.set_channels(self.address, self.channels)

    def describe(self) -> str:
        return f"{self.__class__.__name__}: address={self.address}, mode={self.mode}"
