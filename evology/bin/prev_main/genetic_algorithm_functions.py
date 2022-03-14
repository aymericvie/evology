from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from deap import gp
import numpy as np
import random
from operator import attrgetter
import parameters
import sys


# # =============================================================================
# # Fixed parameters
# # =============================================================================

RANDOM_SEED = parameters.RANDOM_SEED
POPULATION_SIZE = parameters.POPULATION_SIZE
MAX_TIME_HORIZON = parameters.MAX_TIME_HORIZON
MUTATION_RATE = parameters.MUTATION_RATE
MAX_GENERATIONS = parameters.MAX_GENERATIONS
CROSSOVER_RATE = parameters.CROSSOVER_RATE
MIN_TIME_HORIZON = parameters.MIN_TIME_HORIZON
INITIAL_PRICE = parameters.INITIAL_PRICE
TOURNAMENT_SIZE = parameters.TOURNAMENT_SIZE
INITIAL_ASSETS = parameters.INITIAL_ASSETS
INITIAL_CASH = parameters.INITIAL_CASH
MIN_VALUATION = parameters.MIN_VALUATION
MAX_VALUATION = parameters.MAX_VALUATION
PROBA_TF = parameters.PROBA_TF
PROBA_VI = parameters.PROBA_VI


toolbox = base.Toolbox()

# Create the fitness object
creator.create("fitness_strategy", base.Fitness, weights=(1.0,))
# Create the individual object
creator.create("individual", list, typecode="d", fitness=creator.fitness_strategy)
# Create the individual list
toolbox.register(
    "generate_tf_strategy", random.randint, MIN_TIME_HORIZON, MAX_TIME_HORIZON
)
toolbox.register("generate_wealth", random.randint, 0, 0)
toolbox.register("generate_cash", random.randint, INITIAL_CASH, INITIAL_CASH)
toolbox.register("generate_asset", random.randint, INITIAL_ASSETS, INITIAL_ASSETS)
toolbox.register("generate_loan", random.randint, 0, 0)
toolbox.register("generate_trading_signal", random.randint, 0, 0)
toolbox.register("generate_excess_demand", random.randint, 0, 0)
toolbox.register("generate_profit", random.randint, 0, 0)
toolbox.register("generate_ema", random.randint, 0, 0)
toolbox.register("generate_margin", random.randint, 0, 0)

toolbox.register(
    "generate_tf_individual",
    tools.initCycle,
    creator.individual,
    (
        toolbox.generate_tf_strategy,
        toolbox.generate_wealth,
        toolbox.generate_cash,
        toolbox.generate_asset,
        toolbox.generate_loan,
        toolbox.generate_trading_signal,
        toolbox.generate_excess_demand,
        toolbox.generate_profit,
        toolbox.generate_ema,
        toolbox.generate_margin,
    ),
    n=1,
)
toolbox.register(
    "tf_population_creation", tools.initRepeat, list, toolbox.generate_tf_individual
)

toolbox.register(
    "generate_tf_individual2",
    tools.initCycle,
    creator.individual,
    (toolbox.generate_tf_strategy),
    n=1,
)
toolbox.register(
    "tf_population_creation2", tools.initRepeat, list, toolbox.generate_tf_individual2
)


toolbox.register("generate_no_asset", random.randint, 0, 0)

toolbox.register(
    "generate_hyper_tf_individual",
    tools.initCycle,
    creator.individual,
    (
        toolbox.generate_tf_strategy,
        toolbox.generate_wealth,
        toolbox.generate_cash,
        toolbox.generate_no_asset,
        toolbox.generate_loan,
        toolbox.generate_trading_signal,
        toolbox.generate_excess_demand,
        toolbox.generate_profit,
        toolbox.generate_ema,
        toolbox.generate_margin,
    ),
    n=1,
)

toolbox.register(
    "generate_hyper_tf_individual2",
    tools.initRepeat,
    creator.individual,
    toolbox.generate_tf_strategy,
    n=1,
)


