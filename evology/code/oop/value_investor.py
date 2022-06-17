from fund import Fund
from math import tanh, log2

class ValueInvestor(Fund):
    def __init__(self, cash, asset, req_rate_return, interest_rate, dividend_growth_rate):
        super().__init__(cash, asset)
        self.req_rate_return = req_rate_return
        self.type = "VI"
        self.valuation = None
        self.discount_rate = (1.0 + (interest_rate + self.req_rate_return) - dividend_growth_rate) ** (1.0 / 252.0) - 1.0

    def update_valuation(self, dividend, interest_rate_daily):
        self.valuation = dividend * (1. + interest_rate_daily) / self.discount_rate
        if self.valuation < 0:
            raise RuntimeError('Negative VI valuation', self.valuation)

    def get_excess_demand_function(self):
        def func(price):
            value = (self.wealth * self.leverage / price) * tanh((self.signal_scale * log2(self.valuation / max(price,0.0001))) + 0.0 ) - self.asset
            return max(value, - self.leverage * self.max_short_size - self.asset)
        self.excess_demand = func

    def compute_trading_signal(self, price):
        self.trading_signal = log2(self.valuation / price)

