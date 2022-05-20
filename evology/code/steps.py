import balance_sheet_cython as bsc
import ga as ga
import timeit
from parameters import *
import market_clearing as mc
import market as mk
import creation as cr
from scipy import optimize
from scipy import stats
import numpy as np
import data
import fitness as fit
import pandas as pd
import random
from tqdm import tqdm
import warnings
import matplotlib
import matplotlib.pyplot as plt
import investment as iv
import linear_clearing as lc
import math
import dividend as div

def ga_evolution(
    pop, space, generation, wealth_coordinates, PROBA_SELECTION, MUTATION_RATE, Horizon
):

    if generation > SHIELD_DURATION:
        (
            pop,
            CountSelected,
            CountMutated,
            CountCrossed,
            StratFlow,
        ) = ga.strategy_evolution(
            space,
            pop,
            PROBA_SELECTION,
            MUTATION_RATE,
            wealth_coordinates,
        )
    else:
        CountSelected, CountMutated, CountCrossed = 0, 0, 0
        StratFlow = 6 * [0]
    return pop, CountSelected, CountMutated, CountCrossed, StratFlow


#def decision_updates(pop, price_history, dividend_history, CurrentPrice):
#    bs.DetermineTsvProc(pop, price_history, CurrentPrice)
#    bs.UpdateFval(pop, dividend_history)
#    bs.DetermineEDF(pop)
#    return pop


def marketClearing(pop, current_price, price_history, spoils, solver, volume):
    try:
        if solver == "esl":
            ed_functions, ToLiquidate = bs.agg_ed_esl(pop, spoils, volume)
            current_price = float(mc.solve(ed_functions, current_price)[0])
        elif solver == "esl.true":
            ed_functions, ToLiquidate = bs.agg_ed_esl(pop, spoils, volume)
            current_price = mc.CircuitClearing(ed_functions, current_price)
        elif solver == "newton":
            ed_functions, ToLiquidate = bs.agg_ed(pop, spoils, volume)
            current_price = max(
                optimize.newton(
                    func=ed_functions[0],
                    x0=current_price,
                    x1=1,
                    maxiter=10000,
                    rtol=10,
                    tol=0.01,
                ),
                0.01,
            )
        elif solver == "newton.true":
            ed_functions, ToLiquidate = bs.agg_ed(pop, spoils, volume)
            current_price = min(
                max(
                    optimize.newton(
                        func=ed_functions[0], x0=current_price
                    ),
                    0.5 * current_price,
                ),
                2 * current_price,
            )
        elif solver == "brentq":
            ed_functions, ToLiquidate = bs.agg_ed(pop, spoils)
            current_price = optimize.brentq(
                # ed_functions[0], 0.01, 10 * current_price
                ed_functions[0],
                0.01,
                10000,
            )
        elif solver == "scipy.min":
            ed_functions, ToLiquidate = bs.agg_ed(pop, spoils)
            current_price = optimize.minimize(ed_functions[0], current_price).x[0]
        elif solver == "root":
            ed_functions, ToLiquidate = bs.agg_ed(pop, spoils)
            current_price = optimize.root(ed_functions[0], current_price).x[0]
        elif solver == "univ_brent":
            ed_functions, ToLiquidate = bs.agg_ed(pop, spoils)
            current_price = optimize.minimize_scalar(ed_functions[0], method="brent").x
        elif solver == "univ_bounds":
            ed_functions, ToLiquidate = bs.agg_ed(pop, spoils)
            current_price = optimize.minimize_scalar(
                ed_functions[0],
                method="bounded",
                bounds=(0.9 * current_price, 1.1 * current_price),
            ).x
        elif solver == "nelder-mead":
            ed_functions, ToLiquidate = bs.agg_ed(pop, spoils)
            current_price = optimize.minimize(
                ed_functions[0], current_price, method="nelder-mead"
            ).x
        elif solver == "bfgs":
            ed_functions, ToLiquidate = bs.agg_ed(pop, spoils)
            current_price = optimize.minimize(
                ed_functions[0], current_price, method="bfgs"
            ).x
        elif solver == "newton-CG":
            ed_functions, ToLiquidate = bs.agg_ed(pop, spoils)
            current_price = optimize.minimize(
                ed_functions[0], current_price, method="Newton-CG"
            ).x
        elif solver == "trust-ncg":
            ed_functions, ToLiquidate = bs.agg_ed(pop, spoils)
            current_price = optimize.minimize(
                ed_functions[0], current_price, method="trust-ncg"
            ).x
        elif solver == "trust-exact":
            ed_functions, ToLiquidate = bs.agg_ed(pop, spoils)
            current_price = optimize.minimize(
                ed_functions[0], current_price, method="trust-exact"
            ).x
        
        elif solver == 'linear':
            current_price, ToLiquidate = bsc.linear_solver(pop, spoils, volume, current_price)

        else:
            raise ValueError("No maintained solver was selected.")

    except Exception as e:
        ed_functions, ToLiquidate = bs.agg_ed(pop, spoils, volume)
        func = ed_functions[0]
        print("Debuggig from steps.py")
        print(current_price)
        print(func(0))
        print(func(0.01))
        print(func(1))
        print(func(100000))
        print(e)

        # print("Avg ED at current price")
        # edtf, edvi, ednt = 0, 0, 0
        # tf, vi, nt = 0, 0, 0
        # for ind in pop:
        #     if ind.type == "tf":
        #         tf += 1
        #         edtf += ind.edf(ind, current_price)
        #     if ind.type == "nt":
        #         nt += 1
        #         ednt += ind.edf(ind, current_price)
        #     if ind.type == "vi":
        #         vi += 1
        #         edvi += ind.edf(ind, current_price)
        # print([ednt / nt, edvi / vi, edtf / tf])
        # print(nt, vi, tf)

        # print("Avg ED at 1")
        # edtf, edvi, ednt = 0, 0, 0
        # tf, vi, nt = 0, 0, 0
        # for ind in pop:
        #     if ind.type == "tf":
        #         tf += 1
        #         edtf += ind.edf(ind, 1)
        #     if ind.type == "nt":
        #         nt += 1
        #         ednt += ind.edf(ind, 1)
        #     if ind.type == "vi":
        #         vi += 1
        #         edvi += ind.edf(ind, 1)
        # print([ednt / nt, edvi / vi, edtf / tf])

        # print("Avg ED at 0.1")
        # edtf, edvi, ednt = 0, 0, 0
        # tf, vi, nt = 0, 0, 0
        # for ind in pop:
        #     if ind.type == "tf":
        #         tf += 1
        #         edtf += ind.edf(ind, 0.1)
        #     if ind.type == "nt":
        #         nt += 1
        #         ednt += ind.edf(ind, 0.1)
        #     if ind.type == "vi":
        #         vi += 1
        #         edvi += ind.edf(ind, 0.1)
        # print([ednt / nt, edvi / vi, edtf / tf])

        # for ind in pop:
        #     print([ind.type, ind.tsv, ind.edf(ind, current_price), ind.edf(ind, 1)])

        # func2 = np.vectorize(ed_functions[0])

        # x = np.linspace(0,100,100)
        # y = func2(x)
        # fig = plt.figure()
        # ax = fig.add_subplot(1, 1, 1)
        # plt.plot(x,y, 'r')
        # plt.show()

        raise ValueError("Solver exception.")

    # bs.CalcTsvVINT(pop, current_price)
    price_history.append(current_price)

    return pop, current_price, price_history, ToLiquidate





