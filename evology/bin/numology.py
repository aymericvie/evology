import numba as nb
from numba import jit
import numpy as np
import random

IniCash = 10
IniAsset = 10
IniLoan = 0
EMAHorizon = 252
GammaNT = 0.2 * np.sqrt(1 / 252)
MuNT = 1
RhoNT = 0.00045832561
TradingDays = 252
YearG = 0.01
DailyG = ((1 + YearG) ** (1 / TradingDays)) - 1
YearK = 0.02


PopLength = 10

""" column 0 : W // column 1: C // column 2: S // column 3: L / /column 4: prevW"""
"""
0   1     2 3 4  5  6 7   8   9  10
typ Strat W C S L PW Pi Ema Proc

Code for strategies
0: NT // 1: VI // 2: TF
"""


@jit(nopython=True)
def GenNTind():
    Ind = [0, 100, 0, IniCash, IniAsset, IniLoan, 0, 0, 0, 1]
    return Ind


@jit(nopython=True)
def GenVIind():
    Ind = [1, 100, 0, IniCash, IniAsset, IniLoan, 0, 0, 0, 1]
    return Ind


@jit(nopython=True)
def GenTFind():
    Ind = [2, 2, 0, IniCash, IniAsset, IniLoan, 0, 0, 0, 1]
    return Ind


@jit(nopython=True)
def GenRdind(coords):
    if sum(coords) != 1:
        raise ValueError("Sum Coords is not equal to 1.")
    rd = random.random()
    if rd <= coords[0]:
        return GenNTind()
    elif rd <= coords[0] + coords[1]:
        return GenVIind()
    else:
        return GenTFind()


# @jit(nopython=True)
def create_pop(n, coords):
    pop = np.zeros((1, PopLength))
    # Create 3 different types individuals
    pop = np.vstack((pop, GenNTind()))
    pop = np.vstack((pop, GenVIind()))
    pop = np.vstack((pop, GenTFind()))
    for index in range(n - 3):
        pop = np.vstack((pop, GenRdind(coords)))
    pop = np.delete(pop, 0, 0)
    return pop


@jit(nopython=True)
def CalcWealth(pop, p):
    pop[:, 6] = pop[:, 2]  # Update previous wealth
    pop[:, 2] = pop[:, 3] + pop[:, 4] * p - pop[:, 5]  # Update current wealth
    pop[:, 7] = pop[:, 2] - pop[:, 6]  # Calculate profits


@jit(nopython=True)
def GetWealth(pop, i):
    return pop[pop[:, 0] == i, :].sum(axis=0)[1]


@jit(nopython=True)
def GetTotalWealth(pop):
    total = 0
    for i in range(3):
        total += GetWealth(pop, i)
    return total


@jit(nopython=True)
def GetNum(pop, i):
    return len(pop[pop[:, 0] == i, :])


@jit(nopython=True)
def Transfer(pop, i, amount):
    for ind in pop:
        if ind[0] == i:
            ind[5] -= amount


@jit(nopython=True)
def DetRatio(x, y):
    return np.linalg.det(x) / np.linalg.det(y)


# @jit(nopython=True)
def WealthShield(pop, coords):

    WealthNT = GetWealth(pop, 0)
    WealthVI = GetWealth(pop, 1)
    WealthTF = GetWealth(pop, 2)

    TargetNT = coords[0]
    TargetVI = coords[1]
    TargetTF = coords[2]

    WealthSum = WealthNT + WealthVI + WealthTF

    if TargetTF + TargetVI + TargetNT != 1:
        raise ValueError("Target coordinates do not sum to 1.")

    D = np.array(
        [
            [1 - TargetNT, -TargetNT, -TargetNT],
            [-TargetVI, 1 - TargetVI, -TargetNT],
            [-TargetTF, -TargetTF, 1 - TargetTF],
        ]
    )

    Dx = np.array(
        [
            [TargetNT * WealthSum - WealthNT, -TargetNT, -TargetNT],
            [TargetVI * WealthSum - WealthVI, 1 - TargetVI, -TargetNT],
            [TargetTF * WealthSum - WealthTF, -TargetTF, 1 - TargetTF],
        ]
    )

    Dy = np.array(
        [
            [1 - TargetNT, TargetNT * WealthSum - WealthNT, -TargetNT],
            [-TargetVI, TargetVI * WealthSum - WealthVI, -TargetNT],
            [-TargetTF, TargetTF * WealthSum - WealthTF, 1 - TargetTF],
        ]
    )

    Dz = np.array(
        [
            [1 - TargetNT, -TargetNT, TargetNT * WealthSum - WealthNT],
            [-TargetVI, 1 - TargetVI, TargetVI * WealthSum - WealthVI],
            [-TargetTF, -TargetTF, TargetTF * WealthSum - WealthTF],
        ]
    )

    TransferNT = DetRatio(Dx, D)
    TransferVI = DetRatio(Dy, D)
    TransferTF = DetRatio(Dz, D)

    NumNT = GetNum(pop, 0)
    NumVI = GetNum(pop, 1)
    NumTF = GetNum(pop, 2)

    PcTransferNT = TransferNT / NumNT
    PcTransferVI = TransferVI / NumVI
    PcTransferTF = TransferTF / NumTF

    # print([PcTransferNT, PcTransferVI, PcTransferTF])

    Transfer(pop, 0, PcTransferNT)
    Transfer(pop, 1, PcTransferVI)
    Transfer(pop, 2, PcTransferTF)


