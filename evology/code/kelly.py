import numpy as np
from data import Barr
import math
from scipy.stats import pearsonr
# from parameters import ShieldResults

def KellyInvestment(pop, InvestmentSupply, InvestmentIntensity, generation, InvestmentHorizon):

    # TODO implemenent effect of InvestmnetHorizon?
    # For Kelly investment, it just smoothes down the probabilities applied. Should not change drastically the results.

    if generation > InvestmentHorizon and InvestmentHorizon > 0:
        total_wealth = 0
        sum_ir = 0
        for ind in pop:
            if ind.wealth != np.nan:
                total_wealth += (ind.wealth ** InvestmentIntensity)
        
        if total_wealth != 0:
            for ind in pop:
                ind.investment_ratio = 0
                if ind.type == 'nt':
                    ind.investment_ratio = (ind.wealth ** InvestmentIntensity) / total_wealth
                if ind.type == 'vi':
                    ind.investment_ratio = (ind.wealth ** InvestmentIntensity) / total_wealth
                if ind.type == 'tf':
                    ind.investment_ratio = (ind.wealth ** InvestmentIntensity) / total_wealth
            
                sum_ir += ind.investment_ratio
                amount = ind.investment_ratio * InvestmentSupply
                ind.investor_flow = amount
                ind.cash += amount
        if round(sum_ir, 3) != 1:
            print(sum_ir)
            for ind in pop:
                print(ind.investment_ratio)
            raise ValueError('Sum of investment ratios is not one.')

    return pop

def compute_sharpe(ind, DataSlice):
    std_value = np.std(DataSlice)
    if std_value != 0.0:
        ind.sharpe = np.mean(DataSlice) / std_value
    else:
        ind.sharpe = np.nan
    return ind


def MeasureSignificance(returns_tracker, generation, InvestmentHorizon, pop, TestThreshold):
    ReturnData = returns_tracker[generation-InvestmentHorizon:generation,:]

    # Define results variables
    num_test = 0
    num_signif_test = 0
    number_deviations = 0
    sum_tvalue_cpr_abs = 0

    # Compute sharpe ratios
    for i, ind in enumerate(pop):
        DataSlice = ReturnData[:,i]
        ind = compute_sharpe(ind, DataSlice)

    # Compare sharpe ratios
    for i, ind in enumerate(pop):
        if math.isnan(ind.sharpe) == False:
            ind.tvalue_cpr = 0
            DataSlice = ReturnData[:,i]
            S = ind.sharpe

            for j, ind2 in enumerate(pop):
                if j != i and math.isnan(ind2.sharpe) == False:
                    DataSlice2 = DataSlice = ReturnData[:,j]
                    S2 = ind2.sharpe
                    P = pearsonr(DataSlice, DataSlice2)[0]
                    if P != 1:
                        SE = np.sqrt((1.0 / InvestmentHorizon) * (2 - 2 * P + 0.5 * (S ** 2 + S2 ** 2 - 2 * S * S2 * (P ** 2))))
                        T = (S - S2) / SE

                        if SE == 0.0:
                            print([S, S2, 1.0 * InvestmentHorizon, P])
                            print(np.sqrt((1.0 / InvestmentHorizon) * (2 - 2 * P + 0.5 * (S ** 2 + S2 ** 2 - 2 * S * S2 * (P ** 2)))))
                            raise ValueError('Null SE for Sharpe test.')

                        ind.tvalue_cpr += T
                        num_test += 1
                        bounds = [(S - S2) - TestThreshold * SE, (S - S2) + TestThreshold * SE]

                        if T > 0:
                            if bounds[0] > 0:
                                num_signif_test += 1.0
                                number_deviations += (bounds[0] / SE)
                        if T < 0:
                            if bounds[1] < 0:
                                num_signif_test += 1.0
                                number_deviations += abs(bounds[1] / SE)

    # Record some results
    for ind in pop:
        sum_tvalue_cpr_abs += abs(ind.tvalue_cpr)

    if num_test != 0:
        AvgValSignif = sum_tvalue_cpr_abs / num_test
        PerSignif = 100 * num_signif_test / num_test
    else:
        AvgValSignif = 0
        PerSignif = 0
    NumDev = number_deviations / len(pop)

    return pop, AvgValSignif, PerSignif, NumDev
    

