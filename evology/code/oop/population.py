from trend_follower import TrendFollower
from value_investor import ValueInvestor
from noise_trader import NoiseTrader

class Population:

    def __init__(self, population_size):
        self.size = population_size
        self.agents = []

    def create_pop(self):
        if self.size == 3:
            self.agents.append(NoiseTrader(10, 10, 10, 10))
            self.agents.append(ValueInvestor(10, 10, 10, 10, 0.1))
            self.agents.append(TrendFollower(10, 10, 10, 10, 1))
        else:
            raise RuntimeError('Population size is not 3.')

    def count_wealth(self, price):
        for ind in self.agents:
            ind.wealth = ind.count_wealth(price) 
