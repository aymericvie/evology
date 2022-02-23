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

def learning_runs(repetitions, time, agents):
    went_smoothly = True
    i = 0
    while i < repetitions:
        wealth_coordinates = np.random.dirichlet(np.ones(3),size=1)[0].tolist()
        print(wealth_coordinates)
        try: 
            seed = random.randint(0,100)
            np.random.seed(seed)
            df,pop = main('scholl', solver, wealth_coordinates, time, agents, PROBA_SELECTION, MUTATION_RATE, ReinvestmentRate = 1.0, InvestmentHorizon = 252, InvestorBehavior = 'profit', tqdm_display=True, reset_wealth = False)
        except Exception as e: 
            went_smoothly = False
            print('Seed ' + str(seed))
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
            df,pop = main('scholl', solver, wealth_coordinates, agents, time, PROBA_SELECTION, MUTATION_RATE, ReinvestmentRate = 1.0, InvestmentHorizon = 252, InvestorBehavior = 'profit', tqdm_display=True, reset_wealth = True)

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
            seed = random.randint(0,100)
            np.random.seed(seed)
            wealth_coordinates = np.random.dirichlet(np.ones(3),size=1)[0].tolist()
            print(wealth_coordinates)
            df,pop = main('scholl', solver, wealth_coordinates, agents, time, 0, 0, ReinvestmentRate = 1.0, InvestmentHorizon = 252, InvestorBehavior = 'profit', tqdm_display=True, reset_wealth = False)

        except Exception as e: 
            went_smoothly = False
            print('Seed ' + str(seed))
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
            df,pop = main('scholl', solver, wealth_coordinates, agents, time, 0, 0, ReinvestmentRate=1.0, InvestmentHorizon = 252, InvestorBehavior = 'profit', tqdm_display=True, reset_wealth = True)

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

        print("Seed, Wealth Coord")
        print(seed)
        print(wealth_coordinates)
        
        np.random.seed(seed)
        df,pop = main('scholl', solver, wealth_coordinates, agents, time, 0, 0, ReinvestmentRate=1.0, InvestmentHorizon = 252, InvestorBehavior = 'profit', tqdm_display=True, reset_wealth = False)
        np.random.seed(seed)
        df2,pop2 = main('scholl', solver, wealth_coordinates, agents, time, 0, 0, ReinvestmentRate=1.0, InvestmentHorizon = 252, InvestorBehavior = 'profit', tqdm_display=True, reset_wealth = False)

        if df['Price'].iloc[-1] != df2['Price'].iloc[-1]:
            print(seed)
            print(wealth_coordinates)
            went_smoothly = False
            print('Price trajectory is not reproducible.')
        if pop[-1] != pop2[-1]:
            print(seed)
            print(wealth_coordinates)
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

        print("Seed, Wealth Coord")
        print(seed)
        print(wealth_coordinates)

        np.random.seed(seed)
        df,pop = main('scholl', solver, wealth_coordinates, agents, time, PROBA_SELECTION, MUTATION_RATE, ReinvestmentRate=1.0, InvestmentHorizon = 252, InvestorBehavior = 'profit', tqdm_display=True, reset_wealth = False)
        np.random.seed(seed)
        df2,pop2 = main('scholl', solver, wealth_coordinates, agents, time, PROBA_SELECTION, MUTATION_RATE, ReinvestmentRate=1.0, InvestmentHorizon = 252, InvestorBehavior = 'profit', tqdm_display=True, reset_wealth = False)

        if df['Price'].iloc[-1] != df2['Price'].iloc[-1]:
            print(seed)
            print(wealth_coordinates)
            went_smoothly = False
            print('Price trajectory is not reproducible.')
        if pop[-1] != pop2[-1]:
            print(seed)
            print(wealth_coordinates)
            went_smoothly = False
            print('Final population is not reproducible.')
    return went_smoothly

def test_det_pop_learning(repetitions, time, agents):
    went_smoothly = det_pop_learning(repetitions, time, agents)
    assert went_smoothly == True