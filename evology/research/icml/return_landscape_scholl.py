# Imports
import numpy as np
import pandas as pd
import sys
import tqdm

# import warnings
import time
import ternary
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
TimeHorizon = 252 * 10
PopulationSize = 100
reps = 10
scale = 25  # increment = 1/scale


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
            reset_wealth=True,
        )
        result = [
            coords[0],  # Initial NT WS
            coords[1],  # Initial VI WS
            coords[2],  # Initial TF WS
            df["NT_returns"].mean(),
            df["VI_returns"].mean(),
            df["TF_returns"].mean(),
            df["NT_returns"].std(),
            df["VI_returns"].std(),
            df["TF_returns"].std(),
            df["Gen"].iloc[-1],
        ]
        return result
    except Exception as e:
        print(e)
        print("Failed run" + str(coords) + str(e))
        result = [coords[0], coords[1], coords[2]]
        for _ in range(6):
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
    df["WS_NT"] = data[:, 0]
    df["WS_VI"] = data[:, 1]
    df["WS_TF"] = data[:, 2]
    # Outputs
    df["NT_returns_mean"] = data[:, 3]
    df["VI_returns_mean"] = data[:, 4]
    df["TF_returns_mean"] = data[:, 5]
    df["NT_returns_std"] = data[:, 6]
    df["VI_returns_std"] = data[:, 7]
    df["TF_returns_std"] = data[:, 8]
    df["Gen"] = data[:, 9]

    # Print and save the dataframes
    print(df)
    df.to_csv("data/data_return_landscape_scholl.csv")
    print("Completion time: " + str(time.time() - startTime))
