"""
This experiment investigates how learning rates and reinvestment rates affect population dynamics. 
It takes a fixed initial condition (wealth coordinates), time horizon and population size. 
"""

# Imports 
import numpy as np
import pandas as pd
import sys
if sys.platform == 'darwin':
    sys.path.append('/Users/aymericvie/Documents/GitHub/evology/evology/code')
if sys.platform == 'linux':
    sys.path.append('/home/vie/Documents/GitHub/evology/evology/code')
from main import main as evology
import multiprocessing as mp

# Fixed parameters 
TimeHorizon = 100 # 252 * 100 + 3 * 21 # 100 Years + 3 months to compensate early period without recording data.
PopulationSize = 100
Coordinates = [1/3, 1/3, 1/3]
seed = 8
reps = 1

Config1 = [Coordinates, PopulationSize, TimeHorizon, 0, 0, 0] # Static
Config2 = [Coordinates, PopulationSize, TimeHorizon, 0, 1/252, 1/252] # Learning 1Y
Config3 = [Coordinates, PopulationSize, TimeHorizon, 0, 1/252, 0] # Imitation-only 1Y
Config4 = [Coordinates, PopulationSize, TimeHorizon, 0, 0, 1/252] # Mutation-only 1Y
Config5 = [Coordinates, PopulationSize, TimeHorizon, 0, 1/(252*2), 1/(252*2)] # Learning 2Y
Config6 = [Coordinates, PopulationSize, TimeHorizon, 0, 1/(252*3), 1/(252*3)] # Learning 3Y

Config = Config1
def job1(iteration):
    np.random.seed()
    df,pop = evology('scholl', 'esl.true', Config[0], Config[1], Config[2], Config[3], Config[4], Config[5], False, False)
    return df['WShare_NT'], df['WShare_VI'], df['WShare_TF']

Config = Config2
def job2(iteration):
    np.random.seed()
    df,pop = evology('scholl', 'esl.true', Config[0], Config[1], Config[2], Config[3], Config[4], Config[5], False, False)
    return df['WShare_NT'], df['WShare_VI'], df['WShare_TF']

Config = Config3
def job3(iteration):
    np.random.seed()
    df,pop = evology('scholl', 'esl.true', Config[0], Config[1], Config[2], Config[3], Config[4], Config[5], False, False)
    return df['WShare_NT'], df['WShare_VI'], df['WShare_TF']

Config = Config4
def job4(iteration):
    np.random.seed()
    df,pop = evology('scholl', 'esl.true', Config[0], Config[1], Config[2], Config[3], Config[4], Config[5], False, False)
    return df['WShare_NT'], df['WShare_VI'], df['WShare_TF']

Config = Config5
def job5(iteration):
    np.random.seed()
    df,pop = evology('scholl', 'esl.true', Config[0], Config[1], Config[2], Config[3], Config[4], Config[5], False, False)
    return df['WShare_NT'], df['WShare_VI'], df['WShare_TF']

Config = Config6
def job6(iteration):
    np.random.seed()
    df,pop = evology('scholl', 'esl.true', Config[0], Config[1], Config[2], Config[3], Config[4], Config[5], False, False)
    return df['WShare_NT'], df['WShare_VI'], df['WShare_TF']

def main1():
    p = mp.Pool()
    data = p.map(job1, [i for i in range(reps)])
    p.close()
    data = np.array(list(data))
    return data

def main2():
    p = mp.Pool()
    data = p.map(job2, [i for i in range(reps)])
    p.close()
    data = np.array(list(data))
    return data

def main3():
    p = mp.Pool()
    data = p.map(job3, [i for i in range(reps)])
    p.close()
    data = np.array(list(data))
    return data

def main4():
    p = mp.Pool()
    data = p.map(job4, [i for i in range(reps)])
    p.close()
    data = np.array(list(data))
    return data

def main5():
    p = mp.Pool()
    data = p.map(job5, [i for i in range(reps)])
    p.close()
    data = np.array(list(data))
    return data

def main6():
    p = mp.Pool()
    data = p.map(job6, [i for i in range(reps)])
    p.close()
    data = np.array(list(data))
    return data

if __name__ == '__main__':
    data = main1()
    dfNT = pd.DataFrame()
    dfVI= pd.DataFrame()
    dfTF = pd.DataFrame()

    for i in range(reps):
        name = 'Rep%s' % i
        dfNT[name] = data[i,0]
        dfVI[name] = data[i,1]
        dfTF[name] = data[i,2]

    dfNT.to_csv("data_config1/MC_NT.csv")
    dfVI.to_csv("data_config1/MC_VI.csv")
    dfTF.to_csv("data_config1/MC_TF.csv")

    data = main2()
    dfNT = pd.DataFrame()
    dfVI= pd.DataFrame()
    dfTF = pd.DataFrame()

    for i in range(reps):
        name = 'Rep%s' % i
        dfNT[name] = data[i,0]
        dfVI[name] = data[i,1]
        dfTF[name] = data[i,2]

    dfNT.to_csv("data_config2/MC_NT.csv")
    dfVI.to_csv("data_config2/MC_VI.csv")
    dfTF.to_csv("data_config2/MC_TF.csv")

    data = main3()
    dfNT = pd.DataFrame()
    dfVI= pd.DataFrame()
    dfTF = pd.DataFrame()

    for i in range(reps):
        name = 'Rep%s' % i
        dfNT[name] = data[i,0]
        dfVI[name] = data[i,1]
        dfTF[name] = data[i,2]

    dfNT.to_csv("data_config3/MC_NT.csv")
    dfVI.to_csv("data_config3/MC_VI.csv")
    dfTF.to_csv("data_config3/MC_TF.csv")

    data = main4()
    dfNT = pd.DataFrame()
    dfVI= pd.DataFrame()
    dfTF = pd.DataFrame()

    for i in range(reps):
        name = 'Rep%s' % i
        dfNT[name] = data[i,0]
        dfVI[name] = data[i,1]
        dfTF[name] = data[i,2]

    dfNT.to_csv("data_config4/MC_NT.csv")
    dfVI.to_csv("data_config4/MC_VI.csv")
    dfTF.to_csv("data_config4/MC_TF.csv")

    data = main5()
    dfNT = pd.DataFrame()
    dfVI= pd.DataFrame()
    dfTF = pd.DataFrame()

    for i in range(reps):
        name = 'Rep%s' % i
        dfNT[name] = data[i,0]
        dfVI[name] = data[i,1]
        dfTF[name] = data[i,2]

    dfNT.to_csv("data_config5/MC_NT.csv")
    dfVI.to_csv("data_config5/MC_VI.csv")
    dfTF.to_csv("data_config5/MC_TF.csv")

    data = main6()
    dfNT = pd.DataFrame()
    dfVI= pd.DataFrame()
    dfTF = pd.DataFrame()

    for i in range(reps):
        name = 'Rep%s' % i
        dfNT[name] = data[i,0]
        dfVI[name] = data[i,1]
        dfTF[name] = data[i,2]

    dfNT.to_csv("data_config6/MC_NT.csv")
    dfVI.to_csv("data_config6/MC_VI.csv")
    dfTF.to_csv("data_config6/MC_TF.csv")











