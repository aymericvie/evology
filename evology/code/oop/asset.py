from math import sqrt
import numpy as np
from scipy.optimize import root

class Asset:

    dividend_growth_rate_yearly = 0.01
    dividend_growth_rate_daily = ((1.0 + dividend_growth_rate_yearly) ** (1.0 / 252.0)) - 1.0
    dividend_volatility = 0.1 / sqrt(252)
    dividend_autocorrelation = 0.1
    dividend_autocorrelation_lag = 1
    ema_horizons = 2 # TODO convert to list
    ema_smoothing_factors = 2 / 3
    # ema_smoothing_factors = [2. / (ema_horizons[i] + 1.) for i in len(ema_horizons)]

    def __init__(self, time_horizon, seed):
        self.time_horizon = time_horizon
        self.price = 100 # Initial price
        self.dividend = 0.003983 # Initial dividend
        self.seed = seed
        self.dividend_series = self.compute_dividend_series(self.time_horizon, self.seed)
        self.price_emas = [self.price] # For a single time horizon
        self.volume = 0.0
        self.mismatch = 0.0

    def get_dividend(self, generation):
        self.dividend = self.dividend_series[0, generation]

    def compute_dividend_series(self, time_horizon, seed):
        dividend_series = np.zeros((1, time_horizon))
        rd_dividend_series = np.zeros((1, time_horizon))
        rng = np.random.default_rng(seed=seed)
        z_process = rng.standard_normal(time_horizon)
        dividend_series[0, 0] = self.dividend
        rd_dividend_series[0, 0] = z_process[0]
        dividend = self.dividend

        for i in range(time_horizon):
            wiener_back = z_process[i]
            if i > Asset.dividend_autocorrelation_lag:
                wiener_back = (
                    (1.0 - Asset.dividend_autocorrelation ** 2) 
                    * z_process[i]
                    + Asset.dividend_autocorrelation * rd_dividend_series[0, 
                    i - Asset.dividend_autocorrelation_lag - 1])
            dividend = abs(dividend + Asset.dividend_growth_rate_daily * dividend + 
                Asset.dividend_volatility * dividend * wiener_back)
            dividend_series[0, i] = dividend
            rd_dividend_series[0, i] = wiener_back

        return dividend_series

    def compute_price_emas(self):
        #self.price_emas = [(self.price * Asset.ema_smoothing_factors[i] + self.price_emas[i] * (1. - Asset.ema_horizons[i])) for i in range(Asset.ema_horizons)]
        self.price_emas = [(self.price * Asset.ema_smoothing_factors + self.price_emas[0] * (1. - Asset.ema_smoothing_factors))]

    def market_clearing(self, aggregate_demand):
        self.price = root(aggregate_demand, self.price, method="hybr").x
        # TODO: install circuit breaker
        if self.price < 0:
            raise RuntimeError('Negative price', self.price)
