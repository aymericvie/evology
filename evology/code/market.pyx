#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True

from balance_sheet_cython import count_long_assets, count_short_assets, clear_debt
import numpy as np
from parameters import div_atc, G, div_vol, G_day, Short_Size_Percent
cimport cythonized
from libc.math cimport isnan, log2, exp

cpdef sigmoid(double x):
    cdef double result 
    result = 1. / (1. + exp(-x))
    return result

'''
cpdef draw_dividend(double dividend, list random_dividend_history):

    cdef double Z = np.random.normal(0,1)
    cdef double random_dividend

    if len(random_dividend_history) > 2:
        random_dividend =  (
            div_atc * random_dividend_history[-2] 
            + (1.0 - div_atc ** 2.0) * Z)
    else:
        random_dividend = Z
    #) * random_dividend + parameters.div_atc * random_dividend_history[
    #    - 1.0 - 1.0
        #]
    dividend = abs(
        dividend * (1 + G_day)
        + div_vol * dividend * random_dividend
    )
    return dividend, random_dividend
'''

cpdef earnings(list pop, double dividend, double interest_day):
    cdef cythonized.Individual ind
    cdef double div_asset = 0.
    cdef double interest_cash = 0.

    for ind in pop:
        div_asset = ind.asset * dividend  # Determine gain from dividends
        interest_cash = ind.cash * interest_day  # Determine gain from interest
        ind.cash += div_asset + interest_cash
        
    return pop

cpdef determine_multiplier(list pop, double spoils, double ToLiquidate, double asset_supply):

    cdef double total_buy = 0.0
    cdef double total_sell = 0.0
    cdef double total_short = 0.0
    cdef double total_sell_short = 0.0
    cdef double short_ratio = 0.0

    cdef cythonized.Individual ind
    cdef double order_ratio = 0.0
    cdef double temp_sell = 0.0
    cdef double effective_possible_short
    cdef double multiplier_sell
    cdef double multiplier_buy
    cdef double CountShort

    for ind in pop:
        if ind.edv > 0:
            total_buy += ind.edv
        elif ind.edv < 0:
            # If we sell, but have assets in stocks, this is a simple sell.
            if ind.asset >= abs(ind.edv):
                total_sell += abs(ind.edv)
            # If we sell more than we own:
            elif ind.asset < abs(ind.edv):
                temp_sell = abs(ind.edv)
                if ind.asset > 0:
                    # Register as simple sell what we can sell up to our current stocks 
                    total_sell += ind.asset
                    temp_sell -= ind.asset 
                # Register the reminder as short selling
                total_short += temp_sell

    if spoils > 0:
        total_sell += abs(ToLiquidate)
    if spoils < 0:
        total_buy += ToLiquidate

    total_sell_short += total_sell
    # Now we have total buy and total sell. Decide how much we include total_short.
    # In this determination, short positions already in spoils and population have the priority.
    CountShort = count_short_assets(pop, spoils)
    if CountShort >= asset_supply + 1:
        print(CountShort)
        print(asset_supply)
        raise ValueError('Limit on short position size was violated before computing order ratio. ')
    
    effective_possible_short = min(total_short, max(0, Short_Size_Percent * 0.01 * asset_supply - CountShort))

    if total_short != 0:
        short_ratio = effective_possible_short / total_short

    total_sell_short += effective_possible_short

    if total_sell_short != 0:
        order_ratio = total_buy / total_sell_short

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

    if round(abs(total_buy * multiplier_buy - total_sell_short * multiplier_sell),5) >= 0.1:
        if abs(total_buy * multiplier_buy - total_sell_short * multiplier_sell) >= abs(
            0.1 * ((total_buy * multiplier_buy) + (total_sell_short * multiplier_sell))
        ):
            print([total_buy, total_sell])
            print([multiplier_buy, multiplier_sell])
            print(total_buy * multiplier_buy)
            print(total_sell_short * multiplier_sell)
            raise ValueError(
                "Total buy * Mul is different from Total sell * Mul by more than 1 (abs difference)"
            )
    if short_ratio > 1:
        print(short_ratio)
        raise ValueError('Short ratio above 1')

    return multiplier_buy, multiplier_sell, short_ratio


