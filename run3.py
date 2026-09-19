import ftd2xx
import time
import threading

from light_ai import ask_ai

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

def execute_command(tetra, command):

    action = command.get("action")

    if action == "blackout":
        tetra.blackout()
        tetra.manual()

    elif action == "white":
        tetra.manual()
        tetra.white(command["value"])

    elif action == "uv":
        tetra.manual()
        tetra.uv()

    elif action == "water":
        tetra.manual()
        tetra.water(command["value"])

    elif action == "fireball":
        tetra.manual()
        tetra.fireball(command["colour"])

    elif action == "laser":
        tetra.manual()
        tetra.laser(command["colour"])

    elif action == "strobe":
        tetra.manual()
        tetra.strobe(command["value"])

    elif action == "water_speed":
        tetra.manual()
        tetra.water_speed(command["value"])

    elif action == "fire_speed":
        tetra.manual()
        tetra.fireball_speed(command["value"])

    elif action == "laser_rotate":
        tetra.manual()
        tetra.laser_rotation(command["value"])

    elif action == "auto1":
        tetra.auto1()

    elif action == "auto2":
        tetra.auto2()

    elif action == "sound1":
        tetra.sound1()

    elif action == "sound2":
        tetra.sound2()

    else:
        print("AI did not understand the command.")



def main():

    tetra = Tetra(address=1)

    # Make sure we start in manual mode
    tetra.manual()
    tetra.blackout()

    controller = LightController(tetra)

    value = 0
    while True:
        #command = {"action": "water", "value": value}
        #execute_command(tetra, command)
        #text = input("water value " + str(value) + "> ")
        #value += 1
        #continue
                

        text = input("AI> ")

        if text.lower() in ("quit", "exit"):
            break

        if text.__len__() < 2:
            continue

        if text[0] == ".":
            arr = text[1:].split(" ")
            command = {"action": arr[0], "value": int(arr[1])}
            execute_command(tetra, command)
            continue

        command = ask_ai(text)

        print("AI:", command)

        execute_command(tetra, command)



    
if __name__ == "__main__":
    main()