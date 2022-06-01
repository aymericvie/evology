#cython: boundscheck=False, wraparound = False, initializedcheck=False, cdivision=True
cimport cythonized
import cythonized
from libc.math cimport log2, tanh, isnan, fabs, fmin, fmax
from parameters import G, GAMMA_NT, RHO_NT, MU_NT, LeverageNT, LeverageVI, LeverageTF, max_strat_lag
from parameters import G_day, SCALE_NT, SCALE_TF, SCALE_VI, liquidation_perc, interest_day
from parameters import tf_daily_ma_horizons
import warnings
import math
import numpy as np
cdef float NAN
NAN = float("nan")

cpdef mean(series):
    cdef double cumsum = 0.
    cdef int length = 0
    for item in series:
        cumsum += item
        length += 1
    return cumsum / length

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
            ind.DailyReturn = max((ind.wealth - ind.prev_wealth) / ind.prev_wealth, -1)
        else:
            ind.DailyReturn = NAN
        # Update age
        ind.age += 1

        
    return pop, replace

'''
cpdef NoiseProcess(list pop, rng, double process):

    #cdef double[:] randoms = rng.normal(GAMMA_NT,1,size=len(pop))
    cdef double randoms = rng.normal(0, 1)
    #cdef int i
    cdef cythonized.Individual ind
    #cdef double a
    #cdef double b
    process = RHO_NT * (MU_NT - process) + GAMMA_NT * randoms

    #for i, ind in enumerate(pop):
    for ind in pop:
        if ind.type_as_int == 0:
            # Calculate process value, including individual strategy (bias)
            a = ind.strategy - ind.process
            b = RHO_NT * (MU_NT - a) + randoms
            ind.process = b
            #if b < 0:
            #    ind.process = abs(b)

            #ind.process = abs(RHO_NT * (MU_NT + ind.strategy  - ind.process) + randoms) 
            #ind.process = process #+ ind.strategy * RHO_NT
            ind.process = process


    return pop
'''

cpdef subset_means(list series, int max_lag):
    cdef int i 
    cdef list subset_list
    cdef list means 

    #subset_list = [series[-i:] for i in range(1, max_lag + 1)]
    subset_list = [series[-i:] for i in tf_daily_ma_horizons]
    means = [mean(subset) for subset in subset_list]
    return means

cpdef CalculateTSV_staticf(list pop, list price_history, double CurrentPrice, double process, rng):
    cdef cythonized.Individual ind
    cdef int i 
    cdef int t
    cdef list price_means = subset_means(price_history, max_strat_lag)
    cdef double[:] randoms = rng.normal(0, 0.1, len(pop))
    #cdef double ma5_price = price_means[4]

    for i, ind in enumerate(pop):
        t = ind.type_as_int
        if t == 0: # NT
            ind.tsv = process - MU_NT / 2. #+ ind.strategy #* randoms[i]
        elif t == 1: # VI
            ''' for previous-price VI '''
            ind.tsv = log2(ind.val / CurrentPrice) 
            #ind.tsv = log2(ind.val / price_means[0])
            ''' for contemporaneous VI '''
            pass    
        elif t == 2: # TF
            if len(price_history) >= ind.strategy:
                ''' Rate of change TF (compare price values)'''
                #ind.last_price = price_history[-int(ind.strategy)]
                #ind.tsv =  log2(CurrentPrice / ind.last_price)
                ''' Moving average TF (compares p(t-1) to moving average at time horizon'''
                #ind.tsv = log2((CurrentPrice / price_means[int(ind.strategy_index)]) + 0.5)
                ind.tsv = log2((CurrentPrice / price_means[int(ind.strategy_index)]))
                #print('TF with strat ' + str(ind.strategy) + '// Current Price ' + str(CurrentPrice) + ' vs MA ' + str(price_means[int(ind.strategy_index)]) + ' gives tsv ' + str(tanh(ind.tsv))) 
                #ind.tsv = log2(price_means[0] / price_means[int(ind.strategy_index)]) 
                ''' this setting has big impact on price jumps and ecology dynamics '''
            else:
                ind.tsv = 0.5 #0.0
        else:
            pass
            # BH stay at 1, IR stay at 0, AV is not computed here, VI cannot compute before price is known
    return pop, price_means

