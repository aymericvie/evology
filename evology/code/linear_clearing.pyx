#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
cimport cythonized
from parameters import LeverageNT, LeverageVI, LeverageTF, SCALE_NT, SCALE_TF, SCALE_VI, liquidation_perc
from libc.math cimport isnan, tanh, fmin, fabs, fmax

cpdef DetermineLiquidation(double spoils, double volume):    
    cdef double ToLiquidate = 0.0
    if spoils > 0:
        ToLiquidate = -fmin(spoils, fmin(liquidation_perc * volume, 10000))
    #elif spoils == 0:
    #    ToLiquidate = 0
    elif spoils < 0:
        ToLiquidate = fmin(fabs(spoils), fmin(liquidation_perc * volume, 10000))
    return ToLiquidate


cpdef linear_solver(list pop, double ToLiquidate, double prev_price):
    cdef double price 
    cdef cythonized.Individual ind
    cdef double a = 0.0
    cdef double b = 0.0
    cdef double l 
    cdef double c
    cdef double d

    b += ToLiquidate

    for ind in pop:
        if ind.type_as_int == 0: #NT
            l = LeverageNT * 1.0
            c = SCALE_NT * 1.0
        if ind.type_as_int == 1: #VI
            l = LeverageVI * 1.0
            c = SCALE_VI * 1.0
        if ind.type_as_int == 2: #TF
            l = LeverageTF * 1.0
            c = SCALE_TF * 1.0
        if ind.type_as_int == 3: #AV
            l = 1.
            c = 1.
        b += ind.asset
        d = (tanh(c * ind.tsv + 0.5)) * ind.wealth
        a += l * d

    price = fmin(fmax(a/b, 0.8*prev_price), 1.2*prev_price)
    price = fmax(price, 0.01)

    
    if isnan(price) == True:
        print(price)
        print(a)
        print(b)
        raise ValueError('Price is nan.')
    '''
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
    '''

    return price

cpdef UpdatePriceHistory(list price_history, double current_price):
    price_history.append(current_price)
    return price_history

