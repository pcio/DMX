# =========================================================
# PAR100
# =========================================================

class PAR100:

    def __init__(self, address=1, mode=11):
        self.address = address
        self.mode = mode
        self.channels = [0] * 11
    