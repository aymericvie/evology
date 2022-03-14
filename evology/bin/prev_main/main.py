import random
import matplotlib.pyplot as plt
import numpy as np

np.set_printoptions(precision=4)
np.set_printoptions(suppress=True)
import genetic_algorithm_functions as ga
import genetic_programming_functions as gp
import market
import market_clearing_leap as mc_leap
from parameters import *
import data
import brownian_motion as bm
import population_generation as popgen

RANDOM_SEED = parameters.RANDOM_SEED
random.seed(RANDOM_SEED)
POPULATION_SIZE = parameters.POPULATION_SIZE
MAX_TIME_HORIZON = parameters.MAX_TIME_HORIZON
# MUTATION_RATE = parameters.MUTATION_RATE
MAX_GENERATIONS = parameters.MAX_GENERATIONS
# CROSSOVER_RATE = parameters.CROSSOVER_RATE
MIN_TIME_HORIZON = parameters.MIN_TIME_HORIZON
INITIAL_PRICE = parameters.INITIAL_PRICE
TOURNAMENT_SIZE = parameters.TOURNAMENT_SIZE
INITIAL_DIVIDEND = parameters.INITIAL_DIVIDEND
INTEREST_RATE = parameters.INTEREST_RATE
DIVIDEND_GROWTH_RATE_G = parameters.DIVIDEND_GROWTH_RATE_G
share_increment = parameters.share_increment
short_bound = parameters.short_bound
CONSUMPTION_RATE = parameters.CONSUMPTION_RATE
INITIAL_CASH = parameters.INITIAL_CASH
INITIAL_ASSETS = parameters.INITIAL_ASSETS


