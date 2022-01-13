import numpy as np
from parameters import *
from market import *
import math
import warnings

import cythonized


def clear_debt(pop, price):
    for ind in pop:
        if ind.loan > 0:  # If the agent has outstanding debt:
            if ind.cash >= ind.loan + 100 * price:  # If the agent has enough cash:
                ind.loan = 0
                ind.cash -= ind.loan
            if (
                ind.cash < ind.loan + 100 * price
            ):  # If the agent does not have enough cash:
                ind.loan -= ind.cash - 100 * price
                ind.cash = 100 * price
    return ind


def update_margin(pop, current_price):
    for ind in pop:
        ind.cash += ind.margin
        ind.margin = 0
        if ind.asset < 0:
            ind.margin += ind.asset * current_price
            ind.cash -= ind.asset * current_price
        if ind.cash < 0:
            ind.loan += abs(ind.cash)
            ind.cash = 0
    return ind


def UpdatePrevWealth(pop):
    for ind in pop:
        ind.prev_wealth = ind.wealth


def calculate_wealth(pop, current_price):
    for ind in pop:
        ind.wealth = ind.cash + ind.asset * current_price - ind.loan


def DetermineTsvProc(mode, pop, price_history):
    # Pre-generate the random number once for all, to reduce Numpy calling
    # overhead.
    randoms = np.random.normal(0, 1, len(pop))
    for count, ind in enumerate(pop):
        if ind.type == "tf":
            if len(price_history) >= ind[0]:
                ind.tsv = math.log2(price_history[-1]) - math.log2(
                    price_history[-ind[0]]
                )
            elif len(price_history) < ind[0]:
                ind.tsv = 0
        elif ind.type == "nt":
            ind.process = abs(
                ind.process
                + RHO_NT * (math.log2(MU_NT) - math.log2(ind.process))
                + GAMMA_NT * randoms[count]
            )
            if ind.process < 0:
                warnings.warn("Negative process value for NT")


def UpdateFval(pop, dividend_history):
    estimated_daily_div_growth = (
        (1 + DIVIDEND_GROWTH_RATE_G) ** (1 / TRADING_DAYS)
    ) - 1

    if len(dividend_history) >= 1:
        numerator = (1 + estimated_daily_div_growth) * dividend_history[-1]
    elif len(dividend_history) < 1:
        numerator = (1 + estimated_daily_div_growth) * INITIAL_DIVIDEND

    for ind in pop:
        denuminator = (
            1 + (AnnualInterestRate + ind.strategy) - DIVIDEND_GROWTH_RATE_G
        ) ** (1 / 252) - 1
        fval = numerator / denuminator

        if fval < 0:
            warnings.warn("Negative fval found in update_fval.")

        if ind.type == "vi" or ind.type == "nt":
            ind[0] = fval
    return pop


def DetermineEDF(pop):
    for ind in pop:
        if ind.type == "tf":
            ind.edf = (
                lambda ind, p: (LeverageTF * ind.wealth / p)
                * math.tanh(SCALE_TF * ind.tsv)
                - ind.asset
            )
        elif ind.type == "vi":
            ind.edf = (
                lambda ind, p: (LeverageVI * ind.wealth / p)
                * math.tanh((5 / ind[0]) * (ind[0] - p))
                - ind.asset
            )
        elif ind.type == "nt":
            ind.edf = (
                lambda ind, p: (LeverageNT * ind.wealth / p)
                * math.tanh((5 / (ind[0] * ind.process)) * (ind[0] * ind.process - p))
                - ind.asset
            )
        else:
            raise Exception(f"Unexpected ind type: {ind.type}")
    return pop


def calculate_edv(pop, price):
    total_edv = 0
    for ind in pop:
        ind.edv = ind.edf(ind, price)
        total_edv += ind.edv
    return pop, total_edv


def count_pop_long_assets(pop):
    count = 0
    for ind in pop:
        count += ind.asset
    return count


def count_long_assets(pop, spoils):
    count = 0
    for ind in pop:
        count += ind.asset
    count += spoils
    return count


def count_short_assets(pop, spoils):
    count = 0
    for ind in pop:
        if ind.asset < 0:
            count += abs(ind.asset)
    if spoils < 0:
        count += abs(spoils)
    return count


def count_pop_short_assets(pop):
    count = 0
    for ind in pop:
        if ind.asset < 0:
            count += abs(ind.asset)
    return count


def earnings(pop, prev_dividend):
    dividend, random_dividend = draw_dividend(prev_dividend)
    for ind in pop:
        div_asset = ind.asset * dividend  # Determine gain from dividends
        interest_cash = ind.cash * INTEREST_RATE  # Determine gain from interest
        ind.cash += REINVESTMENT_RATE * (
            div_asset + interest_cash
        )  # Apply reinvestment

    return pop, dividend, random_dividend


def pop_report(pop):
    for ind in pop:
        agent_report(ind)


