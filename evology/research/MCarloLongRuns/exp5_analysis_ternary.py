""" ternary plot for final wealth shares """

import pandas as pd

data = pd.read_csv(
    "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data/data5.csv"
)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.ndimage.filters import gaussian_filter
import ternary
import numpy as np
from ternary.helpers import simplex_iterator

sns.set(font_scale=1)
fontsize = 18

# print(data['WS_TF_final'].isnull().sum())

# print(data)

data = pd.read_csv(
    "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data/data5.csv"
)
# data['WS_TF_final'] = data['WS_TF_final'].fillna(100)
# data['WS_NT_final'] = data['WS_NT_final'].fillna(0)
# data['WS_VI_final'] = data['WS_VI_final'].fillna(0)
data = data.dropna().reset_index(drop=True)


def PathPoints(df, scale):
    points = []
    N = len(df)
    for i in range(N):
        x = int((df.loc[i, "WS_TF_final"] / 100) * scale)
        y = int((df.loc[i, "WS_NT_final"] / 100) * scale)
        z = int((df.loc[i, "WS_VI_final"] / 100) * scale)
        points.append((x, y, z))
    return points


def DensityData(points, scale):
    density = dict()
    total_count = (scale + 1) * (scale + 2) / 2
    sum_count = 0
    total_enum = 0
    for (i, j, k) in simplex_iterator(scale):
        count = 0
        total_enum += 1
        for point in points:
            if i == point[0] and j == point[1]:
                count += 1
        density[(i, j)] = (count / total_count) / 10
        sum_count += density[(i, j)]
    return density


scale = 24
points = PathPoints(data, scale)
# print(points)
density = DensityData(points, scale)
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(density, style="triangular", cmap="Reds", vmin=0, vmax=0.15)
# tax.heatmap(density, style='triangular',cmap='Reds', vmin=0,vmax=1)
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("NT Final Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("VI Final Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Final Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("Wealth asymptotic distributions density (F=2, H=252)", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("Experiment5_density.png", dpi=300)
plt.show()

data = pd.read_csv(
    "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data/data5b.csv"
)
# data['WS_TF_final'] = data['WS_TF_final'].fillna(100)
# data['WS_NT_final'] = data['WS_NT_final'].fillna(0)
# data['WS_VI_final'] = data['WS_VI_final'].fillna(0)
# data = data.dropna()
data = data.dropna().reset_index(drop=True)


scale = 24
points = PathPoints(data, scale)
# print(points)
density = DensityData(points, scale)
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(density, style="triangular", cmap="Reds", vmin=0, vmax=0.15)
# tax.heatmap(density, style='triangular',cmap='Reds', vmin=0,vmax=1)
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("NT Final Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("VI Final Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Final Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("Wealth asymptotic distributions density (F=2, H=21)", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("Experiment5b_density.png", dpi=300)
plt.show()


data = pd.read_csv(
    "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data/data5c.csv"
)
# data['WS_TF_final'] = data['WS_TF_final'].fillna(100)
# data['WS_NT_final'] = data['WS_NT_final'].fillna(0)
# data['WS_VI_final'] = data['WS_VI_final'].fillna(0)
# data = data.dropna()
data = data.dropna().reset_index(drop=True)


scale = 24
points = PathPoints(data, scale)
# print(points)
density = DensityData(points, scale)
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(density, style="triangular", cmap="Reds", vmin=0, vmax=0.15)
# tax.heatmap(density, style='triangular',cmap='Reds', vmin=0,vmax=1)
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("NT Final Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("VI Final Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Final Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("Wealth asymptotic distributions density (F=3, H=252)", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("Experiment5c_density.png", dpi=300)
plt.show()
