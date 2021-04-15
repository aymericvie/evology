# =============================================================================
# Imports
# =============================================================================

from deap import base
from deap import creator
from deap import tools
import random
import math
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
MUTATION_RATE = 0.05
MAX_GENERATIONS = 50
CROSSOVER_RATE = 0.5
MIN_WEALTH = 10
MAX_WEALTH = 10
MIN_TIME_HORIZON = 1
INITIAL_PRICE = 1

REINVESTMENT_RATE = 1
INTEREST_RATE = 0.1

EMA_HORIZON = 20 #♣252

# =============================================================================
# Setup the evolutionary operators
# =============================================================================

# Agent representaiton:
#     [Theta Wealth Cash Asset Loan TradingSignal ExcessDemand     Profit     EMA profit]
#     [ 0       1     2    3     4         5             6           7            8 ]

toolbox = base.Toolbox()

# Create the fitness object
creator.create("fitness_strategy", base.Fitness, weights=(1.0,))
# Create the individual object
creator.create("individual", list, typecode = 'd', fitness=creator.fitness_strategy)
# Create the individual list 
toolbox.register("generate_strategy", random.randint, MIN_TIME_HORIZON, MAX_TIME_HORIZON)
toolbox.register("generate_wealth", random.randint, 0, 0)
toolbox.register("generate_cash", random.randint, 1, 5)
toolbox.register("generate_asset", random.randint, 1, 5)
toolbox.register("generate_loan", random.randint, 0, 0)
toolbox.register("generate_trading_signal", random.randint, 0, 0)
toolbox.register("generate_excess_demand", random.randint, 0, 0)
toolbox.register("generate_profit", random.randint, 0, 0)
toolbox.register("generate_ema", random.randint, 0, 0)

toolbox.register("generate_individual", tools.initCycle, creator.individual, 
                 (toolbox.generate_strategy, toolbox.generate_wealth, toolbox.generate_cash, 
                  toolbox.generate_asset, toolbox.generate_loan, toolbox.generate_trading_signal, 
                  toolbox.generate_excess_demand,toolbox.generate_profit,toolbox.generate_ema), n=1)
toolbox.register("population_creation", tools.initRepeat, list, toolbox.generate_individual)


'''
For the initialisation:
    - Wealth is not determined first, it will depend on cash asset and loan
    - Cash and Assets are initialiased at 50-50
    - @Maarten: what price? what initial wealth amount?
    - I am temporarily setting cash as 5, asset as 5 and initial price as 1
'''

# Temporary Fitness definition
def max_horizon_fitness(individual):
    return individual
toolbox.register("evaluate", max_horizon_fitness)
# def max_horizon_fitness(pop):
#     for ind in pop:
#         print(ind)
#         # return ind[8]


# Creating our own crossover operator:
def feasible_crossover(ind1,ind2,CROSSOVER_RATE):
    if random.random() < CROSSOVER_RATE:
        upperb = max(ind1,ind2)[0]
        lowerb = min (ind1,ind2)[0]
        ind1[0] = random.randint(lowerb,upperb)
        ind2[0] = random.randint(lowerb,upperb)
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
        if ind[0] == MAX_TIME_HORIZON: #we can only mutate lower
            ind[0] -= 1
        elif ind[0] == 1: #we can only mutate higher
            ind[0] += 1
        else: 
            mutate_both_ways(ind) # we can mutate lower or higher
    return(ind)

toolbox.register("feasible_mutation", feasible_mutation)
toolbox.register("mutate", toolbox.feasible_mutation)

def random_decimal(low, high):
    # number = float(random.randint(low*1000, high*1000))/1000
    global number
    if low >= 0 and high >= 0:
        number = float(random.randint(round(low*1000),round(high*1000))/1000)
    if low < 0 and high < 0:
        number = - float(random.randint(round(-low*1000),round(-high*1000))/1000)
    return number

