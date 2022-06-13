class Fund:
    def __init__(self, cash, asset, loan, margin):
        self.cash = cash
        self.asset = asset
        self.loan = loan
        self.margin = margin
        self.wealth = 0
        self.trading_signal = None
        self.type = None
        self.excess_demand = None
        self.leverage = 1.
        self.signal_scale = 1.

    def count_wealth(self, price):
        self.wealth = self.cash + self.asset * price - self.loan
        return self.wealth