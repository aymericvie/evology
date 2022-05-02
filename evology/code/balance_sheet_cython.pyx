#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
cimport cythonized
from libc.math cimport log2, tanh, isnan
from parameters import G, GAMMA_NT, RHO_NT, MU_NT, LeverageNT, LeverageVI, LeverageTF
from parameters import G_day, SCALE_NT, SCALE_TF, SCALE_VI, interest_year, liquidation_perc
import warnings
import math
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
        if isnan(ind.wealth) == True:
            print([ind.cash, ind.asset, current_price, ind.loan, ind.wealth])
            raise ValueError('ind.wealth is nan')
        # Compute profit
        ind.profit = ind.wealth - ind.prev_wealth
        #ind.profit_internal = ind.wealth - ind.investor_flow - ind.prev_wealth
        ind.profit_internal = ind.wealth - ind.prev_wealth
        # Compute return
        if ind.prev_wealth != 0:
            ind.DailyReturn = (ind.wealth - ind.prev_wealth) / ind.prev_wealth
        else:
            ind.DailyReturn = NAN
        # Update age
        ind.age += 1

        
    return pop, replace

cpdef NoiseProcess(pop):

    cdef double[:] randoms = np.random.normal(GAMMA_NT,1,size=len(pop))
    cdef int i
    cdef cythonized.Individual ind

    for i, ind in enumerate(pop):
        if ind.type_as_int == 0:
            # Calculate process value, including individual strategy (bias)
            #ind.process = abs(ind.process + RHO_NT * (MU_NT + ind.strategy - ind.process) + randoms[i])
            ind.process += RHO_NT * (MU_NT + ind.strategy - ind.process) + randoms[i]
            if ind.process < 0:
                ind.process = abs(ind.process)


    return pop

cpdef CalculateTSV(list pop, list price_history, list dividend_history, double CurrentPrice):
    cdef cythonized.Individual ind
    cdef int i 
    cdef int t

    for i, ind in enumerate(pop):
        t = ind.type_as_int
        if t == 0: # NT
            ind.tsv = (ind.process - 1)
        elif t == 1: # VI
            ind.tsv = log2(ind.val / CurrentPrice)
            if isnan(ind.tsv) == True:
                raise ValueError('ind.tsv is NAN')
        else: # TF
            if len(price_history) >= ind.strategy:
                ind.tsv =  log2(CurrentPrice / price_history[-int(ind.strategy)])
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
            fval = numerator / ind.val_net # TODO: Val_net only changes when val changes
            if fval != np.inf:
                ind.val = fval
            #if ind.val < 0:
            #    warnings.warn("Negative fval found in update_fval.")
            #if ind.val == np.inf:
            #    print(numerator)
            #    print(ind.val_net)
            ##    print(ind.strategy)
            #    print(interest_year)
            #    print(ind.val)
            #    print((interest_year + ind.strategy) - G)
            #    raise ValueError('Infinite FVal.')
    return pop

def DetermineEDF(pop):
# Cant cpdef because closures are not supported
    cdef cythonized.Individual ind
    cdef int t
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
                #* tanh(SCALE_NT * ind.tsv)
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
        if isnan(ind.wealth) == True:
            print(ind.wealth)
            print(ind.cash)
            print(ind.asset)
            print(current_price)
            print(ind.loan)
            print(ind.age)
            raise ValueError('ind.wealth is NAN')
    return pop, replace
      


cpdef UpdateQuarterlyWealth(list pop, double generation):
    cdef cythonized.Individual ind
    if generation % 63 == 0:
        for ind in pop:
            ind.quarterly_wealth = ind.wealth
    return pop
    
cpdef UpdateWealthSeries(list pop):
    cdef cythonized.Individual ind
    for ind in pop:
        if len(ind.wealth_series) < 63:
            pass
        else:
            del ind.wealth_series[0]
        ind.wealth_series.append(ind.wealth)
        ind.last_wealth = ind.wealth_series[0]
    return pop

cpdef CalculateEDV(list pop, double current_price):
    cdef cythonized.Individual ind
    cdef double mismatch = 0.0
    
    #for ind in pop:
    #    ind.edv = ind.edf(ind, current_price)
    #return pop

    cdef int t
    for ind in pop:
        t = ind.type_as_int
        if t==2:
            ind.edv = (LeverageTF * ind.wealth / current_price) * tanh(SCALE_TF * ind.tsv + 0.5) - ind.asset
        elif t==1:
            ind.edv = (LeverageVI * ind.wealth / current_price) * tanh(SCALE_VI * ind.tsv + 0.5) - ind.asset
        elif t == 0:
            ind.edv = (LeverageNT * ind.wealth / current_price) * tanh(SCALE_NT * ind.tsv + 0.5) - ind.asset
        else:
            raise Exception(f"Unexpected ind type: {ind.type}")
        mismatch += ind.edv
    return pop, mismatch

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