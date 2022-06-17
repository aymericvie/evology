from types import FunctionType
from trend_follower import TrendFollower
from value_investor import ValueInvestor
from noise_trader import NoiseTrader
from fund import Fund
from math import isnan
import numpy as np

class Population:

    asset_supply = 0

    def __init__(self, population_size, max_generations, interest_rate, dividend_growth_rate, seed):
        self.size = population_size
        self.max_generations = max_generations
        self.agents = []
        self.interest_rate = interest_rate
        self.dividend_growth_rate = dividend_growth_rate
        self.seed = seed
        self.aggregate_demand = FunctionType

        self.wealthNT = 0.
        self.wealthVI = 0.
        self.wealthTF = 0.
        self.wshareNT = 0.
        self.wshareVI = 0.
        self.wshareTF = 0.
        self.VI_val = 0.
        self.average_annual_return = 0.
        self.NT_flows = 0.
        self.VI_flows = 0.
        self.TF_flows = 0.
        self.NT_asset = 0.
        self.VI_asset = 0.
        self.TF_asset = 0.
        self.NT_cash = 0.
        self.VI_cash = 0.
        self.TF_cash = 0.

        # TODO self.assetNT and things like that at the level of the population?

    def create_pop(self):
        if self.size == 3:
            self.agents.append(NoiseTrader(100_000_000, 500_000, 0.01, self.interest_rate, self.dividend_growth_rate))
            self.agents.append(ValueInvestor(100_000_000, 500_000, 0.01, self.interest_rate, self.dividend_growth_rate))
            self.agents.append(TrendFollower(100_000_000, 500_000, 1))
        else:
            raise RuntimeError('Population size is not 3.')

        total_asset = 0
        for ind in self.agents:
            total_asset += ind.asset
        Population.asset_supply = total_asset
    
    '''
    def set_max_short_size(self):
        for fund in self.agents:
            fund.max_short_size = 500_000
    '''

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
                ##
                ind.update_valuation(dividend, interest_rate_daily)
            elif isinstance(ind, TrendFollower):
                ind.get_price_ema(price, price_ema[0])
    
    def get_excess_demand_functions(self):
        for ind in self.agents:
            ind.excess_demand_function = ind.get_excess_demand_function()

    def get_aggregate_demand(self):
        def func(price):
            result = 0.0
            for ind in self.agents:
                try:
                    result += ind.excess_demand(price)
                except Exception as e:
                    print(e)
                    raise RuntimeError('Failed to get ED(price) from agent.', ind.type, price)
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
        sum_demand = 0.0
        for ind in self.agents:
            ind.execute_demand(price)
            sum_demand += ind.demand
            volume += abs(ind.demand) # abs: buy & sell don't cancel out

        total_short = self.get_short_positions()

        if total_short >= Population.asset_supply + 1.:
            print(total_short, Population.asset_supply)
            for ind in self.agents:
                print(ind.type, ind.asset, ind.wealth, ind.demand)
            raise RuntimeError('Short size position exceeded.') 

        if abs(sum_demand) >= 1:
            # revert changes 
            for ind in self.agents:
                ind.asset -= ind.demand
                ind.cash += ind.demand * price 
            print(sum_demand)
            print(price)
            for ind in self.agents:
                print(ind.type, ind.demand, ind.asset, ind.wealth)
                print(ind.excess_demand(price), ind.demand)
                print(- ind.leverage * ind.max_short_size - ind.asset)
            raise ValueError('Sum demand not equal to 0.')
        
        total_assets = 0.
        for ind in self.agents:
            total_assets += ind.asset 
        
        if abs(total_assets - Population.asset_supply) >= 1:
            print(total_assets)
            print(Population.asset_supply)
            for ind in self.agents:
                print(ind.type, ind.asset, ind.demand, ind.wealth)
            raise ValueError('Asset supply violated', total_assets, Population.asset_supply)

        if volume == 0:
            raise RuntimeError('Volume is 0.')
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

    def update_margin(self, price):
        for ind in self.agents:
            ind.update_margin(price)

    def liquidate_insolvent(self):
        for ind in self.agents:
            ind.liquidate_insolvent()

    def compute_profit(self):
        for ind in self.agents:
            ind.compute_profit()

    def update_wealth_history(self):
        for ind in self.agents:
            ind.update_wealth_history()

    def compute_average_return(self):

        # Compute average annual return
        total_profit, count_funds = 0.,0
        for ind in self.agents:
            if isnan(ind.get_annual_return()) == False:
                total_profit += ind.get_annual_return()
                count_funds += 1
        if count_funds != 0:
            self.average_annual_return = total_profit / count_funds
        else:
            self.average_annual_return = np.nan
        
        # Check that average return is not aberrant
        if self.average_annual_return > 10:
            print(self.average_annual_return)
            raise ValueError('self average annual return > 10')

        # Compute average monthly return
        total_profit, count_funds = 0.,0
        for ind in self.agents:
            if isnan(ind.get_monthly_return()) == False:
                total_profit += ind.get_monthly_return()
                count_funds += 1
        if count_funds != 0:
            self.average_monthly_return = total_profit / count_funds
        else:
            self.average_monthly_return = np.nan

    def compute_excess_profit(self):
        for ind in self.agents:
            ind.excess_annual_return = ind.annual_return - self.average_annual_return    

    def get_wealth_statistics(self):

        wealthNT = 0.
        wealthVI = 0.
        wealthTF = 0.

        for ind in self.agents:
            if isinstance(ind, NoiseTrader):
                wealthNT += ind.wealth 
            elif isinstance(ind, ValueInvestor):
                wealthVI += ind.wealth
            elif isinstance(ind, TrendFollower):
                wealthTF += ind.wealth
        
        total_wealth = wealthNT + wealthVI + wealthTF

        self.wealthNT = wealthNT
        self.wealthVI = wealthVI 
        self.wealthTF = wealthTF
        self.wshareNT = wealthNT / total_wealth
        self.wshareVI = wealthVI / total_wealth
        self.wshareTF = wealthTF / total_wealth

    def get_short_positions(self):
        total_short = 0
        for ind in self.agents:
            if ind.asset < 0:
                total_short += abs(ind.asset)
        return total_short


    def get_activity_statistics(self):
        VI_val, VI_count = 0, 0
        for ind in self.agents:
            if isinstance(ind, ValueInvestor):
                VI_val += ind.valuation * ind.wealth
                VI_count += ind.wealth
        self.VI_val = VI_val / VI_count

    def get_investment_flows(self):
        NTflows, VIflows, TFflows = 0., 0., 0.
        for ind in self.agents:
            if isinstance(ind, NoiseTrader):
                NTflows += ind.net_flow
            elif isinstance(ind, ValueInvestor):
                VIflows += ind.net_flow
            elif isinstance(ind, TrendFollower):
                TFflows += ind.net_flow
        
        total_flows = abs(NTflows) + abs(VIflows) + abs(TFflows)
        if total_flows != 0:
            self.NT_flows = NTflows / total_flows
            self.VI_flows = VIflows / total_flows
            self.TF_flows = TFflows / total_flows
        else:
            self.NT_flows, self.VI_flows, self.TF_flows = 0.,0.,0.

    def get_positions(self):
        NT_asset, VI_asset, TF_asset = 0.,0.,0.
        NT_cash, VI_cash, TF_cash = 0.,0.,0.
        for ind in self.agents:
            if isinstance(ind, NoiseTrader):
                NT_asset += ind.asset
                NT_cash += ind.cash
            elif isinstance(ind, ValueInvestor):
                VI_asset += ind.asset
                VI_cash += ind.cash
            elif isinstance(ind, TrendFollower):
                TF_asset += ind.asset
                TF_cash += ind.cash

        self.NT_asset = NT_asset
        self.VI_asset = VI_asset
        self.TF_asset = TF_asset
        self.NT_cash = NT_cash
        self.VI_cash = VI_cash
        self.TF_cash = TF_cash