@jit(nopython=True)
def ComputeFitness(pop):
    pop[:, 8] = (2 / (EMAHorizon + 1)) * (pop[:, 7] - pop[:, 8]) + pop[:, 8]


@jit(nopython=True)
def DetProc(pop):
    for ind in pop:
        ind[9] = np.abs(
            ind[9]
            + RhoNT * (np.log2(MuNT) - np.log2(np.abs(ind[9])))
            + GammaNT * random.normalvariate(0, 1)
        )


@jit(nopython=True)
def DetFval(pop, Dividend):
    Fval = ((1 + DailyG) * Dividend) / ((1 + YearK - YearG) ** (1 / 252) - 1)
    for ind in pop:
        if ind[0] == 0 or ind[0] == 1:
            ind[1] = Fval


####
#!/usr/bin/env python3

""" 
from parameters import *
from sampling import *
import sampling
import pandas as pd
import balance_sheet as bs
import ga as ga
import data
import random
import market as mk
from tqdm import tqdm
import esl_market_clearing as esl_mc
import creation as cr
import timeit
from steps import *
random.seed(random.random())

def main(mode, MAX_GENERATIONS, PROBA_SELECTION, POPULATION_SIZE, MUTATION_RATE, wealth_coordinates, tqdm_display, reset_wealth):
    # Initialise important variables and dataframe to store results
    generation, current_price, dividend, asset_supply, spoils = 0, INITIAL_PRICE, INITIAL_DIVIDEND, POPULATION_SIZE * INITIAL_ASSETS, 0
    results = np.zeros((MAX_GENERATIONS - SHIELD_DURATION, data.variables))
    price_history, dividend_history = [], []
    extended_dividend_history = mk.dividend_series(1*252)
    create_pop = cr.generate_creation_func(wealth_coordinates)
    # Create the population
    pop = create_pop(mode, POPULATION_SIZE)


    for generation in tqdm(range(MAX_GENERATIONS), disable=tqdm_display):

        pop, timeA = update_wealth(pop, current_price, generation, wealth_coordinates, POPULATION_SIZE, reset_wealth)
        pop, replacements, spoils, timeB = ga.hypermutate(pop, mode, asset_supply, current_price, generation, spoils) # Replace insolvent agents     
        pop, timeC = ga_evolution(pop, mode, generation, wealth_coordinates, PROBA_SELECTION, MUTATION_RATE)
        pop, timeD  = decision_updates(pop, mode, price_history, extended_dividend_history)
        pop, mismatch, current_price, price_history, ToLiquidate, timeE = marketClearing(pop, current_price, price_history, spoils)

        pop, volume, dividend, random_dividend, dividend_history, extended_dividend_history, spoils, timeF = marketActivity(pop, 
            current_price, asset_supply, dividend, dividend_history, extended_dividend_history, spoils, ToLiquidate)

        results = data.record_results(results, generation, current_price, mismatch, 
        dividend, random_dividend, volume, replacements, pop, price_history, spoils, 
        asset_supply, timeA, timeB, timeC, timeD, timeE, timeF)

    df = pd.DataFrame(results, columns = data.columns)
    
    return df
    """


Dividend = 0.003983

# Params
n = 10
p = 100
tmax = 20  # 20_000
coords = [1 / 2, 1 / 4, 1 / 4]
print(coords)

# Imports
import numpy as np

np.set_printoptions(suppress=True, precision=1)
from functions import *
import timeit