# Creation of our customised selection operator
def selRoulette_first_item (individuals, k, fit_attr="fitness"):
    s_inds = sorted(individuals, key=attrgetter(fit_attr), reverse=True)
    sum_fits = sum(getattr(ind, fit_attr).values[0] for ind in individuals)
    chosen = []
    for i in range(k):
        u = random.random() * sum_fits
        sum_ = 0
        for ind in s_inds:
            sum_ += getattr(ind, fit_attr).values[0]
            if sum_ > u:
                toolbox.register("generate_wealth_selection", random_decimal, individuals[i][1], individuals[i][1])
                toolbox.register("generate_strategy_selection", random_decimal, ind[0], ind[0])
                toolbox.register("generate_cash_selection", random_decimal, individuals[i][2], individuals[i][2])
                toolbox.register("generate_asset_selection", random_decimal, individuals[i][3], individuals[i][3])
                toolbox.register("generate_loan_selection", random_decimal, individuals[i][4], individuals[i][4])
                toolbox.register("generate_trading_signal_selection", random_decimal, individuals[i][5], individuals[i][5])
                toolbox.register("generate_excess_demand_selection", random_decimal, individuals[i][6], individuals[i][6])
                # print(toolbox.generate_excess_demand_selection())
                toolbox.register("generate_profit_selection", random_decimal, individuals[i][7], individuals[i][7])
                # print(individuals[i][7])
                # print(random.randint(round(individuals[i][7]*1000),round(individuals[i][7]*1000)))
                # print(float(random.randint(round(individuals[i][7]*1000),round(individuals[i][7]*1000))/1000))
                # print(toolbox.generate_profit_selection())
                toolbox.register("generate_ema_selection", random_decimal, individuals[i][8], individuals[i][8])
                toolbox.register("generate_individual_selection", tools.initCycle, creator.individual,
                 (toolbox.generate_strategy_selection, toolbox.generate_wealth_selection, toolbox.generate_cash_selection, 
                  toolbox.generate_asset_selection, toolbox.generate_loan_selection, toolbox.generate_trading_signal_selection, 
                  toolbox.generate_excess_demand_selection, toolbox.generate_profit_selection, toolbox.generate_ema_selection), n=1)

                # Is there a simpler wayN Just copy ind_sel = individuals[i] and only modify ind_sel[0] by ind[0]?
                ind_sel = toolbox.generate_individual_selection()
                chosen.append(ind_sel)

                break
    return chosen

toolbox.register("selRoulette_first_item", selRoulette_first_item)
toolbox.register("select", toolbox.selRoulette_first_item)

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

# Function to recompute fitness of invalid individuals
def fitness_for_invalid(offspring):
    freshIndividuals = [ind for ind in offspring if not ind.fitness.valid]
    freshFitnessValues = list(map(toolbox.evaluate, freshIndividuals))
    for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
        individual.fitness.values = fitnessValue


# Agent representaiton:
#     [Theta Wealth Cash Asset Loan TradingSignal ExcessDemand]
#     [ 0       1     2    3     4         5             6    ]

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def draw_dividend():
    '''
    @Maarten: issues with the equations defining  the dividend process
    I temporarily have a random dividend in (0,1)
    '''
    global dividend
    dividend = truncate(random.randint(-3,3),3)
    print("Dividend today is " + str(dividend))
    return dividend

        
def wealth_earnings(pop):
    for ind in pop:
        # Update profit
        ind[7] = truncate(REINVESTMENT_RATE * (INTEREST_RATE * ind[2] + dividend * ind[3]),3)
        print("profit is " + str(ind[7]))
        
        # Update cash
        ind[2] += REINVESTMENT_RATE * (INTEREST_RATE * ind[2] + dividend * ind[3])
        ind[2] = truncate(ind[2],3)
    return ind

def update_wealth(pop, price):
    for ind in pop:
        ind[1] = truncate(ind[2] + ind[3] * price  - ind[4],3)
    return ind
        
def compute_ema(pop):
    for ind in pop:
        ind[8] = (2 / (EMA_HORIZON + 1)) * (ind[7] - ind[8]) + ind[8]
    return ind
    
# =============================================================================
# Define the main evolutionary loop
# =============================================================================

