#cython: boundscheck=False, wraparound = False, initializedcheck=False, cdivision=True
cimport cythonized
import cythonized
from libc.math cimport log2, tanh, isnan, fabs, fmin, fmax
from parameters import G, GAMMA_NT, RHO_NT, MU_NT, LeverageNT, LeverageVI, LeverageTF
from parameters import G_day, SCALE_NT, SCALE_TF, SCALE_VI, liquidation_perc
from parameters import tf_daily_ma_horizons, ema_factors
from parameters import G
import warnings
import math
import numpy as np
cdef float NAN
NAN = float("nan")

cpdef mean(list series):
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

'''
cpdef back_slice(list arr, int index):
    " A fast function to extract the mean of last n items of a list "
    cdef double[:] arr_sliced[index]
    cdef double mean_arr_sliced

    arr_sliced = arr[-index:]
    mean_arr_sliced = mean(arr_sliced)

    return mean_arr_sliced


cpdef subset_means(list series, int max_lag, list tf_daily_ma_horizons):
    # adding list tf etc does not make any difference.
    cdef int i 
    #cdef list subset_list
    cdef list means 

    #subset_list = [series[-i:] for i in tf_daily_ma_horizons]
    means = [back_slice(series, i) for i in tf_daily_ma_horizons]
    #means = [mean(subset) for subset in subset_list]
    return means
'''

cpdef price_emas(double price, list emas):
    cdef int i 
    #print(ema_factors)
    #print(emas)
    #print(ema_factors[0])
    #print(emas[0])
    
    emas = [(ema_factors[i] * (price - emas[i]) + emas[i]) for i in range(len(emas))]

    return emas

cpdef CalculateTSV_staticf(list pop, list price_history, double CurrentPrice, double process, rng, list price_emas):
    cdef cythonized.Individual ind
    cdef int i 
    cdef int t
    #cdef double[:] randoms = rng.normal(0, 0.1, len(pop))
    #cdef double ma5_price = price_means[4]

    for i, ind in enumerate(pop):
        t = ind.type_as_int
        if t == 0: # NT
            ind.tsv = process  #+ ind.strategy #* randoms[i]
            #ind.tsv = log2((process * ind.val) / price_emas[0]) 
        elif t == 1: # VI
            ''' for previous-price VI '''
            #ind.tsv = log2(ind.val / price_emas[0]) 
            ind.tsv = log2(ind.val / CurrentPrice)
            #if isnan(ind.tsv) == True:
            #    print(ind.val)
            #    print(price_emas[0])
            #    raise RuntimeError('NaN VI tsv')
            #''' for contemporaneous VI '''
            #ind.tsv = process
            pass 
        elif t == 2: # TF
            if len(price_history) >= ind.strategy:
                ''' Rate of change TF (compare price values)'''
                #ind.last_price = price_history[-int(ind.strategy)]
                #ind.tsv =  log2(CurrentPrice / ind.last_price)
                ''' Moving average TF (compares p(t-1) to moving average at time horizon'''
                #ind.tsv = log2((CurrentPrice / price_means[int(ind.strategy_index)]) + 0.5)
                
                
                #ind.tsv = log2((CurrentPrice / price_emas[int(ind.strategy_index)]))

                # ind.tsv = log2((price_emas[0] / price_emas[int(ind.strategy_index)]))
                ind.tsv = log2((CurrentPrice / price_emas[int(ind.strategy_index)]))

                #print('TF with strat ' + str(ind.strategy) + '// Current Price ' + str(CurrentPrice) + ' vs MA ' + str(price_means[int(ind.strategy_index)]) + ' gives tsv ' + str(tanh(ind.tsv))) 
                #ind.tsv = log2(price_means[0] / price_means[int(ind.strategy_index)]) 

                ''' TSV for TSF using contemporaneous price '''
                #ind.tsv = price_emas[int(ind.strategy_index)]

            else:
                ind.tsv = NAN #0.0
        else:
            pass
            # BH stay at 1, IR stay at 0, AV is not computed here, VI cannot compute before price is known
    return pop