cpdef CalculateTSV_avf(list pop, double generation, object strategy, list price_history, double dividend):
    cdef cythonized.Individual ind
    cdef int i 
    cdef int t
    cdef double p1 
    cdef double p2 
    cdef double p3 
    cdef double p4 
    cdef double p5 
    cdef double p6 
    cdef double p7 
    cdef double p8 
    cdef double p9 
    cdef double p10 
    cdef double d = dividend
    cdef double v = (1+G_day) * dividend / (interest_day + 0.01 - G_day)
    cdef double g = G_day
    cdef double r = interest_day
    cdef int length = len(price_history)

    if generation > 10 and strategy != None:
        p1 = price_history[length-1]
        p2 = price_history[length-2]
        p3 = price_history[length-3]
        p4 = price_history[length-4]
        p5 = price_history[length-5]
        p6 = price_history[length-6]
        p7 = price_history[length-7]
        p8 = price_history[length-8]
        p9 = price_history[length-9]
        p10 = price_history[length-10]

        for i, ind in enumerate(pop):
            t = ind.type_as_int
            if t == 3: #AV
                ind.tsv = ind.adaptive_strategy(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, d, v, g, r)

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
            #if fval != np.inf:
            ind.val = fval
    return pop

'''
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
'''

cpdef UpdateFullWealth(list pop, double current_price):
    cdef cythonized.Individual ind
    cdef int replace = 0
    for ind in pop:
        ind.wealth = ind.cash + ind.asset * current_price - ind.loan
        if isnan(ind.wealth) == True:
            print([ind.cash, ind.asset, current_price, ind.loan, ind.wealth])
            raise ValueError('ind.wealth is nan')
        ind.prev_wealth = ind.wealth
        if ind.wealth < 0:
            replace = 1  
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

'''
cpdef CalculateEDV(list pop, double current_price):
    cdef cythonized.Individual ind
    cdef double mismatch = 0.0
    cdef double a
    cdef double b
    cdef double c
    cdef int t

    for ind in pop:
        t = ind.type_as_int
        if t == 2: # TF
            a = (LeverageTF * ind.wealth / current_price)
            b = tanh(SCALE_TF * ind.tsv + 0.5)
            c = ind.asset

        elif t == 1: #VI
            #for contemporaneous VI 
            ind.tsv = log2(ind.val / current_price)

            #for previous-price VI
            a = (LeverageVI * ind.wealth / current_price)
            b = tanh(SCALE_VI * ind.tsv + 0.5)
            c = ind.asset

        elif t == 0: #NT
            a = (LeverageNT * ind.wealth / current_price)
            b = tanh(SCALE_NT * ind.tsv + 0.5)
            c = ind.asset
        
        elif t == 3: #AV
            a = ind.wealth / current_price
            b = tanh(ind.tsv)
            c = ind.asset

        elif t == 4: # BH
            a = 0. #ind.wealth / current_price
            b = 1.
            c = 0. #ind.asset

        elif t == 5: # IR
            a = 0.
            b = 0.
            c = 0. #ind.asset

        ind.edv = a * b - c
        mismatch += ind.edv

        if isnan(ind.edv) == True:
            print(ind.type)
            raise TypeError('NAN EDV')

    return pop, mismatch
'''

cpdef DetermineLiquidation(double spoils, double volume):    
    cdef double ToLiquidate = 0.0
    if spoils > 0:
        ToLiquidate = -fmin(spoils, fmin(liquidation_perc * volume, 10000))
    #elif spoils == 0:
    #    ToLiquidate = 0
    elif spoils < 0:
        ToLiquidate = fmin(fabs(spoils), fmin(liquidation_perc * volume, 10000))
    return ToLiquidate
    
cpdef count_long_assets(list pop, double spoils):    
    cdef cythonized.Individual ind
    cdef double count = 0.0
    for ind in pop:
        if ind.type_as_int != 4:
            count += ind.asset
    count += spoils
    return count

cpdef UpdatePriceHistory(list price_history, double current_price):
    
    price_history.append(current_price)
    return price_history



cpdef count_short_assets(list pop, double spoils):
    cdef cythonized.Individual ind
    cdef double count = 0.0
    for ind in pop:
        if ind.type_as_int != 4:
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





