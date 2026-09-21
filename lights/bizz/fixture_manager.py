from __future__ import annotations

from pathlib import Path
import yaml

from fixtures import PAR100, TMH13, Tetra


class FixtureManager:
    FIXTURE_TYPES = {"par100": PAR100, "tmh13": TMH13, "tetra": Tetra}

    def __init__(self, filename: str | Path):
        self.fixtures = {}
        self.load(filename)

    def load(self, filename: str | Path) -> None:
        with open(filename, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

        for definition in config.get("fixtures", []):
            fixture_id = definition["id"]
            fixture_type = definition["type"].lower()
            fixture_class = self.FIXTURE_TYPES.get(fixture_type)
            if fixture_class is None:
                raise ValueError(f"Unknown fixture type: {fixture_type}")
            if fixture_id in self.fixtures:
                raise ValueError(f"Duplicate fixture id: {fixture_id}")

            self.fixtures[fixture_id] = fixture_class(
                address=int(definition["address"]),
                mode=int(definition.get("mode", 1)),
            )

    def get(self, fixture_id: str):
        try:
            return self.fixtures[fixture_id]
        except KeyError as exc:
            raise KeyError(f"Unknown fixture: {fixture_id}") from exc

    def all(self):
        return self.fixtures.values()

    def ids(self):
        return self.fixtures.keys()
