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
    y=["Volume"],
    kind="line",
    figsize=(15, 6),
)
plt.show()
# %%
