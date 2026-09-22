"""Interactive diagnostic console for every layer below the AI.

Run from the project root:
    python -m lights.tools_console

The console uses the same Engine as the AI.  It therefore tests the actual
fixture, engine and DMX layers instead of having a separate test implementation.
"""

from __future__ import annotations

import shlex

from bizz.engine import Engine
from bizz.fixture_manager import FixtureManager
from ai.ask_ai import ask_ai


HELP = """
AI / ENGINE
  ai <natural language>          Send text through the AI layer and execute it
  command <json-ish>             (reserved for future explicit JSON commands)
  blackout                       Black out everything

FIXTURES
  fixtures                       List configured fixtures
  show <fixture>                 Show address, mode and all fixture channels
  set <fixture> <ch> <value>     Set one fixture channel (1-based)
  color <fixture> <color> [255]  Use fixture color helper where available
  test <fixture>                 Interactive channel test for that fixture

DIRECT DMX (bypasses fixtures/engine helpers)
  dmx show                       Show all non-zero DMX channels
  dmx get <address>              Read one DMX channel
  dmx set <address> <value>      Set one DMX channel
  dmx range <start> <end> <v>   Set an address range to one value
  dmx values <start> <end>      Show a DMX address range
  dmx blackout                   Blackout the raw DMX universe

OTHER
  sync                           Rebuild DMX from all fixture objects
  help                           Show this help
  quit / exit                    Leave console
"""


def print_fixture(engine, name):
    fixture = engine.get_fixture(name)
    print(f"{name}: {fixture.describe()}")
    print("  " + " ".join(f"{i + 1}:{v:3}" for i, v in enumerate(fixture.channels)))
    print("  DMX: " + " ".join(f"{fixture.address + i}:{v:3}" for i, v in enumerate(fixture.channels)))


def test_fixture(engine, name):
    fixture = engine.get_fixture(name)
    print(f"Testing {name}. Enter 'q' to stop. Channels: 1..{fixture.mode}")
    while True:
        raw = input(f"test:{name}> ").strip()
        if raw.lower() in ("q", "quit", "exit"):
            return
        try:
            parts = shlex.split(raw)
            if len(parts) == 2:
                channel, value = map(int, parts)
                engine.set_fixture_channel(name, channel, value)
                print_fixture(engine, name)
            else:
                print("Use: <channel> <value>")
        except Exception as exc:
            print(f"ERROR: {exc}")


def handle_dmx(engine, parts):
    if len(parts) < 2:
        print("Use: dmx show|get|set|range|values|blackout ...")
        return
    cmd = parts[1].lower()
    try:
        if cmd == "show":
            values = engine.dmx.non_zero()
            print("DMX non-zero:", " ".join(f"{a}:{v}" for a, v in values) or "(all zero)")
        elif cmd == "get":
            print(engine.dmx.get_channel(int(parts[2])))
        elif cmd == "set":
            engine.dmx.set_channel(int(parts[2]), int(parts[3]))
            engine.dmx.send()
            print(f"DMX {parts[2]}={parts[3]}")
        elif cmd == "range":
            start, end, value = map(int, parts[2:5])
            for address in range(start, end + 1):
                engine.dmx.set_channel(address, value)
            engine.dmx.send()
            print(f"DMX {start}-{end}={value}")
        elif cmd == "values":
            start, end = map(int, parts[2:4])
            print(" ".join(f"{a}:{engine.dmx.get_channel(a)}" for a in range(start, end + 1)))
        elif cmd == "blackout":
            engine.dmx.blackout()
            engine.dmx.send()
            print("Raw DMX universe blacked out (fixture objects are unchanged).")
        else:
            print("Unknown dmx command")
    except (IndexError, ValueError) as exc:
        print(f"ERROR: {exc}")


def main():
    engine = Engine()
    print("* * * DMX diagnostic console * * *")
    print("Virtual DMX driver active. Type 'help' for commands.")

    while True:
        try:
            raw = input("DMX> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not raw:
            continue
        try:
            parts = shlex.split(raw)
            command = parts[0].lower()
            if command in ("quit", "exit"):
                break
            if command == "help":
                print(HELP)
            elif command == "fixtures":
                for name, fixture in engine.fixtures.all():
                    print(f"{name:15} {fixture.describe()}")
            elif command == "show":
                print_fixture(engine, parts[1])
            elif command == "set":
                engine.set_fixture_channel(parts[1], int(parts[2]), int(parts[3]))
                print_fixture(engine, parts[1])
            elif command == "color":
                fixture = engine.fixture(parts[1])
                color = parts[2]
                brightness = int(parts[3]) if len(parts) > 3 else 255
                if hasattr(fixture, "set_color"):
                    fixture.set_color(color, brightness)
                elif hasattr(fixture, "color"):
                    fixture.color(color, brightness)
                else:
                    raise ValueError(f"{parts[1]} has no color helper")
                fixture.apply_to(engine.dmx)
                engine.dmx.send()
                print_fixture(engine, parts[1])
            elif command == "test":
                test_fixture(engine, parts[1])
            elif command == "dmx":
                handle_dmx(engine, parts)
            elif command == "sync":
                engine.sync_fixtures()
                print("DMX rebuilt from fixture state.")
            elif command == "blackout":
                engine.blackout()
                print("Blackout")
            elif command == "ai":
                text = raw[len(parts[0]):].strip()
                if not text:
                    print("Use: ai <natural language>")
                    continue
                command_json = ask_ai(text)
                print("AI ->", command_json)
                print("ENGINE ->", engine.execute_command(command_json))
            else:
                print("Unknown command. Type 'help'.")
        except Exception as exc:
            print(f"ERROR: {exc}")


if __name__ == "__main__":
    main()
