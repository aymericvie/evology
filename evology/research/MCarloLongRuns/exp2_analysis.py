import pandas as pd

data = pd.read_csv(
    "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data/data2.csv"
)
print(data)
import matplotlib.pyplot as plt
import seaborn as sns

print(data.columns)
import numpy as np
from scipy.ndimage.filters import gaussian_filter

sigma = 2

sns.set(font_scale=1)
fontsize = 18


def heat_data(original_data, columnX, columnY, columnZ):
    data2 = original_data.copy()
    data_temp = pd.DataFrame()
    # data_temp['Gen'] = data2['Unnamed: 0']
    data_temp["F"] = data2[columnX]
    data_temp["H"] = data2[columnY]
    data_temp["T"] = data2[columnZ]

    data_temp2 = data_temp.groupby(["F", "H"], as_index=False).mean()
    # data_temp2 = data_temp.copy()
    data_ready = data_temp2.pivot(index="H", columns="F", values="T")
    return data_ready


print(len(data))
# Removing the failed runs
data = data.loc[
    (data["WS_TF_final"] + data["WS_NT_final"] + data["WS_VI_final"] != np.nan)
]
print(len(data))
data = data.loc[(data["WS_TF_final"] + data["WS_NT_final"] + data["WS_VI_final"] != 0)]
data = data.loc[(data["DiffReturns"] < 2)]
data = data.loc[(data["AvgDiffReturns"] < 3)]
data = data.loc[(data["HighestT"] < 100)]
print(len(data))


#######


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
    ax1.set_xlabel("Wealth Share NT", fontsize=fontsize)
    ax1.set_ylabel("Wealth Share VI", fontsize=fontsize)
    ax2.set_xlabel("Wealth Share VI", fontsize=fontsize)
    ax2.set_ylabel("Wealth Share NT", fontsize=fontsize)
    ax3.set_xlabel("Wealth Share TF", fontsize=fontsize)
    ax3.set_ylabel("Wealth Share NT", fontsize=fontsize)
    ax1.set_title(title1, fontsize=fontsize)
    ax2.set_title(title2, fontsize=fontsize)
    ax3.set_title(title3, fontsize=fontsize)
    ax1.invert_yaxis()
    ax2.invert_yaxis()
    ax3.invert_yaxis()

    plt.tight_layout()
    plt.savefig(figname, dpi=300)
    plt.show()


dataNT = heat_data(data, "WS_NT_initial", "WS_VI_initial", "WS_NT_final")
dataVI = heat_data(data, "WS_VI_initial", "WS_NT_initial", "WS_VI_final")
dataTF = heat_data(data, "WS_TF_initial", "WS_NT_initial", "WS_TF_final")
# fig = GenPlot(dataNT, dataVI, dataTF, "NT Wealth Share", "VI Wealth Share", "TF Wealth Share", 'Experiment2a.png', False)


data_diff1 = heat_data(data, "WS_TF_initial", "WS_VI_initial", "DiffReturns")
data_diff2 = heat_data(data, "WS_TF_initial", "WS_VI_initial", "AvgDiffReturns")
data_diff3 = heat_data(data, "WS_TF_initial", "WS_VI_initial", "HighestT")

# sigma = 5
# gaussian_data3 = gaussian_filter(data_diff3, sigma=sigma, truncate = 0.5)
# print(gaussian_data3)

