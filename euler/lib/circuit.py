class Circuit:
    """I could maintain a list that keeps track of the order
    in which other capacitors were added to the circuit.
    The circuit must be constructed with an initial
    capacitor."""
    def __init__(self, cap=1):
        self.cap = cap

    def get_cap(self):
        return self.cap

    def add_parallel(self, cap=1):
        self.cap += cap
        return self

    def add_series(self, cap=1):
        self.cap = 1 / (1/self.cap + 1/cap)
        return self

    def copy(self):
        return Circuit(self.get_cap())

