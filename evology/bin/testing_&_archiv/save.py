# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 11:01:00 2021

@author: aymeric vie
"""

# =============================================================================
# Imports
# =============================================================================

from deap import base
from deap import creator
from deap import tools
import random
import seaborn as sns

sns.set_theme(style="darkgrid")
import numpy as np
import matplotlib.pyplot as plt
from operator import attrgetter

# =============================================================================
# Fixed parameters
# =============================================================================

RANDOM_SEED = random.random()
POPULATION_SIZE = 2
MAX_TIME_HORIZON = 10
MUTATION_RATE = 0
MAX_GENERATIONS = 2
CROSSOVER_RATE = 0
INITIAL_WEALTH = 11
MIN_WEALTH = 1
MAX_WEALTH = 4
MIN_TIME_HORIZON = 1

# =============================================================================
# Setup the evolutionary operators
# =============================================================================

toolbox = base.Toolbox()

# Create the fitness object
creator.create("fitness_strategy", base.Fitness, weights=(1.0,))
# Create the individual object
creator.create("individual", list, fitness=creator.fitness_strategy)  # , wealth = None)

# Z Create the individual list
toolbox.register(
    "generate_strategy", random.randint, MIN_TIME_HORIZON, MAX_TIME_HORIZON
)
# toolbox.register("generate_wealth", random.randint, INITIAL_WEALTH, INITIAL_WEALTH)
toolbox.register("generate_wealth", random.randint, MIN_WEALTH, MAX_WEALTH)
toolbox.register(
    "generate_individual",
    tools.initCycle,
    creator.individual,
    (toolbox.generate_strategy, toolbox.generate_wealth),
    n=1,
)
toolbox.register(
    "population_creation", tools.initRepeat, list, toolbox.generate_individual
)

# Temporary Fitness definition
def max_horizon_fitness(individual):
    return individual


toolbox.register("evaluate", max_horizon_fitness)

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


# Creation of our customised selection operator
def selRoulette_first_item(individuals, k, fit_attr="fitness"):
    """Select *k* individuals from the input *individuals* using *k*
    spins of a roulette. The selection is made by looking only at the first
    objective of each individual. The list returned contains references to
    the input *individuals*.
    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :param fit_attr: The attribute of individuals to use as selection criterion
    :returns: A list of selected individuals.
    This function uses the :func:`~random.random` function from the python base
    :mod:`random` module.
    .. warning::
       The roulette selection by definition cannot be used for minimization
       or when the fitness can be smaller or equal to 0.
    """

    s_inds = sorted(individuals, key=attrgetter(fit_attr), reverse=True)
    sum_fits = sum(getattr(ind, fit_attr).values[0] for ind in individuals)
    chosen = []
    for i in range(k):
        u = random.random() * sum_fits
        sum_ = 0
        for ind in s_inds:
            sum_ += getattr(ind, fit_attr).values[0]
            if sum_ > u:
                print(str(i) + " i is")
                print(str(ind) + " was selected")
                # ind = [ind[0],individuals[i][1]]
                # Otherwise, selection copies both strategy and wealth; agents can win wealth from nothing
                # issue: the result is not an individual, so has no fitness attribute
                # idea: create a new individual
                # ind_sel.fitness.values = ind.fitness.values
                print("wealth is " + str(individuals[i][1]))
                MIN_WEALTH = individuals[i][1]
                MAX_WEALTH = individuals[i][1]
                MIN_TIME_HORIZON = ind[0]
                MAX_TIME_HORIZON = ind[0]
                print("theta is " + str(MAX_TIME_HORIZON))
                # okay above works. Now the generate individuals does not behave as expected.
                ind_sel = toolbox.generate_individual()
                print(toolbox.generate_strategy())
                print(str(ind_sel) + " was added to chosen")
                chosen.append(ind_sel)
                # chosen.append(ind)
                break

            # also need to cancel these changes
    return chosen


toolbox.register("selRoulette_first_item", selRoulette_first_item)
toolbox.register("select", toolbox.selRoulette_first_item)

# toolbox.register("select", tools.selRoulette)

# Define the hypermutation (insolvency) parameter
round_replacements = 0


def hypermutate(pop):
    pop_temp = list(map(toolbox.clone, pop))

    for i in range(0, len(pop_temp)):
        if pop_temp[i][1] <= 0:
            pop_temp[i] = toolbox.generate_individual()
            del pop_temp[i].fitness.values
            global round_replacements
            round_replacements += 1
    pop[:] = pop_temp
    return pop


toolbox.register("hypermutate", hypermutate)

# =============================================================================
# Define the main evolutionary loop
# =============================================================================


def main():
    random.seed(RANDOM_SEED)

    # Create the population and the results accumulators
    pop = toolbox.population_creation(n=POPULATION_SIZE)
    initial_pop = pop.copy()
    generationCounter = 1
    maxFitnessValues = []
    meanFitnessValues = []
    replacements = []

    fitnessValues = list(map(toolbox.evaluate, pop))
    for individual, fitnessValue in zip(pop, fitnessValues):
        individual.fitness.values = fitnessValue
    fitnessValues = [individual.fitness.values[0] for individual in pop]

    maxFitness = max(fitnessValues)
    meanFitness = sum(fitnessValues) / len(pop)
    maxFitnessValues.append(maxFitness)
    meanFitnessValues.append(meanFitness)
    replacements.append(0)

    while generationCounter < MAX_GENERATIONS:
        print("--------------------------")
        print("Iteration " + str(generationCounter))
        generationCounter += 1
        print(pop)

        # Hypermutation
        global round_replacements
        round_replacements = 0
        hypermutate(pop)
        # Recomputing fitness
        freshIndividuals = [ind for ind in pop if not ind.fitness.valid]
        freshFitnessValues = list(map(toolbox.evaluate, freshIndividuals))
        for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
            individual.fitness.values = fitnessValue
        print("After hypermutation")
        print(pop)

        # Selection
        offspring = toolbox.select(pop, POPULATION_SIZE)
        print("offspring after select")
        print(offspring)
        freshIndividuals = [ind for ind in offspring if not ind.fitness.valid]
        freshFitnessValues = list(map(toolbox.evaluate, freshIndividuals))
        for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
            individual.fitness.values = fitnessValue
        offspring = list(map(toolbox.clone, offspring))
        print("offspring after fitness and clone")
        print(offspring)

        # Crossover
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            toolbox.mate(child1, child2, CROSSOVER_RATE)
            del child1.fitness.values
            del child2.fitness.values

        # Mutation
        for mutant in offspring:
            toolbox.mutate(mutant, MUTATION_RATE)
            del mutant.fitness.values

        # Recomputing fitness
        freshIndividuals = [ind for ind in offspring if not ind.fitness.valid]
        freshFitnessValues = list(map(toolbox.evaluate, freshIndividuals))
        for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
            individual.fitness.values = fitnessValue

        # Replacing
        pop[:] = offspring
        print("pop after replacing")
        print(pop)
        fitnessValues = [ind.fitness.values[0] for ind in pop]

        # I know what the issue is. THe selection operator at L190 copies the wealth of the most succesful agent.

        # Print some results
        maxFitness = max(fitnessValues)
        meanFitness = sum(fitnessValues) / len(pop)
        maxFitnessValues.append(maxFitness)
        meanFitnessValues.append(meanFitness)
        replacements.append(round_replacements)
        print(
            "- Generation {}: Max Fitness = {}, Avg Fitness = {}".format(
                generationCounter, maxFitness, meanFitness
            )
        )

        # Temporary function to apply some fixed cost
        if generationCounter > 0:
            for ind in pop:
                ind[1] -= 1

    return initial_pop, pop, maxFitnessValues, meanFitnessValues, replacements


# =============================================================================
# Exploit the results
# =============================================================================

initial_pop, pop, maxFitnessValues, meanFitnessValues, replacements = main()

# Plot population histograms at the start and at the end
print("--------------------------")
print("--------------------------")
print("--------------------------")
print("Initial population was " + str(initial_pop))
sns.histplot(
    data=np.array(initial_pop),
    legend=False,
    stat="density",
    shrink=0.85,
    discrete=True,
    binrange=(1, 10),
)
plt.show()
print("Current population is " + str(pop))
sns.histplot(
    data=np.array(pop),
    legend=False,
    stat="density",
    shrink=0.85,
    discrete=True,
    binrange=(1, 10),
)
plt.show()

# Plot the fitness evolution over time
plt.plot(maxFitnessValues, color="red", label="Maximum fitness")
plt.plot(meanFitnessValues, color="green", label="Average fitness")
plt.plot(replacements, color="black", label="Hypermutations")
# plt.plot(np.mean(pop, axis =1), color='orange', label = 'Wealth')
plt.xlabel("Generations")
plt.ylabel("Max / Average Fitness")
plt.title("Max and Average Fitness over Generations")
plt.ylim(0, MAX_TIME_HORIZON + 1)
plt.xlim(0, MAX_GENERATIONS + 1)
plt.legend()
plt.show()