# Create population
pop = create_pop(n, nb.typed.List(coords))
""" column 0 : W // column 1: C // column 2: S // column 3: L / /column 4: prevW"""
starttime = timeit.default_timer()

print(pop)

for t in range(tmax):

    # Compute wealth and profits
    CalcWealth(pop, p)

    # Wealth shield
    WealthShield(pop, nb.typed.List(coords))

    # Compute fitness
    ComputeFitness(pop)

    # Strategy evolution

    # Determine tsv/proc
    DetProc(pop)

    # Update fval
    DetFval(pop, Dividend)

    # Determine edf
    # Market clearing
    # Compute tsv
    # Compute mismatch
    # Execute excess demand orders
    # Apply earnings
    # Update margin
    # Clear debt
    # print(pop)

    if t % 1000 == 0:
        print(t)


print("End.")
print(pop)
print(timeit.default_timer() - starttime)

print(
    [
        GetWealth(pop, 0) / GetTotalWealth(pop),
        GetWealth(pop, 1) / GetTotalWealth(pop),
        GetWealth(pop, 2) / GetTotalWealth(pop),
    ]
)

# TODO: The wealth shield generates profits, this will bias returns computations.

import numpy as np

WealthNT = 150000
WealthVI = 10000
WealthTF = 111000
TargetNT = 1 / 4
TargetVI = 1 / 2
TargetTF = 1 / 4

""" Addition: no negative transfer to avoid bankruptcies """

WealthSum = WealthNT + WealthVI + WealthTF
print([WealthNT / WealthSum, WealthVI / WealthSum, WealthTF / WealthSum])


if TargetTF + TargetVI + TargetNT != 1:
    raise ValueError("Target coordinates do not sum to 1.")

D = np.array(
    [
        [1 - TargetNT, -TargetNT, -TargetNT],
        [-TargetVI, 1 - TargetVI, -TargetNT],
        [-TargetTF, -TargetTF, 1 - TargetTF],
    ]
)

Dx = np.array(
    [
        [TargetNT * WealthSum - WealthNT, -TargetNT, -TargetNT],
        [TargetVI * WealthSum - WealthVI, 1 - TargetVI, -TargetNT],
        [TargetTF * WealthSum - WealthTF, -TargetTF, 1 - TargetTF],
    ]
)

Dy = np.array(
    [
        [1 - TargetNT, TargetNT * WealthSum - WealthNT, -TargetNT],
        [-TargetVI, TargetVI * WealthSum - WealthVI, -TargetNT],
        [-TargetTF, TargetTF * WealthSum - WealthTF, 1 - TargetTF],
    ]
)

Dz = np.array(
    [
        [1 - TargetNT, -TargetNT, TargetNT * WealthSum - WealthNT],
        [-TargetVI, 1 - TargetVI, TargetVI * WealthSum - WealthVI],
        [-TargetTF, -TargetTF, TargetTF * WealthSum - WealthTF],
    ]
)

###

TransferNT = np.linalg.det(Dx) / np.linalg.det(D)
TransferVI = np.linalg.det(Dy) / np.linalg.det(D)
TransferTF = np.linalg.det(Dz) / np.linalg.det(D)

# NewWealthNT = WealthNT + TransferNT
# NewWealthVI = WealthVI + TransferVI
# NewWealthTF = WealthTF + TransferTF
# print([NewWealthNT, NewWealthVI,NewWealthTF])
# NewSumWealth = NewWealthNT + NewWealthVI + NewWealthTF

# print(TransferNT, TransferVI, TransferTF)
# print([TargetNT, TargetVI, TargetTF])
# print([NewWealthNT / NewSumWealth, NewWealthVI / NewSumWealth, NewWealthTF / NewSumWealth])

print(TransferNT, TransferVI, TransferTF)

TransferNT = max((np.linalg.det(Dx) / np.linalg.det(D)), 0)
TransferVI = max((np.linalg.det(Dy) / np.linalg.det(D)), 0)
TransferTF = max((np.linalg.det(Dz) / np.linalg.det(D)), 0)

NewWealthNT = WealthNT + TransferNT
NewWealthVI = WealthVI + TransferVI
NewWealthTF = WealthTF + TransferTF
# print([NewWealthNT, NewWealthVI,NewWealthTF])
NewSumWealth = NewWealthNT + NewWealthVI + NewWealthTF

print(TransferNT, TransferVI, TransferTF)
print([TargetNT, TargetVI, TargetTF])
print(
    [NewWealthNT / NewSumWealth, NewWealthVI / NewSumWealth, NewWealthTF / NewSumWealth]
)
