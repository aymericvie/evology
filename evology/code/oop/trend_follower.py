from ast import FunctionDef


from fund import Fund

class TrendFollower(Fund):
    def __init__(self, cash, asset, loan, margin, time_horizon):
        super().__init__(cash, asset, loan, margin)
        self.time_horizon = time_horizon
        self.type = "TF"