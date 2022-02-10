#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True

cimport cythonized
import numpy as np
from libc.math cimport isnan, sqrt
from parameters import INTEREST_RATE, SHIELD_DURATION, ShieldResults, ShieldInvestment
cdef float NAN
NAN = float("nan")

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

cdef compute_sharpe(cythonized.Individual ind, double[:] DataSlice):
    cdef double std_value = std(DataSlice)
    if std_value != 0.0:
        ind.sharpe = mean(DataSlice) / std_value
    else:
        ind.sharpe = NAN
    return ind

cdef compare_sharpe(list pop, double[:,:] ReturnData, double InvestmentHorizon, double TestThreshold, double InvestmentIntensity):
    
    cdef cythonized.Individual ind
    cdef cythonized.Individual ind2
    cdef double T
    cdef double P 
    cdef double S 
    cdef double S2
    cdef double term
    cdef double total_tvalue_cpr = 0.0
    cdef double sum_inv_ratio = 0.0
    cdef double countSignif = 0.0
    cdef double sum_tvalue_cpr_abs = 0.0
    cdef double total_tvalue_cpr_neg = 0.0
    cdef double num_test = 0.0
    cdef double num_signif_test = 0.0
    cdef double SE 
    cdef list bounds
    cdef double number_deviations = 0.0

    #print("---")
    #print(TestThreshold)

    for i, ind in enumerate(pop):
        if isnan(ind.sharpe) == False:
            ind.tvalue_cpr = 0.0
            DataSlice = ReturnData[:,i]
            S = ind.sharpe
            ''' Then we compare to other funds with non-NAN Sharpes'''
            for j, ind2 in enumerate(pop):
                if j != i and isnan(ind2.sharpe) == False:
                    ''' We have selected another fund with defined Sharpe'''
                    DataSlice2 = ReturnData[:,j]
                    S = mean(DataSlice)
                    S2 = mean(DataSlice2)
                    if isnan(S2) == False:
                        # T test for similar variances (difference in std betw 0.5 and 2)
                        # T = (S - S2) / ((sqrt( ((InvestmentHorizon - 1.0) * (std(DataSlice) ** 2) + (InvestmentHorizon - 1.0) * (std(DataSlice2) ** 2)))/(2.0 * InvestmentHorizon - 2)) * sqrt (2.0 / InvestmentHorizon))                    
                        # Simple T Test
                        # T = (S - S2) / sqrt((2/InvestmentHorizon) * ((std(DataSlice) ** 2 + std(DataSlice2) ** 2) / 2))
                        
                        # Welch test (T test for unequal variances, difference in std > 2)
                        # T = (S - S2) / (sqrt((std(DataSlice) ** 2 + std(DataSlice2) ** 2) / (InvestmentHorizon)))
                        #if abs(T) > abs(TestThreshold):
                        #    num_signif_test += 1.0

                        # JKM test
                        P = pearson(DataSlice, DataSlice2)
                        SE = sqrt((1.0 / InvestmentHorizon) * (2 - 2 * P + 0.5 * (ind.sharpe ** 2 + ind2.sharpe ** 2 - 2 * ind.sharpe * ind2.sharpe * (P ** 2))))
                        T = (ind.sharpe - ind2.sharpe) / SE

                        ind.tvalue_cpr += T
                        num_test += 1.0
                        #print(T)
                        bounds = [(ind.sharpe - ind2.sharpe) - TestThreshold * SE, (ind.sharpe - ind2.sharpe) + TestThreshold * SE]

                        if T > 0:
                            if bounds[0] > 0:
                                num_signif_test += 1.0
                                number_deviations += (bounds[0] / SE)
                        if T < 0:
                            if bounds[1] < 0:
                                num_signif_test += 1.0
                                number_deviations += abs(bounds[1] / SE)


    for ind in pop:
        if isnan(ind.tvalue_cpr) == False:
            sum_tvalue_cpr_abs += abs(ind.tvalue_cpr)
            if ind.tvalue_cpr > 0:
                # Apply the exponent Investment Intensity
                ind.tvalue_cpr = ind.tvalue_cpr ** InvestmentIntensity
                total_tvalue_cpr += ind.tvalue_cpr
            if ind.tvalue_cpr < 0:
                # Apply the exponent Investment Intensity, keeping the negative sign of T value.
                ind.tvalue_cpr = - abs(abs(ind.tvalue_cpr) ** InvestmentIntensity)
                total_tvalue_cpr_neg += ind.tvalue_cpr

    if isnan(total_tvalue_cpr) == True:
        raise ValueError('Undefined total_tvalue_cpr')

    for i, ind in enumerate(pop):
        ind.investment_ratio = 0.0
        if isnan(ind.tvalue_cpr) == False and isnan(ind.sharpe) == False:
            if ind.tvalue_cpr > 0:
                ind.investment_ratio = ind.tvalue_cpr / total_tvalue_cpr
            if ind.tvalue_cpr < 0:
                ind.investment_ratio = - (abs(ind.tvalue_cpr / total_tvalue_cpr_neg))
                if ind.investment_ratio > 0:
                    raise ValueError('Investment ratio positive despite negative T statistic value.')

        # print([round(ind.sharpe,2), round(ind.investment_ratio,2), round(ind.tvalue_cpr,2), round(total_tvalue_cpr,2)])

    if round(sum_inv_ratio,3) != 0.0:
        print(sum_inv_ratio)
        raise ValueError('Sum of investment ratios is not null.')

    return pop, (sum_tvalue_cpr_abs / num_test), (100 * num_signif_test / num_test), number_deviations / len(pop)

cdef DistributionInvestment(list pop, double InvestmentSupply):
    cdef cythonized.Individual ind 

    for ind in pop:
        amount = ind.investment_ratio * InvestmentSupply
        ind.investor_flow = amount
        ind.cash += amount
    return pop


def InvestmentProcedure(pop, generation, returns_tracker, InvestmentHorizon, InvestmentSupply, TestThreshold, InvestmentIntensity):
    if InvestmentHorizon > 0 and generation > Barr + InvestmentHorizon + ShieldInvestment and InvestmentHorizon != 1:
        pop, AvgValSignif, PerSignif, NumDev = Investment(returns_tracker, generation, InvestmentHorizon, pop, InvestmentSupply, TestThreshold, InvestmentIntensity)
    else:
        AvgValSignif, PerSignif, NumDev = 0, 0, 0
    return pop, AvgValSignif, PerSignif, NumDev



cdef Investment(double[:, :] returns_tracker, int generation, int InvestmentHorizon, list pop, double InvestmentSupply, double TestThreshold, double InvestmentIntensity):
    cdef cythonized.Individual ind
    cdef double[:, :] ReturnData
    cdef int i = 0

    ReturnData = returns_tracker[generation-InvestmentHorizon:generation,:]
    # Control data size.
    if len(ReturnData) != InvestmentHorizon:
        print(len(ReturnData))
        print(len(InvestmentHorizon))
        raise ValueError('Length of Returndata did not match Investmtent Horizon.')

    for i, ind in enumerate(pop):
        ''' Compute the Sharpe ratio of the fund '''
        DataSlice = ReturnData[:,i]
        ind = compute_sharpe(ind, DataSlice)
        
    pop, AvgVal, PerSignif, NumDev = compare_sharpe(pop, ReturnData, InvestmentHorizon, TestThreshold, InvestmentIntensity)

    pop = DistributionInvestment(pop, InvestmentSupply)

    return pop, AvgVal, PerSignif, NumDev


