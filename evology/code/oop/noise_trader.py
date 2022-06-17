from fund import Fund
import numpy as np
from math import tanh, log2

class NoiseTrader(Fund):

    OU_mean = 1.0
    OU_rho = 0.00045832561
    OU_gamma = 0.2 * np.sqrt(1. / 252.)
    process_series = []
    noise_process = 0.

    def __init__(self, cash, asset, req_rate_return, interest_rate, dividend_growth_rate):
        super().__init__(cash, asset)
        self.type = "NT"
        ##
        self.valuation = None
        self.req_rate_return = req_rate_return
        self.discount_rate = (1.0 + (interest_rate + self.req_rate_return) - dividend_growth_rate) ** (1.0 / 252.0) - 1.0


    @classmethod
    def compute_noise_process(cls, max_generations, seed):
        rng = np.random.default_rng(seed=seed+1)
        randoms = rng.standard_normal(max_generations)
        process_series = []
        value = NoiseTrader.OU_mean
        
        for i in range(max_generations):
            value = abs(value + NoiseTrader.OU_rho * (log2(NoiseTrader.OU_mean) - log2(value)) + NoiseTrader.OU_gamma * randoms[i])
            process_series.append(value)
        return process_series

    def get_noise_process(self, generation):
        NoiseTrader.noise_process = NoiseTrader.process_series[generation]
        self.trading_signal = NoiseTrader.noise_process

    def get_excess_demand_function(self):
        # Noisy VI setup for NT to avoid unbounded orders
        def func(price):
            value = (self.wealth * self.leverage / price) * tanh(self.signal_scale * (log2((self.valuation) / max(price,0.0001))) + 0.5) - self.asset
            return max(value, - self.leverage * self.max_short_size - self.asset)
            
        self.excess_demand = func
        

    ##
    def update_valuation(self, dividend, interest_rate_daily):
        self.valuation = (dividend * (1. + interest_rate_daily) / self.discount_rate) * self.trading_signal
        if self.valuation < 0:
            raise RuntimeError('Negative NT valuation', self.valuation)

    def get_pod_demand(self):
        def func(price):
            #print(self.leverage)
            mt = tanh(log2((self.valuation * self.trading_signal) / max(price, 0.0001)))
            if mt <= Fund.mt_short:
                return (1 - self.leverage) * self.wealth / price
            elif mt > Fund.mt_long:
                return self.leverage * self.wealth / price
            else:
                return self.signal_scale * mt * self.wealth / price
        self.pod_demand = func





        

        
    