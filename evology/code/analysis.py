
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
# Import the data
if sys.platform == 'darwin':
    df = pd.read_csv("/Users/aymericvie/Documents/GitHub/evology/evology/code/rundata/run_data.csv")

print('Average wealth per fund in the strategy')
df.plot(x="Gen", y = ["NT_nav", "VI_nav", "TF_nav", "AV_wealth"],
        kind="line", figsize=(15, 6))
plt.show()
