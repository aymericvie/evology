from math import log2, tanh
from fund import Fund

class TrendFollower(Fund):
    def __init__(self, cash, asset, time_horizon):
        super().__init__(cash, asset)
        self.time_horizon = time_horizon
        self.type = "TF"
        
    def get_price_ema(self, price, price_ema):
        self.trading_signal = log2(price / price_ema)

    def get_excess_demand_function(self):
        def func(price):
            value = (self.wealth * self.leverage / price) * tanh(self.signal_scale * self.trading_signal + 0.0) - self.asset
            return max(value, - self.leverage * self.max_short_size - self.asset)
        self.excess_demand = func
