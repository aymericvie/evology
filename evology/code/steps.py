import balance_sheet as bs
import ga as ga
import timeit
from parameters import *
import esl_market_clearing as esl_mc
import market as mk
import creation as cr
from scipy import optimize
from scipy import stats
import numpy as np
import data
import pandas as pd
import random
from tqdm import tqdm
import warnings
import matplotlib
import matplotlib.pyplot as plt

# random.seed(random.random())


def ga_evolution(
    pop, mode, space, generation, wealth_coordinates, PROBA_SELECTION, MUTATION_RATE
):
    if generation > SHIELD_DURATION:
        ga.compute_fitness(pop)
        (
            pop,
            CountSelected,
            CountMutated,
            CountCrossed,
            StratFlow,
        ) = ga.strategy_evolution(
            mode,
            space,
            pop,
            PROBA_SELECTION,
            MUTATION_RATE,
            wealth_coordinates,
            generation,
        )
    else:
        CountSelected, CountMutated, CountCrossed = 0, 0, 0
        StratFlow = 6 * [0]
    return pop, CountSelected, CountMutated, CountCrossed, StratFlow


def decision_updates(pop, mode, price_history, dividend_history):
    bs.DetermineTsvProc(mode, pop, price_history)
    bs.UpdateFval(pop, dividend_history)
    bs.DetermineEDF(pop)
    return pop


def marketClearing(pop, current_price, price_history, spoils, solver):
    if solver == "esl":
        ed_functions, ToLiquidate = bs.agg_ed_esl(pop, spoils)
        current_price = float(esl_mc.solve(ed_functions, current_price)[0])
    elif solver == "esl.true":
        ed_functions, ToLiquidate = bs.agg_ed_esl(pop, spoils)
        current_price = esl_mc.CircuitClearing(ed_functions, current_price)
    elif solver == "newton":
        ed_functions, ToLiquidate = bs.agg_ed(pop, spoils)
        current_price = max(
            optimize.newton(func=ed_functions[0], x0=current_price, maxiter=1000), 0.01
        )
    elif solver == "newton.true":
        ed_functions, ToLiquidate = bs.agg_ed(pop, spoils)
        current_price = min(
            max(
                optimize.newton(func=ed_functions[0], x0=current_price, maxiter=1000),
                0.5 * current_price,
            ),
            2 * current_price,
        )
    elif solver == "brentq":
        ed_functions, ToLiquidate = bs.agg_ed(pop, spoils)
        current_price = optimize.brentq(
            ed_functions[0], 0.5 * current_price, 2 * current_price
        )
    else:
        raise ValueError(
            "No solver was selected. Available options: esl, newton, brentq"
        )
    bs.CalcTsvVINT(pop, current_price)
    price_history.append(current_price)
    pop, mismatch = bs.calculate_edv(pop, current_price)
    return pop, mismatch, current_price, price_history, ToLiquidate


def marketActivity(
    pop, current_price, asset_supply, dividend, dividend_history, spoils, ToLiquidate
):
    pop, volume, spoils = mk.execute_ed(
        pop, current_price, asset_supply, spoils, ToLiquidate
    )
    pop, dividend, random_dividend = bs.earnings(pop, dividend)
    dividend_history.append(dividend)
    bs.update_margin(pop, current_price)
    bs.clear_debt(pop, current_price)
    return pop, volume, dividend, random_dividend, dividend_history, spoils


def update_wealth(
    pop, current_price, generation, wealth_coordinates, POPULATION_SIZE, reset_wealth
):
    bs.calculate_wealth(pop, current_price)  # Compute agents' wealth
    bs.update_profit(pop)
    bs.ComputeReturn(pop)
    bs.AgeUpdate(pop)
    return pop