cpdef CalculateTSV_avf(list pop, double generation, object strategy, list price_history, double dividend, double interest_day):
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


cpdef UpdateFval(list pop, double dividend, double interest_year):

    cdef double estimated_daily_div_growth
    cdef double numerator
    cdef double denuminator
    cdef double fval
    cdef cythonized.Individual ind
    
    numerator = (1 + G_day) * dividend
    for ind in pop:
        t = ind.type_as_int
        if t==1 or t==0:
            if ind.val_net == 0.0 or ind.val_net < 0:
                print(ind.strategy)
                print(ind.val_net)
                print(ind.type)
                raise ValueError('ind.val_net <= 0')
            fval = numerator / ind.val_net # TODO: Val_net only changes when val changes
            #if fval != np.inf:
            ind.val = fval
            #print(fval)

            if ind.val == 0.0 or isnan(ind.val) == True or ind.val < 0:
                print('ind.val, numerator, ind.val_net, ind.strategy, actual formula for ind.val_net in creation')
                print(ind.val)
                print(numerator)
                print(ind.val_net)
                print(ind.strategy)
                print((1.0 + (interest_year + ind.strategy) - G) ** (
                    1.0 / 252.0
                ) - 1.0)
                print(numerator/ ((1.0 + (interest_year + ind.strategy) - G) ** (
                    1.0 / 252.0
                ) - 1.0))
                print(ind.type)
                raise RuntimeError('Nan or 0 ind.val')
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

'''
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
'''

cpdef clear_debt(list pop, double price, double interest_day):
    cdef cythonized.Individual ind
    for ind in pop:
        if isnan(ind.cash) == True:
            raise RuntimeError('NAN cash 1')
        ind.loan = ind.loan * (1 + interest_day)
        if ind.loan < 0:
            ind.cash += abs(ind.loan)
            ind.loan = 0.0
        if ind.loan > 0:  # If the agent has outstanding debt:
            if ind.cash >= ind.loan:  # If the agent has enough cash:
                ind.loan = 0.0
                ind.cash -= ind.loan
            else: # If the agent does not have enough cash:
                ind.loan -= ind.cash 
                ind.cash = 0.0
        if isnan(ind.cash) == True:
            raise RuntimeError('NAN cash')
    return pop

cpdef Wealth_Shares(list pop, double price):

    cdef cythonized.Individual ind
    cdef int t
    cdef double wealth_nt = 0.0
    cdef double wealth_vi = 0.0
    cdef double wealth_tf = 0.0
    cdef double wealth_av = 0.0
    cdef double wshare_nt
    cdef double wshare_vi
    cdef double wshare_tf
    cdef double wshare_av = 0.0
    cdef double total_wealth = 0.0
    cdef double total_cash = 0.0
    cdef double new_cash = 0.0

    # Calculate current wealth, wealth shares and current money supply
    for ind in pop:
        ind.wealth = ind.cash + ind.asset * price - ind.loan
        t = ind.type_as_int
        if t == 0: # NT
            wealth_nt += ind.wealth
            total_cash += ind.cash - ind.loan
        if t == 1: # VI
            wealth_vi += ind.wealth
            total_cash += ind.cash - ind.loan
        if t == 2: # TF
            wealth_tf += ind.wealth
            total_cash += ind.cash - ind.loan
        if t == 3: # AV
            wealth_av += ind.wealth
            total_cash += ind.cash - ind.loan

        ##if ind.loan != 0:
        #    print([ind.type, ind.cash, ind.loan, ind.asset, ind.wealth])
        #    raise RuntimeError('Agent had a loan during wealth normalisation.')
        if ind.margin != 0:
            raise RuntimeError('Agent had a margin during wealth normalisation.')

    total_wealth = wealth_nt + wealth_vi + wealth_tf + wealth_av
    wshare_nt = 100. * wealth_nt / total_wealth
    wshare_vi = 100. * wealth_vi / total_wealth
    wshare_tf = 100. * wealth_tf / total_wealth
    wshare_av = 100. * wealth_av / total_wealth

    if isnan(wshare_nt)== True:
        raise RuntimeError('NAN WShare NT')

    if isnan(wshare_vi)== True:
        raise RuntimeError('NAN WShare VI')

    if isnan(wshare_tf)== True:
        raise RuntimeError('NAN WShare TF')

    if isnan(wshare_av)== True:
        raise RuntimeError('NAN WShare AV')

    return wshare_nt, wshare_vi, wshare_tf, wshare_av, total_cash


