from __future__ import annotations

from pathlib import Path

from bizz.dmx_layer import DMXLayer
from bizz.fixture_manager import FixtureManager
from bizz.groups import GroupManager


class Engine:
    def __init__(self, config_file: str | Path | None = None):
        root = Path(__file__).resolve().parents[1]
        config_file = Path(config_file) if config_file else root / "config" / "fixtures.yaml"

        self.fixtures = FixtureManager(config_file)
        self.dmx = DMXLayer()

        config = self._load_config(config_file)
        self.groups = GroupManager(self.fixtures, config.get("groups", {}))
        self.scenes = {}

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
