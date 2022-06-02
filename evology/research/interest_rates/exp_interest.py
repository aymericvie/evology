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
TimeHorizon = 100_000 
PopulationSize = 1000
obs = 10000
reps = 100
coords = [0.1, 0.8, 0.1]


def job(param):
    try:
        df, pop = evology(
            strategy=None,
            space="extended",
            wealth_coordinates=coords,
            POPULATION_SIZE=PopulationSize,
            MAX_GENERATIONS=TimeHorizon,
            interest_year=param[0],
            investment=None,
            seed=param[1],
            tqdm_display=True,
            reset_wealth=False,
        )
        # Compute mispricing
        df["Mispricing"] = (df["Mean_VI"] / df["Price"]) - 1
        mispricing = df["Mispricing"].mean()

        # Compute volatility
        if df["Gen"].iloc[-1] >= 252:
            df["LogPriceReturns"] = np.log(df["Price"] / df["Price"].shift(1))
            df["Volatility"] = df["LogPriceReturns"].rolling(
                window=252
            ).std() * np.sqrt(252)
            volatility = df["Volatility"].mean()
        else:
            volatility = np.nan
            print('Failed to compute volatility: not enough generations.')
            
        df_tail = df.tail(obs)
        result = [
            # Seed 
            param[0],
            param[1],

            # Final wealth share (means)
            df_tail["WShare_NT"].mean(),
            df_tail["WShare_VI"].mean(),
            df_tail["WShare_TF"].mean(),

            # Average wealth share
            df["WShare_NT"].mean(),
            df["WShare_VI"].mean(),
            df["WShare_TF"].mean(),
            df["WShare_NT"].std(),
            df["WShare_VI"].std(),
            df["WShare_TF"].std(),

            # Market malfunction
            mispricing,
            volatility,

            # Final returns (means and std)
            df_tail["NT_returns"].mean(),
            df_tail["VI_returns"].mean(),
            df_tail["TF_returns"].mean(),
            df_tail["NT_returns"].std(),
            df_tail["VI_returns"].std(),
            df_tail["TF_returns"].std(),

            # Average returns (means and std)
            df["NT_returns"].mean(),
            df["VI_returns"].mean(),
            df["TF_returns"].mean(),
            df["NT_returns"].std(),
            df["VI_returns"].std(),
            df["TF_returns"].std(),

            # Convergence / early exit metrics
            df_tail["DiffReturns"].mean(),
            df["Gen"].iloc[-1],

            # Substrategies compositions
            df_tail["Mean_NT"].mean(),
            df_tail["Mean_VI"].mean(),
            df_tail["Mean_TF"].mean(),

            df["Mean_NT"].mean(),
            df["Mean_VI"].mean(),
            df["Mean_TF"].mean(),

            df["Mean_NT"].std(),
            df["Mean_VI"].std(),
            df["Mean_TF"].std(),
        ]
        return result
    except Exception as e:
        print(e)
        # traceback.print_stack()
        print("Failed run" + str(param) + str(e))
        result = [param[0], param[1]]
        for _ in range(34):
            result.append(np.nan)
        return result


# Define the domains
randoms = np.random.randint(0, 100000, reps)
param = []
for seed in randoms:
    param.append([0.01, int(seed)])
    param.append([0.02, int(seed)])
print(len(param)) 

def main():
    p = mp.Pool()
    data = p.map(job, tqdm.tqdm(param))
    p.close()
    data = np.array(data)
    return data

# Run experiment
if __name__ == "__main__":
    data = main()
    df = pd.DataFrame()

    # Inputs
    df["interest_rate"] = data[:, 0]
    df["seed"] = data[:, 1]

    # Outputs
    df["WS_NT_final"] = data[:, 2]
    df["WS_VI_final"] = data[:, 3]
    df["WS_TF_final"] = data[:, 4]

    df["WS_NT_avg"] = data[:, 5]
    df["WS_VI_avg"] = data[:, 6]
    df["WS_TF_avg"] = data[:, 7]
    df["WS_NT_avg_std"] = data[:, 8]
    df["WS_VI_avg_std"] = data[:, 9]
    df["WS_TF_avg_std"] = data[:, 10]

    df["Mispricing"] = data[:, 11]
    df["Volatility"] = data[:, 12]

    df["NT_returns_final"] = data[:, 13]
    df["VI_returns_final"] = data[:, 14]
    df["TF_returns_final"] = data[:, 15]
    df["NT_returns_final_std"] = data[:, 16]
    df["VI_returns_final_std"] = data[:, 17]
    df["TF_returns_final_std"] = data[:, 18]

    df["NT_returns_avg"] = data[:, 19]
    df["VI_returns_avg"] = data[:, 20]
    df["TF_returns_avg"] = data[:, 21]
    df["NT_returns_avg_std"] = data[:, 22]
    df["VI_returns_avg_std"] = data[:, 23]
    df["TF_returns_avg_std"] = data[:, 24]

    df["DiffReturns"] = data[:, 25]
    df["Gen"] = data[:, 26]

    df["Mean_NT_final"] = data[:, 27]
    df["Mean_VI_final"] = data[:, 28]
    df["Mean_TF_final"] = data[:, 29]
    df["Mean_NT_avg"] = data[:, 30]
    df["Mean_VI_avg"] = data[:, 31]
    df["Mean_TF_avg"] = data[:, 32]
    df["Mean_NT_avg_std"] = data[:, 33]
    df["Mean_VI_avg_std"] = data[:, 34]
    df["Mean_TF_avg_std"] = data[:, 35]

    print(df)

    df.to_csv("data/ir_noinv.csv")
    print("Completion time: " + str(time.time() - startTime))
