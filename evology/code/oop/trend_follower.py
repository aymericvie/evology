from math import log2, tanh
from fund import Fund

class TrendFollower(Fund):
    def __init__(self, cash, asset, time_horizon):
        super().__init__(cash, asset)
        self.time_horizon = time_horizon
        self.type = "TF"
        
    def get_price_ema(self, price, price_ema):
        self.trading_signal = log2(price / price_ema)
        #print("-----")
        #print(price, price_ema)
        #print('TF trading signal ', self.trading_signal)

    def get_excess_demand_function(self):
        def func(price):
            value = (self.wealth * self.leverage / price) * tanh(self.signal_scale * self.trading_signal + 0.0) - self.asset
            return max(value, - self.leverage * self.max_short_size - self.asset)
        self.excess_demand = func

    def get_pod_demand(self):
        def func(price):
            mt = (self.trading_signal + 0.5)
            if mt <= Fund.momentum_short:
                return (1 - self.leverage) * self.wealth / price
            elif mt > Fund.momentum_long:
                return self.leverage * self.wealth / price
            else:
                return self.signal_scale * mt * self.wealth / price
        self.pod_demand = func