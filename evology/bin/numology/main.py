#!/usr/bin/env python3

''' 
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
    '''


Dividend = 0.003983    

# Params
n = 10
p = 100
tmax = 20# 20_000
coords = [1/2, 1/4, 1/4]
print(coords)

# Imports
import numpy as np
np.set_printoptions(suppress=True, precision = 1)
from functions import *
import timeit

# Create population
pop = create_pop(n, nb.typed.List(coords)) 
''' column 0 : W // column 1: C // column 2: S // column 3: L / /column 4: prevW'''
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


print('End.')
print(pop)
print(timeit.default_timer() - starttime)

print([GetWealth(pop, 0) / GetTotalWealth(pop), GetWealth(pop, 1) / GetTotalWealth(pop), GetWealth(pop, 2) / GetTotalWealth(pop)])

# TODO: The wealth shield generates profits, this will bias returns computations.