# %%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import math

# Import the data
if sys.platform == "darwin":
    df = pd.read_csv(
        "/Users/aymericvie/Documents/GitHub/evology/evology/data/replication_data_sample2.csv"
    )

# %%
print(df.columns)
# %%
df.plot(
    x="Unnamed: 0",
    y=["Price", "NT_signal", "VI_signal"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

# %%
df.plot(
    x="Unnamed: 0",
    y=["TF_signal"],
    kind="line",
    figsize=(15, 6),
)
plt.show()
# %%
df.plot(
    x="Unnamed: 0",
    y=["Dividends"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df['Mispricing'] = np.log2(df['VI_signal'] / df['Price'])

df.plot(
    x="Unnamed: 0",
    y=["VI_signal"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

# %%
df.plot(
    x="Unnamed: 0",
    y=["Mispricing"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.plot(
    x="Unnamed: 0",
    y=["VI_stocks"],
    kind="line",
    figsize=(15, 6),
)
plt.show()
# %%
