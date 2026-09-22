from __future__ import annotations

from pathlib import Path

from bizz.dmx_layer import DMXLayer
from bizz.fixture_manager import FixtureManager
from bizz.groups import GroupManager
from bizz.scene_engine import SceneEngine
from scenes.rock import scene_rock

class Engine:
    def __init__(self, config_file: str | Path | None = None):
        root = Path(__file__).resolve().parents[1]
        config_file = Path(config_file) if config_file else root / "config" / "fixtures.yaml"

        self.fixtures = FixtureManager(config_file)
        self.dmx = DMXLayer()

        config = self._load_config(config_file)
        self.groups = GroupManager(self.fixtures, config.get("groups", {}))
        self.scenes = {}

        self.scenes_engine = SceneEngine(self)
        self.scenes_engine.register("rock", scene_rock)

        self.blackout()

    @staticmethod
    def _load_config(filename):
        import yaml
        with open(filename, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def fixture(self, fixture_id):
        return self.fixtures.get(fixture_id)

    def group(self, name):
        return self.groups.get(name)

    def blackout(self):
        for fixture in self.fixtures.all():
            fixture.blackout()
        return self.update()

    def update(self):
        return self.dmx.send(self.fixtures.all())

    def set_color(self, target, color, brightness=255):
        targets = self._targets(target)
        for fixture in targets:
            if hasattr(fixture, "set_color"):
                fixture.set_color(color, brightness)
            else:
                raise ValueError(f"{fixture.__class__.__name__} has no colour operation")
        return self.update()

    def run_scene(self, name):
        try:
            scene = self.scenes[name]
        except KeyError as exc:
            raise KeyError(f"Unknown scene: {name}") from exc
        scene(self)
        return self.update()

    def register_scene(self, name, callback):
        self.scenes[name] = callback

    def _targets(self, target):
        if target in self.fixtures.fixtures:
            return [self.fixture(target)]
        return self.group(target)


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

