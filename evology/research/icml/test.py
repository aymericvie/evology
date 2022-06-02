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
TimeHorizon = 252 * 30
PopulationSize = 100
reps = 10
scale = 25  # 30 # increment = 1/scale


def job(coords):
    outcome = coords[0]
    return [coords[0], coords[1], coords[2], outcome]
    # except Exception as e:
    #    print(e)
    #    print("Failed run" + str(coords) + str(e))
    #    result = [coords[0], coords[1], coords[2]]
    #    for _ in range(7):
    #        result.append(np.nan)
    #    return result


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
    df["Test"] = data[:, 3]

    # Print and save the dataframes
    print(df)
    df.to_csv("data/data_test.csv")
    print("Completion time: " + str(time.time() - startTime))
