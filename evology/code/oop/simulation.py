from tqdm import tqdm
from noise_trader import NoiseTrader
from population import Population
from asset import Asset
from results import Result
from investor import Investor
import sys

class Simulation:
    def __init__(self, max_generations, population_size, interest_rate, investment_bool, seed):
        self.max_generations = max_generations
        self.population_size = population_size
        self.interest_rate = interest_rate
        self.interest_rate_daily = ((1.0 + self.interest_rate) ** (1.0 / 252.0)) - 1.0
        self.seed = seed
        self.generation = 0
        self.data = None
        self.disable = Simulation.set_display(self)
        self.investment_bool = investment_bool
    
    def set_display(self):
        if sys.platform == "darwin":
            return False
        elif sys.platform == 'linux': 
            return True

    def return_data(self):
        return self.data

    def simulate(self):
        result = Result(self.max_generations)
        asset = Asset(self.max_generations, self.seed)
        pop = Population(self.population_size, self.max_generations, self.interest_rate, Asset.dividend_growth_rate_yearly, self.seed)
        NoiseTrader.process_series = NoiseTrader.compute_noise_process(self.max_generations, self.seed)
        investor = Investor(self.investment_bool)

        """ TODO Improve pop creation with coords """
        pop.create_pop() 
        pop.count_wealth(asset.price)

        for self.generation in tqdm(range(self.max_generations), disable = self.disable):

            # print("Generation", generation)
            """TODO cythonize """
            """ TODO wealth reset mode """
            """ TODO Hypermutate with liquidate, remove, split system"""
            pop.liquidate_insolvent()
            asset.get_dividend(self.generation)
            """ TODO extend EMA to many lags """
            asset.compute_price_emas()
            pop.update_trading_signal(asset.dividend, self.interest_rate_daily, self.generation, asset.price, asset.price_emas)
            """ TODO TSV computation for the AV agent """
            pop.get_excess_demand_functions()
            pop.get_aggregate_demand()
            """ TODO add liquidation system and spoils to market clearing """
            asset.market_clearing(pop.aggregate_demand)
            asset.mismatch = pop.compute_demand_values(asset.price)
            """ TODO add check to not overtake short pos size """
            """ TODO what to do with very small deviations from asset supply (0.01)?"""
            """ TODO system to prevent short pos size excess and maybe cancel some buy orders """
            asset.volume = pop.execute_demand(asset.price)
            pop.earnings(asset.dividend, self.interest_rate_daily)
            pop.update_margin(asset.price)
            pop.clear_debt()
            pop.count_wealth(asset.price)
            pop.update_wealth_history()
            pop.compute_average_return()
            pop.compute_excess_profit()
            pop.compute_profit()
            investor.investment_flows(pop)
            pop.count_wealth(asset.price) 
            pop.get_wealth_statistics()
            pop.get_activity_statistics()
            pop.get_positions()
            pop.get_investment_flows()
            """ TODO collect strategy return data"""
            result.update_results(
                self.generation, 
                asset.price, 
                asset.dividend, 
                asset.volume,
                NoiseTrader.noise_process,
                pop.VI_val,
                pop.wshareNT,
                pop.wshareVI,
                pop.wshareTF,
                pop.NT_flows,
                pop.VI_flows,
                pop.TF_flows,
                pop.NT_asset,
                pop.VI_asset,
                pop.TF_asset,
                pop.NT_cash,
                pop.VI_cash,
                pop.TF_cash,
            )
        
        self.data = result.convert_df()




