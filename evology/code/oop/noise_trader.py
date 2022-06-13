from fund import Fund

class NoiseTrader(Fund):
    def __init__(self, cash, asset, loan, margin):
        super().__init__(cash, asset, loan, margin)
        self.type = "NT"
    