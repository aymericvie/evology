from fund import Fund
from math import tanh, log2

class ValueInvestor(Fund):
    def __init__(self, cash, asset, loan, margin, req_rate_return, interest_rate, dividend_growth_rate):
        super().__init__(cash, asset, loan, margin)
        self.req_rate_return = req_rate_return
        self.type = "VI"
        self.valuation = None
        self.discount_rate = (1.0 + (interest_rate + self.req_rate_return) - dividend_growth_rate) ** (1.0 / 252.0) - 1.0

    def update_valuation(self, dividend, interest_rate_daily):
        self.valuation = dividend * (1. + interest_rate_daily) / self.discount_rate

    def get_excess_demand_function(self):
        def func(price):
            return (self.wealth * self.leverage / price) * tanh(self.signal_scale * log2(self.valuation / price)) - self.asset
        self.excess_demand = func
