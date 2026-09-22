from ai.ask_ai import ask_ai
from bizz.engine import Engine



def main():
    engine = Engine()
    

    print("* * * Lighting system initialized * * *")
    print("Type 'quit' to exit.")

    while True:
        text = input("AI> ").strip()
        if text.lower() in ("quit", "exit"):
            break
        if len(text) < 2:
            continue

        command = ask_ai(text)
        print("AI:", command)

        try:
            engine.execute_command(engine, command)
        except (KeyError, ValueError) as exc:
            print("Command error:", exc)


if __name__ == "__main__":
    main()
