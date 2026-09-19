# =========================================================
# TMH13
# =========================================================

class TMH13:

    def __init__(self, address=1, mode=11):
        self.address = address
        self.mode = mode
        self.channels = [0] * 11
