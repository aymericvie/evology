#!/usr/bin/env python3

import sys
sys.path.append('./evology/code/')
from main import *
import random
import numpy as np
random.seed = random.random()
from parameters import *
import traceback

solver = 'esl.true'

np.random.seed(8)

def learning_runs(repetitions, time, agents):
    went_smoothly = True
    i = 0
    while i < repetitions:
        wealth_coordinates = np.random.dirichlet(np.ones(3),size=1)[0].tolist()
        print(wealth_coordinates)
        try: 
            df,pop = main("between", 'scholl', solver, time, PROBA_SELECTION, agents, MUTATION_RATE, wealth_coordinates, tqdm_display=True, reset_wealth = False, ReinvestmentRate = 0)

        except Exception as e: 
            went_smoothly = False
            print('Process ' + str(i) + ' encoutered an exception.')
            print(str(e))
            traceback.print_exc()
            break
        i += 1
    return went_smoothly

def test_learning(repetitions, time, agents):
    went_smoothly = learning_runs(repetitions, time, agents)
    assert went_smoothly == True

def learning_runs_reset(repetitions, time, agents):
    went_smoothly = True
    i = 0
    while i < repetitions:
        wealth_coordinates = np.random.dirichlet(np.ones(3),size=1)[0].tolist()
        print(wealth_coordinates)
        try: 
            df,pop = main("between", 'scholl', solver, time, PROBA_SELECTION, agents, MUTATION_RATE, wealth_coordinates, tqdm_display=True, reset_wealth = True, ReinvestmentRate = 0)

        except Exception as e: 
            went_smoothly = False
            print('Process ' + str(i) + ' encoutered an exception.')
            print(str(e))
            traceback.print_exc()
            break
        i += 1
    return went_smoothly

def test_learning_reset(repetitions, time, agents):
    went_smoothly = learning_runs_reset(repetitions, time, agents)
    assert went_smoothly == True

def nolearning_runs(repetitions, time, agents):

    went_smoothly = True
    i = 0
    while i < repetitions:
        try: 
            wealth_coordinates = np.random.dirichlet(np.ones(3),size=1)[0].tolist()
            print(wealth_coordinates)
            df,pop = main("static", 'scholl', solver, time, 0, agents, 0, wealth_coordinates, tqdm_display=True, reset_wealth = False, ReinvestmentRate = 0)

        except Exception as e: 
            went_smoothly = False
            print('Process ' + str(i) + ' encoutered an exception.')
            print(str(e))
            traceback.print_exc()
            break
        i += 1
    return went_smoothly


def test_nolearning(repetitions, time, agents):
    went_smoothly = nolearning_runs(repetitions, time, agents)
    assert went_smoothly == True


def nolearning_runs_reset(repetitions, time, agents):

    went_smoothly = True
    i = 0
    while i < repetitions:
        try: 
            wealth_coordinates = np.random.dirichlet(np.ones(3),size=1)[0].tolist()
            print(wealth_coordinates)
            df,pop = main("static", 'scholl', solver, time, 0, agents, 0, wealth_coordinates, tqdm_display=True, reset_wealth = True, ReinvestmentRate=0)

        except Exception as e: 
            went_smoothly = False
            print('Process ' + str(i) + ' encoutered an exception.')
            print(str(e))
            traceback.print_exc()
            break
        i += 1
    return went_smoothly


def test_nolearning_reset(repetitions, time, agents):
    went_smoothly = nolearning_runs_reset(repetitions, time, agents)
    assert went_smoothly == True

def det_pop_nolearning(repetitions, time, agents):

    went_smoothly = True

    for _ in range(repetitions):
        seed = random.randint(0,10)
        np.random.seed(seed)
        wealth_coordinates = np.random.dirichlet(np.ones(3),size=1)[0].tolist()
        np.random.seed(seed)
        df,pop = main("between", 'scholl', solver, time, 0, agents, 0, wealth_coordinates, tqdm_display=True, reset_wealth = False,ReinvestmentRate=0)
        np.random.seed(seed)
        df2,pop2 = main("between", 'scholl', solver, time, 0, agents, 0, wealth_coordinates, tqdm_display=True, reset_wealth = False,ReinvestmentRate=0)

        if df['Price'].iloc[-1] != df2['Price'].iloc[-1]:
            went_smoothly = False
            print('Price trajectory is not reproducible.')
        if pop[-1] != pop2[-1]:
            went_smoothly = False
            print('Final population is not reproducible.')
    return went_smoothly

def test_det_pop_nolearning(repetitions, time, agents):
    went_smoothly = det_pop_nolearning(repetitions, time, agents)
    assert went_smoothly == True

def det_pop_learning(repetitions, time, agents):

    went_smoothly = True

    for _ in range(repetitions):
        seed = random.randint(0,10)
        np.random.seed(seed)
        wealth_coordinates = np.random.dirichlet(np.ones(3),size=1)[0].tolist()
        np.random.seed(seed)
        df,pop = main("between", 'scholl', solver, time, PROBA_SELECTION, agents, MUTATION_RATE, wealth_coordinates, tqdm_display=True, reset_wealth = False, ReinvestmentRate=0)
        np.random.seed(seed)
        df2,pop2 = main("between", 'scholl', solver, time, PROBA_SELECTION, agents, MUTATION_RATE, wealth_coordinates, tqdm_display=True, reset_wealth = False, ReinvestmentRate=0)

        if df['Price'].iloc[-1] != df2['Price'].iloc[-1]:
            went_smoothly = False
            print('Price trajectory is not reproducible.')
        if pop[-1] != pop2[-1]:
            went_smoothly = False
            print('Final population is not reproducible.')
    return went_smoothly

def test_det_pop_learning(repetitions, time, agents):
    went_smoothly = det_pop_learning(repetitions, time, agents)
    assert went_smoothly == True