from math import nan
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from operator import attrgetter
from creation import *
import timeit
import warnings
import cythonized


def CreateFractionalFund(pop, MaxFund, divisions):

    if pop[MaxFund].type == "nt":
        half = IndCreation("nt")
    elif pop[MaxFund].type == "vi":
        half = IndCreation("vi")
    elif pop[MaxFund].type == "tf":
        half = IndCreation("tf")
    else:
        # MaxFund is AV, BH or IR
        half = IndCreation("vi")

    # Copy fund MaxFund intangible characteristics
    # TSV, EDF, EDV are totally reset.
    half.tsv = 0.0
    # half.edf = None
    half.edv = 0.0
    half.strategy = pop[MaxFund].strategy
    # half.process = pop[MaxFund].process
    half.ema = pop[MaxFund].ema
    half.fitness = pop[MaxFund].fitness
    half.val = pop[MaxFund].val
    half.val_net = pop[MaxFund].val_net
    half.age = 0
    half.profit = 0.0

    # Copy fund j characteristics to be divided
    half.prev_wealth = pop[MaxFund].prev_wealth / divisions
    half.wealth = pop[MaxFund].wealth / divisions
    half.cash = pop[MaxFund].cash / divisions
    half.loan = pop[MaxFund].loan / divisions
    half.asset = pop[MaxFund].asset / divisions
    half.margin = pop[MaxFund].margin / divisions
    return half


def hypermutate(pop, spoils, replace):
    round_replacements = 0

    if replace == 1:
        InitialPopSize = len(pop)
        i = 0

        index_to_replace = []
        wealth_list = []
        for i, ind in enumerate(pop):
            wealth_list.append(pop[i].wealth)
            if ind.wealth < 0:
                index_to_replace.append(i)

        MaxFund = wealth_list.index(max(wealth_list))
        NumberReplace = len(index_to_replace)

        if NumberReplace == len(pop):
            warnings.warn("Evology wiped out")
            round_replacements = -1
            return pop, round_replacements, spoils

        elif NumberReplace != 0:
            for index in index_to_replace:
                # print("Replaced " + str(pop[index].type) + "; " + str(round(pop[index].wealth)) + "; " + str(round(pop[index].asset)))
                half = CreateFractionalFund(pop, MaxFund, NumberReplace + 1)
                spoils += pop[index].asset
                del pop[index]
                pop.insert(index, half)
                round_replacements += 1
            # FInally, add the last subdivision in place of the maximum fund.
            half = CreateFractionalFund(pop, MaxFund, NumberReplace + 1)
            del pop[MaxFund]
            pop.insert(MaxFund, half)
        # Check that the new population size is unchanged.
        if len(pop) != InitialPopSize:
            print([NumberReplace, round_replacements])
            raise ValueError(
                "After replace and split, population size changed. " + str(len(pop))
            )

        if NumberReplace != round_replacements:
            print([NumberReplace, round_replacements])
            raise ValueError("Mismatch number replace and round replacements")

        # Check that we did not leave anyone with a negative wealth
        for ind in pop:
            if ind.wealth < 0:
                raise ValueError("Insolvent funds after hypermutation.")

    return pop, round_replacements, spoils


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
    raise ValueError("Not updated to ind.strategy")
    if np.random.random() < 0.5:
        ind[0] -= 1
    else:
        ind[0] += 1


def feasible_mutation(ind, MUTATION_RATE):
    raise ValueError("Not updated to ind.strategy")
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


def strategy_evolution(space, pop, PROBA_SELECTION, MUTATION_RATE, wealth_coordinates):

    TowardsNT = 0
    TowardsVI = 0
    TowardsTF = 0
    FromNT = 0
    FromVI = 0
    FromTF = 0
    CountSelected = 0
    CountMutated = 0
    CountCrossed = 0

    if PROBA_SELECTION > 0 or MUTATION_RATE > 0:

        if space == "scholl":
            # Individuals can select & imitate, and switch

            # Selection
            if PROBA_SELECTION > 0:
                SelectionRd = np.random.rand(len(pop))
                for i in range(len(pop)):
                    if SelectionRd[i] < PROBA_SELECTION:  # Social learning
                        # Create the tournament and get the winner
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
                        # pop[i].leverage = winner.leverage

            # Mutation
            if MUTATION_RATE > 0:
                types = ["nt", "vi", "tf"]

                # cum_proba = [0, 0, 0]
                # cum_proba[0] = wealth_coordinates[0]
                # i = 1
                # while i < len(wealth_coordinates):
                #     cum_proba[i] = cum_proba[i - 1] + wealth_coordinates[i]
                #     if cum_proba[i] > 1.0001:
                #         raise ValueError("Cum proba > 1 " + str(cum_proba))
                #     i += 1
                # if sum(cum_proba) == 0:
                #     raise ValueError("Sum cumproba = 0")
                cum_proba = np.cumsum(wealth_coordinates)

                MutationRd = np.random.rand(len(pop))
                for i in range(len(pop)):
                    if MutationRd[i] < MUTATION_RATE:
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
            if MUTATION_RATE > 0 or PROBA_SELECTION > 0:
                raise ValueError(
                    "Strategy evolution for extended space is not yet implemented."
                )

    StratFlow = [TowardsNT, TowardsVI, TowardsTF, FromNT, FromVI, FromTF]

    return pop, CountSelected, CountMutated, CountCrossed, StratFlow
