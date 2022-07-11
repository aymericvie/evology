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
    df = pd.read_csv(
        r"D:\OneDrive\Research\2021_Market_Ecology\evology\evology\code\oop\rundata\run_data.csv"
    )

# %%
title_fontsize = 20
label_size = 15

ax_color = "black"

fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10, 8))
ax[0].set_title("Stock Price & Fund. Value", fontsize=title_fontsize, color=ax_color)
ax[1].set_title("Volume", fontsize=title_fontsize, color=ax_color)
ax[2].set_title("Wealth Shares", fontsize=title_fontsize, color=ax_color)

ax[0].plot(df.index, df["Price"], color="black", linewidth=1)
ax[0].plot(df.index, df["VI_val"], color="red", linewidth=0.5)
ax[2].plot(df.index, df["WShare_NT"], color="green", label="Noise traders", linewidth=1)
ax[2].plot(df.index, df["WShare_VI"], color="red", label="Value investors", linewidth=1)
ax[2].plot(
    df.index, df["WShare_TF"], color="blue", label="Trend followers", linewidth=1
)
ax[1].plot(df.index, df["Volume"], color="black", linewidth=1)

ax[2].set_xlabel("Time (days)", fontsize=label_size)
ax[2].set_ylabel("Share (%)", fontsize=label_size)
ax[0].set_ylabel("Price", fontsize=label_size)
ax[1].set_ylabel("Volume", fontsize=label_size)
plt.legend(loc=8, fontsize=label_size)

ax[0].yaxis.label.set_color(ax_color)
ax[0].tick_params(axis="x", colors=ax_color)
ax[0].tick_params(axis="y", colors=ax_color)
ax[1].tick_params(axis="x", colors=ax_color)
ax[1].tick_params(axis="y", colors=ax_color)
ax[2].xaxis.label.set_color(ax_color)
ax[1].xaxis.label.set_color(ax_color)
ax[1].yaxis.label.set_color(ax_color)
ax[2].yaxis.label.set_color(ax_color)
ax[2].tick_params(axis="x", colors=ax_color)
ax[2].tick_params(axis="y", colors=ax_color)
plt.tight_layout()
if sys.platform == "darwin":
    plt.savefig(
        "/Users/aymericvie/Documents/GitHub/evology/evology/code/oop/rundata/overview.png",
        dpi=300,
    )
elif sys.platform == "win32":
    plt.savefig(
        r"D:\OneDrive\Research\2021_Market_Ecology\evology\evology\code\oop\rundata\overview.png",
        dpi=300,
    )

plt.show()


# %%
# df.plot(
#     x="Generation",
#     y=["NT_flows", "VI_flows", "TF_flows"],
#     kind="line",
#     figsize=(15, 6),
# )
# plt.show()

span = 252 * 10
df["EMA_NT_flows"] = df["NT_flows"].ewm(span=span).mean()
df["EMA_VI_flows"] = df["VI_flows"].ewm(span=span).mean()
df["EMA_TF_flows"] = df["TF_flows"].ewm(span=span).mean()

df.plot(
    x="Generation",
    y=["EMA_NT_flows", "EMA_VI_flows", "EMA_TF_flows"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.plot(
    x="Generation",
    y=["WShare_NT", "WShare_VI", "WShare_TF"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

#
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
df.plot(
    x="Generation",
    y=["NT_asset", "VI_asset", "TF_asset"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

# Average proportion of shorts 
# For 3 agents, asset supply is 1_500_000
asset_supply = 1_500_000
total_short = 0

for i in range(len(df)):
    if df["NT_asset"].iloc[i] < 0:
        total_short += df["NT_asset"].iloc[i]
    if df["VI_asset"].iloc[i] < 0:
        total_short += df["VI_asset"].iloc[i]
    if df["TF_asset"].iloc[i] < 0:
        total_short += df["TF_asset"].iloc[i]

avg_prop_short = 100 * abs(total_short) / (asset_supply * len(df))
print(avg_prop_short)

# %%
df.plot(
    x="Generation",
    y=["NT_cash", "VI_cash", "TF_cash"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

# %%
df.tail(1000).plot(
    x="Generation",
    y=["NT_process"],
    kind="line",
    figsize=(15, 6),
)
plt.show()
# %%
# %%
