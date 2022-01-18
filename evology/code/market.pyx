#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True

from balance_sheet import count_long_assets, count_pop_long_assets
import numpy as np

import parameters

cimport cythonized


def draw_dividend(dividend):
    DIVIDEND_GROWTH_RATE = ((1 + parameters.DIVIDEND_GROWTH_RATE_G) ** (1 / parameters.TRADING_DAYS)) - 1
    random_dividend = np.random.normal(0, 1)
    if len(parameters.random_dividend_history) > parameters.DIVIDEND_ATC_TAU:
        random_dividend = (
            1 - parameters.DIVIDEND_AUTOCORRELATION ** 2
        ) * random_dividend + parameters.DIVIDEND_AUTOCORRELATION * parameters.random_dividend_history[
            -1 - parameters.DIVIDEND_ATC_TAU
        ]
    dividend = abs(
        dividend
        + DIVIDEND_GROWTH_RATE * dividend
        + parameters.DIVIDEND_GROWTH_VOLATILITY * dividend * random_dividend
    )
    return dividend, random_dividend


def dividend_series(horizon):
    history, rdiv_history = [], []
    dividend = parameters.INITIAL_DIVIDEND
    history.append(dividend)
    rdiv_history.append(0)
    for i in range(horizon - 1):
        dividend, rdiv = draw_dividend(dividend)
        history.append(dividend)
        rdiv_history.append(rdiv)
    return history, rdiv_history

def earnings(pop, prev_dividend):
    dividend, random_dividend = draw_dividend(prev_dividend)
    for ind in pop:
        div_asset = ind.asset * dividend  # Determine gain from dividends
        interest_cash = ind.cash * parameters.INTEREST_RATE  # Determine gain from interest
        ind.cash += div_asset + interest_cash
    return pop, dividend, random_dividend

cdef determine_multiplier(list pop, double spoils, double ToLiquidate):

    total_buy = 0.0
    total_sell = 0.0

    cdef cythonized.Individual ind
    for ind in pop:
        if ind.edv > 0:
            total_buy += ind.edv
        elif ind.edv < 0:
            total_sell += abs(ind.edv)

    if spoils > 0:
        total_sell += abs(ToLiquidate)
    if spoils < 0:
        total_buy += ToLiquidate

    if total_sell != 0:
        order_ratio = total_buy / total_sell
    elif total_sell == 0:
        order_ratio = 0

    if order_ratio < 0:
        raise ValueError(
            "Negative order ratio (total sell/buy): "
            + str(total_sell)
            + "/"
            + str(total_buy)
            + "/"
            + str(ToLiquidate)
        )

    # Default values
    multiplier_buy = 0
    multiplier_sell = 0
    if order_ratio == 0:  # either noone buys, or no one sells
        pass
        # No orders will be executed (no supply or no demand)
    elif order_ratio < 1:
        multiplier_buy = 1
        multiplier_sell = order_ratio
        # Selling will be restricted according to demand
    elif order_ratio == 1:
        multiplier_buy = 1
        multiplier_sell = 1
        # All orders will be executed (supply =  demand)
    elif order_ratio > 1:
        multiplier_buy = 1 / order_ratio
        multiplier_sell = 1
        # Buying will be restricted according to supply
    else:
        raise ValueError("order_ratio has a strange value: " + str(order_ratio))

    if multiplier_buy < 0:
        raise ValueError("Multiplier Buy is negative")
    if multiplier_sell < 0:
        raise ValueError("Multiplier Sell is negative")

    if abs(total_buy * multiplier_buy - total_sell * multiplier_sell) != 0:
        if abs(total_buy * multiplier_buy - total_sell * multiplier_sell) >= abs(
            0.01 * ((total_buy * multiplier_buy) + (total_sell * multiplier_sell))
        ):
            print(total_buy * multiplier_buy)
            print(total_sell * multiplier_sell)
            raise ValueError(
                "Total buy * Mul is different from Total sell * Mul by more than 1 (abs difference)"
            )

    return multiplier_buy, multiplier_sell


