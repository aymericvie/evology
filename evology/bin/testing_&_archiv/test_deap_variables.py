# # -*- coding: utf-8 -*-
# """
# Created on Fri Apr 16 09:19:15 2021

# @author: aymer
# """
# import random
# from deap import base
# from deap import creator
# from deap import tools
# toolbox = base.Toolbox()
# creator.create("fitness_strategy", base.Fitness, weights=(1.0,))
# creator.create("individual", list, typecode = 'd', fitness=creator.fitness_strategy)
# toolbox.register("generate_strategy", random.uniform, 0, 1)

# toolbox.register("generate_wealth", random.randint, 0, 1)

# toolbox.register("generate_individual", tools.initCycle, creator.individual,
#                  (toolbox.generate_strategy, toolbox.generate_wealth), n=1)
# toolbox.register("population_creation", tools.initRepeat, list, toolbox.generate_individual)


# pop = toolbox.population_creation(n=2)
# print(pop)
# print(type(pop))
# print(type(pop[0]))
# # Return fitness as the second list element
# def second_element_fitness(pop):
#     return pop[::1]
# toolbox.register("evaluate", second_element_fitness)
# print(second_element_fitness(pop))

# fitnessValues = list(map(toolbox.evaluate, pop))
# for individual, fitnessValue in zip(pop, fitnessValues):
#     individual.fitness.values = fitnessValue
# fitnessValues = [individual.fitness.values[0] for individual in pop]

# print(fitnessValues)


import random

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
#                      define 'attr_bool' to be an attribute ('gene')
#                      which corresponds to integers sampled uniformly
#                      from the range [0,1] (i.e. 0 or 1 with equal
#                      probability)
toolbox.register("attr_bool", random.randint, 0, 3)

# Structure initializers
#                         define 'individual' to be an individual
#                         consisting of 100 'attr_bool' elements ('genes')
toolbox.register(
    "individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 3
)

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evalOneMax(individual):
    print(type(sum(individual)))
    # return sum(individual),
    return (individual[1],)


# ----------
# Operator registration
# ----------
# register the goal / fitness function
toolbox.register("evaluate", evalOneMax)
pop = toolbox.population(n=3)
print(pop)
fitnesses = list(map(toolbox.evaluate, pop))
print(fitnesses)
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit
print(fit)
