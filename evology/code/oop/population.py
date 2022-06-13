from trend_follower import TrendFollower
from value_investor import ValueInvestor
from noise_trader import NoiseTrader

class Population:

    def __init__(self, population_size, max_generations, interest_rate, dividend_growth_rate, seed):
        self.size = population_size
        self.max_generations = max_generations
        self.agents = []
        self.interest_rate = interest_rate
        self.dividend_growth_rate = dividend_growth_rate
        self.seed = seed

    def create_pop(self):
        if self.size == 3:
            self.agents.append(NoiseTrader(10, 10, 10, 10))
            self.agents.append(ValueInvestor(10, 10, 10, 10, 0.01, self.interest_rate, self.dividend_growth_rate))
            self.agents.append(TrendFollower(10, 10, 10, 10, 1))
        else:
            raise RuntimeError('Population size is not 3.')

    def count_wealth(self, price):
        for ind in self.agents:
            ind.wealth = ind.count_wealth(price) 
    
    def update_trading_signal(self, dividend, interest_rate_daily, generation, price, price_ema):
        # First, update VI valuation
        for ind in self.agents:
            if isinstance(ind, ValueInvestor):
                ind.update_valuation(dividend, interest_rate_daily)
            elif isinstance(ind, NoiseTrader):
                ind.get_noise_process(generation)
            elif isinstance(ind, TrendFollower):
                ind.get_price_ema(price, price_ema[0])
