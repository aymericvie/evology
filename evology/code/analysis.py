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
