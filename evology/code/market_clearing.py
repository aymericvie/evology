import warnings
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
import scipy
import numpy as np
import balance_sheet_cython as bsc
import math


def solve(my_excess_demand_functions: list, current_price):

    i = identity([0, 1])
    p = property(i)
    market_agent = esl.simulation.identity([0])

    initial_price = price(int(current_price * 100), currencies.USD)
    initial_quote = quote(initial_price)
    model = excess_demand_model({p: initial_quote})  # for one asset
    excess_demand_functions = []

    class OrderWrapper(differentiable_order_message):
        def __init__(self, function, sender, recipient, sent, received):
            super().__init__(sender, recipient, sent, received)
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
    del initial_price
    return prices


def esl_solver(ed_functions, current_price):
    new_price = float(solve(ed_functions, current_price)[0])
    if new_price < 0:
        new_price = 0.01
    return new_price


def scipy_solver(ed_functions, current_price):
    tolerance = 1. #0.1
    new_price = scipy.optimize.root(ed_functions, current_price, method="hybr").x
    if (
        new_price > (1.0 + tolerance) * current_price
        or new_price < (1.0 - tolerance) * current_price
    ):
        # new_price = scipy.optimize.minimize(ed_functions, current_price, bounds=[(current_price * 0.5,current_price*2)]).x
        # new_price = scipy.optimize.brentq(ed_functions, 0.01, current_price * 10)
        if new_price > (1.0 + tolerance) * current_price:
            new_price = (1.0 + tolerance) * current_price
        elif new_price < (1.0 - tolerance) * current_price:
            new_price = (1.0 - tolerance) * current_price
    if new_price < 0:
        new_price = 0.01
    if math.isnan(new_price) == True:
        raise TypeError("NaN price")

    return new_price


"""
def CircuitClearing(ed_functions, current_price):

    ClearingPrice = float(solve(ed_functions, current_price)[0])

    LimitBelow = current_price * 0.5
    LimitUp = current_price * 2

    if ClearingPrice > LimitUp:
        ClearingPrice = LimitUp
    if ClearingPrice < LimitBelow:
        ClearingPrice = LimitBelow
    return ClearingPrice
"""
