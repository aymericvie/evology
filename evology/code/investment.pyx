#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
from scipy.special import stdtrit
cimport cythonized
import numpy as np
from libc.math cimport isnan, sqrt
from parameters import INTEREST_RATE, SHIELD_DURATION, ShieldResults, ShieldInvestment

cdef double Barr = max(SHIELD_DURATION, ShieldResults) 

cdef double mean(double[:] x) nogil:
    cdef int N = len(x)
    cdef double out = 0.0
    for i in range(N):
        out += x[i]
    return out / N


cdef double std(double[:] x) nogil:
    cdef int N = len(x)
    cdef double _mean = mean(x)
    cdef double out = 0.0
    for i in range(N):
        out += (x[i] - _mean) ** 2
    return sqrt(out / N)


def InvestmentProcedure(pop, generation, returns_tracker, InvestmentHorizon, InvestmentSupply):
    if InvestmentHorizon > 0:
        pop, propSignif = Investment(returns_tracker, generation, InvestmentHorizon, pop, InvestmentSupply)
    else:
        propSignif = 0
    return returns_tracker, pop, propSignif



cdef Investment(double[:, :] returns_tracker, int generation, int InvestmentHorizon, list pop, double InvestmentSupply):

    cdef double TestThreshold
    cdef list TestValues
    cdef double MeanReturns 
    cdef double StdReturns
    cdef double Sharpe
    cdef double SESharpe
    cdef double TValue
    cdef int countSignif
    cdef double SumTValues
    cdef cythonized.Individual ind
    cdef double[:, :] ReturnData
    cdef double[:] DataSlice

    if generation > Barr + InvestmentHorizon + ShieldInvestment:
        # Control Investment Horizon.
        if InvestmentHorizon <= 1:
            raise ValueError('Investment horizon <= 1. Impossible to compute Sharpe ratios without standard errors.')
        ReturnData = returns_tracker[generation-InvestmentHorizon:generation,:]
        # Control data size.
        if len(ReturnData) != InvestmentHorizon:
            print(len(ReturnData))
            print(len(InvestmentHorizon))
            raise ValueError('Length of Returndata did not match Investmtent Horizon.')

        # For each fund, estimate Sharpe ratio and its significance.
        TestThreshold = stdtrit(InvestmentHorizon, 0.95)
        TestValues = [0] * len(pop)

        for i in range(len(pop)):
            DataSlice = ReturnData[:,i]
            MeanReturns = mean(DataSlice)
            StdReturns = std(DataSlice)

            if StdReturns != 0:
                Sharpe = MeanReturns / StdReturns
            else:
                Sharpe = np.nan

            if not isnan(Sharpe):
                SESharpe = sqrt(1 + 0.5 * Sharpe ** 2) / sqrt(InvestmentHorizon)
                # SESharpe = ((1 + 0.5 * Sharpe ** 2) / InvestmentHorizon) ** 1/2
                TValue = (Sharpe - INTEREST_RATE) / SESharpe
                TestValues[i] = TValue
            else:
                TestValues[i] = 0

        # Decide investment ratios and apply the investment.
        SumTValues = sum(TestValues)
        countSignif = 0
        for i, ind in enumerate(pop):
            if SumTValues != 0:
                ind.investment_ratio = (TestValues[i] / SumTValues) 
            else:
                ind.investment_ratio = 1/len(pop)
            ind.investor_flow = ind.investment_ratio * InvestmentSupply
            ind.cash += ind.investor_flow
            if TestValues[i] > TestThreshold:
                countSignif += 1
        propSignif = 100 * (countSignif / len(pop))

        return pop, propSignif
    else:
        return pop, 0


