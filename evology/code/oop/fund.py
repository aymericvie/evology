from types import FunctionType


class Fund:
    def __init__(self, cash, asset):
        self.cash = cash
        self.asset = asset
        self.loan = 0.
        self.margin = 0.
        self.wealth = 0
        self.trading_signal = 0.
        self.type = str
        self.excess_demand = FunctionType
        self.leverage = 1.
        self.signal_scale = 1.
        self.demand = 0.

    def count_wealth(self, price):
        self.wealth = self.cash + self.asset * price - self.loan + self.margin
        if self.wealth < 0:
            raise RuntimeError('Insolvent agent', self.type, self.wealth, self.cash, self.asset, self.loan, self.margin, self.wealth + self.margin)
        return self.wealth
    
    def compute_demand(self, price):
        self.demand = self.excess_demand(price)
        # print([self.type, self.trading_signal, self.demand])

    def execute_demand(self, price):
        # TODO: possible issue if we have some mismatch?
        self.asset += self.demand
        self.cash -= self.demand * price 

    def clear_debt(self):
        if self.loan > 0 and self.cash > 0:
            self.cash -= self.loan 
            self.loan = 0
        if self.loan < 0:
            self.cash += self.loan
            self.loan = 0

    def earnings(self, dividend, interest_rate_daily):
        self.cash += interest_rate_daily * self.cash 
        self.cash += dividend * self.asset

    def update_margin(self, price):
        self.cash += self.margin 
        self.margin = 0.
        if self.asset < 0:
            self.margin = abs(self.asset) * price
            self.cash -= abs(self.asset) * price
        if self.margin < 0:
            raise RuntimeError('Negative margin', self.type, self.margin)


    def liquidate_insolvent(self):
        if self.wealth < 0:
            raise RuntimeError('Insolvent agent', self.wealth, self.type, self.asset, self.cash, self.margin)
    def get_assets(self):
        return self.asset
