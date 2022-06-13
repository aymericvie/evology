from tqdm import tqdm
from noise_trader import NoiseTrader
from population import Population
from asset import Asset

class Simulation:
    def __init__(self, max_generations, population_size, interest_rate, seed):
        self.max_generations = max_generations
        self.population_size = population_size
        self.interest_rate = interest_rate
        self.interest_rate_daily = ((1.0 + self.interest_rate) ** (1.0 / 252.0)) - 1.0
        self.seed = seed
        


    def simulate(self):
        asset = Asset(self.max_generations, self.seed)
        pop = Population(self.population_size, self.max_generations, self.interest_rate, Asset.dividend_growth_rate_yearly, self.seed)
        
        NoiseTrader.process_series = NoiseTrader.compute_noise_process(self.max_generations, self.seed)

        """ TODO Improve pop creation with coords """
        pop.create_pop() 
        pop.count_wealth(asset.price)

        
        for generation in tqdm(range(self.max_generations)):
            print("Generation", generation)
            """ TODO Hypermutate """
            dividend = asset.get_dividend(generation)
            """ TODO extend EMA to many lags """
            """ TODO asset: must create price ema """
            asset.compute_price_emas()
            pop.update_trading_signal(dividend, self.interest_rate_daily, generation, asset.price, asset.price_emas)
            """ TODO TSV computation for the AV agent """
            pop.get_excess_demand_functions()
            aggregate_demand = pop.get_aggregate_demand()
            asset.market_clearing(aggregate_demand)
        print([[ind.type, ind.wealth] for ind in pop.agents])



