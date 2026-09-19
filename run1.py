import ftd2xx
import time
import sys


# ---------------------------------------------------------
# QTX TETRA 4-in-1
#
# DMX channels:
#
# 1  Water wave colour
# 2  White
# 3  Fireball colour
# 4  Laser colour
# 5  UV
# 6  Effect combination
# 7  Strobe
# 8  Water wave speed
# 9  Fireball speed
# 10 Laser rotation
# 11 Program
#
# Tetra must be set to DMX address 001
# ---------------------------------------------------------


class Tetra:
    def __init__(self, address=1):
        self.address = address
        self.channels = [0] * 11

    # -----------------------------------------------------
    # Basic DMX channel handling
    # -----------------------------------------------------

    def set_channel(self, channel, value):
        if not 1 <= channel <= 11:
            raise ValueError("Tetra channel must be 1..11")

        value = max(0, min(255, int(value)))
        self.channels[channel - 1] = value

    def blackout(self):
        self.channels = [0] * 11

    # -----------------------------------------------------
    # Effects
    # -----------------------------------------------------

    def water(self, value=128):
        # 0-24 = off
        # 25-255 = colour sequence
        self.set_channel(1, value)

    def white(self, on=True):
        self.set_channel(2, 255 if on else 0)

    def fireball(self, colour):
        values = {
            "off": 0,
            "red": 25,
            "green": 60,
            "blue": 95,
            "yellow": 130,
            "cyan": 165,
            "magenta": 200,
            "white": 235
        }

        if colour not in values:
            raise ValueError(
                "fireball colour: "
                + ", ".join(values.keys())
            )

        self.set_channel(3, values[colour])

    def laser(self, colour):
        values = {
            "off": 0,
            "red": 50,
            "green": 150,
            "red_green": 225
        }

        if colour not in values:
            raise ValueError(
                "laser colour: "
                + ", ".join(values.keys())
            )

        self.set_channel(4, values[colour])

    def uv(self, on=True):
        self.set_channel(5, 255 if on else 0)

    def effects(self, value=0):
        # 0-7 = all effects
        # 8-255 = combinations
        self.set_channel(6, value)

    def strobe(self, value=0):
        # 0-9 off
        # 10-255 slow -> fast
        self.set_channel(7, value)

    def water_speed(self, value=0):
        # 0-9 off
        # 10-255 fast -> slow
        self.set_channel(8, value)

    def fireball_speed(self, value=0):
        self.set_channel(9, value)

    def laser_rotation(self, value=0):
        # 0-9 off
        # 10-127 clockwise
        # 128-255 anticlockwise
        self.set_channel(10, value)

    # -----------------------------------------------------
    # Programs
    # -----------------------------------------------------

    def manual(self):
        self.set_channel(11, 0)

    def auto1(self):
        self.set_channel(11, 100)

    def auto2(self):
        self.set_channel(11, 175)

    def sound1(self):
        self.set_channel(11, 225)

    def sound2(self):
        self.set_channel(11, 255)

    # -----------------------------------------------------
    # Debug
    # -----------------------------------------------------

    def show(self):
        print()
        print("TETRA DMX")
        print("-" * 35)

        for i, value in enumerate(self.channels, start=1):
            print(f"CH {i:2}: {value:3}")

        print("-" * 35)


# =========================================================
# ENTTEC OPEN DMX USB
# =========================================================

class OpenDMX:
    def __init__(self):

        devices = ftd2xx.listDevices()

        if not devices:
            raise RuntimeError(
                "No FTDI / ENTTEC Open DMX device found."
            )

        print("FTDI devices:")
        for device in devices:
            print(" ", device)

        self.device = ftd2xx.open(0)

        # DMX512:
        # 250000 baud
        # 8 data bits
        # 2 stop bits
        # no parity

        self.device.setBaudRate(250000)
        self.device.setDataCharacteristics(8, 2, 0)

        self.device.purge(3)

        self.universe = bytearray(513)

        # DMX start code
        self.universe[0] = 0

    def set_channel(self, channel, value):

        if not 1 <= channel <= 512:
            raise ValueError("DMX channel must be 1..512")

        self.universe[channel] = max(
            0,
            min(255, int(value))
        )

    def send(self):

        # DMX BREAK
        self.device.setBreakOn()
        time.sleep(0.0001)       # ~100 us

        # MARK AFTER BREAK
        self.device.setBreakOff()
        time.sleep(0.000012)     # ~12 us

        # Send start code + 512 channels
        self.device.write(bytes(self.universe))

    def close(self):
        self.device.close()


# =========================================================
# TEST
# =========================================================

def main():

    tetra = Tetra()

    # -----------------------------------------------------
    # Create OpenDMX connection
    # -----------------------------------------------------

    try:
        dmx = OpenDMX()
    except Exception as e:
        print()
        print("ERROR:")
        print(e)
        print()
        sys.exit(1)

    # -----------------------------------------------------
    # Tetra starts at DMX address 1
    # -----------------------------------------------------

    print()
    print("Connected to ENTTEC Open DMX USB")
    print("Tetra address = 001")
    print()
    print("Press Ctrl+C to stop.")
    print()

    try:

        # ---------------------------------------------
        # Start with everything OFF
        # ---------------------------------------------

        tetra.blackout()

        # Send initial state
        while True:

            # Copy Tetra channels into DMX universe
            for i, value in enumerate(tetra.channels):
                dmx.set_channel(
                    tetra.address + i,
                    value
                )

            dmx.send()

            # ~40 FPS
            time.sleep(0.025)

    except KeyboardInterrupt:

        print()
        print("Stopping...")

        # ---------------------------------------------
        # BLACKOUT
        # ---------------------------------------------

        tetra.blackout()

        for i, value in enumerate(tetra.channels):
            dmx.set_channel(
                tetra.address + i,
                value
            )

        # Send blackout a few times
        for _ in range(5):
            dmx.send()
            time.sleep(0.025)

    finally:
        dmx.close()


if __name__ == "__main__":
    main()