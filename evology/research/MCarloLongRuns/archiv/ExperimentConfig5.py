# Imports
import numpy as np
import pandas as pd
import sys

if sys.platform == "darwin":
    sys.path.append("/Users/aymericvie/Documents/GitHub/evology/evology/code")
    # Need to be executed from cd to MCarloLongRuns
if sys.platform == "linux":
    sys.path.append("/home/vie/Documents/GitHub/evology/evology/code")
from main import main as evology
import multiprocessing as mp

TimeHorizon = (
    252 * 100 + 3 * 21
)  # 100 Years + 3 months to compensate early period without recording data.
PopulationSize = 100
Coordinates = [1 / 3, 1 / 3, 1 / 3]
reps = 50


def job(iteration):
    np.random.seed()
    try:
        df, pop = evology(
            space="scholl",
            solver="esl.true",
            wealth_coordinates=Coordinates,
            POPULATION_SIZE=PopulationSize,
            MAX_GENERATIONS=TimeHorizon,
            PROBA_SELECTION=1 / (252 * 2),
            MUTATION_RATE=1 / (252 * 2),
            ReinvestmentRate=0,
            tqdm_display=True,
            reset_wealth=False,
        )
        return df["WShare_NT"], df["WShare_VI"], df["WShare_TF"]
    except:
        print("Job failed and passed.")
        array = np.zeros((TimeHorizon - 3 * 21))
        return pd.Series(array), pd.Series(array), pd.Series(array)


def main():
    p = mp.Pool()
    data = p.map(job, [i for i in range(reps)])
    p.close()
    data = np.array(list(data))
    return data


if __name__ == "__main__":
    data = main()
    dfNT = pd.DataFrame()
    dfVI = pd.DataFrame()
    dfTF = pd.DataFrame()

    for i in range(reps):
        name = "Rep%s" % i
        dfNT[name] = data[i, 0]
        dfVI[name] = data[i, 1]
        dfTF[name] = data[i, 2]

    dfNT.to_csv("data_config5/MC_NT.csv")
    dfVI.to_csv("data_config5/MC_VI.csv")
    dfTF.to_csv("data_config5/MC_TF.csv")