def execute_ed(list pop, double current_price, asset_supply, double spoils, double ToLiquidate):
    # Determine adjustements to edv if we have some mismatch
    cdef double multiplier_buy
    cdef double multiplier_sell
    multiplier_buy, multiplier_sell = determine_multiplier(pop, spoils, ToLiquidate)
    volume = 0.0

    cdef cythonized.Individual ind
    cdef double amount
    for ind in pop:
        amount = 0.0

        if ind.edv > 0:
            amount = ind.edv * multiplier_buy

        if ind.edv < 0:
            amount = ind.edv * multiplier_sell

        ind.asset += amount
        ind.cash -= amount * current_price
        volume += abs(amount)

        # Apply some some readjustment to avoid negative cash
        if ind.cash < 0:
            ind.loan += abs(ind.cash)
            ind.cash = 0

    # Record that we liquidated some spoils
    if spoils > 0:
        # Spoils are positive. We wanted to sell some shares. TL is negative.
        # Ex: from spoils 1000, we sold 100 (TL = -100) for mul = 1. New spoils is 1000 - 100 = 900.
        spoils += ToLiquidate * multiplier_sell
    if spoils < 0:
        # Spoils are negative. We wanted to buy back some shares. TL is positive.
        # Ex: from spoils -1000, we bought 100 (TL = 100) for mul=1. New spoils is -1000 + 100 = -900.
        spoils += ToLiquidate * multiplier_buy
        # Isn't that a minus sign here instead?

    if abs(count_long_assets(pop, spoils) - asset_supply) > 0.01 * asset_supply:
        # If we violate the asset supply constraint by more than 1%, raise an error.
        if abs(count_long_assets(pop, spoils) - asset_supply) >= 0.01 * asset_supply:
            print("Spoils " + str(spoils))
            print("ToLiquidate " + str(ToLiquidate))
            print("Pop ownership " + str(count_pop_long_assets(pop)))
            raise ValueError(
                "Asset supply cst violated "
                + str(count_long_assets(pop, spoils))
                + "/"
                + str(asset_supply)
            )

    cdef double SupplyCorrectionRatio
    # If the violation of the asset supply is minor (less than 1%), correct the rounding error.
    if abs(count_long_assets(pop, spoils) - asset_supply) <= 0.01 * asset_supply:
        SupplyCorrectionRatio = asset_supply / count_long_assets(pop, spoils)
        spoils = spoils * SupplyCorrectionRatio
        for ind in pop:
            # previous = ind.asset
            # if ind.asset > 0:
            ind.asset = SupplyCorrectionRatio * ind.asset
            # if ind.asset < 0:
            #     ind.asset = (1/SupplyCorrectionRatio) * ind.asset
            # if spoils > 0:

            # if spoils < 0:
            #     spoils = spoils * (1/SupplyCorrectionRatio)
            # if ind.asset != previous * SupplyCorrectionRatio:
            #     warnings.warn('Previous asset = new ind.asset ' + str(previous) + '/' + str(ind.asset) + '/' + str(SupplyCorrectionRatio) + '/' + str(previous * SupplyCorrectionRatio))

        # If the resulting violation is still superior to 0.1% after rounding correction, raise an error.
        if abs(count_long_assets(pop, spoils) - asset_supply) > 0.001 * asset_supply:
            print(abs(count_long_assets(pop, spoils) - asset_supply))
            print("---")
            for ind in pop:
                print(ind.asset)
            raise ValueError(
                "Rounding violation of asset supply was not succesfully corrected. "
                + str(SupplyCorrectionRatio)
                + "//"
                + str(count_long_assets(pop, spoils))
                + "//"
                + str(asset_supply)
                + "//"
                + str(spoils)
            )

    return pop, volume, spoils
