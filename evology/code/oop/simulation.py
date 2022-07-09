from tqdm import tqdm
from noise_trader import NoiseTrader
from population import Population
from asset import Asset
from results import Result
from investor import Investor
import sys


class Simulation:
    def __init__(
        self, max_generations, population_size, wealth_coords, interest_rate, investment_bool, seed
    ):
        self.max_generations = max_generations
        self.population_size = population_size
        self.interest_rate = interest_rate
        self.interest_rate_daily = ((1.0 + self.interest_rate) ** (1.0 / 252.0)) - 1.0
        self.seed = seed
        self.generation = 0
        self.data = None
        self.disable = Simulation.set_display(self)
        self.investment_bool = investment_bool
        self.wealth_coords = wealth_coords

    def set_display(self):
        if sys.platform == "darwin":
            return False
        elif sys.platform == "linux":
            return True

    def return_data(self):
        return self.data

    def simulate(self):
        result = Result(self.max_generations)
        asset = Asset(self.max_generations, self.seed)
        pop = Population(
            self.population_size,
            self.max_generations,
            self.wealth_coords,
            self.interest_rate,
            Asset.dividend_growth_rate_yearly,
            self.seed,
        )
        NoiseTrader.process_series = NoiseTrader.compute_noise_process(
            self.max_generations, self.seed
        )
        investor = Investor(self.investment_bool)
        pop.create_pop()
        pop.count_wealth(asset.price)

        for self.generation in tqdm(range(self.max_generations), disable=self.disable):

            # print("Generation", generation)
            """TODO cythonize"""
            """ TODO wealth reset mode """
            """ TODO Hypermutate with liquidate, remove, split system"""
            """ TODO leverage and hypermutation? how do we deal with loans from borrowing cash to buy assets? should not change anything right? yes but double check"""
            pop.liquidate_insolvent()
            asset.get_dividend(self.generation)
            """ TODO extend EMA to many lags """
            asset.compute_price_emas()
            pop.update_trading_signal(
                asset.dividend,
                self.interest_rate_daily,
                self.generation,
                asset.price,
                asset.price_emas,
            )
            """ TODO TSV computation for the AV agent """
            # pop.get_excess_demand_functions()
            pop.get_pod_demand_functions()  #
            """ TODO TF does not seem to participate in the market, or very linearly with bias, + without bais sells it all in first period """
            """ TODO we have to check what happens in first period, maybe saving results once before the loop. VI on short already? strange"""
            """ TODO can't have the bias, creates unwanted shorts. But we do something for TF in early periods to avoid all selling"""
            # pop.get_aggregate_demand()
            pop.get_pod_aggregate_demand()  #
            """ TODO add liquidation system and spoils to market clearing """
            asset.market_clearing(pop.aggregate_demand)
            # asset.mismatch = pop.compute_demand_values(asset.price)
            asset.mismatch = pop.compute_pod_demand_values(asset.price)  #
            # asset.volume = pop.execute_demand(asset.price)
            asset.volume = pop.execute_pod_demand(asset.price)
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
            pop.get_returns_statistics()
            pop.get_wealth_statistics()
            pop.get_activity_statistics()
            pop.get_positions()
            """ TODO investment flows need some noise! we need to estimate it from the raw data"""
            pop.get_investment_flows()
            """ TODO collect traing signal / tsv / excess demand data"""
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
                pop.NT_returns,
                pop.VI_returns,
                pop.TF_returns
            )

        self.data = result.convert_df()
