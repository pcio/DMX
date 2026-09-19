# =========================================================
# DMX_LAYER
# =========================================================

from fixtures.tetra import Tetra


class DMXLayer:

    def __init__(self):
        self.tetra = Tetra(address=1)
      
        # Make sure we start in manual mode
        self.tetra.manual()
        self.tetra.blackout()
