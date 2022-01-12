import operator
import math
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

import matplotlib.pyplot as plt
import networkx as nx
import graphviz
# import pygraphviz as pgv 
from networkx.drawing.nx_agraph import graphviz_layout
#in Conda prompt conda install -c alubbock pygraphviz run in admin mode


# Define new functions
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
# pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))
pset.renameArguments(ARG0='x')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)
import numpy as np
def evalSymbReg(individual, points):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression
    # and the real function : x**4 + x**3 + x**2 + x
    sqerrors = ((func(x) - x**4 - x**3 - x**2 - x)**2 for x in points)
    return math.fsum(sqerrors) / len(points),



toolbox.register("evaluate", evalSymbReg, points=[x/10. for x in range(-10,10)])
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

def main(mode):
    random.seed(318)

    hof = tools.HallOfFame(1)
    pop_size = 50
    halloffame = hof
    population = toolbox.population(n=pop_size)
    cxpb = 0.5
    ngen =100
    mutpb = 0.1
    
    verbose=True
    
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)
    stats=mstats
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness

        
    print("new fitness")
        


    
    balance_sheet = np.array([0, 10, 5, 2, 0, 0, 0, 0, 0])
    for i in range(pop_size):
        ind_bs = np.array([0, 10, 5, 2, 0, 0, 0, 0, 0])
        balance_sheet = np.vstack((balance_sheet, ind_bs))
    balance_sheet = balance_sheet.astype('float64')
    balance_sheet[0,3] = 0

    
    
    def profitn(idx, val, balance_sheet):
        return balance_sheet[idx,3],
    
    scores = []
    for idx, val in enumerate(population):
        scores.append(profitn(idx, val, balance_sheet))
    print(scores)
    
    print("First fitness computaiton")
    
    if mode == "ecology":
        print("ecology")
        for ind, fit in zip(population, scores):
                ind.fitness.values = fit
                # print(ind)
                # print(fit)
    
    if mode == "deap":
        print("deap")
        
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            # print(ind)
            # print(fit)


    # for ind in population:
    #     print(ind)
    #     print(ind.fitness)
        
    print("--------------------------------")
    
    # for ind in population:
    #     print(ind)
    #     print(ind.fitness.values)

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}

    logbook.record(gen=0, nevals=len(population), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Select the next generation individuals
        
        # print("-----------------------")
        # print(population)
        offspring = toolbox.select(population, len(population))
        # print("-----------------------")
        # print(offspring)
        # print("-----------------------")

        # Vary the pool of individuals
        offspring = [toolbox.clone(ind) for ind in offspring]

        for i in range(1, len(offspring), 2):
            if random.random() < cxpb:
                offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                          offspring[i])
            del offspring[i - 1].fitness.values, offspring[i].fitness.values

        for i in range(len(offspring)):
            if random.random() < mutpb:
                offspring[i], = toolbox.mutate(offspring[i])
                del offspring[i].fitness.values
                
        # print("Next fitness computaitons")

        if mode == "ecology":
            # print("ecology")
            for ind, fit in zip(offspring, scores):
                    ind.fitness.values = fit
                    # print(ind)
                    # print(fit)
        
        if mode == "deap":
            # print("deap")
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            # print(invalid_ind)
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
                # print(ind)
                # print(fit)


        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring
        # Append the current generation statistics to the logbook
        # for ind in population:
        #     print(ind)
        #     print(ind.fitness)
        
        if gen >= ngen:
            fitnesses = toolbox.map(toolbox.evaluate, population)
            for ind, fit in zip(population, fitnesses):
                ind.fitness.values = fit
        record = stats.compile(population) if stats else {}
        if mode == "ecology":
            logbook.record(gen=gen, nevals=len(population), **record)
        if mode == "deap":
            logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

        
        # bests = tools.selBest(population, k=1)
        # print(bests[0])
    # print log
    return population, logbook, hof

population = toolbox.population(n=10)
for ind in population:
    print(ind)
    print(type(ind))
    print(ind[0])

run = False
if run == True:
    pop, log, hof = main("deap")
    bests = tools.selBest(pop, k=1)

    nodes, edges, labels = gp.graph(bests[0])
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    pos = graphviz_layout(graph, prog = 'dot') #run dot -c in conda prompt
    plt.figure(figsize=(7,7))
    nx.draw_networkx_nodes(graph, pos, node_size=900, node_color="w")
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_labels(graph, pos, labels)
    plt.axis("off")
    plt.show()

    def plot_graph(tree):
        nodes, edges, labels = gp.graph(tree)
        graph = nx.Graph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)
        pos = graphviz_layout(graph, prog = 'dot') #run dot -c in conda prompt
        plt.figure(figsize=(7,7))
        nx.draw_networkx_nodes(graph, pos, node_size=900, node_color="w")
        nx.draw_networkx_edges(graph, pos)
        nx.draw_networkx_labels(graph, pos, labels)
        plt.axis("off")
        plt.show()



    print("Best ")
    print(bests[0])


    # def bestf(x):
    #     return toolbox.compile(expr=bests[0])(x)

    # def func(x):
    #     return x*x*x*x - x*x*x - x*x - x

    # print(bestf(1))
    # XXX = np.linspace(-10,10,100)
    # y = []
    # for ix in XXX:
    #     y.append(bestf(ix))
    # z = []
    # for ix in XXX:
    #     z.append(func(ix))

    # print("figure")
    # plt.plot(y, label="best fit")
    # plt.plot(z, label = "actual func")
    # plt.xlim(-10,10)
    # plt.legend()
    # plt.show()


