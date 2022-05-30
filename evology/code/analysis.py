# %%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from py import process
df = pd.read_csv("/Users/aymericvie/Documents/GitHub/evology/evology/code/rundata/run_data.csv")


# %%
df.plot(x="Gen", y = ['Price'],
        kind="line", figsize=(15, 6))
# plt.savefig('/Users/aymericvie/Documents/GitHub/evology/evology/figures/validation/dividends.png')
plt.show()

# %%
df.plot(x="Gen", y = ['NT_process'],
        kind="line", figsize=(15, 6))
plt.show()

df.plot(x="Gen", y = ['NT_stocks'],
        kind="line", figsize=(15, 6))
plt.show()

# %%
df.plot(x="Gen", y = ['Volume'],
        kind="line", figsize=(15, 6))
plt.show()
# %%
df.plot(x="Gen", y = ['Mismatch'],
        kind="line", figsize=(15, 6))
plt.show()
# %%
GAMMA_NT = 0.2 * np.sqrt(1 / 252)
MU_NT = 1.
RHO_NT = 0.00045832561

def ExogeneousProcess(MAX_GENERATIONS, rng):
    process_series = []
    value = 1. # Initial value of the process
    randoms = rng.normal(0, 1, MAX_GENERATIONS)

    for i in range(MAX_GENERATIONS):
        value = value + RHO_NT * (MU_NT - 1. - value) + GAMMA_NT * randoms[i]
        process_series.append(value)

    return process_series

# %%
import numpy as np
prices = [100, 10, 20, 10, 30]
subset = prices[-2:]
print(subset)
print(np.mean(subset))
# %%

def subset_means(series, max_lag):
        subset_list = [series[-i:] for i in range(1, max_lag + 1)]
        means = [np.mean(subset) for subset in subset_list]
        return means

print(subset_means(prices, 5))


# %%
import numpy as np

x_values = [1, 2, 3, 4, 5]
x = [.05 , .2, .2, .5, .05 ]

# sample from `x` 100 times according to `x`
n_samples = 100
samples = np.random.choice(x_values, n_samples, p=x)

print(samples)

# %%
