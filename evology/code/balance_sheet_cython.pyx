#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
cimport cythonized
from libc.math cimport log2
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
                ind.tsv =  log2(price_history[-1]) - log2(
                    price_history[-ind[0]]
                )
            else:
                ind.tsv = 0
    return pop