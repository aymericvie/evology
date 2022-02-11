import numpy as np
from data import Barr
from parameters import ShieldResults

def KellyInvestment(pop, InvestmentSupply, InvestmentHorizon, results, generation):


    count_nt, count_vi, count_tf = 0,0,0

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
    if InvestmentHorizon > 0 and generation >  InvestmentHorizon + ShieldResults:
        WealthDataNT = results[generation-InvestmentHorizon-Barr:generation-Barr, 15]
        WealthDataVI = results[generation-InvestmentHorizon-Barr:generation-Barr, 16]
        WealthDataTF = results[generation-InvestmentHorizon-Barr:generation-Barr, 17]

        sum_wealth_nt = np.mean(WealthDataNT)
        sum_wealth_vi = np.mean(WealthDataVI)
        sum_wealth_tf = np.mean(WealthDataTF)
        total_wealth = sum_wealth_nt + sum_wealth_vi + sum_wealth_tf

        ratio_nt = sum_wealth_nt / total_wealth
        ratio_vi = sum_wealth_vi / total_wealth
        ratio_tf = sum_wealth_tf / total_wealth
        total_wealth = sum_wealth_nt + sum_wealth_vi + sum_wealth_tf

        if round(ratio_nt + ratio_vi + ratio_tf, 3) != 1.0:
            raise ValueError('Sum of wealth shares is not one for Kelly investment.')

        for ind in pop:
            if ind.type == 'nt':
                count_nt += 1
            if ind.type == 'vi':
                count_vi += 1
            if ind.type == 'tf':
                count_tf += 1
        
        for ind in pop:
            if ind.type == 'nt':
                ind.investment_ratio = ratio_nt / count_nt
            if ind.type == 'vi':
                ind.investment_ratio = ratio_vi / count_vi
            if ind.type == 'tf':
                ind.investment_ratio = ratio_tf / count_tf
            
            amount = ind.investment_ratio * InvestmentSupply
            ind.investor_flow = amount
            ind.cash += amount

    return pop
