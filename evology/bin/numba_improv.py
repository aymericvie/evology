#!/usr/bin/env python3

from numba.np.ufunc import parallel
from main import *
from parameters import *

wealth_coordinates = [1 / 3, 1 / 3, 1 / 3]
mode = "static"
POPULATION_SIZE = 10
price = 100
reps = 20 * 50000
import numba
from numba import jit, prange

create_pop = cr.generate_creation_func(wealth_coordinates)
pop = create_pop(mode, POPULATION_SIZE)


@jit(nopython=True)
def calculate_wealth0(pop, current_price):
    for ind in pop:
        ind.prev_wealth = ind.wealth
        ind.wealth = ind.cash + ind.asset * current_price - ind.loan
    return ind


starttime = timeit.default_timer()
for i in range(reps):
    calculate_wealth0(pop, price)
timeZ = timeit.default_timer() - starttime
print("Normal + nb function " + str(timeZ))


def calculate_wealth(pop, current_price):
    for ind in pop:
        ind.prev_wealth = ind.wealth
        ind.wealth = ind.cash + ind.asset * current_price - ind.loan
    return ind


starttime = timeit.default_timer()
for i in range(reps):
    calculate_wealth(pop, price)
timeA = timeit.default_timer() - starttime
print("Normal function " + str(timeA))


pop = np.zeros((POPULATION_SIZE, 5))
""" column 0 : W // column 1: C // column 2: S // column 3: L / /column 4: prevW"""


@jit(nopython=False)
def calculate_wealth2(pop, price):
    pop[:, 4] = pop[:, 0]
    pop[:, 0] = pop[:, 1] + pop[:, 2] * price - pop[:, 3]


starttime = timeit.default_timer()
for i in range(reps):
    calculate_wealth2(pop, price)
timeB = timeit.default_timer() - starttime
print("Numbaed function, jit false " + str(timeB))

pop = np.zeros((POPULATION_SIZE, 5))
""" column 0 : W // column 1: C // column 2: S // column 3: L / /column 4: prevW"""


@jit(nopython=True)
def calculate_wealth3(pop, price):
    pop[:, 4] = pop[:, 0]
    pop[:, 0] = pop[:, 1] + pop[:, 2] * price - pop[:, 3]


starttime = timeit.default_timer()
for i in range(reps):
    calculate_wealth3(pop, price)
timeC = timeit.default_timer() - starttime
print("Numbaed function, jit true " + str(timeC))

pop = np.zeros((POPULATION_SIZE, 5))
""" column 0 : W // column 1: C // column 2: S // column 3: L / /column 4: prevW"""


@jit(nopython=True, parallel=True)
def calculate_wealth4(pop, price):
    for i in prange(len(pop)):
        pop[i, 4] = pop[i, 0]
        pop[i, 0] = pop[i, 1] + pop[i, 2] * price - pop[i, 3]


for i in range(reps):
    calculate_wealth4(pop, price)
timeD = timeit.default_timer() - starttime
print("Numbaed function, parallel true " + str(timeD))
