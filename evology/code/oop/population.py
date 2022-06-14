from types import FunctionType
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
        self.aggregate_demand = FunctionType

        # TODO self.assetNT and things like that at the level of the population?

    def create_pop(self):
        if self.size == 3:
            self.agents.append(NoiseTrader(100_000_000, 500_000))
            self.agents.append(ValueInvestor(100_000_000, 500_000, 0.01, self.interest_rate, self.dividend_growth_rate))
            self.agents.append(TrendFollower(100_000_000, 500_000, 1))
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
    
    def get_excess_demand_functions(self):
        for ind in self.agents:
            ind.excess_demand_function = ind.get_excess_demand_function()

    def get_aggregate_demand(self):
        def func(price):
            result = 0.0
            for ind in self.agents:
                result += ind.excess_demand(price)
            return result 
        self.aggregate_demand = func

    def compute_demand_values(self, price):
        mismatch = 0.0
        for ind in self.agents:
            if isinstance(ind, ValueInvestor):
                ind.compute_trading_signal(price)
            ind.compute_demand(price)
            mismatch += ind.demand
        return mismatch

    def execute_demand(self, price):
        volume = 0.0
        for ind in self.agents:
            ind.execute_demand(price)
            volume += abs(ind.demand) # abs: buy & sell don't cancel out
        return volume

    def clear_debt(self):
        for ind in self.agents:
            ind.clear_debt()

    def earnings(self, dividend, interest_rate_daily):
        for ind in self.agents:
            ind.earnings(dividend, interest_rate_daily)

    def count_assets(self):
        total = 0.0
        for ind in self.agents:
            total += ind.get_assets()
        return total
        # TODO add an error if we violate the asset supply cst