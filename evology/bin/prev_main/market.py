import math
import random
import parameters
import numpy as np

np.set_printoptions(precision=4)
np.set_printoptions(suppress=True)

REINVESTMENT_RATE = parameters.REINVESTMENT_RATE
INTEREST_RATE = parameters.INTEREST_RATE
EMA_HORIZON = parameters.EMA_HORIZON
DIVIDEND_GROWTH_RATE_G = parameters.DIVIDEND_GROWTH_RATE_G
DIVIDEND_GROWTH_VOLATILITY = parameters.DIVIDEND_GROWTH_VOLATILITY
DIVIDEND_AUTOCORRELATION = parameters.DIVIDEND_AUTOCORRELATION

dividend_history = parameters.dividend_history
random_dividend_history = parameters.random_dividend_history
random_dividend = parameters.INITIAL_RANDOM_DIVIDEND
dividend = parameters.INITIAL_DIVIDEND
DIVIDEND_ATC_TAU = parameters.DIVIDEND_ATC_TAU
TRADING_DAYS = parameters.TRADING_DAYS
LAMBDA_TF = parameters.LAMBDA_TF
STRATEGY_AGGRESSIVENESS_TF = parameters.STRATEGY_AGGRESSIVENESS_TF

# Agent representaiton:
#     [Theta Wealth Cash Asset Loan TradingSignal ExcessDemand     Profit     EMA profit]
#     [ 0       1     2    3     4         5             6           7            8 ]


def truncate(number, digits) -> float:
    stepper = 10.0**digits
    return math.trunc(stepper * number) / stepper


def determine_dividend_growth(DIVIDEND_GROWTH_RATE_G):
    global DIVIDEND_GROWTH_RATE
    DIVIDEND_GROWTH_RATE = ((1 + DIVIDEND_GROWTH_RATE_G) ** (1 / TRADING_DAYS)) - 1
    return DIVIDEND_GROWTH_RATE


"""
def draw_dividend(DIVIDEND_GROWTH_RATE):
    
    global dividend
    global random_dividend
    random_dividend = random.normalvariate(0, 1)
    if len(random_dividend_history) > DIVIDEND_ATC_TAU:
        random_dividend = (1 - DIVIDEND_AUTOCORRELATION ** 2) * random.normalvariate(0,1) + DIVIDEND_AUTOCORRELATION * random_dividend_history[-1 - DIVIDEND_ATC_TAU]
    dividend = abs(dividend + DIVIDEND_GROWTH_RATE * dividend + DIVIDEND_GROWTH_VOLATILITY * dividend * random_dividend)
    # print("Dividend today is " + str(dividend))
    return dividend, random_dividend
"""


def draw_dividend(DIVIDEND_GROWTH_RATE):

    global dividend
    global random_dividend

    random_dividend = truncate(random.normalvariate(0, 1), 3)
    if len(random_dividend_history) > DIVIDEND_ATC_TAU:
        random_dividend = (
            1 - DIVIDEND_AUTOCORRELATION**2
        ) * random_dividend + DIVIDEND_AUTOCORRELATION * random_dividend_history[
            len(random_dividend_history) - 1 - DIVIDEND_ATC_TAU
        ]
    # wiener.append(random_dividend)

    dividend = abs(
        dividend
        + DIVIDEND_GROWTH_RATE * dividend
        + DIVIDEND_GROWTH_VOLATILITY * dividend * random_dividend
    )
    dividend = truncate(dividend, 3)
    return dividend, random_dividend


"""TO REMOVE"""


def wealth_earnings(pop, dividend):
    # print(INTEREST_RATE)
    # print(REINVESTMENT_RATE)
    for ind in pop:
        # Update profit
        ind[7] = truncate(
            REINVESTMENT_RATE * (INTEREST_RATE * ind[2] + dividend * ind[3]), 3
        )
        # print("profit is " + str(ind[7]))

        # Update cash
        ind[2] += REINVESTMENT_RATE * (INTEREST_RATE * ind[2] + dividend * ind[3])
        ind[2] = truncate(ind[2], 3)
    return ind


def bs_wealth_earnings(balance_sheet, dividend):
    for row in balance_sheet:
        # Update Profit
        row[6] = truncate(
            REINVESTMENT_RATE * (INTEREST_RATE * row[1] + dividend * row[2]), 3
        )
        # Update Cash
        row[1] += REINVESTMENT_RATE * (INTEREST_RATE * row[1] + dividend * row[2])
        row[1] = truncate(row[1], 3)


""" TO REMOVE """


def update_wealth(pop, price):
    for ind in pop:
        ind[1] = truncate(ind[2] + ind[3] * price - ind[4], 3)
    return ind


""" TO REMOVE """


def consumption(pop, CONSUMPTION_RATE, price):
    for ind in pop:
        if ind[2] >= CONSUMPTION_RATE:
            ind[2] -= CONSUMPTION_RATE
        if ind[2] < CONSUMPTION_RATE:
            ind[2] = 0
            consume_amount = CONSUMPTION_RATE - ind[2]
            if ind[3] <= 0:
                ind[1] -= 1_000
            if ind[3] > 0:
                # agent will try to sell assets to fund consumption
                if ind[3] * price >= consume_amount:
                    ind[3] -= consume_amount / price
                    # sells
                if ind[3] * price < consume_amount:
                    ind[1] -= 1_000


""" TO REMOVE """


