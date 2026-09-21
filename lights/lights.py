from ai.ask_ai import ask_ai
from bizz.engine import Engine
from bizz.scene_engine import SceneEngine
from scenes.rock import scene_rock


def main():
    engine = Engine()
    scenes = SceneEngine(engine)
    scenes.register("rock", scene_rock)

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
            execute_command(engine, command)
        except (KeyError, ValueError) as exc:
            print("Command error:", exc)


def execute_command(engine, command):
    intent = command.get("intent")

    if intent == "unknown":
        print("I don't know how to express that as a lighting command.")
    elif intent == "blackout":
        engine.blackout()
    elif intent == "scene":
        engine.run_scene(command["name"])
    elif intent == "color":
        engine.set_color(
            command["target"],
            command["color"],
            command.get("brightness", 255),
        )
    elif intent == "effect":
        fixture = engine.fixture(command["target"])
        effect = command["effect"]
        if effect == "strobe" and hasattr(fixture, "strobe"):
            fixture.strobe(command.get("value", 100))
        elif effect == "none":
            fixture.blackout()
        else:
            raise ValueError(f"Unsupported effect '{effect}' for {command['target']}")
        engine.update()
    elif intent == "movement":
        fixture = engine.fixture(command["target"])
        movement = command["movement"]
        value = command.get("value", 128)
        if movement == "pan":
            fixture.pan(value)
        elif movement == "tilt":
            fixture.tilt(value)
        else:
            raise ValueError(f"Unsupported movement '{movement}'")
        engine.update()
    else:
        raise ValueError(f"Unknown command intent: {intent}")


if __name__ == "__main__":
    main()
