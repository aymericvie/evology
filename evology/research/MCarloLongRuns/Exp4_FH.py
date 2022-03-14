# Imports
import numpy as np
import pandas as pd
import sys
import tqdm
import warnings
import time
import ternary
import traceback
from ternary.helpers import simplex_iterator
import multiprocessing as mp

warnings.simplefilter("ignore")

if sys.platform == "darwin":
    sys.path.append("/Users/aymericvie/Documents/GitHub/evology/evology/code")
    # Need to be executed from cd to MCarloLongRuns
if sys.platform == "linux":
    sys.path.append("/home/vie/Documents/GitHub/evology/evology/code")
from main import main as evology


startTime = time.time()
TimeHorizon = 100_000
PopulationSize = 3
obs = 10000


def job(param):
    np.random.seed()
    try:
        df, pop = evology(
            space="scholl",
            solver="esl.true",
            wealth_coordinates=[1 / 3, 1 / 3, 1 / 3],
            POPULATION_SIZE=PopulationSize,
            MAX_GENERATIONS=TimeHorizon,
            PROBA_SELECTION=0,
            MUTATION_RATE=0,
            ReinvestmentRate=param[0],
            InvestmentHorizon=param[1],
            InvestorBehavior="profit",
            tqdm_display=True,
            reset_wealth=False,
        )
        df_tail = df.tail(obs)
        result = [
            param[0],
            param[1],
            df_tail["WShare_NT"].mean(),
            df_tail["WShare_VI"].mean(),
            df_tail["WShare_TF"].mean(),
            df_tail["DiffReturns"].mean(),
            df["DiffReturns"].mean(),
            df["HighestT"].mean(),
        ]
        return result
    except Exception as e:
        print(e)
        # traceback.print_stack()
        print("Failed run" + str(param) + str(e))
        result = [param[0], param[1]]
        for _ in range(6):
            result.append(np.nan)
        return result


# Define the domains
domain_f = [x / 10.0 for x in range(10, 31, 1)]
domain_H = [x for x in range(21, 252, 21 * 2)]
addH = [x for x in range(253, 252 * 4, 21 * 6)]
for z in addH:
    domain_H.append(z)


def GenerateParam(reps):
    param = []
    for i in range(len(domain_f)):
        for j in range(len(domain_H)):
            for _ in range(reps):
                config = [domain_f[i], domain_H[j]]
                param.append(config)
    return param


reps = 15
param = GenerateParam(reps)
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
    df["F"] = data[:, 0]
    df["H"] = data[:, 1]
    # Outputs
    df["WS_NT_final"] = data[:, 2]
    df["WS_VI_final"] = data[:, 3]
    df["WS_TF_final"] = data[:, 4]
    df["DiffReturns"] = data[:, 5]
    df["AvgDiffReturns"] = data[:, 6]
    df["HighestT"] = data[:, 7]
    print(df)

    df.to_csv("data/data4.csv")
    print("Completion time: " + str(time.time() - startTime))
