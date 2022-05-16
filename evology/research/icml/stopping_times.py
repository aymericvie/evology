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
TimeHorizon = 252 * 500
obs = 10000
reps = 10
scale = 25 #increment = 1/scale

def job(coords):
    np.random.seed()
    try:
        df, pop, stats = evology(
            strategy = None,
            space = "extended",
            wealth_coordinates = [coords[0], coords[1], coords[2]],
            POPULATION_SIZE = coords[3],
            MAX_GENERATIONS = TimeHorizon,
            tqdm_display = True,
            reset_wealth = False,
        )
        df_tail = df.tail(obs)
        
        stopping_time = TimeHorizon
        df["Rolling_DR"] = df["DiffReturns"].rolling(252).mean()
        for i in range(len(df["Gen"])):
            if df["Rolling_DR"].iloc[i] <= 0.000001:
                stopping_time = i
                break

        result = [
            coords[0],
            coords[1],
            coords[2],
            coords[3],

            df_tail["WShare_NT"].mean(),
            df_tail["WShare_VI"].mean(),
            df_tail["WShare_TF"].mean(),

            stopping_time,
            df["Gen"].iloc[-1],
        ]
        return result
    except Exception as e:
        print(e)
        # traceback.print_stack()
        print("Failed run" + str(coords) + str(e))
        result = [coords[0], coords[1], coords[2], coords[3]]
        for _ in range(6):
            result.append(np.nan)
        return result


# Define the domains
def GenerateCoords(reps, scale):
    param = []
    for popsize in [100, 200, 300, 400, 500, 1000]:
        for (i, j, k) in simplex_iterator(scale):
            for _ in range(reps):
                param.append([i / scale, j / scale, k / scale, popsize])
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
    df["PopSize"] = data[:, 3]

    # Outputs
    df["WS_NT_final"] = data[:, 4]
    df["WS_VI_final"] = data[:, 5]
    df["WS_TF_final"] = data[:, 6]

    df["StopTime"] = data[:, 7]
    df["Gen"] = data[:, 8]

    print(df)

    df.to_csv("data/stop_time.csv")
    print("Completion time: " + str(time.time() - startTime))

    print(df["StopTime"].unique())

