from math import nan
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from operator import attrgetter
from creation import *
import balance_sheet as bs
import timeit
import warnings

import cythonized

"""
def adjust_mode(pop, mode):
    if mode == "between":
        for ind in pop:
            if ind.type == "tf":
                ind[0] = 2
            if ind.type == "vi":
                ind[0] = 100
            if ind.type == "nt":
                ind[0] = 100
    return pop"""


def hypermutate(
    pop, mode, asset_supply, current_price, generation, spoils, wealth_coordinates
):

    round_replacements = 0
    """ 
    hyperm = False

    if hyperm == True:
        for i in range(0, len(pop)):
            
            if pop[i].wealth < 0:
                warnings.warn("Replacing // Gen " + str(generation) + " // Type: " + str(pop[i].type) + ", C: " + str(int(pop[i].cash)) + ", S+: " + str(int(pop[i].asset)) + ", L: " + str(int(pop[i].loan)) + ", M: " + str(int(pop[i].margin)) + ", W: " + str(int(pop[i].wealth)))
                spoils += pop[i].asset
                pop[i] = toolbox.gen_rd_ind(wealth_coordinates)
                pop[i].cash = 50_000_000
                pop[i].wealth = pop[i].cash + pop[i].asset * current_price - pop[i].loan
                pop[i].MonWealth = np.zeros((1, 21))[0]
                pop[i].prev_wealth = 0
                del pop[i].fitness.values
                round_replacements += 1
        
        if mode == "between":
            pop = adjust_mode(pop, mode)

    if hyperm == False:
        replaced = False
        ReplacedCount = 0
        for ind in pop:
            if ind.wealth < 0:
                ReplacedCount += 1
                replaced = True
                ind.loan -= 2 * abs(ind.wealth)
                ind.wealth = ind.cash + ind.asset * current_price - ind.loan
                    
        if replaced == True:
            print('Bailed out today (' + str(ReplacedCount) + ').')

    """

    """ 
    Bailing out: helps funds who performed poorly, distrubs wealth shares, returns and the nature of interactions 
        (losing could lead to winning the bailout money!)
    Simple replacement: leads to inject new wealth in the system, disturb wealth shares as it weakens the 
        relative wealth of surviving funds
    Simple removal: no bias on wealth shares or the quantity of wealth in circulation ; but it may lead in situations
        where the population size shreds up to 1, or situations of hyperconcentration of wealth that are neither realistic
        not desirable for the robustness of results. 

    Our suggestion: simple removal of the insolvent fund AND the wealthiest fund splits in half. IN this way, we have no 
        bias on the wealth shares, the returns of the strategy. In addition, it adds a security against hyperconcentration of wealth.
        Splitting a fund in half is neutral on market clearing and wealth shares in the population, and maintains its size constant.
    WARNING: every attribute needs to be divided by half, including the previous wealth.   
    """
    InitialPopSize = len(pop)
    i = 0
    while i < len(pop):
        if pop[i].wealth < 0:  # The fund is insolvent and we will remove it.
            round_replacements += 1
            # Mandate an administrator to liquidate the insolvent fund shares
            spoils += pop[i].asset
            del pop[i]  # We suppress the fund.

            # Determine who is the wealthiest fund
            MaxWealth = 0
            MaxFund = 999
            for j in range(len(pop)):
                if pop[j].wealth >= MaxWealth:
                    MaxFund = j
            if MaxFund > len(pop):
                raise ValueError(
                    "MaxFund is higher than len pop "
                    + str(MaxFund)
                    + "/"
                    + str(len(pop))
                    + "/"
                    + str(MaxWealth)
                )

            # Wealthiest fund is fund index MaxFund. Create two halfs of fund, sharing the attributes.
            for k in range(2):
                # Create a fund of the correct strategy
                if pop[MaxFund].type == "nt":
                    half = IndCreation("nt")
                if pop[MaxFund].type == "vi":
                    half = IndCreation("vi")
                if pop[MaxFund].type == "tf":
                    half = IndCreation("tf")

                # Copy fund MaxFund intangible characteristics
                # TSV, EDF, EDV are totally reset.
                half.tsv = 0
                half.edf = None
                half.edv = 0
                half.strategy = pop[MaxFund].strategy
                half.process = pop[MaxFund].process
                half.ema = pop[MaxFund].ema
                half.fitness = pop[MaxFund].fitness
                half[0] = pop[MaxFund][0]
                half.age = 0.0

                # Copy fund j characteristics to be divided
                half.prev_wealth = pop[MaxFund].prev_wealth / 2
                half.wealth = pop[MaxFund].wealth / 2
                half.cash = pop[MaxFund].cash / 2
                half.loan = pop[MaxFund].loan / 2
                half.asset = pop[MaxFund].asset / 2
                half.margin = pop[MaxFund].margin / 2
                half.profit = pop[MaxFund].profit / 2

                # Add the half copy to the population
                pop.append(half)

            # We have appended the two half-copies of j. We remove j.
            del pop[MaxFund]
            i = 0
        if pop[i].wealth >= 0:
            i += 1

    # Check that the new population size is unchanged.
    if len(pop) != InitialPopSize:
        raise ValueError(
            "After replace and split, population size changed. " + str(len(pop))
        )

    # Check that we did not leave anyone with a negative wealth
    for ind in pop:
        if ind.wealth < 0:
            raise ValueError("Insolvent funds after hypermutation.")

    return pop, round_replacements, spoils


def compute_fitness(pop):
    for ind in pop:

        ema = (2 / (EMA_HORIZON + 1)) * (ind.profit + ind.investor_flow - ind.ema) + ind.ema
        ind.ema = ema
        ind.fitness.values = (ema,)
    return ind


