# !pip install eslpy
import esl
print(esl.version())

from esl.economics.markets.walras import excess_demand_model
from esl.economics import price, USD
initial_price = price(100, USD)

def dmd1(x):
    return -5/x + 5
def dmd2 (x):
    return -5/x + 5
def dmd3 (x):
    return -5/x + 5

excess_demand_functions = [dmd1, dmd2, dmd3]

def clear_market(initial_prices, excess_demand_functions):
    model = excess_demand_model(initial_prices)
    model.excess_demand_functions = excess_demand_functions

    # change other settings for the solver, such as circuit breaker

    model.circuit_breaker = (0.5, 2.0)
    return model.compute_clearing_quotes()

clear_market(initial_price, excess_demand_functions)





##

!pip install deap