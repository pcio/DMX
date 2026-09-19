import ftd2xx
import time
import threading

from ai.ask_ai import ask_ai
from bizz.engine import Engine
    
def main():
    engined = Engine()  # Assuming you have a function to initialize the engine

    print("* * * Lighting system initialized * * *")

    while True:
        text = input("AI> ")

        if text.lower() in ("quit", "exit"):
            break

        if text.__len__() < 2:
            continue

        command = ask_ai(text)

        print("AI:", command)

        #engine.execute_command(engine, command)





if __name__ == "__main__":
    main()


