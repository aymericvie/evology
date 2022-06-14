# %%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import math

# Import the data
if sys.platform == "darwin":
    df = pd.read_csv(
        "/Users/aymericvie/Documents/GitHub/evology/evology/code/oop/rundata/run_data.csv"
    )
if sys.platform == "win32":
    pass
    
# %%
df.plot(
    x="Generation",
    y=["Price"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.plot(
    x="Generation",
    y=["Dividend"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.plot(
    x="Generation",
    y=["Volume"],
    kind="line",
    figsize=(15, 6),
)
plt.show()
# %%
df.plot(
    x="Generation",
    y=["NT_process"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

# %%
df.plot(
    x="Generation",
    y=["WShare_NT", "WShare_VI", "WShare_TF"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.head(20000).plot(
    x="Generation",
    y=["WShare_NT", "WShare_VI", "WShare_TF"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

# %%
from noise_trader import NoiseTrader
import numpy as np
import matplotlib.pyplot as plt

process = NoiseTrader.compute_noise_process(10000, 1)
plt.plot(process)
plt.show()
# %%


process = NoiseTrader.compute_noise_process(10000, np.random.randint(0, 1000))
plt.plot(process)
plt.show()
# %%
