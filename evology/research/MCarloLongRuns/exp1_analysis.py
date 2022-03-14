import pandas as pd

data = pd.read_csv(
    "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data/data1.csv"
)
# print(data)
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage.filters import gaussian_filter
import ternary
import numpy as np

sns.set(font_scale=1)
fontsize = 18
sigma = 1


def heat_data(original_data, columnX, columnY, columnZ):
    data2 = original_data.copy()
    data_temp = pd.DataFrame()
    data_temp["Gen"] = data2["Unnamed: 0"]
    data_temp["F"] = data2[columnX]
    data_temp["H"] = data2[columnY]
    data_temp["T"] = data2[columnZ]

    data_temp2 = data_temp.groupby(["F", "H"], as_index=False).mean()
    # data_temp2 = data_temp.copy()
    data_ready = data_temp2.pivot(index="H", columns="F", values="T")
    return data_ready


# print(dataNT)
def GenPlot(dataNT, dataVI, dataTF, title1, title2, title3, figname, bounds):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6), sharey=True, sharex=True)
    cmap = "seismic"
    if bounds == True:
        vmin = -0.2
        vmax = 0.2
        sns.heatmap(dataNT, ax=ax1, cmap=cmap, vmin=vmin, vmax=vmax)
        sns.heatmap(dataVI, ax=ax2, cmap=cmap, vmin=vmin, vmax=vmax)
        sns.heatmap(dataTF, ax=ax3, cmap=cmap, vmin=vmin, vmax=vmax)
    else:
        sns.heatmap(dataNT, ax=ax1, cmap=cmap)
        sns.heatmap(dataVI, ax=ax2, cmap=cmap)
        sns.heatmap(dataTF, ax=ax3, cmap=cmap)
    ax1.set_xlabel("Initial Wealth Share NT", fontsize=fontsize)
    ax1.set_ylabel("Initial Wealth Share VI", fontsize=fontsize)
    ax2.set_xlabel("Initial Wealth Share VI", fontsize=fontsize)
    ax2.set_ylabel("Initial Wealth Share NT", fontsize=fontsize)
    ax3.set_xlabel("Initial Wealth Share TF", fontsize=fontsize)
    ax3.set_ylabel("Initial Wealth Share NT", fontsize=fontsize)
    ax1.set_title(title1, fontsize=fontsize)
    ax2.set_title(title2, fontsize=fontsize)
    ax3.set_title(title3, fontsize=fontsize)
    ax1.invert_yaxis()
    ax2.invert_yaxis()
    ax3.invert_yaxis()

    plt.tight_layout()
    plt.savefig(figname, dpi=300)
    plt.show()


dataNT = heat_data(data, "WS_NT", "WS_VI", "NT_returns_mean")
dataVI = heat_data(data, "WS_VI", "WS_NT", "VI_returns_mean")
dataTF = heat_data(data, "WS_TF", "WS_NT", "TF_returns_mean")
fig = GenPlot(
    dataNT,
    dataVI,
    dataTF,
    "NT returns",
    "VI returns",
    "TF returns",
    "Experiment1.png",
    False,
)

data["AvgReturn"] = (
    data["NT_returns_mean"] + data["VI_returns_mean"] + data["TF_returns_mean"]
) / 3
data["Net_NT_returns"] = data["NT_returns_mean"] - data["AvgReturn"]
data["Net_VI_returns"] = data["VI_returns_mean"] - data["AvgReturn"]
data["Net_TF_returns"] = data["TF_returns_mean"] - data["AvgReturn"]

dataNT = heat_data(data, "WS_NT", "WS_VI", "Net_NT_returns")
dataVI = heat_data(data, "WS_VI", "WS_NT", "Net_VI_returns")
dataTF = heat_data(data, "WS_TF", "WS_NT", "Net_TF_returns")
fig = GenPlot(
    dataNT,
    dataVI,
    dataTF,
    "NT net returns",
    "VI net returns",
    "TF net returns",
    "Experiment1b.png",
    True,
)

data["NT_weighted_returns"] = data["NT_returns_mean"] / np.sqrt(data["WS_NT"])
data["VI_weighted_returns"] = data["VI_returns_mean"] / np.sqrt(data["WS_VI"])
data["TF_weighted_returns"] = data["TF_returns_mean"] / np.sqrt(data["WS_TF"])

dataNT = heat_data(data, "WS_NT", "WS_VI", "NT_weighted_returns")
dataVI = heat_data(data, "WS_VI", "WS_NT", "VI_weighted_returns")
dataTF = heat_data(data, "WS_TF", "WS_NT", "TF_weighted_returns")
fig = GenPlot(
    dataNT,
    dataVI,
    dataTF,
    "NT weighted returns",
    "VI weighted returns",
    "TF weighted returns",
    "Experiment1bb.png",
    False,
)