cpdef execute_ed(list pop, double current_price, double asset_supply, double spoils, double ToLiquidate):

    cdef double multiplier_buy
    cdef double multiplier_sell
    cdef double short_ratio
    cdef double Liquidations = 0.0
    cdef cythonized.Individual ind
    cdef double amount
    cdef double volume = 0.0
    cdef double SupplyCorrectionRatio
    cdef double CurrentCount 
    cdef double amount_before_corrected
    cdef double amount_after_correction

    multiplier_buy, multiplier_sell, short_ratio = determine_multiplier(pop, spoils, ToLiquidate, asset_supply)

    for ind in pop:
        amount = 0.0

        if ind.edv > 0:
            if multiplier_buy != 0.0:
                amount = ind.edv * multiplier_buy
            if isnan(amount) == True:
                print([ind.edv, multiplier_buy])
                raise ValueError('nan amount (buy)')

        if ind.edv < 0:
            if abs(ind.edv) * multiplier_sell <= ind.asset:
            # If we have enough to simple sell as much as we want to
                amount = ind.edv * multiplier_sell
            elif abs(ind.edv) * multiplier_sell > ind.asset:
            # If instead we want to sell more than our inventory:
                temp = abs(ind.edv) * multiplier_sell
                if ind.asset > 0:
                # If we have assets to sell, we sell those according to mulitplier_sell
                    amount -= ind.asset
                    temp -= ind.asset
                # The reminder is a short sell. Hence, both multiplier_sell AND short_ratio apply.
                amount -= temp * short_ratio
            if isnan(amount) == True:
                print([ind.edv, multiplier_buy])
                raise ValueError('nan amount (sell)')

        '''
        if ind.cash - amount * current_price < 0:
            print('Measuring info before negative cash')
            print([ind.type, ind.cash, ind.loan, ind.asset, amount, ind.wealth])
            print(current_price)
        '''

        ind.asset += amount
        ind.cash -= amount * current_price
        volume += abs(amount)

        # Apply some some readjustment to avoid negative cash
        if ind.cash < 0:
            '''
            print([ind.type, ind.cash, ind.loan, ind.asset, amount, ind.wealth])
            print([multiplier_buy, multiplier_sell])
            print([sigmoid(log2(ind.val / current_price))])
            print(ind.edv)
            print([ind.cash + ind.asset * current_price - ind.loan])
            raise RuntimeError('Negative cash after transaction.')
            '''
            ind.loan += abs(ind.cash)
            ind.cash = 0

        if isnan(ind.cash) == True or isnan(ind.asset) == True:
            print([ind.type, amount, ind.cash, ind.asset, ind.loan, ind.wealth, ind.edv, ind.tsv])
            raise ValueError('Nan cash and asset at market')

    # Record that we liquidated some spoils
    if spoils > 0:
        # Spoils are positive. We wanted to sell some shares. TL is negative.
        # Ex: from spoils 1000, we sold 100 (TL = -100) for mul = 1. New spoils is 1000 - 100 = 900.
        Liquidations = ToLiquidate * multiplier_sell
        spoils += Liquidations #+= because for sell side, ToLiquidate is negative.
    if spoils < 0:
        # Spoils are negative. We wanted to buy back some shares. TL is positive.
        # Ex: from spoils -1000, we bought 100 (TL = 100) for mul=1. New spoils is -1000 + 100 = -900.
        Liquidations = ToLiquidate * multiplier_buy
        spoils += Liquidations
        # Isn't that a minus sign here instead?


    if count_short_assets(pop, spoils) >= Short_Size_Percent * 0.01 * asset_supply + 1 :
        print(count_short_assets(pop, spoils))
        print(count_long_assets(pop, spoils))
        print(asset_supply)
        print([multiplier_buy, multiplier_sell])
        raise ValueError('Limit on short position size has been violated after execution of excess demand orders.')

    CurrentCount = count_long_assets(pop, spoils)
    if CurrentCount - asset_supply >= 1:
        amount_before_corrected = CurrentCount - asset_supply
        SupplyCorrectionRatio = asset_supply / CurrentCount
        # Adjust the spoils quantity 
        spoils = spoils * SupplyCorrectionRatio
        for i, ind in enumerate(pop):
            # Adjust the assets quantity
            ind.asset = SupplyCorrectionRatio * ind.asset
            # Compensate in cash accordingly.
            ind.cash = ind.cash / SupplyCorrectionRatio
        amount_after_correction = count_long_assets(pop, spoils) - asset_supply

        if abs(amount_before_corrected) < abs(amount_after_correction):
            print(amount_before_corrected)
            print(amount_after_correction)
            print(SupplyCorrectionRatio)
            raise ValueError('Rounding error correction increased asset supply violation. ')

    if count_long_assets(pop, spoils) - asset_supply >= 0.01 * asset_supply:
        print('Count Long assets different from asset supply: count, supply, diff, spoils, amount before / after')
        print(count_long_assets(pop, spoils))
        print(asset_supply)
        print(count_long_assets(pop, spoils) - asset_supply)
        print(spoils)
        print(amount_before_corrected)
        print(amount_after_correction)
        raise ValueError('Asset supply violated by more than 1%.')
    return pop, volume, spoils, Liquidations

'''
cpdef MarketActivity(list pop, double current_price, double asset_supply,
    double dividend, list dividend_history, double spoils, double ToLiquidate, list random_dividend_history):

    cdef double volume 
    cdef double random_dividend
    cdef double Liquidations

    pop, volume, spoils, Liquidations = execute_ed(pop, current_price, asset_supply, spoils, ToLiquidate)
    
    pop, dividend, random_dividend = earnings(pop, dividend, random_dividend_history)
    dividend_history.append(dividend)
    pop = update_margin(pop, current_price)
    pop = clear_debt(pop, current_price)
    return (
        pop,
        volume,
        dividend,
        random_dividend,
        dividend_history,
        spoils,
        Liquidations,
    )
    '''