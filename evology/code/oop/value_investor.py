from fund import Fund

class ValueInvestor(Fund):
    def __init__(self, cash, asset, loan, margin, req_rate_return):
        super().__init__(cash, asset, loan, margin)
        self.req_rate_return = req_rate_return
        self.type = "VI"