def main(mode, selection_proba, CROSSOVER_RATE, MUTATION_RATE):
    pop = ga.toolbox.tf_population_creation(n=POPULATION_SIZE)

    pop_ex, pop_op, balance_sheet, types = popgen.generate_population(mode)
    print("initialised bs")
    print(balance_sheet)
    print(balance_sheet[0, 0])
    # pop = pop_ex.copy() #temp

    # Create the population and the results accumulators
    generationCounter = 1
    price = INITIAL_PRICE
    extended_price_history = bm.generate_bm_series(MAX_TIME_HORIZON + 1)
    extended_price_history = [abs(x) for x in extended_price_history]
    # assetQ = market.count_assets(pop)
    assetQ = market.count_assets2(balance_sheet)
    dividend = INITIAL_DIVIDEND

    (
        maxFitnessValues,
        meanFitnessValues,
        replacements,
        dividend_history,
        random_dividend_history,
        price_history,
    ) = ([], [], [], [], [], [])
    (
        generation_history,
        mismatch_history,
        asset_count_history,
        mean_theta,
        mean_wealth,
        size_pos_pos,
        size_neg_pos,
    ) = ([], [], [], [], [], [], [])

    print("Initial population")
    print(("{}\n" * len(pop)).format(*pop))
    print("Agent representation")
    print(
        "[Theta Wealth Cash Asset Loan TradingSignal RawExcessDemand     Profit     EMA profit   Margin]"
    )
    print(
        "[ 0       1     2    3     4         5             6           7            8              9]"
    )

    # "Put this as a single function"
    # fitnessValues = list(map(ga.toolbox.evaluate, pop))
    # for individual, fitnessValue in zip(pop, fitnessValues):
    #     individual.fitness.values = fitnessValue
    # fitnessValues = [individual.fitness.values[0] for individual in pop]
    print(("{}\n" * len(pop_ex)).format(*pop_ex))
    while generationCounter < MAX_GENERATIONS:
        print("----------------------------------------------------------------------")
        print("Generation " + str(generationCounter))
        # print(('{}\n'*len(pop)).format(*pop))

        """ A) Draw dividends """
        DIVIDEND_GROWTH_RATE = market.determine_dividend_growth(DIVIDEND_GROWTH_RATE_G)
        dividend, random_dividend = market.draw_dividend(DIVIDEND_GROWTH_RATE)
        dividend_history.append(dividend)
        print("dividend is " + str(dividend))
        random_dividend_history.append(random_dividend)

        # print("bs before B")
        # print(balance_sheet)
        """ B) Apply dividends, interest rate and reinvestment, update profit """
        market.wealth_earnings(pop, dividend)  # temp

        # print("before/after bs narket wealth earnings")
        # print(balance_sheet)
        market.bs_wealth_earnings(balance_sheet, dividend)
        # print(balance_sheet)

        """ C) Update wealth and margin as a function of price """
        market.consumption(pop, CONSUMPTION_RATE, price)  # temp
        market.update_wealth(pop, price)  # temp
        market.update_margin(pop, price)  # temp
        market.bs_wealth_update(balance_sheet, price, CONSUMPTION_RATE)

        """ D) Hypermutation operator """

        balance_sheet[0, 0] = 0  # temp

        pop, round_replacements = ga.hypermutate(pop)  # temp

        ga.fitness_for_invalid(pop)  # temp

        pop_ex, pop_op, types, balance_sheet, round_replacements = ga.hypermutate2(
            pop_ex, pop_op, types, balance_sheet, mode
        )
        # fitness_for_invalid seems to work here, but we need a different evaluate

        ga.fitness_for_invalid2(pop_ex, balance_sheet)
        # ga.fitness_for_invalid2(pop_op, balance_sheet) TODO
        """ Maybe this does not 
        work well because of i and the fact that here pop_op should be i + 
        len)pop_ex) or sometng like this """

        """ E) Deduce fitness as EMA """
        market.compute_ema(pop)  # temp

        # print("compute ema before/after")
        # print(balance_sheet)
        market.compute_ema2(balance_sheet)
        # print(balance_sheet)
        # print("fitness for all before/after")
        # print(pop_ex)
        fitnessValues = ga.fitness_for_all(pop_ex, balance_sheet)
        # print(individual.fitness.values for individual in pop_ex)
        # print("fit values and pop_ex")
        # print(fitnessValues)
        # print(pop_ex)

        # print("Fitness check: ind and fitness value of ind")
        # print(balance_sheet)
        # for ind in pop_ex:
        #     print(ind)
        #     print(ind.fitness.values)

        ga.set_fitness(pop_ex, balance_sheet)

        print("Fitness check2: ind and fitness value of ind")
        for ind in pop_ex:
            print(ind)
            print(ind.fitness)

        # """ This here needs redo (same instruction as before, for all ind """

        # fitnessValues = list(map(ga.toolbox.evaluate, pop))
        # for individual, fitnessValue in zip(pop, fitnessValues):
        #     individual.fitness.values = fitnessValue
        # fitnessValues = [individual.fitness.values[0] for individual in pop]

        # print("After fitness, dividends, wealth, hypermuation updates")
        # print(('{}\n'*len(pop)).format(*pop))

        """  F) GA evolution of strategies with last period fitness  """

        # Selection
        if selection_proba == 1:
            offspring = ga.toolbox.select(pop, POPULATION_SIZE, TOURNAMENT_SIZE)
            ga.fitness_for_invalid(offspring)
            offspring = list(map(ga.toolbox.clone, offspring))

            # Crossover
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                ga.toolbox.mate(child1, child2, CROSSOVER_RATE)
                del child1.fitness.values
                del child2.fitness.values

            # Mutation
            for mutant in offspring:
                ga.toolbox.mutate(mutant, MUTATION_RATE)
                del mutant.fitness.values

            # Recomputing fitness
            ga.fitness_for_invalid(offspring)

            # Replacing
            pop[:] = offspring
            fitnessValues = [ind.fitness.values[0] for ind in pop]

        """ G) Actions are now set. Update trading signals """
        # print(extended_price_history)
        market.update_trading_signal(pop, extended_price_history)

        """ H) Deduce excess demand and create an order book of ED functions of price"""

        market.update_excess_demand(pop)
        list_excess_demand_func = market.order_excess_demand(pop)
        """ list_excess_demand_func is now the list of ED functions """
        # aggregate_ed = market.compute_aggregate_excess_demand(pop)
        aggregate_ed = market.compute_aggregate_excess_demand(
            pop, list_excess_demand_func
        )

        # print("After trading signal, GA, ED update, right before clearing")
        # print(('{}\n'*len(pop)).format(*pop))

        """ I) Clear the market with the aggregate ED, obtain the new price """

        price = mc_leap.leap_solver(pop, price)
        # price = mc_leap.solver_linear_shortcut(pop, price)
        print("Price is " + str(price))

        # testing block

        # sum_ag = 0
        # for i in range(POPULATION_SIZE):
        #     sum_ag += list_excess_demand_func[i](price)
        #     print("Agent " + str(i) + " ED(pt+1) is " + str(list_excess_demand_func[i](price)))
        # print("Sum AG " + str(sum_ag))
        extended_price_history = np.append(extended_price_history, price)
        price_history.append(price)

        """ J) Update inventories """
        market.update_inventory(pop, price, assetQ, share_increment, short_bound)

        """ K) Record results """
        maxFitness = max(fitnessValues)
        meanFitness = sum(fitnessValues) / len(pop)
        maxFitnessValues.append(maxFitness)
        meanFitnessValues.append(meanFitness)
        replacements.append(round_replacements)
        asset_count_history.append(market.count_assets(pop))
        mean_theta.append(data.theta_stats(pop))
        mean_wealth.append(market.count_wealth(pop))
        size_pos_pos.append(market.count_assets(pop))
        size_neg_pos.append(market.count_size_short(pop))

        # print("agg_price before mismatch")
        # print(aggregate_ed(price))
        # print(abs(market.truncate(aggregate_ed(price),3)))
        mismatch_history.append(abs(market.truncate(aggregate_ed(price), 3)))
        #  Could this print results be automated? We have it twice

        print(
            "- Generation {}: Max Fitness = {}, Avg Fitness = {}".format(
                generationCounter, maxFitness, meanFitness
            )
        )
        generation_history.append(generationCounter)
        generationCounter += 1

    df = data.generate_df(
        generation_history,
        price_history,
        mismatch_history,
        mean_theta,
        mean_wealth,
        meanFitnessValues,
        asset_count_history,
        dividend_history,
        random_dividend_history,
        size_pos_pos,
        size_neg_pos,
        replacements,
    )

    # return
    # return price, initial_pop, pop, maxFitnessValues, meanFitnessValues, replacements, agent0_profit, agent0_ema, dividend_history, price_history, random_dividend_history, list_excess_demand_func, aggregate_ed, df
    print(("{}\n" * len(pop)).format(*pop))
    return df, extended_price_history, pop_ex, balance_sheet