toolbox.register("generate_vi_strategy", random.randint, MIN_VALUATION, MAX_VALUATION)
toolbox.register(
    "generate_vi_individual",
    tools.initCycle,
    creator.individual,
    (
        toolbox.generate_vi_strategy,
        toolbox.generate_wealth,
        toolbox.generate_cash,
        toolbox.generate_asset,
        toolbox.generate_loan,
        toolbox.generate_trading_signal,
        toolbox.generate_excess_demand,
        toolbox.generate_profit,
        toolbox.generate_ema,
        toolbox.generate_margin,
    ),
    n=1,
)
toolbox.register(
    "vi_population_creation", tools.initRepeat, list, toolbox.generate_vi_individual
)

toolbox.register(
    "generate_vi_individual2",
    tools.initCycle,
    creator.individual,
    (toolbox.generate_vi_strategy),
    n=1,
)
toolbox.register(
    "vi_population_creation2", tools.initRepeat, list, toolbox.generate_vi_individual2
)


toolbox.register(
    "generate_hyper_vi_individual",
    tools.initCycle,
    creator.individual,
    (
        toolbox.generate_vi_strategy,
        toolbox.generate_wealth,
        toolbox.generate_cash,
        toolbox.generate_no_asset,
        toolbox.generate_loan,
        toolbox.generate_trading_signal,
        toolbox.generate_excess_demand,
        toolbox.generate_profit,
        toolbox.generate_ema,
        toolbox.generate_margin,
    ),
    n=1,
)

toolbox.register(
    "generate_hyper_vi_individual2",
    tools.initRepeat,
    creator.individual,
    toolbox.generate_vi_strategy,
    n=1,
)


def determine_mixed_strategy(PROBA_TF, PROBA_VI):
    global types
    rd = random.random()
    if rd <= PROBA_TF:
        types = np.vstack((types, "TF"))
        return toolbox.generate_tf_strategy()
    elif rd > PROBA_TF and rd <= PROBA_TF + PROBA_VI:
        types = np.vstack((types, "VI"))
        return toolbox.generate_vi_strategy()


toolbox.register("generate_mix_strategy", determine_mixed_strategy, PROBA_TF, PROBA_VI)


def create_mixed_population(POPULATION_SIZE, PROBA_TF, PROBA_VI):
    global types
    types = np.array(["NA"])

    def determine_mixed_strategy(PROBA_TF, PROBA_VI):
        global types
        rd = random.random()
        if rd <= PROBA_TF:
            types = np.vstack((types, "TF"))
            return toolbox.generate_tf_strategy()
        elif rd > PROBA_TF and rd <= PROBA_TF + PROBA_VI:
            types = np.vstack((types, "VI"))
            return toolbox.generate_vi_strategy()

    toolbox.register(
        "generate_mix_strategy", determine_mixed_strategy, PROBA_TF, PROBA_VI
    )
    # toolbox.register("generate_mix_individual", tools.initCycle, creator.individual,
    #                  (toolbox.generate_mix_strategy, toolbox.generate_wealth,
    #                   toolbox.generate_cash, toolbox.generate_asset,
    #                   toolbox.generate_loan, toolbox.generate_trading_signal,
    #                   toolbox.generate_excess_demand,toolbox.generate_profit,
    #                   toolbox.generate_ema, toolbox.generate_margin), n=1)
    toolbox.register(
        "generate_mix_individual",
        tools.initRepeat,
        creator.individual,
        toolbox.generate_mix_strategy,
        n=1,
    )
    toolbox.register(
        "mix_population_creation",
        tools.initRepeat,
        list,
        toolbox.generate_mix_individual,
    )
    pop = toolbox.mix_population_creation(n=POPULATION_SIZE)
    return pop, types


toolbox.register(
    "generate_hyper_mix_individual",
    tools.initCycle,
    creator.individual,
    (
        toolbox.generate_mix_strategy,
        toolbox.generate_wealth,
        toolbox.generate_cash,
        toolbox.generate_no_asset,
        toolbox.generate_loan,
        toolbox.generate_trading_signal,
        toolbox.generate_excess_demand,
        toolbox.generate_profit,
        toolbox.generate_ema,
        toolbox.generate_margin,
    ),
    n=1,
)


""" TO REMOVE """
# Fitness definition
def ema_fitness(individual):
    return (individual[8],)


toolbox.register("evaluate", ema_fitness)


# Fitness definition
def ema_fitness2(balance_sheet, index_list):
    # print("ema_fitnss2")
    fit_vec = []
    for i in index_list:
        fit_vec.append(balance_sheet[i, 7])
        # print(fit_vec)
    # return balance_sheet[index_list,7]
    return (fit_vec,)


