#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
cimport cythonized
from libc.math cimport log2, tanh, isnan
from parameters import G, GAMMA_NT, RHO_NT, MU_NT, LeverageNT, LeverageVI, LeverageTF
from parameters import G_day, SCALE_NT, SCALE_TF, SCALE_VI, interest_year, liquidation_perc
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
#        t = ind.type_as_int
        if ind.type_as_int == 0:
            # Calculate process value
            X = ind.process
            ind.process = abs(X + RHO_NT * (MU_NT - X) + GAMMA_NT * randoms[i])
    return pop

cpdef CalculateTSV(list pop, list price_history, list dividend_history, double CurrentPrice):
    cdef cythonized.Individual ind

    #randoms = np.random.normal(0, GAMMA_NT, len(pop))

    for i, ind in enumerate(pop):
        t = ind.type_as_int
        if t == 0:
            # Calculate TSV
            #ind.strategy = (1.0 + avg_phi / 100.0) * ind.strategy
            #ind.tsv = (randoms[i] + ind.strategy - 1) 
            
            ind.tsv = (ind.process - 1)
        elif t == 1:
            # Calculate TSV
            ind.tsv = log2(ind.val / CurrentPrice)
            if isnan(ind.tsv) == True:
                print(ind.tsv)
                print(ind.val)
                print(CurrentPrice)
                print(log2(ind.val/CurrentPrice))
                raise ValueError('ind.tsv is NAN')
            #sum_tsv += ind.tsv
            #count += 1.0
        else: # t==2
            # Calculate TSV
            if len(price_history) >= ind.strategy:
                #print(price_history)
                #print(price_history[0])
                #print(price_history[-1])
                #print(type(price_history[-1]))
                ind.tsv =  log2(CurrentPrice / price_history[-int(ind.strategy)])
            else:
                ind.tsv = 0
            #sum_tsv += ind.tsv
            #count += 1.0
    return pop
    #, sum_tsv/len(pop)

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
      
cpdef linear_solver(list pop, double spoils, double volume, double prev_price):
    cdef double price 
    cdef cythonized.Individual ind
    cdef double a = 0.0
    cdef double b = 0.0
    cdef double l 
    cdef double c

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
        if isnan(a) == True:
            print(a)
            print([ind.type, ind.tsv, ind.wealth, l, c])  
            raise ValueError('NAN output a for linear solver a/b.')  
    price = min(max(a/b, 0.2*prev_price), 5*prev_price)


    if isnan(price) == True:
        print(price)
        print(a)
        print(b)
        raise ValueError('Price is nan.')

    if price < 0:
        print(price)
        print(a)
        print(b)
        print(ToLiquidate)
        raise ValueError('Price is negative.')

    return price, ToLiquidate