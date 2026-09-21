class SceneEngine:
    def __init__(self, engine):
        self.engine = engine

    def register(self, name, scene):
        self.engine.register_scene(name, scene)

    def run(self, name):
        return self.engine.run_scene(name)