def update_margin(pop, price):
    for ind in pop:
        if ind[3] < 0:
            ind[2] += ind[9]
            ind[9] = 0
            ind[9] = abs(ind[3]) * price
            ind[2] -= ind[9]
            if ind[2] < 0:
                """If not enough cash for margin, and since we are in debt,
                we are automatically replaced"""
                ind[1] = -1_000
    return ind


def bs_wealth_update(balance_sheet, price, CONSUMPTION_RATE):
    for row in balance_sheet:

        # Apply consumption
        if row[1] >= CONSUMPTION_RATE:
            row[1] -= CONSUMPTION_RATE
        if row[1] < CONSUMPTION_RATE:
            row[1] = 0
            consume_amount = CONSUMPTION_RATE - row[1]
            if row[2] <= 0:
                row[1] -= 1_000
            if row[2] > 0:
                # agent will try to sell assets to fund consumption
                if row[2] * price >= consume_amount:
                    row[2] -= consume_amount / price
                    # sells
                if row[2] * price < consume_amount:
                    row[1] -= 1_000

        # Update margin
        if row[2] < 0:
            row[1] += row[8]
            row[8] = 0
            row[8] = abs(row[2]) * price
            row[1] -= row[8]
            if row[1] < 0:
                """If not enough cash for margin, and since we are in debt,
                we are automatically replaced"""
                row[1] = -1_000

        # Update wealth
        row[0] = truncate(row[1] + row[2] * price - row[3], 3)


""" TO REMOVE """


def compute_ema(pop):
    for ind in pop:
        ind[8] = truncate((2 / (EMA_HORIZON + 1)) * (ind[7] - ind[8]) + ind[8], 4)
    return ind


def compute_ema2(balance_sheet):
    for i in range(len(balance_sheet)):
        balance_sheet[i, 7] = truncate(
            (2 / (EMA_HORIZON + 1)) * (balance_sheet[i, 6] - balance_sheet[i, 7])
            + balance_sheet[i, 7],
            4,
        )

        # Agent representaiton:


#     [Theta Wealth Cash Asset Loan TradingSignal ExcessDemand     Profit     EMA profit]
#     [ 0       1     2    3     4         5             6           7            8 ]


def update_trading_signal(pop, extended_price_history):
    """
    Will require an update once we add different strategies
    """

    for ind in pop:
        if len(extended_price_history) > 1:
            if len(extended_price_history) > ind[0]:
                # print("Extended Price History")
                # print(extended_price_history)
                # print(np.log(extended_price_history))
                ind[5] = truncate(
                    np.log2(extended_price_history[-1])
                    - np.log2(extended_price_history[-ind[0]]),
                    3,
                )
            if len(extended_price_history) <= ind[0]:
                # The trader does not have the information to run her strategy. She waits in indifference.
                ind[5] = 0
        if len(extended_price_history) <= 1:
            ind[5] = 0
    return ind


def update_excess_demand(pop):
    for ind in pop:
        ind[6] = truncate(
            ind[1] * LAMBDA_TF * (np.tanh(STRATEGY_AGGRESSIVENESS_TF * ind[5]) + 0.5), 4
        )
    return ind


def order_excess_demand(pop):
    list_excess_demand_func = []
    for ind in pop:

        def ed(x):

            return truncate((ind[6] / x) - ind[3], 4)

        list_excess_demand_func.append(ed)
        # print(ed(1))
        del ed
    return list_excess_demand_func


def compute_aggregate_excess_demand(pop, list_excess_demand_func):
    def aggregate_ed(x):
        result = 0
        for i in range(len(pop)):
            result += list_excess_demand_func[i](x)
        return result

    return aggregate_ed


""" TO REMOVE """


def count_assets(pop):
    count = 0
    for ind in pop:
        if ind[3] > 0:
            count += ind[3]
    return count


def count_assets2(balance_sheet):
    count = 0
    for row in balance_sheet:
        if row[2] > 0:
            count += row[2]
    return count


def count_size_short(pop):
    count = 0
    for ind in pop:
        if ind[3] <= 0:
            count += ind[3]
    return count


def count_wealth(pop):
    total_wealth = 0
    for ind in pop:
        total_wealth += ind[1]
    return total_wealth / len(pop)


def update_inventory(pop, price, assetQ, share_increment, short_bound):
    for ind in pop:
        former_asset = ind[3]
        former_loan = ind[4]
        realised_ed = truncate(ind[6] / price - ind[3], 4)
        # print("agent wants up to " + str(realised_ed)) #this is correct

        """ If we want to buy assets: non-negative cash buying procedure """
        cash = ind[2] + ind[3] * price + former_loan - ind[4]

        # print("agent wants up to " + str(realised_ed))
        if realised_ed > 0:
            i = 0
            while i < realised_ed - share_increment:
                if cash - price * share_increment > 0:
                    if count_assets(pop) < assetQ:
                        ind[3] += share_increment
                        # cash -= price
                        ind[2] -= price * share_increment
                i += share_increment
        if realised_ed < 0:

            i = 0
            while i < abs(realised_ed) - share_increment:

                if ind[3] < 1:
                    """short selling"""
                    if count_assets(pop) - count_size_short(pop) > share_increment:
                        ind[3] -= share_increment
                        ind[9] += price * share_increment

                if ind[3] >= share_increment:
                    """simple selling"""
                    ind[3] -= share_increment
                    ind[2] += price * share_increment

                i += share_increment

        # 	 Clear the margin if we are out of the short position
        if ind[3] >= 0:
            ind[2] += ind[9]
            ind[9] = 0
    return ind