data_diff1 = heat_data(data, "WS_TF_initial", "WS_VI_initial", "DiffReturns")
data_diff2 = heat_data(data, "WS_TF_initial", "WS_VI_initial", "AvgDiffReturns")
data_diff3 = heat_data(data, "WS_TF_initial", "WS_VI_initial", "HighestT")
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6), sharey=True, sharex=True)
cmap = "seismic"
# fig1 = sns.heatmap(data1, ax=ax1, cmap = cmap)
# fig2 = sns.heatmap(data2, ax=ax2, cmap = cmap)
# fig3 = sns.heatmap(data3, ax=ax3, cmap = cmap)
sns.heatmap(data_diff1, cmap="seismic", ax=ax1)
sns.heatmap(data_diff2, cmap="seismic", ax=ax2)
model = sns.heatmap(data_diff3, cmap="seismic", ax=ax3)
# sns.heatmap(gaussian_data3, cmap = 'seismic', ax=ax3)
ax3.set_xticklabels(model.get_xticklabels(), rotation=90)
ax3.set_yticklabels(model.get_yticklabels(), rotation=0)
ax1.set_xlabel("Initial Wealth Share TF", fontsize=fontsize)
ax1.set_ylabel("Initial Wealth Share VI", fontsize=fontsize)
ax2.set_xlabel("Initial Wealth Share TF", fontsize=fontsize)
ax2.set_ylabel("Initial Wealth Share VI", fontsize=fontsize)
ax3.set_xlabel("Initial Wealth Share TF", fontsize=fontsize)
ax3.set_ylabel("Initial Wealth Share VI", fontsize=fontsize)
ax1.set_title("Difference in returns (last sim.)", fontsize=fontsize)
ax2.set_title("Difference in returns (full sim.)", fontsize=fontsize)
ax3.set_title("Avg. Highest T", fontsize=fontsize)
ax1.invert_yaxis()
ax2.invert_yaxis()
ax3.invert_yaxis()
plt.tight_layout()
plt.savefig("Experiment3.png", dpi=300)
plt.show()


data_diff1 = heat_data(data, "WS_TF_final", "WS_VI_final", "DiffReturns")
data_diff2 = heat_data(data, "WS_TF_final", "WS_VI_final", "AvgDiffReturns")
data_diff3 = heat_data(data, "WS_TF_final", "WS_VI_final", "HighestT")
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6), sharey=True, sharex=True)
cmap = "seismic"
# fig1 = sns.heatmap(data1, ax=ax1, cmap = cmap)
# fig2 = sns.heatmap(data2, ax=ax2, cmap = cmap)
# fig3 = sns.heatmap(data3, ax=ax3, cmap = cmap)
sns.heatmap(data_diff1, cmap="seismic", ax=ax1)
sns.heatmap(data_diff2, cmap="seismic", ax=ax2)
model = sns.heatmap(data_diff3, cmap="seismic", ax=ax3)
# sns.heatmap(gaussian_data3, cmap = 'seismic', ax=ax3)
ax3.set_xticklabels(model.get_xticklabels(), rotation=90)
ax3.set_yticklabels(model.get_yticklabels(), rotation=0)
ax1.set_xlabel("Initial Wealth Share TF", fontsize=fontsize)
ax1.set_ylabel("Initial Wealth Share VI", fontsize=fontsize)
ax2.set_xlabel("Initial Wealth Share TF", fontsize=fontsize)
ax2.set_ylabel("Initial Wealth Share VI", fontsize=fontsize)
ax3.set_xlabel("Initial Wealth Share TF", fontsize=fontsize)
ax3.set_ylabel("Initial Wealth Share VI", fontsize=fontsize)
ax1.set_title("Difference in returns (last sim.)", fontsize=fontsize)
ax2.set_title("Difference in returns (full sim.)", fontsize=fontsize)
ax3.set_title("Avg. Highest T", fontsize=fontsize)
ax1.invert_yaxis()
ax2.invert_yaxis()
ax3.invert_yaxis()
plt.tight_layout()
# plt.savefig('Experiment3b.png', dpi=300)
plt.show()

