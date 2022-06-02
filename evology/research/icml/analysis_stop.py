# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.ndimage.filters import gaussian_filter
import ternary
import numpy as np
from math import isnan
from ternary.helpers import simplex_iterator
from matplotlib.colors import ListedColormap

sns.set(font_scale=1)
scale = 15
fontsize = 18

data = pd.read_csv(
    "/Users/aymericvie/Documents/GitHub/evology/evology/research/icml/data/stop_time.csv"
)
del data["PopSize"]

# %%
data.hist("StopTime")
plt.show()

# %%
data.hist("Gen")
plt.show()


# %%
data_group = data.groupby(
    ["WS_VI_initial", "WS_TF_initial", "WS_NT_initial"], as_index=False
).mean()

# %%
def gen_data(scale):
    gens = dict()
    l = 0
    for (i, j, k) in simplex_iterator(scale):
        gens[(i, j)] = data_group.loc[l, "Gen"]
        l += 1
    return gens


# %%
gens = gen_data(scale)
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(gens, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("Max generations", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
# plt.savefig('figures/generations_ext.png',dpi=300)
# %%

# %%
def gen_data(scale):
    gens = dict()
    l = 0
    for (i, j, k) in simplex_iterator(scale):
        gens[(i, j)] = data_group.loc[l, "StopTime"]
        l += 1
    return gens


gens = gen_data(scale)
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(gens, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("Stop time", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()

# %%
def gen_data(scale):
    gens = dict()
    l = 0
    for (i, j, k) in simplex_iterator(scale):
        if data_group.loc[l, "StopTime"] < data_group.loc[l, "Gen"]:
            gens[(i, j)] = data_group.loc[l, "StopTime"]
        else:
            gens[(i, j)] = data_group.loc[l, "Gen"]
        l += 1
    return gens


gens = gen_data(scale)
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(gens, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("Min(Gen, Stop time)", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()

# %%
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
from sklearn import preprocessing
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

data["Time"] = 0

for i in range(len(data)):
    data["Time"].iloc[i] = min(data["Gen"].iloc[i], data["StopTime"].iloc[i])


X = pd.DataFrame(data["PopSize"])
y = pd.DataFrame(data["Time"])
model = LinearRegression()
scores = []
kfold = KFold(n_splits=3, shuffle=True, random_state=42)
for i, (train, test) in enumerate(kfold.split(X, y)):
    model.fit(X.iloc[train, :], y.iloc[train, :])
    score = model.score(X.iloc[test, :], y.iloc[test, :])
    scores.append(score)
print(scores)

# %%
del data["Unnamed: 0"]
fig_1 = plt.figure(figsize=(12, 10))
new_correlations = data.corr()
sns.heatmap(new_correlations, annot=True, cmap="Greens", annot_kws={"size": 8})
plt.title("Pearson Correlation Matrix")
plt.show()

# %%


def generate_random_heatmap_data(scale):
    tf_ws = dict()
    vi_ws = dict()
    nt_ws = dict()
    attractor = dict()
    l = 0
    for (i, j, k) in simplex_iterator(scale):
        nt_ws[(i, j)] = data_group.loc[l, "WS_NT_final"]
        vi_ws[(i, j)] = data_group.loc[l, "WS_VI_final"]
        tf_ws[(i, j)] = data_group.loc[l, "WS_TF_final"]
        if data_group.loc[l, "WS_TF_final"] >= 90:
            attractor[(i, j)] = 0
        elif data_group.loc[l, "WS_TF_final"] > 10:
            attractor[(i, j)] = 1
        else:
            attractor[(i, j)] = 2
        l += 1
    return nt_ws, vi_ws, tf_ws, attractor


nt_r, vi_r, tf_r, attractor = generate_random_heatmap_data(scale)

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(nt_r, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("NT final wealth share", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/WS_NT_ext.png", dpi=300)
# plt.show()

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(vi_r, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("VI final wealth share", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/WS_VI_ext.png", dpi=300)

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(tf_r, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("TF final wealth share", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/WS_TF_ext.png", dpi=300)
# plt.show()

# %%
def PathPoints(data):
    points = []
    for i in range(len(data["WS_NT_final"])):
        x = (data.loc[i, "WS_VI_final"] / 100) * scale
        y = (data.loc[i, "WS_TF_final"] / 100) * scale
        z = (data.loc[i, "WS_NT_final"] / 100) * scale
        points.append((x, y, z))
    return points


points = PathPoints(data)

origin = [((100 / 3, 100 / 3, 100 / 3))]
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.gridlines(color="gray", multiple=10)
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.scatter(points, marker="D", color="red", label="Simulations")
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.get_axes().axis("off")
tax.set_title("title", fontsize=fontsize)
plt.legend(loc="upper right", fontsize=fontsize)
plt.tight_layout()
tax._redraw_labels()
plt.savefig("figures/scatterplot_ext.png", dpi=300)
# plt.show()

# %%
