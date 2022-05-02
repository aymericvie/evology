#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
cimport cythonized
import numpy as np
import time 
from libc.math cimport isnan, sqrt, exp
from parameters import SHIELD_DURATION, ShieldResults
cdef float NAN
NAN = float("nan")

cpdef double sigmoid(double x):
    return 1.0 / exp(-2.68735918 * (x - 0.43503506))

cpdef Emp_Investment(list pop):
    cdef cythonized.Individual ind
    cdef int i
    cdef double ind_wealth
    cdef double first_wealth

    cdef double[:] randoms = np.random.random(size=len(pop))
    cdef double[:] gumbel_draws_positive = np.random.gumbel(3.89050923, 2.08605884, size=len(pop))
    cdef double[:] gumbel_draws_negative = np.random.gumbel(3.55311431, 2.13949923, size=len(pop))

    for i, ind in enumerate(pop):

        if ind.age >= 63:
            ind_wealth = ind.wealth
            first_wealth = ind.last_wealth
            if randoms[i] <= sigmoid((ind_wealth / first_wealth) - 1.): # negative side
                ind.cash += (- gumbel_draws_negative[i] / (6300)) * ind_wealth
            else:
                ind.cash += (gumbel_draws_positive[i] / (6300)) * ind_wealth
    return pop

'''
        
        # Calculate quarterly return
        if len(ind.wealth_series) == 63:
            ind_wealth = ind.wealth
            quarterly_return = (ind_wealth / ind.wealth_series[0]) - 1.

            # Draw the sign of the investment flow
            if randoms[i] <= sigmoid(quarterly_return):
                # Draw the value of the investment flow from Gumbel distributions (negative side)
                ind.investment_ratio = - np.random.gumbel(3.89050923, 2.08605884) 
            else: #positive side
                ind.investment_ratio = np.random.gumbel(3.55311431, 2.13949923) 

            # Apply investment flows converted to daily amounts and ratios instead of percentages
            flow = (ind.investment_ratio / (63 * 100)) * ind_wealth
            ind.investor_flow = flow
            ind.cash += ind.investor_flow

            #ind.investment_series.append(ind.investor_flow)
            #if len(ind.investment_series) > 63:
            #    del ind.investment_series[0]
        
        else:
            ind.investor_flow = NAN


'''

'''
cdef double Barr = max(SHIELD_DURATION, ShieldResults) 

cdef double mean(double[:] x) nogil:
    cdef int N = len(x)
    cdef double out = 0.0
    cdef int i = 0
    for i in range(N):
        out += x[i]
    return out / N

cdef double std(double[:] x) nogil:
    cdef int N = len(x)
    cdef double _mean = mean(x)
    cdef double out = 0.0
    cdef int i = 0
    for i in range(N):
        out += (x[i] - _mean) ** 2
    return sqrt(out / N)

cdef double pearson(double[:] x, double[:] y) nogil:
    cdef int N = len(x)
    cdef double mx = mean(x)
    cdef double my = mean(y)
    cdef double num = 0.0
    cdef double denum1 = 0.0
    cdef double denum2 = 0.0
    cdef double result
    cdef double P

    for i in range(N):
        num += (x[i] - mx) * (y[i] - my)
        denum1 += (x[i] - mx) ** 2
        denum2 += (y[i] - my) ** 2

    result = num / sqrt(denum1 * denum2)

    if result < -1.1 or result > 1.1:
        raise ValueError('Pearson correlation out of bounds.')

    return result

#cpdef Profit_Investment(list pop, double ReinvestmentRate, double[:,:] returns_tracker, int InvestmentHorizon, double TestThreshold, int generation):
cpdef Profit_Investment(list pop, double ReinvestmentRate, int InvestmentHorizon, int generation):
    pop = Returns_Investment(pop, ReinvestmentRate)
    #pop, AvgT, PropSignif, HighestT, AvgAbsT = ProfitSignificance(returns_tracker, generation, InvestmentHorizon, pop, TestThreshold)
    AvgT, PropSignif, HighestT, AvgAbsT = 0,0,0,0
    return pop, AvgT, PropSignif, HighestT, AvgAbsT


cpdef ProfitSignificance(double[:,:] returns_tracker, int generation, int InvestmentHorizon, list pop, double TestThreshold):
    # Define results variables
    cdef cythonized.Individual ind
    cdef cythonized.Individual ind2
    cdef double[:,:] ReturnData
    cdef list T_values = [0] * len(pop)
    cdef list MeanReturns = [0] * len(pop)
    cdef list StdReturns = [0] * len(pop)
    cdef int H = InvestmentHorizon
    cdef int i = 0
    cdef int j = 0
    cdef int NumSignif = 0
    cdef double PropSignif 
    cdef int CountTest = 0
    cdef double T
    cdef double fit
    cdef double SumT = 0.0

    #startTime = time.time()
    ReturnData = returns_tracker[generation-InvestmentHorizon:generation,:]

    # Compute mean and std of returns 
    for i, ind in enumerate(pop):
        DataSlice = ReturnData[:,i]
        #ind = compute_sharpe(ind, DataSlice)
        MeanReturns[i] = mean(DataSlice)
        StdReturns[i] = std(DataSlice)
    #print(time.time() - startTime)

    # Compute and record T statistic values
    #startTime = time.time()
    for i, ind in enumerate(pop):
        DataSlice = ReturnData[:,i]
        for j, ind2 in enumerate(pop):
            if j != i:
                DataSlice2 = ReturnData[:,j]
                T = (mean(DataSlice) - mean(DataSlice2)) / (std(DataSlice) + std(DataSlice2) / sqrt(H))
                T_values[i] += T
                CountTest += 1
                SumT += abs(T)
                if abs(T) >= TestThreshold:
                    NumSignif += 1
        ind.tvalue = T_values[i]
    #    # TODO: is there an issue with replacements and nan?
    #print(time.time() - startTime)
    
    # Record key results 
    #startTime = time.time()
    HighestT = max(T_values)
    AvgT = sum(T_values) / len(pop)
    PropSignif = NumSignif / CountTest
    AvgAbsT = SumT / len(pop)
    #print(time.time() - startTime)
    # Absolute sum of T?

    return pop, AvgT, PropSignif, HighestT, AvgAbsT

cpdef Returns_Investment(list pop, double ReinvestmentRate):
    # apply investment
    for ind in pop:
        ind.investor_flow = 0.0
        #fit = float('.'.join(str(ele) for ele in ind.fitness.values))
        fit = ind.DailyReturn
        # fitness depends on profits, and profits are W(t)-W(t-1). We might have a steanrioll issue.
        if isnan(fit) == False:
            ind.investor_flow = fit * (ReinvestmentRate - 1.0)
            ind.cash += ind.investor_flow
        #if isnan(fit) == True:
        #    print(fit)
        #    raise ValueError('NAN investor flow.') 
    return pop
'''
