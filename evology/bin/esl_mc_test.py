import esl
from esl.economics.markets.walras import (
    excess_demand_model,
    differentiable_order_message,
)
from esl.law import property
from esl.simulation import identity
from esl.economics.markets import quote
from esl.economics import price
from esl.economics import currencies
import numpy as np

i = identity([0, 1])
p = property(i)


def solve(my_excess_demand_functions: list):

    i = identity([0, 1])
    p = property(i)
    initial_price = price(10000, currencies.USD)
    initial_quote = quote(initial_price)
    model = excess_demand_model({p: initial_quote})  # for one asset

    market_agent = esl.simulation.identity([0])
    excess_demand_functions = []

    class OrderWrapper(differentiable_order_message):
        def __init__(self, function, sender, recipient, sent, received):
            super().__init__(sender, recipient, sent, received)
            # TODO (Maarten): this should be exposed through base class
            self.sender = sender
            self.function = function

        def excess_demand(self, quotes) -> dict:
            """
            :param quotes: A dict with property_identifier keys and pairs (quote, variable)
            :return:
            """
            ed = {
                k: self.function(k, float(v[0]) * v[1])
                for i, (k, v) in enumerate(quotes.items())
            }
            return ed

    for i, edf in enumerate(my_excess_demand_functions):
        order = OrderWrapper(edf, esl.simulation.identity([i + 1]), market_agent, 0, 0)
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


def func1(asset_key, price):  # value investor
    return ((50_000_000 + 500_000 * price) / price) * (
        np.tanh(np.log2(10_000) - np.log2(price)) + 0.5
    ) - 500_000


def func2(asset_key, price):  # noise trader
    return ((50_000_000 + 500_000 * price) / price) * (
        np.tanh(np.log2(10_000) - np.log2(price)) + 0.5
    ) - 500_000


def func3(asset_key, price):  # trend follower
    return ((50_000_000 + 500_000 * price) / price) * (np.tanh(0) + 0.5) - 500_000


functions = [func1, func2, func3]
new_price = solve(functions)
print(new_price)
print(float(new_price[0]))
print(func1(i, float(new_price[0])))
print(func2(i, float(new_price[0])))
print(func3(i, float(new_price[0])))
