# =========================================================
# ENGINE - state manager
# =========================================================

from bizz.fixture_manager import FixtureManager


class Engine:

    def __init__(self):
        manager = FixtureManager("lights/config/fixtures.yaml")

        #controller = LightController(tetra)

        par = manager.get("par_left")

        par.set_color("red")
        par.set_brightness(100)

   



