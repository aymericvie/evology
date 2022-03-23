import numpy as np
import math
import warnings
from parameters import *
import cythonized
cimport cythonized
from cythonized import calculate_edv


cpdef clear_debt(list pop, double price):
    cdef cythonized.Individual ind
    for ind in pop:
        if ind.loan > 0:  # If the agent has outstanding debt:
            if ind.cash >= ind.loan + 100.0 * price:  # If the agent has enough cash:
                ind.loan = 0.0
                ind.cash -= ind.loan
            if (
                ind.cash < ind.loan + 100.0 * price
            ):  # If the agent does not have enough cash:
                ind.loan -= ind.cash - 100.0 * price
                ind.cash = 100.0 * price
    return pop


cpdef update_margin(list pop, double current_price):
    cdef cythonized.Individual ind
    for ind in pop:
        ind.cash += ind.margin
        ind.margin = 0.0
        if ind.asset < 0.0:
            ind.margin += ind.asset * current_price
            ind.cash -= ind.asset * current_price
        if ind.cash < 0.0:
            ind.loan += abs(ind.cash)
            ind.cash = 0.0
    return pop


def UpdatePrevWealth(pop):
    for ind in pop:
        ind.prev_wealth = ind.wealth


def calculate_wealth(pop, current_price):
    replace = False
    for ind in pop:
        ind.wealth = ind.cash + ind.asset * current_price - ind.loan
        if ind.wealth < 0.0:
            replace = True
    return pop, replace

def count_pop_long_assets(pop):
    count = 0
    for ind in pop:
        count += ind.asset
    return count


cpdef count_long_assets(list pop, double spoils):    
    cdef cythonized.Individual ind
    cdef double count = 0.0
    for ind in pop:
        count += ind.asset
    count += spoils
    return count


cpdef count_short_assets(list pop, double spoils):
    cdef cythonized.Individual ind
    cdef double count = 0.0
    for ind in pop:
        if ind.asset < 0:
            count += abs(ind.asset)
    if spoils < 0:
        count += abs(spoils)
    return count

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


def agg_ed(pop, spoils, volume):
    functions = []
    ToLiquidate = 0

    if spoils > 0:
        ToLiquidate = -min(spoils, liquidation_perc * volume)
    elif spoils == 0:
        ToLiquidate = 0
    elif spoils < 0:
        ToLiquidate = min(abs(spoils), liquidation_perc * volume)

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


def agg_ed_esl(pop, spoils, volume):
    functions = []
    ToLiquidate = 0

    if spoils > 0:
        ToLiquidate = -min(spoils, liquidation_perc * volume)
    elif spoils == 0:
        ToLiquidate = 0
    elif spoils < 0:
        ToLiquidate = min(abs(spoils), liquidation_perc * volume)

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
        if ind.prev_wealth != 0:
            ind.DailyReturn = (ind.wealth - ind.prev_wealth) / ind.prev_wealth
        else:
            ind.DailyReturn = np.nan


def update_profit(pop):
    for ind in pop:
        ind.profit = ind.wealth - ind.prev_wealth
        ind.profit_internal = ind.wealth - ind.investor_flow - ind.prev_wealth

def ApplyReinvestment(pop, ReinvestmentRate):
    if ReinvestmentRate < 0:
        raise ValueError('Negative reinvestment rate is not allowed.')

    if ReinvestmentRate >= 1:
        EffectiveRate = 0
    if ReinvestmentRate < 1:
        EffectiveRate = ReinvestmentRate - 1
    
    for ind in pop:
        ind.cash += EffectiveRate * ind.profit
    return pop

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

def AgeUpdate(pop):
    for ind in pop:
        ind.age += 1
    return pop