toolbox.register("evaluate2", ema_fitness2)


def set_fitness(population, balance_sheet):
    for i in range(len(population)):
        print("i " + str(i))
        population[i].fitness = balance_sheet[i, 7]


def fitness_for_all(population, balance_sheet):
    index_list = []
    for i in range(len(population)):
        index_list.append(i)
    # print(invalid_index_list)
    # freshIndividuals = [ind for ind in population]
    freshFitnessValues = ema_fitness2(balance_sheet, index_list)
    # print("fresh fitness values ")
    # print(freshFitnessValues)

    for individual, fitnessValue in zip(population, freshFitnessValues):
        individual.fitness.values = fitnessValue

    # for i in range(len(population)):
    #     population[i].fitness.values = fitnessValue[i]
    print("Fitness value")
    print(fitnessValue)

    fitnessValues = fitnessValue.copy()
    return fitnessValues


# Function to recompute fitness of invalid individuals
def fitness_for_invalid(offspring):
    freshIndividuals = [ind for ind in offspring if not ind.fitness.valid]
    # print(freshIndividuals)
    # print(type(freshIndividuals))
    freshFitnessValues = list(map(toolbox.evaluate, freshIndividuals))
    # print(freshFitnessValues)
    for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
        individual.fitness.values = fitnessValue


# Function to recompute fitness of invalid individuals using balance sheet
def fitness_for_invalid2(population, balance_sheet):
    invalid_index_list = []
    for i in range(len(population)):
        if not population[i].fitness.valid:
            invalid_index_list.append(i)
    # print("invalid index list")
    # print(invalid_index_list) #this works

    freshIndividuals = [ind for ind in population if not ind.fitness.valid]
    # freshFitnessValues = list(map(toolbox.evaluate2, balance_sheet, invalid_index_list))
    freshFitnessValues = ema_fitness2(balance_sheet, invalid_index_list)
    print(freshFitnessValues)
    for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
        individual.fitness.values = fitnessValue


# Creating our own crossover operator:
def feasible_crossover(ind1, ind2, CROSSOVER_RATE):
    if random.random() < CROSSOVER_RATE:
        upperb = max(ind1, ind2)[0]
        lowerb = min(ind1, ind2)[0]
        ind1[0] = random.randint(lowerb, upperb)
        ind2[0] = random.randint(lowerb, upperb)
        return ind1[0], ind2[0]


toolbox.register("feasible_crossover", feasible_crossover)
toolbox.register("mate", toolbox.feasible_crossover)

# Creating our own mutation operator
def mutate_both_ways(ind):
    if random.random() < 0.5:
        ind[0] -= 1
    else:
        ind[0] += 1


def feasible_mutation(ind, MUTATION_RATE):
    if random.random() < MUTATION_RATE:
        if ind[0] == MAX_TIME_HORIZON:  # we can only mutate lower
            ind[0] -= 1
        elif ind[0] == 1:  # we can only mutate higher
            ind[0] += 1
        else:
            mutate_both_ways(ind)  # we can mutate lower or higher
    return ind


toolbox.register("feasible_mutation", feasible_mutation)
toolbox.register("mutate", toolbox.feasible_mutation)


def random_decimal(low, high):
    # number = float(random.randint(low*1000, high*1000))/1000
    global number
    if low >= 0 and high >= 0:
        number = float(random.randint(round(low * 1000), round(high * 1000)) / 1000)
    if low < 0 and high < 0:
        number = -float(random.randint(round(-low * 1000), round(-high * 1000)) / 1000)
    return number


def selRandom(individuals, k):
    return [random.choice(individuals) for i in range(k)]


# Creation of our customised selection operator (outnrament) that handles positive & negative fitness values
def selTournament(individuals, k, tournsize, fit_attr="fitness"):
    chosen = []
    for i in range(k):
        chosen_i = []
        aspirants = selRandom(individuals, tournsize - 1)
        aspirants.append(individuals[i])
        chosen_i = max(aspirants, key=attrgetter(fit_attr))
        chosen_i[1:10] = individuals[i][1:10]
        chosen.append(chosen_i)
    return chosen


toolbox.register("selTournament", selTournament)
toolbox.register("select", toolbox.selTournament)


