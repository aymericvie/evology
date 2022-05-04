# Imports
import numpy as np
import pandas as pd
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
TimeHorizon = 252 * 400
PopulationSize = 1000
obs = 10000
reps = 10 
scale = 30 # increment = 1/scale

def job(coords):
    np.random.seed()
    try:
        df, pop = evology(
            space="scholl",
            solver="linear",
            wealth_coordinates=coords,
            POPULATION_SIZE=PopulationSize,
            MAX_GENERATIONS=TimeHorizon,
            PROBA_SELECTION=0,
            MUTATION_RATE=0,
            tqdm_display=True,
            reset_wealth=False,
        )
        df_tail = df.tail(obs)
        result = [
            coords[0],
            coords[1],
            coords[2],

            df_tail["WShare_NT"].mean(),
            df_tail["WShare_VI"].mean(),
            df_tail["WShare_TF"].mean(),

            df_tail["NT_returns"].mean(),
            df_tail["VI_returns"].mean(),
            df_tail["TF_returns"].mean(),
            df_tail["NT_returns"].std(),
            df_tail["VI_returns"].std(),
            df_tail["TF_returns"].std(),

            df_tail["DiffReturns"].mean(),
            df["DiffReturns"].mean(),

            df["Gen"].iloc[-1],

            df_tail["Mean_NT"].mean(),
            df_tail["Mean_VI"].mean(),
            df_tail["Mean_TF"].mean(),
        ]
        return result
    except Exception as e:
        print(e)
        # traceback.print_stack()
        print("Failed run" + str(coords) + str(e))
        result = [coords[0], coords[1], coords[2]]
        for _ in range(12):
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

    df["NT_returns_final"] = data[:, 6]
    df["VI_returns_final"] = data[:, 7]
    df["TF_returns_final"] = data[:, 8]
    df["NT_returns_final_std"] = data[:, 9]
    df["VI_returns_final_std"] = data[:, 10]
    df["TF_returns_final_std"] = data[:, 11]

    df["DiffReturns"] = data[:, 12]
    df["AvgDiffReturns"] = data[:, 13]

    df["Gen"] = data[:, 14]

    df["Mean_NT"] = data[:, 15]
    df["Mean_VI"] = data[:, 16]
    df["Mean_TF"] = data[:, 17]

    print(df)

    df.to_csv("data/asym_dis_scholl.csv")
    print("Completion time: " + str(time.time() - startTime))