# dataNT = heat_data(data, 'WS_NT', 'WS_VI', 'AvgReturn')
# dataVI = heat_data(data, 'WS_VI', 'WS_NT', 'AvgReturn')
# dataTF = heat_data(data, 'WS_TF', 'WS_NT', 'AvgReturn')
# fig = GenPlot(dataNT, dataVI, dataTF, "AvgReturn", "AvgReturn", "AvgReturn", 'Experiment1c.png', False)

# fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (15,6), sharex=True)
# sns.scatterplot(x="WS_NT", y="NT_returns_mean", data=data, ax=ax1)
# sns.scatterplot(x="WS_VI", y="VI_returns_mean", data=data, ax=ax2)
# sns.scatterplot(x="WS_TF", y="TF_returns_mean", data=data, ax=ax3)
# plt.show()


# order = 1
data1 = data.loc[data["WS_NT"] == 0.1]
data2 = data.loc[data["WS_VI"] == 0.1]

data1["VI_returns_mean"] = np.log(data1["VI_returns_mean"])
data1["TF_returns_mean"] = np.log(data1["TF_returns_mean"])
data2["NT_returns_mean"] = np.log(data2["NT_returns_mean"])

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6), sharex=True)
# sns.regplot(x="WS_NT", y="NT_returns_mean", data=data2, ax=ax1, lowess = True)
# sns.regplot(x="WS_VI", y="VI_returns_mean", data=data1, ax=ax2, lowess = True)
# sns.regplot(x="WS_TF", y="TF_returns_mean", data=data1, ax=ax3, lowess = True)
sns.regplot(
    x="WS_NT", y="NT_returns_mean", data=data2, ax=ax1, lowess=True
)  # order = order)
sns.regplot(
    x="WS_VI", y="VI_returns_mean", data=data1, ax=ax2, lowess=True
)  # , order = order)
sns.regplot(
    x="WS_TF", y="TF_returns_mean", data=data1, ax=ax3, lowess=True
)  # , order = order)
ax1.set_xlabel("Initial Wealth Share NT (VI = 0.1)", fontsize=fontsize)
ax1.set_ylabel("Log NT returns", fontsize=fontsize)
ax2.set_xlabel("Initial Wealth Share VI (NT = 0.1)", fontsize=fontsize)
ax2.set_ylabel("Log VI returns", fontsize=fontsize)
ax3.set_xlabel("Initial Wealth Share TF (NT = 0.1)", fontsize=fontsize)
ax3.set_ylabel("Log TF returns", fontsize=fontsize)
ax1.set_title("Log NT returns vs size", fontsize=fontsize)
ax2.set_title("Log VI returns vs size", fontsize=fontsize)
ax3.set_title("Log TF returns vs size", fontsize=fontsize)
plt.tight_layout()
plt.savefig("Experiment1d", dpi=300)
plt.show()


""" ternary that does not work 
data = pd.read_csv("/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data/data1.csv")
data_group = data.copy()
print(data_group)
data_group = data_group.groupby(['WS_VI', 'WS_TF', 'WS_NT'], as_index=False).mean()
print(data_group)

def generate_random_heatmap_data(scale):
    tf_r = dict()
    vi_r = dict()
    nt_r = dict()

    for l in range(len(data_group['WS_NT'])):
        (i,j,k) = (int(data_group.loc[l,'WS_NT'] * scale), int(data_group.loc[l,'WS_VI'] * scale), int(data_group.loc[l,'WS_TF'] * scale))
        nt_r[(i,j)] = data_group.loc[l,"NT_returns_mean"]
        vi_r[(i,j)] = data_group.loc[l,"VI_returns_mean"]
        tf_r[(i,j)] = data_group.loc[l,"TF_returns_mean"]
    nt_r[(0.4 * scale,0.58 * scale)] = 10
    return nt_r, vi_r, tf_r


def GenerateTernary(data, title):
    figure, tax = ternary.figure(scale=scale)
    figure.set_size_inches(10, 8)
    tax.heatmap(data, style='triangular')
    tax.boundary()
    tax.clear_matplotlib_ticks()
    ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    tax.ticks(ticks = ticks, axis='lbr', linewidth=1, multiple=10)
    tax.bottom_axis_label("NT (%)", fontsize = fontsize) #VI
    tax.left_axis_label("VI (%)", fontsize = fontsize) #NT
    tax.right_axis_label("TF (%)", fontsize = fontsize)
    tax.get_axes().axis('off')
    tax.set_title(title, fontsize = fontsize)
    plt.tight_layout()
    tax._redraw_labels()
    return figure, tax
    
scale = 50
nt_r, vi_r, tf_r = generate_random_heatmap_data(scale)

fig, tax = GenerateTernary(nt_r, 'NT returns')
tax.show()

fig, tax = GenerateTernary(vi_r, 'VI returns')
# tax.show()

fig, tax = GenerateTernary(tf_r, 'TF returns')
# tax.show()

# print(data.columns)
# data2 = data_group.loc[(data_group['WS_TF'] > 0.55) & (data_group['WS_TF'] < 0.65)]
# print(data2)
"""
