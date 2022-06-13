class Fund:
    def __init__(self, cash, asset, loan, margin):
        self.cash = cash
        self.asset = asset
        self.loan = loan
        self.margin = margin
        self.wealth = 0

    def count_wealth(self, price):
        self.wealth = self.cash + self.asset * price - self.loan
        return self.wealth