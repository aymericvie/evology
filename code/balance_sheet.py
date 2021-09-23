import numpy as np
from parameters import *
from market import *
import inspect


np.seterr(divide = 'ignore') 


def calculate_wealth(pop, price):
    for ind in pop:

        # Attempt to clear debt
        if ind.loan > 0: # If the agent has outstanding debt:
            if ind.cash >= ind.loan: # If the agent has enough cash:
                ind.loan = 0
                ind.cash -= ind.loan
            if ind.cash < ind.loan: # If the agent does not have enough cash:
                ind.loan -= ind.cash
                ind.cash = 0

        # Update margins
        margin_objective = ind.asset_short * price # Margin amount to cover short position at current price.
        if margin_objective > ind.margin: # If our current margin is not enough:
            if ind.cash >= margin_objective - ind.margin: # If we have the cash to adjust:
                # We spend cash to refuel the margin.
                ind.margin += margin_objective - ind.margin
                ind.cash -= margin_objective - ind.margin
            if ind.cash < margin_objective - ind.margin: # If we don't have enough cash to adjust:
                # All available cash goes to the margin, and we have some loan.
                # Loan is a penalty on wealth notably for evaluating solvency.
                ind.margin += ind.cash
                ind.cash = 0
                ind.loan += margin_objective - ind.margin - ind.cash
        if margin_objective < ind.margin: # If our current margin is too high:
            # We get some of the margin back in the form of cash.
            ind.cash += ind.margin - margin_objective
            ind.margin -= ind.margin - margin_objective

        # Update wealth
        ind.wealth = ind.cash + ind.asset_long * price - ind.loan
    return ind

def calculate_ts_edf(pop, extended_price_history):
    for ind in pop:
        if ind.type == "tf":
            # print("tf computes ts")
            # print(extended_price_history[-1])
            # print(extended_price_history[-ind[0]])
            ind.tsv = (np.log2(extended_price_history[-1]) - np.log2(extended_price_history[-ind[0]])) 
            # print(ind.tsv)
            # print(ind.wealth)
            # print(ind.tsv)
            # print(ind.asset)
            # print(LAMBDA_TF)
            # print(STRATEGY_AGGRESSIVENESS_TF)
            # print("previous function")
            # if ind.edf != None:
            #     print(ind.edf(388))
            def func(p):
                return (ind.wealth * LAMBDA_TF / p) * (np.tanh(STRATEGY_AGGRESSIVENESS_TF * ind.tsv) + 0.5) - ind.asset 
            ind.edf = func
            # print("new")
            # print(ind.edf(388))
        elif ind.type == "vi":
            def func(p):
                return (ind.wealth * LAMBDA_VI / p) * (np.tanh(STRATEGY_AGGRESSIVENESS_VI * (np.log2(ind[0]) - np.log2(p))) + 0.5) - ind.asset 
            ind.edf = func
        elif ind.type == "nt":
            ind.process = ind.process + RHO_NT * (MU_NT - ind.process) + GAMMA_NT * random.normalvariate(0,1)
            def func(p):
                return (ind.wealth * LAMBDA_NT / p) * (np.tanh(STRATEGY_AGGRESSIVENESS_NT * (np.log2(ind[0] * ind.process)) -  np.log2(p)) + 0.5) - ind.asset 
            ind.edf = func     
    
     
    return ind

# def calculate_edf(pop):
#     for ind in pop:
#         def func(x):
#             return (ind.wealth * LAMBDA_TF / x) * (np.tanh(STRATEGY_AGGRESSIVENESS_TF * ind.tsv) + 0.5) - ind.asset
#         ind.edf = func
#     return ind

def calculate_edv(pop, price):
    # print("computing edv")
    # print("--------------------------------")
    for ind in pop:
        # print("previous edv & price")
        # print(ind.edv)
        # print(price)
        # ind.edv = ind.edf(price)
        # print("edv 1")
        # print(ind.edv)
        # print(ind.edf(1))
        # How to display edf function in code?
        # print("edf function")
        # lines = inspect.getsource(ind.edf)
        # print(lines)
        # print("contents")
        # print(ind.wealth)
        # print(ind.tsv)
        # print(ind.asset)
        # former_func = ind.edf
        
        if ind.type == "tf":
            
            def func_tf(p):
                return (ind.wealth * LAMBDA_TF / p) * (np.tanh(STRATEGY_AGGRESSIVENESS_TF * ind.tsv) + 0.5) - ind.asset 
            ind.edf = func_tf
            ind.edv = ind.edf(price)
        
        if ind.type == "vi":
            print("--------------------------------")
            print(ind.wealth)
            # print(ind[0])
            print(ind.asset)
            print(np.log2(ind[0]) - np.log2(price))

            ind.edv = ind.edf(price)
            print("former way of edv is")
            print(ind.edv)
            def func_vi(p):
                return (ind.wealth * LAMBDA_VI / p) * (np.tanh(STRATEGY_AGGRESSIVENESS_VI * (np.log2(ind[0]) - np.log2(p))) + 0.5) - ind.asset 
            ind.edf = func_vi
            del func_vi
            ind.edv = ind.edf(price)
            ind.tsv = np.log2(ind[0]) - np.log2(price)
            # print("edv agent is " + str(ind.edv))
            # print("it should be " + str((ind.wealth / price) * (np.tanh(ind.tsv) + 0.5) - ind.asset ))
            
        if ind.type == "nt":
            
            def func_nt(p):
                return (ind.wealth * LAMBDA_NT / p) * (np.tanh(STRATEGY_AGGRESSIVENESS_NT * (np.log2(ind[0] * ind.process)) -  np.log2(p)) + 0.5) - ind.asset 
            ind.edf = func_nt 
            ind.edv = ind.edf(price)
            ind.tsv = np.log2(ind[0] * ind.process) -  np.log2(price)
    return ind

