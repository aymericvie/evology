#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
cimport cythonized
cdef float NAN
NAN = float("nan")


#def UpdateWealthProfitAge(pop, current_price):
#    pop, replace = UpdateWealth(pop, current_price)
#    return pop, replace 


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