def agent_report(ind):
    if ind.type == "tf":
        print(
            "TF agent - "
            + str(round(ind[0], 2))
            + ", Cash "
            + str(int(ind.cash))
            + ", Asset_Long "
            + str(int(ind.asset))
            + ", Wealth "
            + str(int(ind.wealth))
            + ", TS "
            + str(round(ind.tsv, 2))
            + ", EV "
            + str(int(ind.edv))
            + ", Margin "
            + str(int(ind.margin))
            + ", Loan "
            + str(int(ind.loan))
        )  # + ", Profit " + str(int(ind.profit)) + ", Fitness " + str(ind.fitness))
    if ind.type == "vi":
        print(
            "VI agent - "
            + str(round(ind[0], 2))
            + ", Cash "
            + str(int(ind.cash))
            + ", Asset_Long "
            + str(int(ind.asset))
            + ", Wealth "
            + str(int(ind.wealth))
            + ", TS "
            + str(round(ind.tsv, 2))
            + ", EV "
            + str(int(ind.edv))
            + ", Margin "
            + str(int(ind.margin))
            + ", Loan "
            + str(int(ind.loan))
        )  # )#", Profit " + str(int(ind.profit)) + ", Fitness " + str(ind.fitness))
    if ind.type == "nt":
        print(
            "NT agent - "
            + str(round(ind[0], 2))
            + ", Cash "
            + str(int(ind.cash))
            + ", Asset_Long "
            + str(int(ind.asset))
            + ", Wealth "
            + str(int(ind.wealth))
            + ", TS "
            + str(round(ind.tsv, 2))
            + ", EV "
            + str(int(ind.edv))
            + ", Margin "
            + str(int(ind.margin))
            + ", Loan "
            + str(int(ind.loan))
            + ", Process: "
            + str(round(ind.process, 2))
        )  # )#", Profit " + str(int(ind.profit)) + ", Fitness " + str(ind.fitness))


def CalcTsvVINT(pop, price):
    if price < 0:
        warnings.warn("Negative price " + str(price))
    for ind in pop:
        if ind.type == "vi":
            ind.tsv = (5 / ind[0]) * (ind[0] - price)
        if ind.type == "nt":
            ind.tsv = (5 / (ind[0] * ind.process)) * (ind[0] * ind.process - price)
    return ind


def TotalWealth(pop):
    Wealth = 0
    for ind in pop:
        if ind.wealth > 0:
            Wealth += ind.wealth
    return Wealth


def convert_to_array(pop):
    array_pop = np.empty(len(pop), object)
    for idx, ind in enumerate(pop):
        array_pop[idx] = ind
    return array_pop


def agg_ed(pop, spoils):
    functions = []
    ToLiquidate = 0

    if spoils > 0:
        ToLiquidate = -min(spoils, LIQUIDATION_ORDER_SIZE)
    elif spoils == 0:
        ToLiquidate = 0
    elif spoils < 0:
        ToLiquidate = min(abs(spoils), LIQUIDATION_ORDER_SIZE)

    array_pop = convert_to_array(pop)

    def big_edf(price):
        return cythonized.big_edf(array_pop, price, ToLiquidate)

    # def big_edf(price):
    #    result = ToLiquidate
    #    for ind in pop:
    #        result += ind.edf(ind, price)
    #    return result
    functions.append(big_edf)
    return functions, ToLiquidate


def agg_ed_esl(pop, spoils):
    functions = []
    ToLiquidate = 0

    if spoils > 0:
        ToLiquidate = -min(spoils, LIQUIDATION_ORDER_SIZE)
    elif spoils == 0:
        ToLiquidate = 0
    elif spoils < 0:
        ToLiquidate = min(abs(spoils), LIQUIDATION_ORDER_SIZE)

    array_pop = convert_to_array(pop)

    def big_edf(asset_key, price):
        return cythonized.big_edf(array_pop, price, ToLiquidate)

    # def big_edf(asset_key, price):
    #    result = ToLiquidate
    #    for ind in pop:
    #        result += ind.edf(ind, price)
    #    return result
    functions.append(big_edf)
    return functions, ToLiquidate


def ComputeReturn(pop):
    for ind in pop:
        if ind.prev_wealth > 0:
            ind.DailyReturn = (ind.wealth / ind.prev_wealth) - 1
        else:
            ind.DailyReturn = np.nan


def update_profit(pop):
    for ind in pop:
        ind.profit = ind.wealth - ind.prev_wealth


def report_types(pop):
    num_tf = 0
    num_vi = 0
    num_nt = 0
    for ind in pop:
        if ind.type == "tf":
            num_tf += 1
        if ind.type == "vi":
            num_vi += 1
        if ind.type == "nt":
            num_nt += 1
    print("TF: " + str(num_tf) + ", VI: " + str(num_vi) + ", NT: " + str(num_nt))


def GetWealth(pop, strat):
    TotalWealth = 0
    for ind in pop:
        if ind.type == strat:
            TotalWealth += ind.wealth
    return TotalWealth


def GetNumber(pop, strat):
    TotalNumber = 0
    for ind in pop:
        if ind.type == strat:
            TotalNumber += 1
    return TotalNumber
