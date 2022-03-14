# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 10:13:04 2021

@author: aymer
"""

# =============================================================================
# Testing unbiasedness of the initial population
# =============================================================================
sns.histplot(
    data=np.array(toolbox.population_creation(n=10000)),
    legend=False,
    stat="density",
    shrink=0.85,
    discrete=True,
)
# Can probably adjust quality playing with plt.save(dpi), after all this is a matplotlib object.

# =============================================================================
# Testing unbiasedness of our special crossover operator
# =============================================================================


def mate_test():
    return toolbox.feasible_crossover([1], [10], 1)


toolbox.register("mate_test", mate_test)
toolbox.register("crossover_test", tools.initRepeat, list, toolbox.mate_test)
sns.histplot(
    data=np.array(toolbox.crossover_test(n=10000))[:, 0],
    legend=False,
    stat="density",
    shrink=0.85,
    discrete=True,
    binrange=(1, 10),
)
sns.histplot(
    data=np.array(toolbox.crossover_test(n=10000))[:, 1],
    legend=False,
    stat="density",
    shrink=0.85,
    discrete=True,
    binrange=(1, 10),
)

# =============================================================================
# Testing unbiasedness of the mutation operator
# =============================================================================
def mutation_test1():
    return toolbox.mutate([1], 1)


toolbox.register("mutation_test1", mutation_test1)

toolbox.register("mutation1_data", tools.initRepeat, list, toolbox.mutation_test1)
df = toolbox.mutation1_data(n=10000)
sns.histplot(
    data=np.array(df),
    legend=False,
    stat="density",
    shrink=0.85,
    discrete=True,
    binrange=(1, 10),
)
# All mutations of 1 give 2


def mutation_test1():
    return toolbox.mutate([10], 1)


toolbox.register("mutation_test1", mutation_test1)

toolbox.register("mutation1_data", tools.initRepeat, list, toolbox.mutation_test1)
df = toolbox.mutation1_data(n=10000)
sns.histplot(
    data=np.array(df),
    legend=False,
    stat="density",
    shrink=0.85,
    discrete=True,
    binrange=(1, 10),
)
# All mutations of 10 give 9


def mutation_test1():
    return toolbox.mutate([5], 1)


toolbox.register("mutation_test1", mutation_test1)

toolbox.register("mutation1_data", tools.initRepeat, list, toolbox.mutation_test1)
df = toolbox.mutation1_data(n=10000)
sns.histplot(
    data=np.array(df),
    legend=False,
    stat="density",
    shrink=0.85,
    discrete=True,
    binrange=(1, 10),
)
# Mutations of 5 are evenly spread between 4 and 6
