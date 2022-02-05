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


cdef double std_cumulative(double[:] x, double _mean) nogil:
    cdef int N = len(x)
    cdef double out = 0.0
    cdef int i = 0
    for i in range(N):
        out += (x[i] - _mean) ** 2
    return out

cdef double pearson(double[:] x, double[:] y) nogil:
    cdef int N = len(x)
    cdef double mx = mean(x)
    cdef double my = mean(y)
    cdef double num = 0.0
    cdef double denum1 = 0.0
    cdef double denum2 = 0.0

    for i in range(N):
        num += (x[i] - mx) * (y[i] - my)
        denum1 += (x[i] - mx) ** 2
        denum2 += (y[i] - my) ** 2
    return num / sqrt(denum1 * denum2)


def InvestmentProcedure(pop, generation, returns_tracker, InvestmentHorizon, InvestmentSupply):

    if InvestmentHorizon > 0 and generation > Barr + InvestmentHorizon + ShieldInvestment:
        pop, propSignif, AvgValSignif = Investment(returns_tracker, generation, InvestmentHorizon, pop, InvestmentSupply)
    else:
        propSignif, AvgValSignif = 0, 0
    return returns_tracker, pop, propSignif, AvgValSignif



cdef Investment(double[:, :] returns_tracker, int generation, int InvestmentHorizon, list pop, double InvestmentSupply):

    cdef double TestThreshold
    cdef list TestValuesAbsolute
    cdef list TestValuesRelative
    cdef double MeanReturns 
    cdef double StdReturns
    cdef double SharpeAbsolute
    cdef double SESharpe
    cdef double TValueAbsolute 
    cdef double TValueRelative
    cdef int countSignifAbsolute
    cdef double SumTValuesAbsolute
    cdef double AbsSumTValuesAbsolute
    cdef double AbsSumTValuesRelative
    cdef cythonized.Individual ind
    cdef int CumLength = 0
    cdef double[:, :] ReturnData
    cdef double[:] DataSlice
    cdef double[:] AvgFundData = np.zeros(len(pop))
    cdef int i = 0
    cdef double AvgReturn
    cdef double AvgStd = 0.0

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
        TestValuesAbsolute = [0] * len(pop)
        TestValuesRelative = [0] * len(pop)
        AbsSumTValuesAbsolute = 0.0
        AbsSumTValuesRelative = 0.0

        # Computing the Sharpe ratio of the average fund

        for i in range(len(pop)):
            AvgFundData[i] = mean(ReturnData[i, :])
            
        #print(AvgFundData)
        #print(type(AvgFundData))
        #print(len(AvgFundData))

        AvgReturn = mean(AvgFundData)

        for i in range(len(pop)):
            AvgStd += std_cumulative(ReturnData[i,:], AvgReturn)
            CumLength += len(ReturnData[i,:])
        # Compute the actual standard deviation
        AvgStd = sqrt(AvgStd / CumLength) 
        # Apply a correction to compare as if we had the same sample size
        #AvgStd = AvgStd * (sqrt(CumLength) / sqrt(InvestmentHorizon))

        if AvgStd != 0 :
            AvgSharpe = (AvgReturn - INTEREST_RATE) / AvgStd 
        else:
            AvgSharpe = np.nan
        print('AvgSharpe, Individual Sharpes')
        print(AvgSharpe)

        for i, ind in enumerate(pop):
            DataSlice = ReturnData[:,i]
            MeanReturns = mean(DataSlice)
            StdReturns = std(DataSlice)

            if StdReturns != 0:
                SharpeAbsolute = MeanReturns / StdReturns
            else:
                SharpeAbsolute = np.nan
            ind.sharpe = SharpeAbsolute
            
            if not isnan(SharpeAbsolute):
                SESharpe = sqrt(1 + 0.5 * SharpeAbsolute ** 2) / sqrt(InvestmentHorizon)
                # SESharpe = ((1 + 0.5 * Sharpe ** 2) / InvestmentHorizon) ** 1/2
                TValueAbsolute = (SharpeAbsolute - INTEREST_RATE) / SESharpe
                TestValuesAbsolute[i] = TValueAbsolute

                PearsonCorrelation = pearson(AvgFundData, DataSlice)
                if PearsonCorrelation < -1 or PearsonCorrelation > 1:
                    print(PearsonCorrelation)
                    raise ValueError('Pearson correlation out of bounds.')
                term = 0.5 * (SharpeAbsolute ** 2 + AvgSharpe ** 2 - 2 * (SharpeAbsolute * AvgSharpe * PearsonCorrelation ** 2))
                TValueRelative  = (SharpeAbsolute - AvgSharpe) / (((InvestmentHorizon ** (-1)) * (2 - 2 * PearsonCorrelation + term))  ** 0.5)
                TestValuesRelative[i] = TValueRelative

                AbsSumTValuesAbsolute += abs(TValueAbsolute)
                AbsSumTValuesRelative += abs(TValueRelative)
            else:
                TestValuesAbsolute[i] = 0
                TestValuesRelative[i] = 0

        print("Test Values Absolute / Relative")

        # Decide investment ratios and apply the investment.
        SumTValuesAbsolute = sum(TestValuesAbsolute)
        SumTValuesRelative = sum(TestValuesRelative)

        countSignifAbsolute = 0
        for i, ind in enumerate(pop):
            if SumTValuesAbsolute != 0:

                #if ind.sharpe >= AvgSharpe:
                #    ind.investment_ratio = TestValuesRelative[i] / SumTValuesRelative
                #else:
                #    ind.investment_ratio = -TestValuesRelative[i] / SumTValuesRelative
                # TODO: Isnt' the program now rewarding the most extremely divergent funds, including not profitable ones?
                # TODO: the above does not sum to 1

                ind.investment_ratio = TestValuesRelative[i] / SumTValuesRelative

                print([ind.sharpe, TestValuesAbsolute[i] / SumTValuesAbsolute, TestValuesRelative[i] / SumTValuesRelative, ind.investment_ratio])
                ind.investment_ratio = (TestValuesAbsolute[i] / SumTValuesAbsolute) 
            else:
                ind.investment_ratio = 1/len(pop)
            ind.investor_flow = ind.investment_ratio * InvestmentSupply
            ind.cash += ind.investor_flow
            if TestValuesAbsolute[i] > TestThreshold:
                countSignifAbsolute += 1
        propSignifAbsolute = 100 * countSignifAbsolute / len(pop)
        AvgValAbsolute = (AbsSumTValuesAbsolute / len(pop)) / TestThreshold

        return pop, propSignifAbsolute, AvgValAbsolute
    else:
        return pop, 0, 0


