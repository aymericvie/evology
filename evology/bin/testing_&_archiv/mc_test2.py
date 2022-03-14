import esl
from esl.law import property
from esl.simulation import identity
from esl.economics import price
from esl.economics import currencies
from esl.economics.markets import quote
from esl.economics.markets.walras import (
    excess_demand_model,
    differentiable_order_message,
)


def solve(excess_demand_functions: list):
    i = identity([0, 1])
    p = property(i)
    initial_price = price(int(1.23 * currencies.USD.denominator), currencies.USD)
    initial_quote = quote(initial_price)
    market_agent = esl.simulation.identity([0])
    excess_demand_functions = []
    model = excess_demand_model({p: initial_quote})

    # for i, ed in enumerate(my_excess_demand_functions):

    #     order = ed(esl.simulation.identity([i+1]), market_agent, 0, 0)

    #     excess_demand_functions.append(order)

    model.excess_demand_functions = excess_demand_functions
    multipliers = model.compute_clearing_quotes()

    prices = []

    for k, v in multipliers.items():

        prices.append(
            price(
                round(float(initial_price) * v * currencies.USD.denominator),
                currencies.USD,
            )
        )

    del model
    return prices


def aggregate_ed1(x):
    return 3 * x - 10


def aggregate_ed2(x):
    return 5 * x - 7


aggregate_ed = [aggregate_ed1, aggregate_ed2]

prices = solve(aggregate_ed)
print(prices)

import esl
from esl.law import property
from esl.simulation import identity
from esl.economics import price
from esl.economics import currencies
from esl.economics.markets import quote
from esl.economics.markets.walras import (
    excess_demand_model,
    differentiable_order_message,
)


def solve(my_excess_demand_functions: list):

    i = identity([0, 1])
    p = property(i)
    initial_price = price(int(1.23 * currencies.USD.denominator), currencies.USD)
    initial_quote = quote(initial_price)
    model = excess_demand_model({p: initial_quote})

    market_agent = esl.simulation.identity([0])
    excess_demand_functions = []
    for i, ed in enumerate(my_excess_demand_functions):
        order = ed(esl.simulation.identity([i + 1]), market_agent, 0, 0)
        excess_demand_functions.append(order)
    model.excess_demand_functions = excess_demand_functions
    multipliers = model.compute_clearing_quotes()
    prices = []
    for k, v in multipliers.items():
        prices.append(
            price(
                round(float(initial_price) * v * currencies.USD.denominator),
                currencies.USD,
            )
        )
    del model
    return prices


def ed1(x):
    return 3 * x - 10


def ed2(x):
    return 5 * x - 7


functions = [ed1, ed2]

solve(functions)
