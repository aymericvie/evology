import pandas as pd

data = pd.read_csv(
    "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data/data4.csv"
)
print(data)
import matplotlib.pyplot as plt
import seaborn as sns

print(data.columns)
import numpy as np
from scipy.ndimage.filters import gaussian_filter

sigma = 1

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


# print(len(data))
# Removing the failed runs
data = data.loc[
    (data["WS_TF_final"] + data["WS_NT_final"] + data["WS_VI_final"] != np.nan)
]
# print(len(data))
data = data.loc[(data["WS_TF_final"] + data["WS_NT_final"] + data["WS_VI_final"] != 0)]
data = data.loc[(data["DiffReturns"] < 10)]
data = data.loc[(data["AvgDiffReturns"] < 10)]
data = data.loc[(data["HighestT"] < 100)]
print(len(data))

data = data.loc[(data["H"] <= 252)]

# Plot without noise, difficult to extract anything
dataNT = heat_data(data, "F", "H", "WS_NT_final")
dataVI = heat_data(data, "F", "H", "WS_VI_final")
dataTF = heat_data(data, "F", "H", "WS_TF_final")
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6), sharey=True, sharex=True)
cmap = "seismic"
model = sns.heatmap(dataNT, ax=ax1, cmap=cmap)
sns.heatmap(dataVI, ax=ax2, cmap=cmap)
sns.heatmap(dataTF, ax=ax3, cmap=cmap)
ax1.set_xlabel("F", fontsize=fontsize)
ax1.set_ylabel("H", fontsize=fontsize)
ax2.set_xlabel("F", fontsize=fontsize)
ax2.set_ylabel("H", fontsize=fontsize)
ax3.set_xlabel("F", fontsize=fontsize)
ax3.set_ylabel("H", fontsize=fontsize)
ax1.invert_yaxis()
ax2.invert_yaxis()
ax3.invert_yaxis()
title1, title2, title3, figname = (
    "NT Wealth Share",
    "VI Wealth Share",
    "TF Wealth Share",
    "Experiment4.png",
)
ax1.set_title(title1, fontsize=fontsize)
ax2.set_title(title2, fontsize=fontsize)
ax3.set_title(title3, fontsize=fontsize)
plt.tight_layout()
plt.savefig(figname, dpi=300)
plt.show()


dataNT2 = gaussian_filter(dataNT, sigma=sigma)
dataVI2 = gaussian_filter(dataVI, sigma=sigma)
dataTF2 = gaussian_filter(dataTF, sigma=sigma)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6), sharey=True, sharex=True)
cmap = "seismic"
sns.heatmap(dataNT2, ax=ax1, cmap=cmap)
sns.heatmap(dataVI2, ax=ax2, cmap=cmap)
sns.heatmap(dataTF2, ax=ax3, cmap=cmap)
ax1.set_yticklabels(model.get_yticklabels(), rotation=0)
ax2.set_yticklabels(model.get_yticklabels(), rotation=0)
ax3.set_yticklabels(model.get_yticklabels(), rotation=0)
ax1.set_xticklabels(model.get_xticklabels(), rotation=90)
ax2.set_xticklabels(model.get_xticklabels(), rotation=90)
ax3.set_xticklabels(model.get_xticklabels(), rotation=90)
ax1.set_xlabel("F", fontsize=fontsize)
ax1.set_ylabel("H", fontsize=fontsize)
ax2.set_xlabel("F", fontsize=fontsize)
ax2.set_ylabel("H", fontsize=fontsize)
ax3.set_xlabel("F", fontsize=fontsize)
ax3.set_ylabel("H", fontsize=fontsize)
ax1.invert_yaxis()
ax2.invert_yaxis()
ax3.invert_yaxis()
title1, title2, title3, figname = (
    "NT Wealth Share",
    "VI Wealth Share",
    "TF Wealth Share",
    "Experiment4.png",
)
ax1.set_title(title1, fontsize=fontsize)
ax2.set_title(title2, fontsize=fontsize)
ax3.set_title(title3, fontsize=fontsize)
plt.tight_layout()
plt.savefig(figname, dpi=300)
plt.show()


dataNT = heat_data(data, "F", "H", "DiffReturns")
dataVI = heat_data(data, "F", "H", "AvgDiffReturns")
dataTF = heat_data(data, "F", "H", "HighestT")
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6), sharey=True, sharex=True)
cmap = "seismic"
model = sns.heatmap(dataNT, ax=ax1, cmap=cmap)
sns.heatmap(dataVI, ax=ax2, cmap=cmap)
sns.heatmap(dataTF, ax=ax3, cmap=cmap)
ax1.set_xlabel("F", fontsize=fontsize)
ax1.set_ylabel("H", fontsize=fontsize)
ax2.set_xlabel("F", fontsize=fontsize)
ax2.set_ylabel("H", fontsize=fontsize)
ax3.set_xlabel("F", fontsize=fontsize)
ax3.set_ylabel("H", fontsize=fontsize)
ax1.invert_yaxis()
ax2.invert_yaxis()
ax3.invert_yaxis()
title1, title2, title3, figname = (
    "Difference in returns (last)",
    "Difference in returns (full)",
    "Avg. Highest T",
    "Experiment4b.png",
)
ax1.set_title(title1, fontsize=fontsize)
ax2.set_title(title2, fontsize=fontsize)
ax3.set_title(title3, fontsize=fontsize)
plt.tight_layout()
# plt.savefig(figname, dpi=300)
plt.show()


dataTF = heat_data(data, "F", "H", "HighestT")
fig, (ax1) = plt.subplots(1, 1, figsize=(5, 6))
cmap = "seismic"
model = sns.heatmap(dataTF, ax=ax1, cmap=cmap)
ax1.set_xlabel("F", fontsize=fontsize)
ax1.set_ylabel("H", fontsize=fontsize)
ax1.invert_yaxis()
title1, title2, title3, figname = (
    "Difference in returns (last)",
    "Difference in returns (full)",
    "Avg. Highest T",
    "Experiment4b.png",
)
ax1.set_title(title1, fontsize=fontsize)
plt.tight_layout()
plt.show()


dataTF2 = gaussian_filter(dataTF, sigma=sigma)
fig, (ax1) = plt.subplots(1, 1, figsize=(5, 6))
cmap = "seismic"
sns.heatmap(dataTF2, ax=ax1, cmap=cmap)
ax1.set_yticklabels(model.get_yticklabels(), rotation=0)
ax1.set_xticklabels(model.get_xticklabels(), rotation=90)
ax1.set_xlabel("F", fontsize=fontsize)
ax1.set_ylabel("H", fontsize=fontsize)
ax1.invert_yaxis()
title3, figname = "Avg. Highest T", "Experiment4c.png"
ax1.set_title(title3, fontsize=fontsize)
plt.tight_layout()
plt.savefig(figname, dpi=300)
plt.show()
