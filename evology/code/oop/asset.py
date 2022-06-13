from math import sqrt
import numpy

class Asset:

    dividend_growth_rate_yearly = 0.01
    dividend_growth_rate_daily = ((1.0 + dividend_growth_rate_yearly) ** (1.0 / 252.0)) - 1.0
    dividend_volatility = 0.1 / sqrt(252)
    dividend_autocorrelation = 0.1
    dividend_autocorrelation_lag = 1

    def __init__(self):
        self.price = 100 # Initial price
        self.dividend = 0.003983 # Initial dividend
        self.dividend_series = self.compute_dividend_series(self)

    def get_dividend(self, generation):
        self.dividend = self.dividend_series[generation]

    def compute_dividend_series(self):
        return 