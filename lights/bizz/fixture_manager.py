import yaml
import os

from fixtures.par100 import PAR100
from fixtures.tmh13 import TMH13
from fixtures.tetra import Tetra

# =========================================================
# Fixture Manager 
# =========================================================


class FixtureManager:

    FIXTURE_TYPES = {
        "par100": PAR100,
        "tmh13": TMH13,
        "tetra": Tetra,
    }

    def __init__(self, filename):
        self.fixtures = {}

        self.load(filename)

    def load(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        for definition in config.get("fixtures", []):
            fixture_id = definition["id"]
            fixture_type = definition["type"]

            fixture_class = self.FIXTURE_TYPES.get(fixture_type)

            if fixture_class is None:
                raise ValueError(
                    f"Unknown fixture type: {fixture_type}"
                )

            fixture = fixture_class(
                address=definition["address"],
                mode=int(definition["mode"])
            )

            self.fixtures[fixture_id] = fixture

    def get(self, fixture_id):
        return self.fixtures[fixture_id]

    def all(self):
        return self.fixtures.values()