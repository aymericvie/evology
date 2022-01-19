"""
This experiment investigates how learning rates and reinvestment rates affect population dynamics. 
It takes a fixed initial condition (wealth coordinates), time horizon and population size. 
"""

# Imports 
import numpy as np
import pandas as pd
import sys
sys.path.append('evology/code')
from main import main as evology

# Fixed parameters 
TimeHorizon = 252 * 100 + 3 * 21 # 100 Years + 3 months to compensate early period without recording data.
PopulationSize = 100
Coordinates = [1/3, 1/3, 1/3]
seed = 8
reps = 50

Config = [Coordinates, PopulationSize, TimeHorizon, SelectionRate, MutationRate, ReinvestmentRate]

Config1 = [Coordinates, PopulationSize, TimeHorizon, 0, 0, 0] # Static
Config2 = [Coordinates, PopulationSize, TimeHorizon, 0, 1/252, 1/252] # Learning 1Y
Config3 = [Coordinates, PopulationSize, TimeHorizon, 0, 1/252, 0] # Imitation-only 1Y
Config4 = [Coordinates, PopulationSize, TimeHorizon, 0, 0, 1/252] # Mutation-only 1Y
Config5 = [Coordinates, PopulationSize, TimeHorizon, 0, 1/(252*2), 1/(252*2)] # Learning 2Y
Config6 = [Coordinates, PopulationSize, TimeHorizon, 0, 1/(252*3), 1/(252*3)] # Learning 3Y

# TODO: rewrite main without static/between
# TODO: reorderr arguments inside main, it's a mess

def run(Config):
    df, pop = df, pop = main(
            "static", # to delete
            "scholl", 
            "esl",
            Config[0],
            # Coords
            Config[1],
            # Popsize
            Config[2],
            # Time
            Config[3],
            # SelectionRate
            Config[4],
            # MutationRate
            Config[5],
            # ReinvestmentRate
            Config[6],
            0, # relocate
            PopulationSize, # relocate
            0, # relocate
            Coordinates, # relocate
            False,
            False,
            ReinvestmentRate # relocate
        )

def SimulateData(Config, reps, seed):
    np.random.seed(seed)
    
    dfNT = pd.DataFrame()
	dfVI= pd.DataFrame()
	dfTF = pd.DataFrame()



# Then basically, for i in 1, 2... 6, 
''' 
create name = Config i
run the whole experiment with config i as argument
Save datafiles according to i: data_config6 '''


# And then we'll have another file to extract the data into exploitable output and get the plots out.

# We could even plot many things on a same ternary, but maybe this would be too heavy?