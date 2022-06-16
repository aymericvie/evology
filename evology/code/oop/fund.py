from types import FunctionType
import numpy as np
from math import isnan

class Fund:
    def __init__(self, cash, asset):
        self.cash = cash
        self.asset = asset
        self.loan = 0.
        self.margin = 0.
        self.wealth = 0
        self.trading_signal = 0.
        self.type = str
        self.excess_demand = FunctionType
        self.leverage = 1.
        self.signal_scale = 1.
        self.demand = 0.
        self.previous_wealth = 0.
        self.annual_return = 0.
        self.daily_return = 0.
        self.monthly_return = 0.
        self.excess_annual_return = 0.
        self.excess_monthly_return = 0.
        self.wealth_history_year = []
        self.wealth_history_month = []
        self.net_flow = 0.

    def count_wealth(self, price):
        self.wealth = self.cash + self.asset * price - self.loan + self.margin
        if self.wealth < 0:
            raise RuntimeError('Insolvent agent', self.type, self.wealth, self.cash, self.asset, self.loan, self.margin, self.wealth + self.margin, self.net_flow)
        return self.wealth
    
    def compute_demand(self, price):
        self.demand = self.excess_demand(price)

    def execute_demand(self, price):
        # TODO: possible issue if we have some mismatch?
        self.asset += self.demand
        self.cash -= self.demand * price 

    def clear_debt(self):
        if self.loan > 0 and self.cash > 0:
            self.cash -= self.loan 
            self.loan = 0
        if self.loan < 0:
            self.cash += self.loan
            self.loan = 0

    def earnings(self, dividend, interest_rate_daily):
        self.cash += interest_rate_daily * self.cash 
        self.cash += dividend * self.asset

    def update_margin(self, price):
        self.cash += self.margin 
        self.margin = 0.
        if self.asset < 0:
            self.margin = abs(self.asset) * price
            self.cash -= abs(self.asset) * price
        if self.margin < 0:
            raise RuntimeError('Negative margin', self.type, self.margin)

    def compute_profit(self):
        # Compute daily return
        if self.previous_wealth != 0:
            self.daily_return = ((self.wealth - self.net_flow) / self.previous_wealth) - 1. 
        else:
            self.daily_return = np.nan

        # Compute annual return
        if len(self.wealth_history_year) == 252: 

            # Compute annualised geometric mean of daily returns
            self.annual_return = (1. + ((np.product(self.wealth_history_year)) ** (1./252.) - 1.)) ** 252. - 1.

            self.monthly_return = (1. + ((np.product(self.wealth_history_month)) ** (1./21.) - 1.)) ** 21. - 1.


        else:
            self.annual_return = np.nan
        
        # Update previous wealth to current wealth
        self.previous_wealth = self.wealth 

    def update_wealth_history(self):
        # Make a history of daily returns 

        if isnan(self.daily_return) == False:
            entry = float(self.daily_return) + 1.
            self.wealth_history_year.append(entry)
            self.wealth_history_month.append(entry)

        if len(self.wealth_history_year) > 252:
            # Erase observations older than a year 
            del self.wealth_history_year[0]

        if len(self.wealth_history_month) > 21:
            # Erase observations older than a month 
            del self.wealth_history_month[0]


    def liquidate_insolvent(self):
        if self.wealth < 0:
            raise RuntimeError('Insolvent agent', self.wealth, self.type, self.asset, self.cash, self.margin)
    def get_assets(self):
        return self.asset

    def get_annual_return(self):
        return self.annual_return

    def get_monthly_return(self):
        return self.monthly_return