""" TO REMOVE """
# Define the hypermutation (insolvency) parameter
round_replacements = 0


def hypermutate(pop):
    pop_temp = list(map(toolbox.clone, pop))
    round_replacements = 0
    for i in range(0, len(pop_temp)):
        # if pop_temp[i][1] + pop_temp[i][9] <= 0:
        if pop_temp[i][1] <= 0:
            pop_temp[i] = toolbox.generate_hyper_tf_individual()
            del pop_temp[i].fitness.values
            # global round_replacements
            round_replacements += 1
    pop[:] = pop_temp
    return pop, round_replacements


toolbox.register("hypermutate", hypermutate)

# Define the hypermutation (insolvency) parameter
def hypermutate2(pop_ex, pop_op, types, balance_sheet, mode):

    types_temp = np.copy(types)
    balance_sheet_temp = np.copy(balance_sheet)
    pop_ex_temp = pop_ex.copy()
    pop_op_temp = pop_op.copy()

    if mode == "extended":
        PROBA_TF = parameters.PROBA_TF
        PROBA_VI = parameters.PROBA_VI
        PROBA_GP = 0
    if mode == "open":
        PROBA_GP = 1
        PROBA_TF = 0
        PROBA_VI = 0
    if mode == "combined":
        PROBA_GP = parameters.PROBA_GP
        PROBA_TF = parameters.PROBA_TF
        PROBA_VI = parameters.PROBA_VI

    round_replacements = 0

    """ Hypermutate pop_ex """
    for i in range(0, POPULATION_SIZE):
        if balance_sheet[i][0] <= 0:
            # print("i = " + str(i))
            """Agent is insolvent. Delete"""
            if i < len(pop_ex):
                # del pop_ex_temp[i].fitness.values
                del pop_ex_temp[i].fitness
                del pop_ex_temp[i]
            elif i >= len(pop_ex):
                del pop_op_temp[i - len(pop_ex)].fitness.values
                del pop_op_temp[i - len(pop_ex)]

            balance_sheet_temp = np.delete(balance_sheet_temp, (i), axis=0)
            types_temp = np.delete(types_temp, (i), axis=0)

            """ Replace """
            ind_bs = np.array([0, INITIAL_CASH, INITIAL_ASSETS, 0, 0, 0, 0, 0, 0])
            balance_sheet_temp = np.vstack((balance_sheet_temp, ind_bs))

            # Draw the type to choose what pop and type to append
            if PROBA_GP == 1:

                """The incoming agent is of type GP"""
                # add = gp.create-population(.POPULATIOn_SIZE...)
                # pop_op_temp.append(add)
                types_temp = np.vstack((types_temp, "GP"))
                round_replacements += 1

            elif PROBA_TF == 1:

                """The incoming agent is of type TF"""
                pop_ex_temp.append(toolbox.generate_hyper_tf_individual2())
                types_temp = np.vstack((types_temp, "TF"))
                round_replacements += 1

            elif PROBA_VI == 1:
                """The incoming agent is of type VI"""

                pop_ex_temp.append(toolbox.generate_hyper_vi_individual2())
                types_temp = np.vstack((types_temp, "VI"))
                round_replacements += 1

            else:
                rd = random.uniform(0, PROBA_TF + PROBA_VI + PROBA_GP)
                if rd <= PROBA_TF:

                    types_temp = np.vstack((types_temp, "TF"))
                    round_replacements += 1
                    pop_ex_temp.append(toolbox.generate_hyper_tf_individual2())
                elif rd > PROBA_TF and rd <= PROBA_TF + PROBA_VI:

                    types_temp = np.vstack((types_temp, "VI"))
                    round_replacements += 1
                    pop_ex_temp.append(toolbox.generate_hyper_vi_individual2())
                elif rd > PROBA_TF + PROBA_VI:

                    # add = gp.create-population(.POPULATIOn_SIZE...)
                    # pop_op_temp.append(add)
                    types_temp = np.vstack((types_temp, "GP"))
                    round_replacements += 1

    pop_op = pop_op_temp.copy()
    pop_ex = pop_ex_temp.copy()
    balance_sheet = np.copy(balance_sheet_temp)
    types = np.copy(types_temp)

    return pop_ex, pop_op, types, balance_sheet, round_replacements
