from __future__ import annotations


class GroupManager:
    def __init__(self, fixtures, definitions=None):
        self.fixtures = fixtures
        self.groups = {}
        for name, fixture_ids in (definitions or {}).items():
            self.create(name, fixture_ids)

    def create(self, name: str, fixture_ids):
        self.groups[name] = [self.fixtures.get(fid) for fid in fixture_ids]

    def get(self, name: str):
        try:
            return self.groups[name]
        except KeyError as exc:
            raise KeyError(f"Unknown group: {name}") from exc

    def names(self):
        return self.groups.keys()
