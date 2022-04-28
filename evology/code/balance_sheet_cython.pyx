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
        if ind.type_as_int == 0:
            # Calculate process value, including individual strategy (bias)
            X = ind.process
            ind.process = abs(X + RHO_NT * (MU_NT + ind.strategy - X) + GAMMA_NT * randoms[i])
    return pop

cpdef CalculateTSV(list pop, list price_history, list dividend_history, double CurrentPrice):
    cdef cythonized.Individual ind

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
      
cpdef linear_solver(list pop, double spoils, double volume, double prev_price):
    cdef double price 
    cdef cythonized.Individual ind
    cdef double a = 0.0
    cdef double b = 0.0
    cdef double l 
    cdef double c
    cdef double aind

    if spoils > 0:
        ToLiquidate = -min(spoils, min(liquidation_perc * volume, 10000))
    elif spoils == 0:
        ToLiquidate = 0
    elif spoils < 0:
        ToLiquidate = min(abs(spoils), min(liquidation_perc * volume, 10000))

    b += ToLiquidate

    for ind in pop:
        if ind.type_as_int == 0:
            l = LeverageNT * 1.0
            c = SCALE_NT * 1.0
        if ind.type_as_int == 1:
            l = LeverageVI * 1.0
            c = SCALE_VI * 1.0
        if ind.type_as_int == 2:
            l = LeverageTF * 1.0
            c = SCALE_TF * 1.0
        b += ind.asset
        a += ind.wealth * l * (tanh(c * ind.tsv + 0.5))
        if isnan(a) == True or isnan(b) == True:
            print(a)
            print(b)
            print([ind.type, ind.tsv, ind.wealth, l, c])  
            raise ValueError('NAN output a or b for linear solver a/b.')  
    #price = min(max(a/b, 0.2*prev_price), 5*prev_price)
    #price = a/b
    # price = max(a/b, 0.01)
    price = min(max(a/b, 0.75*prev_price), 1.25*prev_price)
    price = max(price, 0.01)


    if isnan(price) == True:

        print(price)
        print(a)
        print(b)


        raise ValueError('Price is nan.')

    if price < 0:
        print("price, a, b, ToLiquidate, pop ind with negative a")
        print(price)
        print(a)
        print(b)
        print(ToLiquidate)
        for ind in pop:
            aind = ind.wealth * (tanh(ind.tsv + 0.5))
            if aind < 0:
                print([ind.type, ind.wealth, ind.tsv, ind.asset, aind])
        raise ValueError('Price is negative.')

    return price, ToLiquidate

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
    return pop

cpdef CalculateEDV(list pop, double current_price):
    cdef cythonized.Individual ind
    for ind in pop:
        ind.edv = ind.edf(ind, current_price)
    if ind.edv == math.inf:
        print([ind.type, ind.edv, ind.tsv, ind.wealth])
        print(ind.wealth / current_price)
        print(tanh(ind.tsv + 0.5))
        print(ind.asset)
        raise ValueError('edv = +inf')
    if ind.edv == - math.inf:
        print([ind.type, ind.edv, ind.tsv, ind.wealth])
        print(ind.wealth / current_price)
        print(tanh(ind.tsv + 0.5))
        print(ind.asset)
        raise ValueError('edv = -inf')
    return pop