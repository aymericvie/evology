from fund import Fund
import numpy as np
from math import tanh

class NoiseTrader(Fund):

    OU_mean = 0.0
    OU_rho = 0.00045832561
    OU_gamma = 0.2 * np.sqrt(1. / 252.)
    process_series = []
    noise_process = 0.

    def __init__(self, cash, asset):
        super().__init__(cash, asset)
        self.type = "NT"

    @classmethod
    def compute_noise_process(cls, max_generations, seed):
        rng = np.random.default_rng(seed=seed+1)
        randoms = rng.standard_normal(max_generations)
        process_series = []
        value = 0.0

        for i in range(max_generations):
            value = value + NoiseTrader.OU_rho * (NoiseTrader.OU_mean - value) + NoiseTrader.OU_gamma * randoms[i]
            process_series.append(value)

        return process_series

    def get_noise_process(self, generation):
        NoiseTrader.noise_process = NoiseTrader.process_series[generation]
        self.trading_signal = NoiseTrader.noise_process

    def get_excess_demand_function(self):
        # Process only 
        def func(price):
            return (self.wealth * self.leverage / price) * tanh(self.signal_scale * self.trading_signal) - self.asset
        self.excess_demand = func

        # TODO NT position becomes unbounded and insolvent.
        # Go back to the Noisy VI setup to avoid that?
        '''
        # Noisy VI
        def func(price):
            return (self.wealth * self.leverage / price) * tanh(self.signal_scale * self.trading_signal) - self.asset
        self.excess_demand = func
        '''




        

        
    