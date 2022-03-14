#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
cimport cythonized
from libc.math cimport log2
from parameters import *
import numpy as np
cdef float NAN
NAN = float("nan")

cpdef UpdateWealthProfitAge(list pop, double current_price):
    cdef cythonized.Individual ind
    cdef int replace = 0
    for ind in pop:
        # Compute wealth
        ind.wealth = ind.cash + ind.asset * current_price - ind.loan
        if ind.wealth < 0:
            replace = 1
        # Compute profit
        ind.profit = ind.wealth - ind.prev_wealth
        ind.profit_internal = ind.wealth - ind.investor_flow - ind.prev_wealth
        # Compute return
        if ind.prev_wealth != 0:
            ind.DailyReturn = (ind.wealth - ind.prev_wealth) / ind.prev_wealth
        else:
            ind.DailyReturn = NAN
        # Update age
        ind.age += 1
        
    return pop, replace

def NoiseProcess(pop):
    randoms = np.random.normal(0, 1, len(pop))
    for i, ind in enumerate(pop):
        if ind.type == "nt":
            # Calculate process value
            X = ind.process
            ind.process = abs(X + RHO_NT * (MU_NT - X) + GAMMA_NT * randoms[i])
            #ind.tsv = math.log2(ind.process * ind[0]) - math.log2(CurrentPrice)
    return pop

cpdef CalculateTSV(list pop, list price_history, list dividend_history, double CurrentPrice):
    cdef cythonized.Individual ind

    for ind in pop:
        if ind.type == "nt":
            # Calculate TSV
            ind.tsv = (ind.process - 1) 
        elif ind.type == "vi":
            # Calculate TSV
            ind.tsv = log2(ind[0] / CurrentPrice)
        else: # ind.type == "tf
            # Calculate TSV
            if len(price_history) >= ind[0]:
                #print(price_history)
                #print(price_history[0])
                #print(price_history[-1])
                #print(type(price_history[-1]))
                ind.tsv =  log2(CurrentPrice / price_history[-ind[0]])
                
            else:
                ind.tsv = 0
    return pop

cpdef UpdateFval(list pop, double dividend):

    cdef double estimated_daily_div_growth
    cdef double numerator
    cdef double denuminator
    cdef double fval
    cdef cythonized.Individual ind

    estimated_daily_div_growth = (
        (1 + DIVIDEND_GROWTH_RATE_G) ** (1 / TRADING_DAYS)
    ) - 1
    numerator = (1 + estimated_daily_div_growth) * dividend
    for ind in pop:
        if ind.type == "vi":
            denuminator = (
                1.0 + (AnnualInterestRate + ind.strategy) - DIVIDEND_GROWTH_RATE_G
            ) ** (1.0 / 252.0) - 1.0
            fval = numerator / denuminator
            ind[0] = fval # TODO This might be something to change later on
            if fval < 0:
                warnings.warn("Negative fval found in update_fval.")
            if fval == np.inf:
                raise ValueError('Infinite FVal.')
    return pop

def DetermineEDF(pop):
    for ind in pop:
        if ind.type == "tf":
            ind.edf = (
                lambda ind, p: (LeverageTF * ind.wealth / p)
                * math.tanh(SCALE_TF * ind.tsv)
                - ind.asset
            )
        #elif ind.type == "vi":
        #    ind.edf = (
        #        lambda ind, p: (parameters.LeverageVI * ind.wealth / p)
        #        * math.tanh((5 / ind[0]) * (ind[0] - p))
        #        - ind.asset
        #    )
        elif ind.type == "vi":
            ind.edf = (
                lambda ind, p: (LeverageVI * ind.wealth / p)
                * math.tanh(SCALE_VI * ind.tsv)
                - ind.asset
            )
        #elif ind.type == "nt":
        #    ind.edf = (
        #        lambda ind, p: (parameters.LeverageNT * ind.wealth / p)
        #        * math.tanh((5 / (ind[0] * ind.process)) * (ind[0] * ind.process - p))
        #        - ind.asset
        #    )
        elif ind.type == "nt":
            ind.edf = (
                lambda ind, p: (LeverageNT * ind.wealth / p)
                * math.tanh(SCALE_NT * ind.tsv)
                - ind.asset
            )
        else:
            raise Exception(f"Unexpected ind type: {ind.type}")
    return pop