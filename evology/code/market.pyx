#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True

from balance_sheet import count_long_assets, count_pop_long_assets, count_short_assets
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

cdef determine_multiplier(list pop, double spoils, double ToLiquidate, double asset_supply):

    cdef double total_buy = 0.0
    cdef double total_sell = 0.0
    cdef double total_short = 0.0
    cdef double total_sell_short = 0.0
    cdef double short_ratio = 0.0

    cdef cythonized.Individual ind
    cdef double order_ratio = 0.0

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
    
    effective_possible_short = min(total_short, max(0, asset_supply - CountShort))

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

    if round(abs(total_buy * multiplier_buy - total_sell_short * multiplier_sell),3) != 0:
        if abs(total_buy * multiplier_buy - total_sell_short * multiplier_sell) >= abs(
            0.0001 * ((total_buy * multiplier_buy) + (total_sell_short * multiplier_sell))
        ):
            print(total_buy * multiplier_buy)
            print(total_sell_short * multiplier_sell)
            raise ValueError(
                "Total buy * Mul is different from Total sell * Mul by more than 1 (abs difference)"
            )
    if short_ratio > 1:
        print(short_ratio)
        raise ValueError('Short ratio above 1')

    return multiplier_buy, multiplier_sell, short_ratio


def execute_ed(list pop, double current_price, double asset_supply, double spoils, double ToLiquidate):
    # Determine adjustements to edv if we have some mismatch
    cdef double multiplier_buy
    cdef double multiplier_sell
    cdef double short_ratio
    cdef double Liquidations = 0.0
    multiplier_buy, multiplier_sell, short_ratio = determine_multiplier(pop, spoils, ToLiquidate, asset_supply)
    volume = 0.0

    cdef cythonized.Individual ind
    cdef double amount
    for ind in pop:
        amount = 0.0

        if ind.edv > 0:
            amount = ind.edv * multiplier_buy

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
        Liquidations = ToLiquidate * multiplier_sell
        spoils += Liquidations #+= because for sell side, ToLiquidate is negative.
    if spoils < 0:
        # Spoils are negative. We wanted to buy back some shares. TL is positive.
        # Ex: from spoils -1000, we bought 100 (TL = 100) for mul=1. New spoils is -1000 + 100 = -900.
        Liquidations = ToLiquidate * multiplier_buy
        spoils += Liquidations
        # Isn't that a minus sign here instead?

    cdef double SupplyCorrectionRatio
    cdef double CurrentCount 

    if count_short_assets(pop, spoils) >= asset_supply + 1 :
        print(count_short_assets(pop, spoils))
        print(count_long_assets(pop, spoils))
        print(asset_supply)
        print([multiplier_buy, multiplier_sell])
        raise ValueError('Limit on short position size has been violated after execution of excess demand orders.')

    CurrentCount = count_long_assets(pop, spoils)
    if CurrentCount - asset_supply >= 1:

        # LogBefore = [CurrentCount - asset_supply, count_pop_long_assets(pop), spoils]

        amount_before_corrected = CurrentCount - asset_supply
        SupplyCorrectionRatio = asset_supply / CurrentCount

        # LogBetween = [count_pop_long_assets(pop) * SupplyCorrectionRatio, spoils * SupplyCorrectionRatio, count_pop_long_assets(pop) * SupplyCorrectionRatio + spoils * SupplyCorrectionRatio - asset_supply]

        # Logpop = np.zeros((len(pop), 4))
        # Adjust the spoils quantity 
        spoils = spoils * SupplyCorrectionRatio
        for i, ind in enumerate(pop):
            # Adjust the assets quantity
            #Logpop[i,0] = ind.asset
            #Logpop[i,1] = ind.asset * SupplyCorrectionRatio
            ind.asset = SupplyCorrectionRatio * ind.asset
            #Logpop[i,2] = ind.asset
            #Logpop[i,3] = Logpop[i,2] - Logpop[i,1]
            # Compensate in cash accordingly.
            ind.cash = ind.cash / SupplyCorrectionRatio
        amount_after_correction = count_long_assets(pop, spoils) - asset_supply
        
        #LogAfter = [amount_after_correction, count_pop_long_assets(pop), spoils]

        if abs(amount_before_corrected) < abs(amount_after_correction):
            print(amount_before_corrected)
            print(amount_after_correction)
            print(SupplyCorrectionRatio)
            #print('Log Before')
            #print(LogBefore)
            #print('Log Between')
            #print(LogBetween)
            #print('Log After')
            #print(LogAfter)
            #print('Pop log')
            #print(Logpop)
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

    #if abs(count_long_assets(pop, spoils) - asset_supply) > 0.01 * asset_supply:
        # If we violate the asset supply constraint by more than 1%, raise an error.
        #if abs(count_long_assets(pop, spoils) - asset_supply) >= 0.01 * asset_supply:
        #    print("Spoils " + str(spoils))
        #    print("ToLiquidate " + str(ToLiquidate))
        #    print("Pop ownership " + str(count_pop_long_assets(pop)))
        #    raise ValueError(
        #        "Asset supply cst violated "
        #        + str(count_long_assets(pop, spoils))
        #        + "/"
        #        + str(asset_supply)
        #    )

    #cdef double SupplyCorrectionRatio
    # If the violation of the asset supply is minor (less than 1%), correct the rounding error.
    #while abs(count_long_assets(pop, spoils) - asset_supply) <= 0.01 * asset_supply and count < 10:
    #    count += 1
    ##count = 0
    #    SupplyCorrectionRatio = asset_supply / count_long_assets(pop, spoils)
    #    spoils = spoils * SupplyCorrectionRatio
    #    for ind in pop:
    #        ind.asset = SupplyCorrectionRatio * ind.asset
        # If the resulting violation is still superior to 0.1% after rounding correction, raise an error.
    #    if abs(count_long_assets(pop, spoils) - asset_supply) > 0.001 * asset_supply:
    #        print(abs(count_long_assets(pop, spoils) - asset_supply))
     #       print("---")
      #      for ind in pop:
      #          print(ind.asset)
      #      raise ValueError(
      #          "Rounding violation of asset supply was not succesfully corrected. "
      #          + str(SupplyCorrectionRatio)
      #          + "//"
      #          + str(count_long_assets(pop, spoils))
      #          + "//"
      #          + str(asset_supply)
      #          + "//"
      #          + str(spoils)
      #      )
    return pop, volume, spoils, Liquidations