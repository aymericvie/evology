#!/usr/bin/env python3
import creation as cr
import timeit
import numpy as np
import pandas as pd

wealth_coordinates = [1 / 3, 1 / 3, 1 / 3]
POP_SIZE = 1_000_000
current_price = 100

create_pop = cr.generate_creation_func(wealth_coordinates)
pop = create_pop("between", POP_SIZE)


def standard_wealth_update(pop, current_price):
    for ind in pop:
        ind.prev_wealth = ind.wealth
        ind.wealth = ind.cash + ind.asset * current_price - ind.loan
    return ind


starttime = timeit.default_timer()
standard_wealth_update(pop, current_price)
print("std wealth update :", timeit.default_timer() - starttime)


def wealth_update2(pop, current_price):
    for ind in pop:
        update2(ind, current_price)
    return pop


def update2(ind, current_price):
    ind.prev_wealth = ind.wealth
    ind.wealth = ind.cash + ind.asset * current_price - ind.loan
    return ind


starttime = timeit.default_timer()
pop = wealth_update2(pop, current_price)
print(" wealth update2 :", timeit.default_timer() - starttime)


def np_update_wealth(array, current_price):
    for i in range(len(array)):
        array[i, 10] = array[i, 9] * current_price + array[i, 11]
    return array


np_bs = np.random.rand(POP_SIZE, 40)
starttime = timeit.default_timer()
pop = np_update_wealth(np_bs, current_price)
print(" wealth np :", timeit.default_timer() - starttime)


def np_update_wealth2(array, current_price):
    array[:, 10] = array[:, 9] * current_price + array[:, 11]


np_bs = np.random.rand(POP_SIZE, 40)
starttime = timeit.default_timer()
pop = np_update_wealth2(np_bs, current_price)
print(" wealth np 2:", timeit.default_timer() - starttime)


print("----")


import timeit
import random

time = 10000
variables = 10

small_starttime = timeit.default_timer()
results = np.zeros((time, variables))
for i in range(time):
    for j in range(variables):
        results[i, j] = random.random()
print(" Element-wise update :", timeit.default_timer() - small_starttime)

small_starttime = timeit.default_timer()
results = np.zeros((1, variables))
for i in range(time):
    new_results = np.random.rand(1, variables)
    results = np.vstack((results, new_results))
results = np.delete(results, (0), axis=0)
print(results)
print(" Row insertion :", timeit.default_timer() - small_starttime)

small_starttime = timeit.default_timer()
df = pd.DataFrame(index=range(1), columns=range(variables))
for i in range(time):
    new_results = [random.random()] * variables
    df.loc[len(df.index)] = new_results
print(" Pandas :", timeit.default_timer() - small_starttime)
