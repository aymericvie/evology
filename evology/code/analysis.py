# %%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import math

# Import the data
if sys.platform == "darwin":
    df = pd.read_csv(
        "/Users/aymericvie/Documents/GitHub/evology/evology/code/rundata/run_data.csv"
    )
if sys.platform == "win32":
    df = pd.read_csv(
        "D:/OneDrive/Research/2021_Market_Ecology/evology/evology/code/rundata/run_data.csv"
    )

def sigmoid(x):
    return 1. / (1. + np.exp(-x))


# %%


df["Dividends (x1,000)"] = 10000 * df["Dividends"]
df["Process (x100)"] = 100 * df["NT_process"].add(1)
df["VI_val_1000"] = df["VI_val"]
df["PriceEma"] = pd.Series.ewm(df["Price"], span=21).mean()

df.plot(
    x="Gen",
    y=["Price", "VI_val_1000"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.plot(x="Gen", y=["NT_asset", "VI_asset", "TF_asset"], kind="line", figsize=(15, 6))
plt.hlines(y=0, xmin=0, xmax=max(df["Gen"]), colors="gray", linestyles="dashed")
plt.show()

df.plot(
    x="Gen", y=["NT_signal", "VI_signal", "TF_signal"], kind="line", figsize=(15, 6)
)

df.plot(
    x="Gen",
    y=["Dividends"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.plot(
    x="Gen",
    y=["NT_process"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df["NT_returns_ma"] = df["NT_returns"].rolling(252 * 10).mean()
df["VI_returns_ma"] = df["VI_returns"].rolling(252 * 10).mean()
df["TF_returns_ma"] = df["TF_returns"].rolling(252 * 10).mean()

print([df["NT_returns"].mean(), df["VI_returns"].mean(), df["TF_returns"].mean()])

df.plot(
    x="Gen",
    y=["NT_returns_ma", "VI_returns_ma", "TF_returns_ma"],
    kind="line",
    figsize=(15, 6),
)
plt.hlines(y=0, xmin=0, xmax=max(df["Gen"]), colors="gray", linestyles="dashed")
plt.show()


df.plot(
    x="Gen",
    y=["WShare_TF", "WShare_VI", "WShare_NT", "AV_WShare"],
    kind="line",
    figsize=(15, 6),
    ylim=(0, 100),
)
plt.show()




df.plot(x="Gen", y=["Volume"], kind="line", figsize=(15, 6))
plt.show()

df.plot(x="Gen", y=["Pos-"], kind="line", figsize=(15, 6))
plt.show()

df.plot(
    x="Gen",
    y=["NT_cash", "VI_cash", "TF_cash"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

# %%

df["Mispricing"] = np.log2(df["VI_val"] / df["Price"])
mispricing = df["Mispricing"].mean()
df.plot(x="Gen", y=["Mispricing"], kind="line", figsize=(15, 6))
plt.show()

df.plot(
    x="Gen",
    y=["NT_edv", "VI_edv", "TF_edv"],
    kind="line",
    figsize=(15, 6),
)
plt.show()



# %%




df["NT_signal2"] = sigmoid(df["NT_signal"]) - 0.5
df["VI_signal2"] = sigmoid(df["VI_signal"]) - 0.5
df["TF_signal2"] = sigmoid(df["TF_signal"]) - 0.5


df.plot(
    x="Gen", y=["NT_signal2", "VI_signal2", "TF_signal2"], kind="line", figsize=(15, 6)
)

df["NT_signalW"] = (sigmoid(df["NT_signal"]) - 0.5) * df["WShare_NT"]
df["VI_signalW"] = (sigmoid(df["VI_signal"]) - 0.5) * df["WShare_VI"]
df["TF_signalW"] = (sigmoid(df["TF_signal"]) - 0.5) * df["WShare_TF"]

df.plot(
    x="Gen", y=["NT_signalW", "VI_signalW", "TF_signalW"], kind="line", figsize=(15, 6)
)
plt.hlines(y=0, xmin=0, xmax=max(df["Gen"]), colors="gray", linestyles="dashed")
plt.show()

df["NT_signalW"] = (sigmoid(df["NT_signal"])- 0.5) * df["NT_nav"]
df["VI_signalW"] = (sigmoid(df["VI_signal"])- 0.5) * df["VI_nav"]
df["TF_signalW"] = (sigmoid(df["TF_signal"])- 0.5) * df["TF_nav"]

df.plot(
    x="Gen", y=["NT_signalW", "VI_signalW", "TF_signalW"], kind="line", figsize=(15, 6)
)
plt.hlines(y=0, xmin=0, xmax=max(df["Gen"]), colors="gray", linestyles="dashed")
plt.show()

#%%
df["NT_signalW_ma"] = df["NT_signalW"].rolling(10000).mean()
df["VI_signalW_ma"] = df["VI_signalW"].rolling(10000).mean()
df["TF_signalW_ma"] = df["TF_signalW"].rolling(10000).mean()

df.plot(
    x="Gen", y=["NT_signalW_ma", "VI_signalW_ma", "TF_signalW_ma"], kind="line", figsize=(15, 6)
)
plt.hlines(y=20, xmin=0, xmax=max(df["Gen"]), colors="gray", linestyles="dashed")
plt.hlines(y=15, xmin=0, xmax=max(df["Gen"]), colors="gray", linestyles="dashed")
plt.hlines(y=10, xmin=0, xmax=max(df["Gen"]), colors="gray", linestyles="dashed")

plt.show()



# %%

df.plot(
    x="Gen",
    y=["NT_cash", "VI_cash", "TF_cash"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.plot(
    x="Gen",
    y=["NT_loans", "VI_loans", "TF_loans"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.plot(
    x="Gen", y=["NT_stocks", "VI_stocks", "TF_stocks"], kind="line", figsize=(15, 6)
)
plt.hlines(y=0, xmin=0, xmax=max(df["Gen"]), colors="gray", linestyles="dashed")
plt.show()




# %%
df["Mispricing"] = np.log2(df["VI_val"] / df["Price"])
mispricing = df["Mispricing"].mean()


if df["Gen"].iloc[-1] >= 252:
    df["LogPriceReturns"] = np.log(df["Price"] / df["Price"].shift(1))
    df["Volatility"] = df["LogPriceReturns"].rolling(window=252).std() * np.sqrt(252)
    volatility = df["Volatility"].mean()

    df.plot(x="Gen", y=["Mispricing"], kind="line", figsize=(15, 6))
    plt.show()
    df.plot(x="Gen", y=["Volatility"], kind="line", figsize=(15, 6))
    plt.show()

df["Mispricing"] = np.tanh(df["VI_val"] / df["Price"] - 1)
mispricing = df["Mispricing"].mean()


df.plot(x="Gen", y=["Mispricing"], kind="line", figsize=(15, 6))
plt.show()




# %%
df["TF_signal2x100"] = 100 * np.tanh(df["TF_signal"])
df["NT_signal2x100"] = 100 * np.tanh(df["NT_signal"])
df["VI_signal2x100"] = 100 * np.tanh(df["VI_signal"])

df["Price_ma"] = df["Price"].rolling(50).mean()

df.plot(
    x="Gen",
    y=["Price", "Price_ma", "TF_signal2x100", "VI_signal2x100", "NT_signal2x100"],
    kind="line",
    figsize=(15, 6),
)
plt.hlines(y=0, xmin=0, xmax=max(df["Gen"]), color="black")
plt.show()
# %%



df.plot(x="Gen", y=["Pos-"], kind="line", figsize=(15, 6))
plt.show()

df.plot(x="Gen", y=["Volume"], kind="line", figsize=(15, 6))
plt.show()

df.plot(x="Gen", y=["Mismatch"], kind="line", figsize=(15, 6))
plt.show()

# %%
df["divlog"] = np.log(df["Dividends"])
df.plot(x="Gen", y=["divlog"], kind="line", figsize=(15, 6))
plt.show()

# %%

df.plot(x="Gen", y=["Price"], kind="line", figsize=(15, 6))
plt.show()

df.plot(x="Gen", y=["Dividends"], kind="line", figsize=(15, 6))
plt.show()

df.plot(x="Gen", y=["NT_process"], kind="line", figsize=(15, 6))
plt.show()

# %%
pct_changes = list(df["nav_pct"])
# print(pct_changes)
print(np.nanmean(pct_changes))
print(len(pct_changes))
for i in range(len(pct_changes)):
    if pct_changes[i] > 100:
        pct_changes[i] = np.nan
print(np.nanmean(pct_changes))
print(max(pct_changes))
bins = range(0, 100)
bins = [item / 100 for item in bins]
plt.hist(pct_changes, bins=bins)
plt.show()
# bins = range(0,10)
# bins = [item / 100 for item in bins]
# plt.hist(pct_changes, bins = bins)
# plt.show()


# %%
# Calibration of short volume ratio

print("short volume ratio")
asset_supply = df["Pos+"].mean() - df["Pos-"].mean()
# Average short volume ratio in our ABM:
print(100 * df["Pos-"].mean() / asset_supply)

print("Short ratio (numb short sold / avg rolling volume)")
# Short interest ratio as days to cover
df["short_ratio"] = df["Pos-"] / (df["Volume"] + 1)
print(df["short_ratio"].mean())
print(df["Pos-"].mean() / df["Volume"].mean())

# Short interest as percentage of float (outstanding)
print("Short % of float ")
df["FloatPer"] = df["Pos-"] / df["Pos+"]
# df["FloatPer"] = df["Pos-"] / asset_supply
print(100 * df["FloatPer"].mean())

df.plot(x="Gen", y=["Pos-", "Pos+"], kind="line", figsize=(15, 6))
plt.show()

# the short volume ratio and short percentage of float are consistent after limiting max short size
# However, the short ratio (to volumne) is higher. It mostly means that the short positions are liquidated much faster in our model.
# But siunce they still occupy the same relative amount to outstanding shares, it just means that they are closed/opened at higher frequencies
# than in regular data. Which makes sense because not all happens at a daily scale, and there are some funds who maintain short positions
# over long time horizons.

# %%

df.plot(x="Gen", y=["Mismatch"], kind="line", figsize=(15, 6))
plt.show()


df.plot(x="Gen", y=["NT_signal"], kind="line", figsize=(15, 6))
plt.show()
# %%

df.plot(x="Gen", y=["Mean_NT"], kind="line", figsize=(5, 6))
plt.show()
df.plot(x="Gen", y=["Mean_VI"], kind="line", figsize=(5, 6), ylim=(-0.02, 0.02))
plt.show()
df.plot(x="Gen", y=["Mean_TF"], kind="line", figsize=(5, 6))
plt.show()
# %%
df.plot(
    x="Gen",
    y=["NT_stocks", "VI_stocks", "TF_stocks", "BH_stocks", "IR_stocks"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.plot(x="Gen", y=["Price"], kind="line", figsize=(15, 6))
plt.show()


df.plot(x="Gen", y=["Pos-"], kind="line", figsize=(15, 6))
plt.show()


# %%

avg = df.tail(1000)["DiffReturns"].mean()
print(avg)


avg = df.tail(252)["DiffReturns"].mean()
print(avg)

# what is the first time after which we have spent 252 days with negligeable diff returns?
df["Rolling_DR"] = df["DiffReturns"].rolling(252).mean()

tol = 0.000001

df.plot(x="Gen", y=["Rolling_DR"], kind="line", figsize=(15, 6))
plt.hlines(y=tol, xmin=0, xmax=20000)
plt.show()

for i in range(len(df["Gen"])):
    if df["Rolling_DR"].iloc[i] <= tol:
        print(i)
        break

# %%
SharpeNT = np.nanmean(df["NT_returns"]) / np.nanstd(df["NT_returns"])
SharpeVI = np.nanmean(df["VI_returns"]) / np.nanstd(df["VI_returns"])
SharpeTF = np.nanmean(df["TF_returns"]) / np.nanstd(df["TF_returns"])

print("Daily Sharpe ratios ")
print(SharpeNT, SharpeVI, SharpeTF)
print("Daily mean returns 2 ")
print(
    [
        np.nanmean(df["NT_returns"]),
        np.nanmean(df["VI_returns"]),
        np.nanmean(df["TF_returns"]),
    ]
)

DiffSharpe = (
    (SharpeNT - SharpeVI) ** 2 + (SharpeNT - SharpeTF) ** 2 + (SharpeVI - SharpeTF) ** 2
)
print(DiffSharpe)

# %%
print(df["Rep"].sum())
if df["Rep"].sum() != 0:
    df.plot(x="Gen", y=["Rep"], kind="line", figsize=(15, 6))
    plt.show()

df2 = pd.DataFrame()
df2["nav_pct-non-nan"] = df["nav_pct"].dropna()
df2["nav_pct-non-nan"] = df2["nav_pct-non-nan"][df2["nav_pct-non-nan"] < 1000]
df2["Gen"] = df["Gen"]
df2.plot(x="Gen", y=["nav_pct-non-nan"], kind="line", figsize=(15, 6))
plt.show()

# %%# Basic plots

df.plot(x="Gen", y=["Num_TF", "Num_VI", "Num_NT"], kind="line", figsize=(15, 6))
plt.savefig(
    "/Users/aymericvie/Documents/GitHub/evology/evology/figures/num_evo.png", dpi=300
)
plt.show()

# %%
""" NAV """
print("Average wealth per fund in the strategy")
df.plot(
    x="Gen",
    y=["NT_nav", "VI_nav", "TF_nav", "AV_wealth", "BH_wealth", "IR_wealth"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.plot(x="Gen", y="AV_wealth")
plt.show()

NT_mul = df["NT_nav"].iloc[-1] / df["NT_nav"].iloc[0]
print(NT_mul)
NT_mul = df["VI_nav"].iloc[-1] / df["VI_nav"].iloc[0]
print(NT_mul)


# %%

df.plot(
    x="Gen",
    y=["NT_loans", "VI_loans", "TF_loans"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.plot(
    x="Gen",
    y=["NT_cash", "VI_cash", "TF_cash"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.plot(
    x="Gen",
    y=["NT_lending", "VI_lending", "TF_lending"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.plot(
    x="Gen",
    y=["NT_nav", "VI_nav", "TF_nav"],
    kind="line",
    figsize=(15, 6),
)
plt.show()
# %%

# %%
df.tail(100).plot(
    x="Gen",
    y=["Price"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.tail(100).plot(
    x="Gen",
    y=["Mismatch"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.tail(100).plot(
    x="Gen",
    y=["NT_cash"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.tail(100).plot(
    x="Gen",
    y=["VI_cash"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.tail(100).plot(
    x="Gen",
    y=["TF_cash"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.tail(100).plot(
    x="Gen",
    y=["NT_asset"],
    kind="line",
    figsize=(15, 6),
)
plt.show()
df.tail(100).plot(
    x="Gen",
    y=["NT_signal", "VI_signal", "TF_signal"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

# Why positive mismatch on the last 15-20 days before the spike?
# 

df.tail(100).plot(
    x="Gen",
    y=["Pos-"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.tail(100).plot(
    x="Gen",
    y=["Price", "VI_val"],
    kind="line",
    figsize=(15, 6),
)
plt.show()
# %%
df.tail(100).plot(
    x="Gen",
    y=["Dividends"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.tail(100).plot(
    x="Gen",
    y=["VI_val"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.tail(100).plot(
    x="Gen",
    y=["VI_signal"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.tail(100).plot(
    x="Gen",
    y=["NT_asset", "VI_asset", "TF_asset"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

# %%
df.tail(100).plot(
    x="Gen",
    y=["NT_process"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.tail(100).plot(
    x="Gen",
    y=["NT_signal"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

#%%
df['Mispricing'] = np.log2(df['VI_val'] / df['Price'])

df.tail(100).plot(
    x="Gen",
    y=["Mispricing"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df.tail(100).plot(
    x="Gen",
    y=["VI_signal"],
    kind="line",
    figsize=(15, 6),
)
plt.show()

df["VI_signal2"] = sigmoid(df["VI_signal"]) - 0.5

df.tail(100).plot(
    x="Gen",
    y=["VI_signal2"],
    kind="line",
    figsize=(15, 6),
)
plt.show()
# %%
df.tail(100).plot(
    x="Gen",
    y=["WShare_TF", "WShare_VI", "WShare_NT", "AV_WShare"],
    kind="line",
    figsize=(15, 6),
    ylim=(0, 100),
)
plt.show()

df.tail(100).plot(
    x="Gen",
    y=["NT_cash"],
    kind="line",
    figsize=(15, 6),
)
plt.show()
df.tail(100).plot(
    x="Gen",
    y=["VI_cash"],
    kind="line",
    figsize=(15, 6),
)
plt.show()
df.tail(100).plot(
    x="Gen",
    y=["TF_cash"],
    kind="line",
    figsize=(15, 6),
)
plt.show()