from math import isnan

class Investor:

    def __init__(self, investment_bool):
        self.active = investment_bool
        
    def investment_flows(self, pop):
        # net capital flows based on Ka and Ho, 2019
        if self.active == True:
            for fund in pop.agents:
                if isnan(fund.excess_annual_return) == False and isnan(fund.annual_return) == False:
                    invested_amount = ((-0.0012 + 0.1089 * fund.excess_annual_return) / 21.) * fund.wealth
                    fund.net_flow = invested_amount
                    fund.cash += fund.net_flow
                    #print(fund.type, fund.wealth, fund.net_flow, fund.cash)
                    #print("Invested" + str(invested_amount) + " " + str(invested_amount / fund.wealth) + " in " + str(fund.type) + " " + str(fund.annual_return) + str(fund.excess_annual_return))