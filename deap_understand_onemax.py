!pip install deap
from deap import base
from deap import creator
from deap import tools
import matplotlib.pyplot as plt

import random

import seaborn as sns

import time
start_time = time.time()

# problem constants:
ONE_MAX_LENGTH = 100  # length of bit string to be optimized

# Genetic Algorithm constants:
POPULATION_SIZE = 50
P_CROSSOVER = 0.2  # probability for crossover
P_MUTATION = 0.05   # probability for mutating an individual
MAX_GENERATIONS = 100

# set the random seed:
RANDOM_SEED = 9
random.seed(RANDOM_SEED)

toolbox = base.Toolbox()

##

# def func(a, b, c=3):
#     print (a, b, c)

# toolbox.register("myFunc", func, c=4)
# toolbox.myFunc(0,0)
# toolbox.unregister("myFunc")
# tools.myFunc(0,0)

###

# import random
# tools.initRepeat(list, random.random, 2)
# tools.initRepeat(list, random.random, 10)
# tools.initRepeat(list, random.randint, 1,5,2)
# toolbox.register("randint15", random.randint, 1, 5)
# tools.initRepeat(list, toolbox.randint15, 2)

# create an operator that randomly returns 0 or 1:
toolbox.register("zeroOrOne", random.randint, 0, 1)

# define a single objective, maximizing fitness strategy:
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# create the Individual class based on list:
creator.create("Individual", list, fitness=creator.FitnessMax)
#creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMax)

# create the individual operator to fill up an Individual instance:
toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, ONE_MAX_LENGTH)

# create the population operator to generate a list of individuals:
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)


# fitness calculation:
# compute the number of '1's in the individual
def oneMaxFitness(individual):
    return sum(individual),  # return a tuple


toolbox.register("evaluate", oneMaxFitness)

# genetic operators:

# Tournament selection with tournament size of 3:
toolbox.register("select", tools.selTournament, tournsize=3)

# Single-point crossover:
toolbox.register("mate", tools.cxOnePoint)

# Flip-bit mutation:
# indpb: Independent probability for each attribute to be flipped
toolbox.register("mutate", tools.mutFlipBit, indpb=1.0/ONE_MAX_LENGTH)


# Genetic Algorithm flow:
def main():

    # create initial population (generation 0):
    population = toolbox.populationCreator(n=POPULATION_SIZE)
    print(population)
    generationCounter = 0

    # calculate fitness tuple for each individual in the population:
    fitnessValues = list(map(toolbox.evaluate, population))  
    # print(fitnessValues)
    # print(type(fitnessValues[0]))
    for individual, fitnessValue in zip(population, fitnessValues):
        individual.fitness.values = fitnessValue
    # extract fitness values from all individuals in population:
    fitnessValues = [individual.fitness.values[0] for individual in population]
    # print(fitnessValues)
    # print(type(fitnessValues[0]))
    
    # fitnessValues = list(list(map(toolbox.evaluate, population))[0])
    # print(fitnessValues)
    # print(type(fitnessValues[0]))
    
    # initialize statistics accumulators:
    maxFitnessValues = []
    meanFitnessValues = []

    # main evolutionary loop:
    # stop if max fitness value reached the known max value
    # OR if number of generations exceeded the preset value:
    while max(fitnessValues) < ONE_MAX_LENGTH and generationCounter < MAX_GENERATIONS:
        # update counter:
        generationCounter = generationCounter + 1

        # apply the selection operator, to select the next generation's individuals:
        offspring = toolbox.select(population, len(population))
        # clone the selected individuals:
        offspring = list(map(toolbox.clone, offspring))
        # print(offspring)

        # apply the crossover operator to pairs of offspring:
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < P_CROSSOVER:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
            print(child1,child2)
        # print(offspring)

        for mutant in offspring:
            if random.random() < P_MUTATION:
                toolbox.mutate(mutant)
                # print("mutation")
                del mutant.fitness.values
        # print(offspring)

        # calculate fitness for the individuals with no previous calculated fitness value:
        freshIndividuals = [ind for ind in offspring if not ind.fitness.valid]
        freshFitnessValues = list(map(toolbox.evaluate, freshIndividuals))
        for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
            individual.fitness.values = fitnessValue
                

        # replace the current population with the offspring:
        population[:] = offspring


        # collect fitnessValues into a list, update statistics and print:
        fitnessValues = [ind.fitness.values[0] for ind in population]

        maxFitness = max(fitnessValues)
        meanFitness = sum(fitnessValues) / len(population)
        maxFitnessValues.append(maxFitness)
        meanFitnessValues.append(meanFitness)
        print("- Generation {}: Max Fitness = {}, Avg Fitness = {}".format(generationCounter, maxFitness, meanFitness))

        # find and print best individual:
        best_index = fitnessValues.index(max(fitnessValues))
        print("Best Individual = ", *population[best_index], "\n")

        best_ind = tools.selBest(population, 1)[0]
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    # Genetic Algorithm is done - plot statistics:
    sns.set_style("whitegrid")
    plt.plot(maxFitnessValues, color='red', label='Maximum fitness')
    plt.plot(meanFitnessValues, color='green', label = 'Average fitness')
    plt.xlabel('Iteration')
    plt.ylabel('Max / Average Fitness')
    plt.title('Max and Average Fitness over Generations')
    plt.ylim(0,ONE_MAX_LENGTH)
    plt.legend()
    plt.savefig('filename.eps')
    plt.show()

if __name__ == '__main__':
    main()


print("--- %s seconds ---" % (time.time() - start_time))














