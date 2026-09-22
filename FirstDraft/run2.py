import ftd2xx
import time
import threading


# =========================================================
# TETRA
# =========================================================

class Tetra:

    def __init__(self, address=1):
        self.address = address
        self.channels = [0] * 11

    def set_channel(self, channel, value):
        self.channels[channel - 1] = max(0, min(255, int(value)))

    def blackout(self):
        self.channels = [0] * 11

    def water(self, value=128):
        self.set_channel(1, value)

    def white(self, value=255):
        self.set_channel(2, value)

    def fireball(self, colour):
        values = {
            "off": 0,
            "red": 25,
            "green": 60,
            "blue": 95,
            "redgreen": 130,
            "greenblue": 165,
            "redblue": 200,
            "all": 235
        }

        self.set_channel(3, values[colour])

    def laser(self, colour):
        values = {
            "off": 0,
            "red": 50,
            "green": 150,
            "redgreen": 225
        }

        self.set_channel(4, values[colour])

    def uv(self, value=255):
        self.set_channel(5, value)

    def effects(self, value=0):
        self.set_channel(6, value)

    def strobe(self, value=0):
        self.set_channel(7, value)

    def water_speed(self, value=0):
        self.set_channel(8, value)

    def fireball_speed(self, value=0):
        self.set_channel(9, value)

    def laser_rotation(self, value=0):
        self.set_channel(10, value)

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


# =========================================================
# ENTTEC OPEN DMX
# =========================================================

class OpenDMX:

    def __init__(self):

        devices = ftd2xx.listDevices()

        if not devices:
            raise RuntimeError("No FTDI device found")

        print("FTDI devices:")

        for device in devices:
            print(" ", device)

        self.device = ftd2xx.open(0)

        self.device.setBaudRate(250000)
        self.device.setDataCharacteristics(8, 2, 0)

        self.device.purge(3)

        # DMX universe
        # byte 0 = start code
        # bytes 1-512 = channels

        self.universe = bytearray(513)

    def set_channel(self, channel, value):

        self.universe[channel] = max(
            0,
            min(255, int(value))
        )

    def send(self):

        # DMX BREAK
        self.device.setBreakOn()
        time.sleep(0.0001)

        # MARK AFTER BREAK
        self.device.setBreakOff()
        time.sleep(0.000012)

        # Send complete DMX universe
        self.device.write(bytes(self.universe))

    def close(self):
        self.device.close()


# =========================================================
# DMX OUTPUT THREAD
# =========================================================

class LightController:

    def __init__(self, tetra):

        self.tetra = tetra
        self.dmx = OpenDMX()

        self.running = True

        self.thread = threading.Thread(
            target=self._output_loop,
            daemon=True
        )

        self.thread.start()

    def _output_loop(self):

        while self.running:

            # Copy Tetra channels into DMX universe

            for i, value in enumerate(self.tetra.channels):

                self.dmx.set_channel(
                    self.tetra.address + i,
                    value
                )

            self.dmx.send()

            # roughly 40 frames/sec
            time.sleep(0.025)

    def stop(self):

        self.running = False

        time.sleep(0.05)

        # blackout

        self.tetra.blackout()

        for i, value in enumerate(self.tetra.channels):

            self.dmx.set_channel(
                self.tetra.address + i,
                value
            )

        for _ in range(5):
            self.dmx.send()
            time.sleep(0.025)

        self.dmx.close()


# =========================================================
# COMMAND LINE
# =========================================================

def print_help():

    print("""
Commands:

  blackout

  white
  uv

  water
  water <value>

  fire red
  fire green
  fire blue
  fire redgreen
  fire greenblue
  fire redblue
  fire all

  laser red
  laser green
  laser redgreen

  strobe <0-255>

  water_speed <0-255>
  fire_speed <0-255>
  laser_rotate <0-255>

  auto1
  auto2

  sound1
  sound2

  ch <channel> <value>

  status

  help
  quit
""")


def main():

    tetra = Tetra(address=1)

    # Make sure we start in manual mode
    tetra.manual()
    tetra.blackout()

    controller = LightController(tetra)

    print()
    print("ENTTEC Open DMX connected")
    print("Tetra DMX address: 001")
    print()
    print("Type 'help' for commands.")
    print()

    try:

        while True:

            command = input("> ").strip().lower()

            if not command:
                continue

            parts = command.split()

            # -----------------------------------------
            # Quit
            # -----------------------------------------

            if parts[0] in ("quit", "exit"):

                break

            # -----------------------------------------
            # Help
            # -----------------------------------------

            elif parts[0] == "help":

                print_help()

            # -----------------------------------------
            # Blackout
            # -----------------------------------------

            elif parts[0] == "blackout":

                tetra.blackout()
                tetra.manual()

                print("Blackout")

            # -----------------------------------------
            # White
            # -----------------------------------------

            elif parts[0] == "white":

                tetra.manual()
                tetra.white()

                print("White LED ON")

            # -----------------------------------------
            # UV
            # -----------------------------------------

            elif parts[0] == "uv":

                tetra.manual()
                tetra.uv()

                print("UV ON")

            # -----------------------------------------
            # Water
            # -----------------------------------------

            elif parts[0] == "water":

                tetra.manual()

                value = int(parts[1]) if len(parts) > 1 else 128

                tetra.water(value)

                print(f"Water wave: {value}")

            # -----------------------------------------
            # Fireball
            # -----------------------------------------

            elif parts[0] == "fire":

                tetra.manual()
                tetra.fireball(parts[1])

                print("Fireball:", parts[1])

            # -----------------------------------------
            # Laser
            # -----------------------------------------

            elif parts[0] == "laser":

                tetra.manual()
                tetra.laser(parts[1])

                print("Laser:", parts[1])

            # -----------------------------------------
            # Strobe
            # -----------------------------------------

            elif parts[0] == "strobe":

                tetra.manual()

                value = int(parts[1])

                tetra.strobe(value)

                print("Strobe:", value)

            # -----------------------------------------
            # Speeds
            # -----------------------------------------

            elif parts[0] == "water_speed":

                tetra.manual()
                tetra.water_speed(int(parts[1]))

            elif parts[0] == "fire_speed":

                tetra.manual()
                tetra.fireball_speed(int(parts[1]))

            elif parts[0] == "laser_rotate":

                tetra.manual()
                tetra.laser_rotation(int(parts[1]))

            # -----------------------------------------
            # Programs
            # -----------------------------------------

            elif parts[0] == "auto1":

                tetra.auto1()
                print("Auto program 1")

            elif parts[0] == "auto2":

                tetra.auto2()
                print("Auto program 2")

            elif parts[0] == "sound1":

                tetra.sound1()
                print("Sound program 1")

            elif parts[0] == "sound2":

                tetra.sound2()
                print("Sound program 2")

            # -----------------------------------------
            # Direct DMX channel
            # -----------------------------------------

            elif parts[0] == "ch":

                channel = int(parts[1])
                value = int(parts[2])

                tetra.set_channel(channel, value)

                print(
                    f"Tetra CH{channel} = {value}"
                )

            # -----------------------------------------
            # Status
            # -----------------------------------------

            elif parts[0] == "status":

                for i, value in enumerate(
                    tetra.channels,
                    start=1
                ):

                    print(
                        f"CH {i:2}: {value:3}"
                    )

            else:

                print("Unknown command. Type 'help'.")

    except KeyboardInterrupt:

        print()

    finally:

        print("Stopping...")

        controller.stop()

        print("Blackout sent.")


if __name__ == "__main__":
    main()