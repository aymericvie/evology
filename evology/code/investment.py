from scipy.special import stdtrit
import numpy as np

def Invest(pop, generation, wealth_tracker, returns_tracker, InvestmentHorizon, ReinvestmentRate):

    # Update our returns history based on latest wealth data
    returns_tracker = ReturnsHistory(pop, generation, wealth_tracker, returns_tracker)

    # Decide investment ratios
    SharpeList, InvestmentRatios = ComputeInvestmentRatios(pop, generation, returns_tracker, InvestmentHorizon, ReinvestmentRate)

    # Apply investment
    pop = ApplyInvestment(pop, InvestmentRatios)

    return pop

def ReturnsHistory(pop, generation, wealth_tracker, returns_tracker):
    if generation > 1:
        for i in range(len(pop)):
            WealthDay2 = wealth_tracker[generation-2, i]
            if WealthDay2 != 0:
                returns_tracker[generation, i] = (wealth_tracker[generation-1, i] - WealthDay2) / WealthDay2
            else:
                returns_tracker[generation, i] = np.nan
    return returns_tracker

def ComputeInvestmentRatios(pop, generation, returns_tracker, InvestmentHorizon, ReinvestmentRate):
    SharpeList = [0] * len(pop)


    if generation > InvestmentHorizon:
        InvestmentRatios = np.empty((1, len(pop),)) * np.nan
        # If we don't have enough data to fit the InvestmentHorizon, the investors are abstaining.
        ReturnData = returns_tracker[generation-InvestmentHorizon:generation,:]
        if len(ReturnData) != InvestmentHorizon:
            raise ValueError('Return data length did not match Investment horizon. ' + str(InvestmentHorizon) + '/' + str(len(ReturnData)))

        TestThreshold = stdtrit(InvestmentHorizon, 0.95)
        TestValues1 = [0] * len(pop)

        for i in range(len(pop)):
            DataSlice = ReturnData[:,i]
            MeanReturns = np.nanmean(DataSlice)
            StdReturns = np.nanstd(DataSlice)
            if StdReturns != 0:
                Sharpe = MeanReturns / StdReturns
            else:
                Sharpe = np.nan

            SESharpe = np.sqrt(1 + 0.5 * Sharpe ** 2) / np.sqrt(InvestmentHorizon)
            SharpeList[i] = Sharpe
            TValue = Sharpe / SESharpe
            TestValues1[i] = TValue

            if TValue < TestThreshold:
                # The Sharpe ratio is not significantly different from 0, we are not investing.
                InvestmentRatios[0,i] = 0
            elif TValue >= TestThreshold:
                # The Sharpe ratio is significantly different from 0. 
                # First, determine the sign.
                if Sharpe > 0:
                    InvestmentRatios[0,i] = ReinvestmentRate - 1
                elif Sharpe < 0:
                    InvestmentRatios[0,i] = - ReinvestmentRate - 1
    else:
        InvestmentRatios = np.zeros((1, len(pop)))


    return SharpeList, InvestmentRatios


def ApplyInvestment(pop, InvestmentRatios):
    for i, ind in enumerate(pop):
        # print(type(InvestmentRatios))
        # print(type(InvestmentRatios[i]))
        # print(type(InvestmentRatios[0,i]))
        # print(InvestmentRatios[0,i])
        ind.investment_ratio = InvestmentRatios[0,i]
    return pop