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
