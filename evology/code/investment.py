from scipy.special import stdtrit
import numpy as np
from parameters import INTEREST_RATE

def WealthTracking(wealth_tracker, pop, generation):
    for i, ind in enumerate(pop):
    # Record the wealth of the fund
        if ind.age > 1:
            wealth_tracker[generation,i] = ind.wealth 
        else: 
            wealth_tracker[generation, i] = np.nan # to mark the replacement in the data
    return wealth_tracker

def ReturnTracking(wealth_tracker, returns_tracker, pop, generation):
    if generation >= 3: # Otherwise there won't be a previous_wealth.
        for i in range(len(pop)):
            previous_wealth = wealth_tracker[generation - 1, i]
            if previous_wealth != 0:
                returns_tracker[generation, i] = (wealth_tracker[generation, i] - previous_wealth) / previous_wealth
            else:
                returns_tracker[generation, i] = np.nan
    return returns_tracker

def Investment(returns_tracker, generation, InvestmentHorizon, pop, InvestmentSupply):

    if generation > InvestmentHorizon:

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
            MeanReturns = np.nanmean(DataSlice)
            StdReturns = np.nanstd(DataSlice)
            if StdReturns != 0:
                Sharpe = MeanReturns / StdReturns
            else:
                Sharpe = np.nan

            SESharpe = np.sqrt(1 + 0.5 * Sharpe ** 2) / np.sqrt(InvestmentHorizon)
            TValue = (Sharpe - INTEREST_RATE) / SESharpe
            TestValues[i] = TValue

        # Decide investment ratios and apply the investment.
        SumTValues = sum(TestValues)
        countSignif = 0
        for i, ind in enumerate(pop):
            # What if TestValues[i] = np.nan?
            ind.investment_ratio = (TestValues[i] / SumTValues) 
            ind.cash += ind.investment_ratio * InvestmentSupply
            if TestValues[i] > TestThreshold:
                countSignif += 1
        propSignif = 100 * (countSignif / len(pop))

        return pop, propSignif
    else:
        return pop, 0




# def Invest(pop, generation, wealth_tracker, returns_tracker, InvestmentHorizon, ReinvestmentRate):


#     if generation > 1:

#         print("Generation " + str(generation))

#         print(wealth_tracker[generation,:])

#         print("Early investing")

#         # Update our returns history based on latest wealth data
#         returns_tracker = ReturnsHistory(pop, generation, wealth_tracker, returns_tracker)
        
#         print(returns_tracker[generation, :])

#         print("ReturnsHistory done")

#         # Decide investment ratios
#         SharpeList, InvestmentRatios = ComputeInvestmentRatios(pop, generation, returns_tracker, InvestmentHorizon, ReinvestmentRate)

#         print(InvestmentRatios)
#         print("IRatios done")

#         # Apply investment
#         pop = ApplyInvestment(pop, InvestmentRatios)

#         print("Applied done")

#     return pop

# def ReturnsHistory(pop, generation, wealth_tracker, returns_tracker):
#     for i in range(len(pop)):
#         WealthDay2 = wealth_tracker[generation-2, i]
#         if WealthDay2 != 0:
#             returns_tracker[generation, i] = (wealth_tracker[generation-1, i] - WealthDay2) / WealthDay2
#         else:
#             returns_tracker[generation, i] = np.nan
#     return returns_tracker

# def ComputeInvestmentRatios(pop, generation, returns_tracker, InvestmentHorizon, ReinvestmentRate):
#     SharpeList = [0] * len(pop)


#     if generation > InvestmentHorizon:
#         InvestmentRatios = np.empty((1, len(pop),)) * np.nan
#         # If we don't have enough data to fit the InvestmentHorizon, the investors are abstaining.
#         ReturnData = returns_tracker[generation-InvestmentHorizon:generation,:]
#         if len(ReturnData) != InvestmentHorizon:
#             raise ValueError('Return data length did not match Investment horizon. ' + str(InvestmentHorizon) + '/' + str(len(ReturnData)))

#         TestThreshold = stdtrit(InvestmentHorizon, 0.95)
#         TestValues1 = [0] * len(pop)

#         for i in range(len(pop)):
#             DataSlice = ReturnData[:,i]
#             MeanReturns = np.nanmean(DataSlice)
#             StdReturns = np.nanstd(DataSlice)
#             if StdReturns != 0:
#                 Sharpe = MeanReturns / StdReturns
#             else:
#                 Sharpe = np.nan

#             SESharpe = np.sqrt(1 + 0.5 * Sharpe ** 2) / np.sqrt(InvestmentHorizon)
#             SharpeList[i] = Sharpe
#             TValue = Sharpe / SESharpe
#             TestValues1[i] = TValue

#             if TValue < TestThreshold:
#                 # The Sharpe ratio is not significantly different from 0, we are not investing.
#                 InvestmentRatios[0,i] = 0
#             elif TValue >= TestThreshold:
#                 # The Sharpe ratio is significantly different from 0. 
#                 # First, determine the sign.
#                 if Sharpe > 0:
#                     InvestmentRatios[0,i] = ReinvestmentRate - 1
#                 elif Sharpe < 0:
#                     InvestmentRatios[0,i] = - ReinvestmentRate - 1
#     else:
#         InvestmentRatios = np.zeros((1, len(pop)))


#     return SharpeList, InvestmentRatios


# def ApplyInvestment(pop, InvestmentRatios):
#     for i, ind in enumerate(pop):
#         # print(type(InvestmentRatios))
#         # print(type(InvestmentRatios[i]))
#         # print(type(InvestmentRatios[0,i]))
#         # print(InvestmentRatios[0,i])
#         ind.investment_ratio = InvestmentRatios[0,i]
#     return pop