import numpy as np
from data import Barr
# from parameters import ShieldResults

def KellyInvestment(pop, InvestmentSupply, InvestmentIntensity, generation, InvestmentHorizon):

    # TODO implemenent effect of InvestmnetHorizon?
    # For Kelly investment, it just smoothes down the probabilities applied. Should not change drastically the results.


    '''
    # Single period Kelly investing
    sum_wealth_nt, sum_wealth_vi, sum_wealth_tf = 0,0,0

    for ind in pop:
        if ind.wealth != np.nan:
            if ind.type == 'nt':
                sum_wealth_nt += ind.wealth
            if ind.type == 'vi':
                sum_wealth_vi += ind.wealth
            if ind.type == 'tf':
                sum_wealth_tf += ind.wealth
    total_wealth = sum_wealth_nt + sum_wealth_vi + sum_wealth_tf

    ratio_nt = sum_wealth_nt / total_wealth
    ratio_vi = sum_wealth_vi / total_wealth
    ratio_tf = sum_wealth_tf / total_wealth
    '''
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
