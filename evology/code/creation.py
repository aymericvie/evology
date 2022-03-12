from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from deap import gp
import numpy as np
import random

toolbox = base.Toolbox()
from parameters import *

import cythonized


def DrawReturnRate(strat):
    if strat == "vi":
        rate = np.random.uniform(MIN_RR_VI, MAX_RR_VI) / 1000
    if strat == "nt":
        rate = np.random.uniform(MIN_RR_NT, MAX_RR_NT) / 1000
    else:
        rate = np.random.uniform(MIN_RR_TF, MAX_RR_TF) / 1000
    return rate


creator.create("fitness_strategy", base.Fitness, weights=(1.0,))

creator.ind = cythonized.Individual

# TODO: individual_ga is a list, individual_gp will be a gp.primitiveTree.

toolbox.register("trader", np.random.randint, 0, 1)
toolbox.register("gen_ind", tools.initCycle, creator.ind, (toolbox.trader,), n=1)


def IndCreation(strat):
    ind = toolbox.gen_ind()
    if strat == "nt":
        ind.type = "nt"
        ind.leverage = LeverageNT
        ind.type_as_int = cythonized.convert_ind_type_to_num("nt")
    if strat == "vi":
        ind.type = "vi"
        ind.leverage = LeverageVI
        ind.type_as_int = cythonized.convert_ind_type_to_num("vi")
    if strat == "tf":
        ind.type = "tf"
        ind.leverage = LeverageTF
        ind.type_as_int = cythonized.convert_ind_type_to_num("tf")
    return ind


def CreatePop(n, space, WealthCoords):

    if n < 3:
        raise ValueError("Cannot create diverse population with less than 3 agents. ")
    if sum(WealthCoords) > 1.001 or sum(WealthCoords) < 0.999:
        raise ValueError("Sum of wealth coordinates is higher than 1. ")

    # Determine total and strategy assets and cash
    TotalAsset, TotalCash = n * RefAssets, n * RefCash
    ShareNT, ShareVI, ShareTF = WealthCoords[0], WealthCoords[1], WealthCoords[2]

    NTAsset, NTCash = ShareNT * TotalAsset, ShareNT * TotalCash
    VIAsset, VICash = ShareVI * TotalAsset, ShareVI * TotalCash
    TFAsset, TFCash = ShareTF * TotalAsset, ShareTF * TotalCash

    # Draw
    pop = []

    NumNT, NumVI, NumTF = 0, 0, 0
    if WealthCoords[0] != 0:
        pop.append(IndCreation("nt"))
        NumNT += 1
    if WealthCoords[1] != 0:
        pop.append(IndCreation("vi"))
        NumVI += 1
    if WealthCoords[2] != 0:
        pop.append(IndCreation("tf"))
        NumTF += 1

    for i in range(n - (NumNT + NumVI + NumTF)):
        rd = np.random.random()
        if rd <= ShareNT:
            pop.append(IndCreation("nt"))
            NumNT += 1
        elif rd > ShareNT and rd <= ShareNT + ShareVI:
            pop.append(IndCreation("vi"))
            NumVI += 1
        elif rd > ShareNT + ShareVI:
            pop.append(IndCreation("tf"))
            NumTF += 1

    if NumNT != 0:
        PcNTCash = NTCash / NumNT
        PcNTAsset = NTAsset / NumNT

    if NumVI != 0:
        PcVICash = VICash / NumVI
        PcVIAsset = VIAsset / NumVI

    if NumTF != 0:
        PcTFCash = TFCash / NumTF
        PcTFAsset = TFAsset / NumTF

    if space == "scholl":
        for ind in pop:
            if ind.type == "nt":
                ind.strategy = 0.01
                ind[0] = 100
            if ind.type == "vi":
                ind.strategy = 0.01
                ind[0] = 100
            if ind.type == "tf":
                ind.strategy = 0.01
                ind[0] = 2

    if space == "extended":
        for ind in pop:
            if ind.type == "nt":
                ind.strategy = DrawReturnRate("nt")
                ind[0] = 100
            if ind.type == "vi":
                ind.strategy = DrawReturnRate("vi")
                ind[0] = 100
            if ind.type == "tf":
                ind.strategy = DrawReturnRate("tf")

    for ind in pop:
        if ind.type == "nt":
            ind.cash = PcNTCash
            ind.asset = PcNTAsset
        if ind.type == "vi":
            ind.cash = PcVICash
            ind.asset = PcVIAsset
        if ind.type == "tf":
            ind.cash = PcTFCash
            ind.asset = PcTFAsset

    return pop, TotalAsset


def WealthReset(pop, space, WealthCoords, generation, ResetWealth):
    # generation > 1 and generation <= SHIELD_DURATION or 
    if ResetWealth == True:
        pop, asset_supply = CreatePop(len(pop), space, WealthCoords)
        for ind in pop:
            ind.age = generation
    return pop