def main():
    random.seed(RANDOM_SEED)
    
    # Create the population and the results accumulators
    pop = toolbox.population_creation(n=POPULATION_SIZE)
    initial_pop = pop.copy()
    generationCounter = 1
    price = INITIAL_PRICE
    maxFitnessValues = []
    meanFitnessValues = []
    replacements = []
    
    # Temp
    agent0_profit = []
    agent0_ema = []
    
    print(pop)
    
    fitnessValues = list(map(toolbox.evaluate, pop))
    for individual, fitnessValue in zip(pop, fitnessValues):
        individual.fitness.values = fitnessValue
    fitnessValues = [individual.fitness.values[0] for individual in pop]
    
    maxFitness = max(fitnessValues)
    meanFitness = sum(fitnessValues) / len(pop)
    maxFitnessValues.append(maxFitness)
    meanFitnessValues.append(meanFitness)
    replacements.append(0)
    # Temp
    agent0_profit.append(pop[0][7])
    agent0_ema.append(pop[0][8])
    
    while generationCounter < MAX_GENERATIONS:
        print("--------------------------")
        print("Generation " + str(generationCounter))
        generationCounter += 1
        
        
        '''
        Here we will need to
        A) Draw dividends
        B) Apply dividends, interest rate and reinvestment
        C) Update wealth sums
        D) Hypermutation (+ update wealth?)
        
    
        @Maarten: where does the extra money from f, r, D(t) go? In the cash?
        D) I'll need to write the dividends, f, r allocation mechanism
        '''
        global dividend
        dividend = draw_dividend()
        wealth_earnings(pop)
        update_wealth(pop, price)
        
        
        print(pop)

        
        # Hypermutation
        global round_replacements
        round_replacements = 0
        hypermutate(pop)
        # Recomputing fitness
        fitness_for_invalid(pop)
        
        
        '''
        E) Update trading signals
        F) Deduce excess demand
        G) Clear the market
        H) Update inventories
        I) Update wealth
        J) Update profits
        K) Deduce fitness as EMA
        J) GA
    '''
        
        # price = market_clearing_function()
        
        compute_ema(pop)
    
    
        # Selection
        offspring = toolbox.select(pop, POPULATION_SIZE)
        fitness_for_invalid(offspring)
        offspring = list(map(toolbox.clone, offspring))
        
        # Crossover
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            toolbox.mate(child1,child2,CROSSOVER_RATE)
            del child1.fitness.values
            del child2.fitness.values
        
        # Mutation
        for mutant in offspring:
            toolbox.mutate(mutant, MUTATION_RATE)
            del mutant.fitness.values
    
        # Recomputing fitness
        fitness_for_invalid(offspring)

        # Replacing
        pop[:] = offspring
        fitnessValues = [ind.fitness.values[0] for ind in pop]
                
        # Print some results
        maxFitness = max(fitnessValues)
        meanFitness = sum(fitnessValues) / len(pop)
        maxFitnessValues.append(maxFitness)
        meanFitnessValues.append(meanFitness)
        replacements.append(round_replacements)
                # Temp
        agent0_profit.append(pop[0][7])
        agent0_ema.append(pop[0][8])
        #  Could this print results be automated? We have it twice
        
        print("- Generation {}: Max Fitness = {}, Avg Fitness = {}".format(generationCounter, maxFitness, meanFitness))
        
                
        # Temporary function to apply some fixed cost
        # if generationCounter > 0:
        #     for ind in pop:
        #         ind[1] -= 1

    
    return initial_pop, pop, maxFitnessValues, meanFitnessValues, replacements, agent0_profit, agent0_ema


# =============================================================================
# Exploit the results
# =============================================================================

initial_pop, pop, maxFitnessValues, meanFitnessValues, replacements, agent0_profit, agent0_ema = main()

# Plot population histograms at the start and at the end
print("--------------------------")
print("--------------------------")
print("--------------------------")
# print("Initial population was " + str(initial_pop))
# sns.histplot(data=np.array(initial_pop), legend = False, stat = "density", shrink = 0.85, discrete=True, bins = 11)
# plt.show()
# print("Current population is " + str(pop))
# sns.histplot(data=np.array(pop), legend = False, stat = "density", shrink = 0.85, discrete=True, bins = 11)
# plt.show()

# Plot the fitness evolution over time
plt.plot(maxFitnessValues, color='red', label='Maximum fitness')
plt.plot(meanFitnessValues, color='green', label = 'Average fitness')
plt.plot(replacements, color='gray', label = 'Hypermutations')
plt.xlabel('Generations')
plt.ylabel('Max / Average Fitness')
plt.title('Max and Average Fitness over Generations')
plt.ylim(0,MAX_TIME_HORIZON+1)
plt.xlim(0,MAX_GENERATIONS+1)
plt.legend()
plt.show()

plt.plot(agent0_ema, color='red', label='EMA')
plt.plot(agent0_profit, color='green', label = 'Profits')
plt.xlabel('Generations')
plt.ylabel('Profit')
plt.title('Profit and EMA profit of Albert')
plt.xlim(0,MAX_GENERATIONS+1)
plt.legend()
plt.show()

print("-----------------------")

print(pop)
for ind in pop:
    # print(ind) returns the first item
    # print(type(ind))
    # print(ind[0])
    print(ind[8])
    
def ema_evaluate(pop):
    values = []
    for ind in pop:
        values.append(ind[8])
    return values
    
result = ema_evaluate(pop)
print(result)
print(type(result))

'''
This is the normal code
'''
result_tradi = toolbox.evaluate(pop)
print(result_tradi)
print(type(result_tradi))
fitnessValues = list(map(toolbox.evaluate, pop))
for individual, fitnessValue in zip(pop, fitnessValues):
    individual.fitness.values = fitnessValue
fitnessValues = [individual.fitness.values[0] for individual in pop]
print(fitnessValues)


'''
This is the new code
'''
toolbox.register("evaluate_ema", ema_evaluate)

# fitnessValues = list(map(toolbox.evaluate_ema, pop))
fitnessValues = toolbox.evaluate_ema(pop)
print(fitnessValues)
for individual, fitnessValue in zip(pop, fitnessValues):
    individual.fitness.values = fitnessValue
fitnessValues = [individual.fitness.values[0] for individual in pop]
print(fitnessValues)