def calculate_total_edv(pop):
    total = 0
    for ind in pop:
        total += ind.edv
    return total

def count_long_assets(pop):
    count = 0
    for ind in pop:
        if ind.asset_long > 0:
            count += ind.asset_long
    return count

def count_negative_assets(pop):
    count = 0
    for ind in pop:
        if ind.asset_short > 0:
            count += - ind.asset_short
    return count

def apply_edv(pop, asset_supply, price):
    num_sell, num_buy = 0, 0
    num_sell_tf, num_sell_vi, num_sell_nt = 0, 0, 0
    num_buy_tf, num_buy_vi, num_buy_nt = 0, 0, 0

    """
    # determine the bank of exchanges
    bank_plus = 0
    bank_minus = 0
    bank_short = 0
    for ind in pop:
        if ind.edv > 0:
            bank_plus += 1
        if ind.edv < 0:
            # If the agent sells from inventory: bank_minus += 1
            # If the agent short sells: bank_short += 1
            """


    for ind in pop:
        if ind.edv > 0:  # the agent wants to buy
            i = 0
            while i < ind.edv:
                if count_positive_assets(pop) < asset_supply: # there are assets to buy
                    if ind.cash >= price: # the agent can afford to buy
                        ind.asset += 1
                        num_buy += 1
                        if ind.type == "tf":
                            num_buy_tf += 1
                        if ind.type == "vi":
                            num_buy_vi += 1
                        if ind.type == "nt":
                            num_buy_nt += 1
                        ind.cash -= price
                i += 1
        if ind.edv < 0:  # the agent wants to sell
            i = 0
            while i < abs(ind.edv):
                if ind.asset >= 1: # the agent can sell from inventory
                    ind.asset -= 1
                    num_sell += 1
                    if ind.type == "tf":
                        num_sell_tf += 1
                    if ind.type == "vi":
                        num_sell_vi += 1
                    if ind.type == "nt":
                        num_sell_nt += 1
                    ind.cash += price
                else: # the agent wants to short sell instead
                    if count_positive_assets(pop) > 0: # there are assets to borrow
                        if count_negative_assets(pop) < 10 * asset_supply: # we don't reach the cap on short position size
                            ind.asset -= 1
                            num_sell += 1
                            if ind.type == "tf":
                                num_sell_tf += 1
                            if ind.type == "vi":
                                num_sell_vi += 1
                            if ind.type == "nt":
                                num_sell_nt += 1
                            ind.margin += price
                i += 1

        # Clear margin if out of short position
        if ind.asset > 0:
            ind.cash += ind.margin
            ind.margin = 0
    return pop, num_buy, num_sell, num_buy_tf, num_buy_vi, num_buy_nt, num_sell_tf, num_sell_vi, num_sell_nt

def update_margin(pop, price):
    for ind in pop:
        if ind.asset < 0:
            ind.cash += ind.margin
            ind.margin = abs(ind.asset) * price
            ind.cash -= ind.margin
            if ind.cash < 0:
                # The agent is insolvent and will try to buy back as much as possible
                # ind.edv = abs(ind.asset)
                ind.cash += ind.margin
                ind.margin = 0
                ind.loan += float('inf')
    return ind

def wealth_earnings(pop, dividend, price):
    dividend, random_dividend = draw_dividend(dividend)
    for ind in pop:
        former_wealth = ind.wealth
        div_asset = ind.asset * dividend # Determine gain from dividends
        interest_cash = ind.cash * INTEREST_RATE # Determine gain from interest
        ind.cash += REINVESTMENT_RATE * (div_asset + interest_cash) # Apply reinvestment
        ind.wealth = ind.cash + ind.asset * price - ind.loan # Compute new wealth
        ind.profit = ind.wealth - former_wealth  # Compute profit as difference of wealth
    return pop, dividend, random_dividend

def pop_report(pop):
    for ind in pop:
        agent_report (ind)

def agent_report(ind):
    if ind.type == "tf":
        print("TF agent - Cash " + str(int(ind.cash)) + ", Asset " + str(ind.asset) + ", Wealth " + str(int(ind.wealth)) + ", TS " + str(ind.tsv) + ", EV " + str(int(ind.edv)) + ", Profit " + str(ind.profit) + ", Fitness " + str(ind.fitness))
    if ind.type == "vi":
        print("VI agent - Cash " + str(int(ind.cash)) + ", Asset " + str(ind.asset) + ", Wealth " + str(int(ind.wealth)) + ", TS " + str(ind.tsv) + ", EV " + str(int(ind.edv)) + ", Profit " + str(ind.profit) + ", Fitness " + str(ind.fitness))
    if ind.type == "nt":
        print("NT agent - Cash " + str(int(ind.cash)) + ", Asset " + str(ind.asset) + ", Wealth " + str(int(ind.wealth)) + ", TS " + str(ind.tsv) + ", EV " + str(int(ind.edv)) + ", Profit " + str(ind.profit) + ", Fitness " + str(ind.fitness))
  