""" 
Attempts to visualise significance / cvgs metrics that did not work.


# Clear we have converged around everywhere

# Returns are similar everywhere for NT, TF but VI has a clear two-regime demarcation. 
data_diff2 = heat_data(data, 'WS_TF_initial', 'WS_VI_initial', 'AvgDiffReturns')
# fig = sns.heatmap(data_diff, cmap = 'seismic')
# plt.ylabel('Initial Wealth Share VI')
# plt.xlabel('Initial Wealth Share TF')
# plt.title('Avg. difference in returns over full simulation')
# plt.show()

data_diff3 = heat_data(data, 'WS_TF_initial', 'WS_VI_initial', 'HighestT')
# fig = sns.heatmap(data_diff, cmap = 'seismic')
# plt.ylabel('Initial Wealth Share VI')
# plt.xlabel('Initial Wealth Share TF')
# plt.title('Avg. highest T-statistic over full simulation')
# plt.show()

data_diff1 = heat_data(data, 'WS_TF_initial', 'WS_VI_initial', 'DiffReturns')
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (15,6), sharey=True, sharex=True)
cmap = 'seismic'
# fig1 = sns.heatmap(data1, ax=ax1, cmap = cmap)
# fig2 = sns.heatmap(data2, ax=ax2, cmap = cmap)
# fig3 = sns.heatmap(data3, ax=ax3, cmap = cmap)
model = sns.heatmap(data_diff1, cmap = 'seismic', ax=ax1)
sns.heatmap(data_diff2, cmap = 'seismic', ax=ax2)
sns.heatmap(data_diff3, cmap = 'seismic', ax=ax3)
ax1.set_xlabel("Initial Wealth Share TF", fontsize=fontsize)
ax1.set_ylabel("Initial Wealth Share VI", fontsize=fontsize)
ax2.set_xlabel("Initial Wealth Share TF", fontsize=fontsize)
ax2.set_ylabel("Initial Wealth Share VI", fontsize=fontsize)
ax3.set_xlabel("Initial Wealth Share TF", fontsize=fontsize)
ax3.set_ylabel("Initial Wealth Share VI", fontsize=fontsize)
ax1.set_title("Difference in returns (last sim.))", fontsize=fontsize)
ax2.set_title("Difference in returns (full sim.)", fontsize=fontsize)
ax3.set_title("Avg. Highest T", fontsize=fontsize)
ax1.invert_yaxis()
ax2.invert_yaxis()
ax3.invert_yaxis()
# plt.tight_layout()
# plt.ylabel('Initial Wealth Share VI')
# plt.xlabel('Initial Wealth Share TF')
# plt.title('Avg. difference in returns over last days')
plt.show()



data1 = gaussian_filter(data_diff1, sigma=sigma)
data2 = gaussian_filter(data_diff2, sigma=sigma)
data3 = gaussian_filter(data_diff3, sigma=sigma)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (15,6), sharey=True, sharex=True)
cmap = 'seismic'
fig1 = sns.heatmap(data1, ax=ax1, cmap = cmap)
fig2 = sns.heatmap(data2, ax=ax2, cmap = cmap)
fig3 = sns.heatmap(data3, ax=ax3, cmap = cmap)
ax1.set_yticklabels(model.get_yticklabels(), rotation = 0)
ax2.set_yticklabels(model.get_yticklabels(), rotation = 0)
ax3.set_yticklabels(model.get_yticklabels(), rotation = 0)

ax1.set_xticklabels(model.get_xticklabels(), rotation = 90)
ax2.set_xticklabels(model.get_xticklabels(), rotation = 90)
ax3.set_xticklabels(model.get_xticklabels(), rotation = 90)
ax1.set_xlabel("Initial Wealth Share TF", fontsize=fontsize)
ax1.set_ylabel("Initial Wealth Share VI", fontsize=fontsize)
ax2.set_xlabel("Initial Wealth Share TF", fontsize=fontsize)
ax2.set_ylabel("Initial Wealth Share VI", fontsize=fontsize)
ax3.set_xlabel("Initial Wealth Share TF", fontsize=fontsize)
ax3.set_ylabel("Initial Wealth Share VI", fontsize=fontsize)
ax1.set_title("Difference in returns (last sim.))", fontsize=fontsize)
ax2.set_title("Difference in returns (full sim.)", fontsize=fontsize)
ax3.set_title("Avg. Highest T", fontsize=fontsize)
ax1.invert_yaxis()
ax2.invert_yaxis()
ax3.invert_yaxis()
plt.tight_layout()
plt.savefig('tt.png', dpi=300)
plt.show()
"""

""" 


data_diff = heat_data(data, 'WS_NT_inital', 'WS_VI_inital', 'NT_returns_final')
sns.heatmap(data_diff, cmap = 'seismic')
plt.show()

data_diff = heat_data(data, 'WS_NT_inital', 'WS_VI_inital', 'VI_returns_final')
sns.heatmap(data_diff, cmap = 'seismic')
plt.show()

data_diff = heat_data(data, 'WS_TF_initial', 'WS_VI_inital', 'TF_returns_final')
sns.heatmap(data_diff, cmap = 'seismic')
plt.show()
"""