cpdef Wealth_Normalisation(list pop, double MoneySupply, double price):

    " This function normalizes wealth to keep money supply "
    " at constant levels "
    # We need money supply (from pop creation)
    # We need current money in circulation
    # We normalise at the fund level, and keep the wealth share constant
    # We'll need an error check for equality of WS before/after normalisation

    cdef double norm_factor
    cdef cythonized.Individual ind
    cdef double wshare_nt
    cdef double wshare_vi
    cdef double wshare_tf
    cdef double wshare_av = 0.0
    cdef double wshare_nt2
    cdef double wshare_vi2
    cdef double wshare_tf2
    cdef double wshare_av2 = 0.0
    cdef double total_cash
    cdef double total_cash2

    wshare_nt, wshare_vi, wshare_tf, wshare_av, total_cash = Wealth_Shares(pop, price)

    if total_cash > MoneySupply:
        # We need to normalise funds' cash as current amount exceeds supply
        norm_factor = MoneySupply / total_cash
        for ind in pop:
            if ind.type_as_int != 'bh' or ind.type_as_int != 'ir':
                ind.cash = ind.cash * norm_factor
                ind.loan = ind.loan * norm_factor

        # Double check our normalisation
        wshare_nt2, wshare_vi2, wshare_tf2, wshare_av2, total_cash2 = Wealth_Shares(pop, price)

        if abs(total_cash2 - MoneySupply) > 0.01:
            print(total_cash2, MoneySupply)
            raise RuntimeError('New cash exceeds money supply')

        if wshare_nt - wshare_nt2 > 0.001:
            print(norm_factor)
            print([wshare_nt, wshare_nt2])
            print([wshare_vi, wshare_vi2])
            print([wshare_tf, wshare_tf2])
            raise RuntimeError('WShares NT have changed after normalisation')

        if wshare_vi - wshare_vi2 > 0.01:
            print([wshare_vi, wshare_vi2])
            raise RuntimeError('WShares VI have changed after normalisation')

        if wshare_tf - wshare_tf2 > 0.01:
            print([wshare_tf, wshare_tf2])
            raise RuntimeError('WShares TF have changed after normalisation')

        if wshare_av - wshare_av2 > 0.01:
            print([wshare_av, wshare_av2])
            raise RuntimeError('WShares AV have changed after normalisation')   
    
    
    if total_cash < MoneySupply:
        raise RuntimeError('total cash < money supply')
    
    '''
        # We need to normalise funds' cash as current amount is below supply
        norm_factor = MoneySupply / total_cash
        for ind in pop:
            if ind.type_as_int != 'bh' or ind.type_as_int != 'ir':
                ind.cash = ind.cash * norm_factor

        # Double check our normalisation
        wshare_nt2, wshare_vi2, wshare_tf2, wshare_av2, total_cash2 = Wealth_Shares(pop, price)

        if abs(total_cash2 - MoneySupply) > 0.01:
            print(total_cash2, MoneySupply)
            raise RuntimeError('New cash exceeds money supply')

        if wshare_nt - wshare_nt2 > 0.01:
            print(norm_factor)
            print([wshare_nt, wshare_nt2])
            raise RuntimeError('WShares NT have changed after normalisation')

        if wshare_vi - wshare_vi2 > 0.01:
            print([wshare_vi, wshare_vi2])
            raise RuntimeError('WShares VI have changed after normalisation')

        if wshare_tf - wshare_tf2 > 0.01:
            print([wshare_tf, wshare_tf2])
            raise RuntimeError('WShares TF have changed after normalisation')

        if wshare_av - wshare_av2 > 0.01:
            print([wshare_av, wshare_av2])
            raise RuntimeError('WShares AV have changed after normalisation')
    '''
    return pop, total_cash2