# Creating our own crossover operator:
def feasible_crossover(ind1, ind2, CROSSOVER_RATE):
    if ind1.type == ind2.type:
        if np.random.random() < CROSSOVER_RATE:
            upperb = max(ind1, ind2)[0]
            lowerb = min(ind1, ind2)[0]
            ind1[0] = np.random.randint(lowerb, upperb + 1)
            ind2[0] = np.random.randint(lowerb, upperb + 1)
    return ind1[0], ind2[0]


toolbox.register("feasible_crossover", feasible_crossover)
toolbox.register("mate", toolbox.feasible_crossover)

# Creating our own mutation operator
def mutate_both_ways(ind):
    if np.random.random() < 0.5:
        ind[0] -= 1
    else:
        ind[0] += 1


def feasible_mutation(ind, MUTATION_RATE):
    if np.random.random() < MUTATION_RATE:
        if ind.type == "tf":
            if ind[0] == MAX_THETA:  # we can only mutate lower
                ind[0] -= 1
            elif ind[0] == MIN_THETA:  # we can only mutate higher
                ind[0] += 1
            else:
                mutate_both_ways(ind)  # we can mutate lower or higher
        if ind.type == "vi":
            if ind[0] == MAX_RR_VI:  # we can only mutate lower
                ind[0] -= 1
            elif ind[0] == MIN_RR_VI:  # we can only mutate higher
                ind[0] += 1
            else:
                mutate_both_ways(ind)  # we can mutate lower or higher
        if ind.type == "nt":
            if ind[0] == MAX_RR_NT:  # we can only mutate lower
                ind[0] -= 1
            elif ind[0] == MIN_RR_NT:  # we can only mutate higher
                ind[0] += 1
            else:
                mutate_both_ways(ind)  # we can mutate lower or higher
    return ind


toolbox.register("feasible_mutation", feasible_mutation)
toolbox.register("mutate", toolbox.feasible_mutation)


def random_decimal(low, high):
    global number
    if low >= 0 and high >= 0:
        number = float(
            np.random.randint(round(low * 1000), round((high + 1) * 1000)) / 1000
        )
    if low < 0 and high < 0:
        number = -float(
            np.random.randint(round(-low * 1000), round((-high - 1) * 1000)) / 1000
        )
    return number


def selRandom(pop, k):
    aspirants = np.random.choice(np.array(pop).flatten(), size=k)
    if len(aspirants) != k:
        raise ValueError(
            "Length of aspirants after selRandom does not match intended tournament size. "
            + str(k)
            + ","
            + str(len(aspirants))
        )
    return aspirants


def strategy_evolution(
    mode, space, pop, PROBA_SELECTION, MUTATION_RATE, wealth_coordinates, generation
):

    CountSelected = 0
    CountMutated = 0
    CountCrossed = 0
    TowardsNT = 0
    TowardsVI = 0
    TowardsTF = 0
    FromNT = 0
    FromVI = 0
    FromTF = 0

    if mode == "between":

        if space == "scholl":
            # Individuals can select & imitate, and switch

            # Selection
            for i in range(len(pop)):
                if np.random.random() < PROBA_SELECTION:  # Social learning
                    # Create the tournament and get the winner
                    # aspirants = selRandom(pop, TOURNAMENT_SIZE-1)
                    # print(aspirants)
                    # aspirant = np.append(aspirants,pop[i])
                    # print(aspirants)
                    winner = max(pop, key=attrgetter("fitness"))

                    # Imitate the winner's type and strategy
                    if pop[i].type != winner.type:
                        CountSelected += 1
                        # TODO: Collect data on the types being adopted / discarded?
                        if pop[i].type == "nt":
                            FromNT += 1
                        if pop[i].type == "vi":
                            FromVI += 1
                        if pop[i].type == "tf":
                            FromTF += 1
                        if winner.type == "nt":
                            TowardsNT += 1
                        if winner.type == "vi":
                            TowardsVI += 1
                        if winner.type == "tf":
                            TowardsTF += 1

                        # warnings.warn('Ind ' + str(pop[i].type) + ' switched to ' + str(winner.type) + ' at time ' + str(generation))
                    pop[i].type = winner.type
                    type_num = cythonized.convert_ind_type_to_num(winner.type)
                    pop[i].type_as_int = type_num
                    pop[i][0] = winner[0]
                    pop[i].leverage = winner.leverage

            # Mutation
            types = ["nt", "vi", "tf"]
            cum_proba = [0, 0, 0]
            cum_proba[0] = wealth_coordinates[0]
            i = 1
            while i < len(wealth_coordinates):
                cum_proba[i] = cum_proba[i - 1] + wealth_coordinates[i]
                if cum_proba[i] > 1.0001:
                    raise ValueError("Cum proba > 1 " + str(cum_proba))
                i += 1
            if sum(cum_proba) == 0:
                raise ValueError("Sum cumproba = 0")

            for i in range(len(pop)):
                if np.random.random() < MUTATION_RATE:
                    CountMutated += 1
                    # Change type totally randomly
                    n = np.random.random()
                    ty = 0
                    while cum_proba[ty] < n:
                        ty += 1
                    pop[i].type = types[ty]
                    type_num = cythonized.convert_ind_type_to_num(types[ty])
                    pop[i].type_as_int = type_num
                    if pop[i].type == "tf":
                        pop[i][0] = 2
                    elif pop[i].type == "nt" or pop[i].type == "vi":
                        pop[i][0] = 100

        if space == "extended":
            raise ValueError(
                "Strategy evolution for extended space is not yet implemented."
            )
    StratFlow = [TowardsNT, TowardsVI, TowardsTF, FromNT, FromVI, FromTF]

    return pop, CountSelected, CountMutated, CountCrossed, StratFlow
