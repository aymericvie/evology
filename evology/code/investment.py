from scipy.special import stdtrit
import numpy as np
import math
from parameters import INTEREST_RATE, SHIELD_DURATION, ShieldResults
Barr = max(SHIELD_DURATION, ShieldResults) 

def WealthTracking(wealth_tracker, pop, generation):
    
    

    if generation >= Barr:
    # print("Wealth tracking first")
    # print(wealth_tracker[generation,:])

        # for ind in pop:
            # print([ind.age, ind.wealth])

        for i, ind in enumerate(pop):
        # Record the wealth of the fund
            if ind.age > 0:
                wealth_tracker[generation,i] = ind.wealth 
                # print(ind.wealth)
            else: 
                wealth_tracker[generation, i] = np.nan # to mark the replacement in the data
                # print('np.nan')
        # print("Wealth tracker after")
        
    return wealth_tracker

def ReturnTracking(wealth_tracker, returns_tracker, pop, generation):
    # print("Generation " + str(generation))
    # print("Wealth")
    # print(wealth_tracker[generation,:])
    if generation >= Barr + 1: # Otherwise there won't be a previous_wealth.
        for i in range(len(pop)):
            previous_wealth = wealth_tracker[generation - 1, i]
            if previous_wealth != 0 or previous_wealth != np.nan:
                returns_tracker[generation, i] = (wealth_tracker[generation, i] - previous_wealth) / previous_wealth
            else:
                returns_tracker[generation, i] = np.nan
        # print("Returns")
        # print(returns_tracker[generation,:])
    return returns_tracker

def Investment(returns_tracker, generation, InvestmentHorizon, pop, InvestmentSupply):

    if generation > Barr + InvestmentHorizon:
        # print("investment")

        # Control Investment Horizon.
        if InvestmentHorizon <= 1:
            raise ValueError('Investment horizon <= 1. Impossible to compute Sharpe ratios without standard errors.')

        ReturnData = returns_tracker[generation-InvestmentHorizon:generation,:]
        # print("Return data")
        # print(ReturnData)

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
            # print("Data slice")
            # print(DataSlice)
            MeanReturns = np.mean(DataSlice)
            StdReturns = np.std(DataSlice)
            
            if StdReturns != 0:
                Sharpe = MeanReturns / StdReturns
            else:
                Sharpe = np.nan

            # print([MeanReturns, StdReturns, Sharpe])
            # print([Sharpe == np.nan, math.isnan(Sharpe)])
            if math.isnan(Sharpe) == False:
                SESharpe = np.sqrt(1 + 0.5 * Sharpe ** 2) / np.sqrt(InvestmentHorizon)
                TValue = (Sharpe - INTEREST_RATE) / SESharpe
                TestValues[i] = TValue
            else:
                TestValues[i] = 0

        # print('Test values')
        # print(TestValues)

        # Decide investment ratios and apply the investment.
        SumTValues = sum(TestValues)
        countSignif = 0
        # print("Inv ratio")
        for i, ind in enumerate(pop):
            # What if TestValues[i] = np.nan?
            if SumTValues != 0:
                ind.investment_ratio = (TestValues[i] / SumTValues) 
            else:
                ind.investment_ratio = 1/len(pop)
            # print(ind.investment_ratio)
            ind.investor_flow = ind.investment_ratio * InvestmentSupply
            ind.cash += ind.investor_flow
            if TestValues[i] > TestThreshold:
                countSignif += 1
        propSignif = 100 * (countSignif / len(pop))

        return pop, propSignif
    else:
        return pop, 0


