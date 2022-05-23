# Imports
import numpy as np
import pandas as pd
from math import isnan
import sys
import tqdm
# import warnings
import time
import ternary
import traceback
from ternary.helpers import simplex_iterator
import multiprocessing as mp

# warnings.simplefilter("ignore")

if sys.platform == "darwin":
    sys.path.append("/Users/aymericvie/Documents/GitHub/evology/evology/code")
    # Need to be executed from cd to MCarloLongRuns
if sys.platform == "linux":
    sys.path.append("/home/vie/Documents/GitHub/evology/evology/code")
from main import main as evology


startTime = time.time()
TimeHorizon = 40_000 #252 * 400 #TBD
PopulationSize = 100# 1000 #TBD
obs = 10000
reps = 10  #TBD
scale = 30

def job(coords):
    
    try:
        df, pop = evology(
            strategy = None,
            space="extended",
            wealth_coordinates = coords,
            POPULATION_SIZE = PopulationSize,
            MAX_GENERATIONS = TimeHorizon,
            seed = np.random.seed(),
            tqdm_display=True,
            reset_wealth=False,
        )

        

        if df["Gen"].iloc[-1] >= 252:
            df["LogPriceReturns"] = np.log(df["Price"]/df["Price"].shift(1))
            df["Volatility"] = df["LogPriceReturns"].rolling(window=252).std()*np.sqrt(252)
            volatility = df["Volatility"].mean()

            df["Mispricing"] = (df["Mean_VI"] / df["Price"]) - 1
            mispricing = df["Mispricing"].mean()
        else:
            volatility = np.nan
            mispricing = np.nan


        if df["NT_nav"].iloc[0] != 0 and isnan(df["NT_nav"].iloc[0]) == False:
            multi_NT = df["NT_nav"].iloc[-1] / df["NT_nav"].iloc[0]
        else:
            multi_NT = 0.0

        if df["VI_nav"].iloc[0] != 0 and isnan(df["VI_nav"].iloc[0]) == False:
            multi_VI = df["VI_nav"].iloc[-1] / df["VI_nav"].iloc[0]
        else:
            multi_VI = 0.0

        if df["TF_nav"].iloc[0] != 0 and isnan(df["TF_nav"].iloc[0]) == False:
            multi_TF = df["TF_nav"].iloc[-1] / df["TF_nav"].iloc[0]
        else:
            multi_TF = 0.0

        multi_BH = df["BH_wealth"].iloc[-1] / df["BH_wealth"].iloc[0]
        multi_IR = df["IR_wealth"].iloc[-1] / df["IR_wealth"].iloc[0] 

        df_tail = df.tail(obs)
        result = [
            coords[0],
            coords[1],
            coords[2],

            df_tail["WShare_NT"].mean(),
            df_tail["WShare_VI"].mean(),
            df_tail["WShare_TF"].mean(),

            mispricing,
            volatility,

            df_tail["NT_returns"].mean(),
            df_tail["VI_returns"].mean(),
            df_tail["TF_returns"].mean(),
            df_tail["NT_returns"].std(),
            df_tail["VI_returns"].std(),
            df_tail["TF_returns"].std(),

            df_tail["DiffReturns"].mean(),

            df["Gen"].iloc[-1],

            df_tail["Mean_NT"].mean(),
            df_tail["Mean_VI"].mean(),
            df_tail["Mean_TF"].mean(),

            df_tail["NT_Sub_Var"].mean(),
            df_tail["VI_Sub_Var"].mean(),
            df_tail["TF_Sub_Var"].mean(),

            multi_NT,
            multi_VI,
            multi_TF,
            multi_BH,
            multi_IR


            
        ]
        return result
    except Exception as e:
        print(e)
        # traceback.print_stack()
        print("Failed run" + str(coords) + str(e))
        result = [coords[0], coords[1], coords[2]]
        for _ in range(24):
            result.append(np.nan)
        return result


# Define the domains
def GenerateCoords(reps, scale):
    param = []
    for (i, j, k) in simplex_iterator(scale):
        for _ in range(reps):
            param.append([i / scale, j / scale, k / scale])
    return param
param = GenerateCoords(reps, scale)
print(len(param))

# Run experiment
def main():
    p = mp.Pool()
    data = p.map(job, tqdm.tqdm(param))
    p.close()
    data = np.array(data)
    return data


if __name__ == "__main__":
    data = main()
    df = pd.DataFrame()
    # Inputs
    df["WS_NT_initial"] = data[:, 0]
    df["WS_VI_initial"] = data[:, 1]
    df["WS_TF_initial"] = data[:, 2]
    # Outputs
    df["WS_NT_final"] = data[:, 3]
    df["WS_VI_final"] = data[:, 4]
    df["WS_TF_final"] = data[:, 5]

    df["Mispricing"] = data[:, 6]
    df["Volatility"] = data[:, 7]

    df["NT_returns_final"] = data[:, 8]
    df["VI_returns_final"] = data[:, 9]
    df["TF_returns_final"] = data[:, 10]
    df["NT_returns_final_std"] = data[:, 11]
    df["VI_returns_final_std"] = data[:, 12]
    df["TF_returns_final_std"] = data[:, 13]

    df["DiffReturns"] = data[:, 14]
    df["Gen"] = data[:, 15]

    df["Mean_NT"] = data[:, 16]
    df["Mean_VI"] = data[:, 17]
    df["Mean_TF"] = data[:, 18]

    df["Var_NT"] = data[:, 19]
    df["Var_VI"] = data[:, 20]
    df["Var_TF"] = data[:, 21]

    df["Multiplier_NT"] = data[:, 22]
    df["Multiplier_VI"] = data[:, 23]
    df["Multiplier_TF"] = data[:, 24]
    df["Multiplier_BH"] = data[:, 25]
    df["Multiplier_IR"] = data[:, 26]

    print(df)

    df.to_csv("data/asym_dis_ext.csv")
    print("Completion time: " + str(time.time() - startTime))

