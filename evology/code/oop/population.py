from types import FunctionType
from trend_follower import TrendFollower
from value_investor import ValueInvestor
from noise_trader import NoiseTrader
from fund import Fund
from math import isnan
import numpy as np
import warnings

class Population:

    asset_supply = 0

    def __init__(
        self,
        population_size,
        max_generations,
        wealth_coords,
        interest_rate,
        dividend_growth_rate,
        seed,
    ):
        self.size = population_size
        self.max_generations = max_generations
        self.wealth_coords = wealth_coords
        self.agents = []
        self.interest_rate = interest_rate
        self.dividend_growth_rate = dividend_growth_rate
        self.seed = seed
        self.aggregate_demand = FunctionType

        self.wealthNT = 0.0
        self.wealthVI = 0.0
        self.wealthTF = 0.0
        self.wshareNT = 0.0
        self.wshareVI = 0.0
        self.wshareTF = 0.0
        self.VI_val = 0.0
        self.average_annual_return = 0.0
        self.NT_flows = 0.0
        self.VI_flows = 0.0
        self.TF_flows = 0.0
        self.NT_asset = 0.0
        self.VI_asset = 0.0
        self.TF_asset = 0.0
        self.NT_cash = 0.0
        self.VI_cash = 0.0
        self.TF_cash = 0.0
        self.NT_return = np.nan
        self.VI_return = np.nan
        self.TF_return = np.nan

        # TODO self.assetNT and things like that at the level of the population?

    def create_fund(self, type):
        if type == "NT":
            fund = NoiseTrader(
                0,
                0,
                0.01,
                self.interest_rate,
                self.dividend_growth_rate,
            )
        elif type == "VI":
            fund = ValueInvestor(
                0,
                0,
                0.01,
                self.interest_rate,
                self.dividend_growth_rate,
            )
        elif type == "TF":
            fund = TrendFollower(
                0, 
                0, 
                1)
        else:
            raise TypeError("Unrecognised requested type for create_fund.")
        return fund

    def create_pop(self):

        # Check we can create a diverse population
        if self.size < 3:
            raise RuntimeError('Population size cannot be inferior to 3.')
        [shareNT, shareVI, shareTF] = self.wealth_coords
        if shareNT + shareVI + shareTF > 1:
            raise RuntimeError("Wealth coordinates sum is higher than 1.")

        # Start the population with three agents of each type.
        self.agents.append(self.create_fund("NT"))
        self.agents.append(self.create_fund("VI"))
        self.agents.append(self.create_fund("TF"))

        # Fill the rest of the population
        NumNT, NumVI, NumTF = 1, 1, 1
        rng = np.random.default_rng(seed=self.seed + 2)
        for _ in range(self.size - 3):
            rd = rng.random()
            if rd <= shareNT:
                self.agents.append(self.create_fund("NT"))
                NumNT += 1
            elif rd > shareNT and rd <= shareNT + shareVI:
                self.agents.append(self.create_fund("VI"))
                NumVI += 1
            elif rd > shareNT + shareVI:
                self.agents.append(self.create_fund("TF"))
                NumTF += 1

        # Amount of cash/asset to split within each subpopulation
        total_cash = Fund.cash_nominal * self.size
        total_asset = Fund.asset_nominal * self.size
        # Initialise cash and assets wrt shares and numbers
        NT_cash, NT_asset = total_cash * shareNT / NumNT, total_asset * shareNT / NumNT
        VI_cash, VI_asset = total_cash * shareVI / NumVI, total_asset * shareVI / NumVI
        TF_cash, TF_asset = total_cash * shareTF / NumTF, total_asset * shareTF / NumTF

        for fund in self.agents:
            if isinstance(fund, NoiseTrader):
                fund.cash, fund.asset = NT_cash, NT_asset
            if isinstance(fund, ValueInvestor):
                fund.cash, fund.asset = VI_cash, VI_asset
            if isinstance(fund, TrendFollower):
                fund.cash, fund.asset = TF_cash, TF_asset

        Population.asset_supply = total_asset



    def count_wealth(self, price):
        for ind in self.agents:
            ind.wealth = ind.count_wealth(price)

    def update_trading_signal(
        self, dividend, interest_rate_daily, generation, price, price_ema
    ):
        # First, update VI valuation
        for ind in self.agents:
            if isinstance(ind, ValueInvestor):
                ind.update_valuation(dividend, interest_rate_daily)
            elif isinstance(ind, NoiseTrader):
                ind.get_noise_process(generation)
                ##
                ind.update_valuation(dividend, interest_rate_daily)
            elif isinstance(ind, TrendFollower):
                if generation >= ind.time_horizon:
                    ind.get_price_ema(price, price_ema[0])
                else:
                    ind.get_price_ema(price, np.nan)

    def get_excess_demand_functions(self):
        for ind in self.agents:
            ind.excess_demand_function = ind.get_excess_demand_function()

    def get_pod_demand_functions(self):
        for ind in self.agents:
            ind.get_pod_demand()

    def get_aggregate_demand(self):
        def func(price):
            result = 0.0
            for ind in self.agents:
                try:
                    result += ind.excess_demand(price)
                except Exception as e:
                    print(e)
                    raise RuntimeError(
                        "Failed to get ED(price) from agent.", ind.type, price
                    )
            return result

        self.aggregate_demand = func

    def get_pod_aggregate_demand(self):
        def func(price):
            result = 0.0
            for ind in self.agents:
                try:
                    result += ind.pod_demand(price)
                except Exception as e:
                    print(e)
                    raise RuntimeError(
                        "Failed to get pod_D(price) from agent.", ind.type, price
                    )
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

    def compute_pod_demand_values(self, price):
        mismatch = 0.0
        for ind in self.agents:
            if isinstance(ind, ValueInvestor):
                ind.compute_trading_signal(price)
            ind.compute_pod_demand(price)
            mismatch += ind.demand
        if mismatch > 1:
            warnings.warn('Mismatch superior to 1 ' + str(mismatch))
        return mismatch

    # def execute_demand(self, price):
    #     volume = 0.0
    #     sum_demand = 0.0
    #     for ind in self.agents:
    #         ind.execute_demand(price)
    #         sum_demand += ind.demand
    #         volume += abs(ind.demand)  # abs: buy & sell don't cancel out

    #     total_short = self.get_short_positions()

    #     if total_short >= Population.asset_supply + 1.0:
    #         print(total_short, Population.asset_supply)
    #         for ind in self.agents:
    #             print(ind.type, ind.asset, ind.wealth, ind.demand)
    #         raise RuntimeError("Short size position exceeded.")

    #     if abs(sum_demand) >= 1:
    #         # revert changes
    #         for ind in self.agents:
    #             ind.asset -= ind.demand
    #             ind.cash += ind.demand * price
    #         print(sum_demand)
    #         print(price)
    #         for ind in self.agents:
    #             print(ind.type, ind.demand, ind.asset, ind.wealth)
    #             print(ind.excess_demand(price), ind.demand)
    #             print(-ind.leverage * ind.max_short_size - ind.asset)
    #         raise ValueError("Sum demand not equal to 0.")

    #     total_assets = 0.0
    #     for ind in self.agents:
    #         total_assets += ind.asset

    #     if abs(total_assets - Population.asset_supply) >= 1:
    #         print(total_assets)
    #         print(Population.asset_supply)
    #         for ind in self.agents:
    #             print(ind.type, ind.asset, ind.demand, ind.wealth)
    #         raise ValueError(
    #             "Asset supply violated", total_assets, Population.asset_supply
    #         )

    #     if volume == 0:
    #         raise RuntimeError("Volume is 0.")
    #     return volume

    def execute_pod_demand(self, price):

        print("Price", price)

        print("- Pop info and sum assets---")
        sum_asset = 0
        for ind in self.agents:
            print(ind.type, ind.wealth, ind.asset, ind.demand)
            sum_asset += ind.asset
        print(sum_asset)

        
        # Verify that excess demand orders balance out
        sum_demand = 0.0
        for ind in self.agents:
            sum_demand += ind.demand
        if abs(sum_demand) > 1:
            # We have an imbalance to solve.
            buy_orders = 0.
            sell_orders = 0.
            for ind in self.agents:
                if ind.demand > 0:
                    buy_orders += ind.demand
                elif ind.demand < 0:
                    sell_orders += abs(ind.demand)
            if sell_orders != 0:
                order_ratio = buy_orders / sell_orders
            else:
                order_ratio = 0

            multiplier_buy = 0.
            multiplier_sell = 0.
            if order_ratio == 0.:  # either noone buys, or no one sells
                warnings.warn("No orders will be executed (no supply or no demand)")
            elif order_ratio < 1.:
                multiplier_buy = 1.
                multiplier_sell = order_ratio
                # Selling will be restricted according to demand
            elif order_ratio == 1:
                multiplier_buy = 1.
                multiplier_sell = 1.
                # All orders will be executed (supply =  demand)
            elif order_ratio > 1:
                multiplier_buy = 1. / order_ratio
                multiplier_sell = 1.
                # Buying will be restricted according to supply
            else:
                raise ValueError("order_ratio has a strange value: " + str(order_ratio))
                            
            warnings.warn('Agents demands adjusted to counter imbalance. ' + str(price) + str(order_ratio))

            for ind in self.agents:
                if ind.demand > 0:
                    ind.demand = ind.demand * multiplier_buy
                elif ind.demand < 0:
                    ind.demand = ind.demand * multiplier_sell

        volume = 0.0
        for ind in self.agents:
            volume += abs(ind.demand - ind.asset)  # abs: buy & sell don't cancel out
            ind.execute_pop_demand(price)

        total_assets = 0.0
        for ind in self.agents:
            total_assets += ind.asset

        if abs(total_assets - Population.asset_supply) >= 1:
            print("agent type, demand")
            for ind in self.agents:
                print(ind.type, ind.wealth, ind.asset, ind.demand)
            raise ValueError(
                "Asset supply violated", total_assets, Population.asset_supply
            )

        if volume == 0:
            raise RuntimeError("Volume is 0.")

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
        total_profit, count_funds = 0.0, 0
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
            raise ValueError("self average annual return > 10")

        # Compute average monthly return
        total_profit, count_funds = 0.0, 0
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

    def get_returns_statistics(self):

        returnNT = 0.0
        returnVI = 0.0
        returnTF = 0.0
        countNT, countVI, countTF = 0, 0, 0

        for ind in self.agents:
            if isinstance(ind, NoiseTrader):
                returnNT += ind.daily_return
                countNT += 1
            elif isinstance(ind, ValueInvestor):
                returnVI += ind.daily_return
                countVI += 1
            elif isinstance(ind, TrendFollower):
                returnTF += ind.daily_return
                countTF += 1

        if countNT != 0:
            self.NT_returns = returnNT / countNT
        else:
            self.NT_returns = np.nan
        if countVI != 0:
            self.VI_returns = returnVI / countVI
        else:
            self.VI_returns = np.nan
        if countTF != 0:
            self.TF_returns = returnTF / countTF
        else:
            self.TF_returns = np.nan

    def get_wealth_statistics(self):

        wealthNT = 0.0
        wealthVI = 0.0
        wealthTF = 0.0

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
        NTflows, VIflows, TFflows = 0.0, 0.0, 0.0
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
            self.NT_flows, self.VI_flows, self.TF_flows = 0.0, 0.0, 0.0

    def get_positions(self):
        NT_asset, VI_asset, TF_asset = 0.0, 0.0, 0.0
        NT_cash, VI_cash, TF_cash = 0.0, 0.0, 0.0
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
