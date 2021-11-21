#!/usr/bin/env python3
from main import *
import pandas as pd
import random
from parameters import *

RANDOM_SEED = random.random()
# wealth_coordinates = [0.42, 0.33, 0.25]
wealth_coordinates = [1/3, 1/3, 1/3]
# wealth_coordinates = [0.2, 0.5, 0.3]
# NT VI TF
# wealth_coordinates = np.random.dirichlet(np.ones(3),size=1)[0].tolist()
print(wealth_coordinates)

# def main(mode, MAX_GENERATIONS, PROBA_SELECTION, POPULATION_SIZE, CROSSOVER_RATE, MUTATION_RATE, wealth_coordinates, tqdm_display):

def run(POPULATION_SIZE, learning_mode, TIME, wealth_coordinates, tqdm_display, reset_wealth):

    if learning_mode == 0:
        df = main("static", TIME, 0, POPULATION_SIZE, 0, wealth_coordinates, tqdm_display, reset_wealth)
    if learning_mode == 1:
        df = main("between", TIME, PROBA_SELECTION, POPULATION_SIZE, MUTATION_RATE, wealth_coordinates, tqdm_display, reset_wealth)
    if learning_mode == 2:
        df = main("between", TIME, PROBA_SELECTION, POPULATION_SIZE, 0, wealth_coordinates, tqdm_display, reset_wealth)
    return df

df = run(50, 0, 22, wealth_coordinates, tqdm_display=False, reset_wealth=False)

df.to_csv("evology/data/run_data.csv")
# print(df)



# TODO: rework pop creation so that we have at least one agent of each type


