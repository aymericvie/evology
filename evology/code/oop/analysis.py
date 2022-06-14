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


title_fontsize = 20
label_size = 15

fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10, 8))
ax[0].set_title('Stock Price & Fund. Value', fontsize=title_fontsize, color='white')
ax[1].set_title('Volume', fontsize=title_fontsize, color = 'white')
ax[2].set_title('Wealth Shares', fontsize=title_fontsize, color = 'white')

ax[0].plot(df.index, df['Price'], color='black', linewidth=1)
ax[0].plot(df.index, df['VI_val'], color='red', linewidth=0.5)
ax[2].plot(df.index, df['WShare_NT'], color='green', label='Noise traders', linewidth=1)
ax[2].plot(df.index, df['WShare_VI'], color='red', label='Value investors', linewidth=1)
ax[2].plot(df.index, df['WShare_TF'], color='blue', label='Trend followers', linewidth=1)
ax[1].plot(df.index, df['Volume'], color = 'black', linewidth = 1)
# ax[1].bar(df.index, df['B'], color='g', label='MACD')

# ax[1].set_xticklabels(df.index, rotation=90)
ax[2].set_xlabel('Time (days)', fontsize = label_size)
ax[2].set_ylabel('Share (%)', fontsize = label_size)
ax[0].set_ylabel('Price', fontsize = label_size)
ax[1].set_ylabel('Volume', fontsize = label_size)
plt.legend(loc=8, fontsize = label_size)

ax[0].yaxis.label.set_color('white')       
ax[0].tick_params(axis='x', colors='white')   
ax[0].tick_params(axis='y', colors='white')
ax[1].tick_params(axis='x', colors='white')   
ax[1].tick_params(axis='y', colors='white')
ax[2].xaxis.label.set_color('white')   
ax[1].xaxis.label.set_color('white')   
ax[1].yaxis.label.set_color('white')   
ax[2].yaxis.label.set_color('white')       
ax[2].tick_params(axis='x', colors='white')   
ax[2].tick_params(axis='y', colors='white')
plt.tight_layout()
plt.savefig('/Users/aymericvie/Documents/GitHub/evology/evology/code/oop/rundata/overview.png', dpi=300)
plt.show()

# %%
df.plot(
    x="Generation",
    y=["NT_process"],
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



# %%

# %%
