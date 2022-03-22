#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
cimport cythonized
from libc.math cimport log2, tanh
from parameters import G, GAMMA_NT, RHO_NT, MU_NT, LeverageNT, LeverageVI, LeverageTF
from parameters import G_day, SCALE_NT, SCALE_TF, SCALE_VI, interest_year
import warnings
import numpy as np
cdef float NAN
NAN = float("nan")

cpdef convert_ind_type_to_num(t):
    # We enumerate the individual type string into integer, for faster access
    # while inside Cython.
    if t == "nt":
        return 0
    elif t == "vi":
        return 1
    else:
        return 2


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
        t = ind.type_as_int
        if t == 0:
            # Calculate process value
            X = ind.process
            ind.process = abs(X + RHO_NT * (MU_NT - X) + GAMMA_NT * randoms[i])
            #ind.tsv = math.log2(ind.process * ind[0]) - math.log2(CurrentPrice)
    return pop

cpdef CalculateTSV(list pop, list price_history, list dividend_history, double CurrentPrice):
    cdef cythonized.Individual ind

    for ind in pop:
        t = ind.type_as_int
        if t == 0:
            # Calculate TSV
            ind.tsv = (ind.process - 1) 
        elif t == 1:
            # Calculate TSV
            ind.tsv = log2(ind[0] / CurrentPrice)
        else: # t==2
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

    
    numerator = (1 + G_day) * dividend
    for ind in pop:
        t = ind.type_as_int
        if t==1:
            denuminator = (
                1.0 + (interest_year + ind.strategy) - G
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
        t = ind.type_as_int
        if t==2:
            ind.edf = (
                lambda ind, p: (LeverageTF * ind.wealth / p)
                * tanh(SCALE_TF * ind.tsv + 0.5)
                - ind.asset
            )
        elif t==1:
            ind.edf = (
                lambda ind, p: (LeverageVI * ind.wealth / p)
                * tanh(SCALE_VI * ind.tsv + 0.5)
                - ind.asset
            )
        elif t==0:
            ind.edf = (
                lambda ind, p: (LeverageNT * ind.wealth / p)
                * tanh(SCALE_NT * ind.tsv + 0.5)
                - ind.asset
            )
        else:
            raise Exception(f"Unexpected ind type: {ind.type}")
    return pop

cpdef UpdateFullWealth(list pop, double current_price):
    cdef cythonized.Individual ind
    cdef int replace = 0
    for ind in pop:
        ind.wealth = ind.cash + ind.asset * current_price - ind.loan
        ind.prev_wealth = ind.wealth
        if ind.wealth < 0:
            replace = 1  
    return pop, replace
      